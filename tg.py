import asyncio
import random
import time
import json
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import List, Dict, Optional, Union, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import aiohttp
import ssl

from telethon import TelegramClient, functions, types
from telethon.tl.functions import account, messages, auth, channels, users
from telethon.tl.types import (
    InputReportReasonSpam, InputReportReasonFake, InputReportReasonViolence,
    InputReportReasonChildAbuse, InputReportReasonIllegalDrugs,
    InputReportReasonPersonalDetails, InputReportReasonPornography,
    InputReportReasonOther, InputReportReasonCopyright,
    InputReportReasonGeoIrrelevant, InputReportReasonFakeNews,
    InputReportReasonUnauthorizedAd,
    InputPeerUser, InputPeerChat, InputPeerChannel,
    CodeSettings, DataJSON
)
from telethon.errors import (
    FloodWaitError, FloodPremiumWaitError, UserDeactivatedError, 
    AuthKeyDuplicatedError, SessionPasswordNeededError,
    PhoneNumberBannedError, ChatAdminRequiredError,
    ChannelPrivateError, UsernameNotOccupiedError,
    UsernameInvalidError, PeerIdInvalidError,
    UserAlreadyParticipantError, RPCError
)
from colorama import Fore, Style, init
from fake_useragent import UserAgent

try:
    import aiofiles
    AIOFILES_AVAILABLE = True
except ImportError:
    AIOFILES_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/telegram_reporter_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

init(autoreset=True)
ua = UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

Path("logs").mkdir(exist_ok=True)
Path("sessions").mkdir(exist_ok=True)

DEFAULT_REPORT_COUNT = 50
MIN_REPORT_COUNT = 10
MAX_REPORT_COUNT = 200
MAX_CONCURRENT_REPORTS = 5

TARGET_SUPPORT_EMAILS = [
    "abuse@telegram.org",
    "dmca@telegram.org", 
    "support@telegram.org",
    "security@telegram.org",
    "stopCA@telegram.org",
    "recover@telegram.org",
    "sms@telegram.org",
    "sticker@telegram.org",
    "abuse@telegram.org"
]

REASON_MAP_USER = [
    ("Spam", InputReportReasonSpam()),
    ("Fake Account", InputReportReasonFake()),
    ("Violence", InputReportReasonViolence()),
    ("Child Abuse", InputReportReasonChildAbuse()),
    ("Illegal Drugs", InputReportReasonIllegalDrugs()),
    ("Personal Details", InputReportReasonPersonalDetails()),
    ("Pornography", InputReportReasonPornography()),
    ("Other", InputReportReasonOther()),
]

REASON_MAP_GROUP_CHANNEL = [
    ("Spam", InputReportReasonSpam()),
    ("Child Abuse", InputReportReasonChildAbuse()),
    ("Violence", InputReportReasonViolence()),
    ("Illegal Goods", InputReportReasonIllegalDrugs()),
    ("Illegal Adult Content", InputReportReasonPornography()),
    ("Personal Data", InputReportReasonPersonalDetails()),
    ("Scam/Fraud", InputReportReasonFake()),
    ("Copyright", InputReportReasonCopyright()),
    ("Fake News", InputReportReasonFakeNews()),
    ("Unauthorized Ad", InputReportReasonUnauthorizedAd()),
    ("Geo Irrelevant", InputReportReasonGeoIrrelevant()),
    ("Other", InputReportReasonOther()),
]

@dataclass
class ReportResult:
    account: str
    reason: str
    success: bool
    error: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class AccountConfig:
    api_id: int
    api_hash: str
    phone: str
    username: Optional[str] = None
    smtp: Optional[Dict] = None
    proxy: Optional[Dict] = None
    session_name: Optional[str] = None

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
            'adaptive_factor': self.adaptive_factor,
            'rate_per_minute': self.rate * 60 * self.adaptive_factor
        }

class AccountManager:
    def __init__(self, accounts_file: str):
        self.accounts_file = accounts_file
        self.accounts: List[AccountConfig] = []
        self.session_clients: List[TelegramClient] = []
        self._load_accounts()
        
    def _load_accounts(self):
        try:
            with open(self.accounts_file, "r", encoding='utf-8') as f:
                data = json.load(f)
            
            for idx, acc in enumerate(data):
                if not all(k in acc for k in ["api_id", "api_hash", "phone"]):
                    logger.warning(f"Skipping account {idx}: missing required fields")
                    continue
                
                config = AccountConfig(
                    api_id=int(acc["api_id"]),
                    api_hash=acc["api_hash"],
                    phone=acc["phone"],
                    username=acc.get("username"),
                    smtp=acc.get("smtp"),
                    proxy=acc.get("proxy"),
                    session_name=acc.get("session_name", f"account_{idx}")
                )
                self.accounts.append(config)
                
            logger.info(f"Loaded {len(self.accounts)} valid accounts")
        except Exception as e:
            logger.error(f"Failed to load accounts: {e}")
            raise

    async def init_sessions(self, auto_authorize: bool = True) -> List[TelegramClient]:
        for config in self.accounts:
            session_path = Path("sessions") / f"{config.session_name}.session"
            
            try:
                proxy = None
                if config.proxy:
                    proxy = {
                        'proxy_type': config.proxy.get('type', 'socks5'),
                        'addr': config.proxy['host'],
                        'port': config.proxy['port'],
                        'username': config.proxy.get('username'),
                        'password': config.proxy.get('password')
                    }
                
                client = TelegramClient(
                    str(session_path), 
                    config.api_id, 
                    config.api_hash,
                    proxy=proxy,
                    device_model="Telegram Reporter Pro",
                    system_version="10.0.0",
                    app_version="1.42.0",
                    lang_code="en"
                )
                
                await client.connect()
                
                if not await client.is_user_authorized():
                    if auto_authorize:
                        print(Fore.YELLOW + f"[{config.phone}] Not authorized, requesting code...")
                        await client.send_code_request(config.phone)
                        code = input(f"Enter code for {config.phone}: ")
                        try:
                            await client.sign_in(config.phone, code)
                        except SessionPasswordNeededError:
                            password = input(f"Enter 2FA password for {config.phone}: ")
                            await client.sign_in(password=password)
                    else:
                        logger.warning(f"Account {config.phone} not authorized, skipping")
                        continue
                
                client._account_phone = config.phone
                client._account_username = config.username
                client._account_config = config
                
                self.session_clients.append(client)
                print(Fore.GREEN + f"[{config.phone}] Session ready")
                
            except PhoneNumberBannedError:
                print(Fore.RED + f"[{config.phone}] Account banned, skipping")
                continue
            except AuthKeyDuplicatedError:
                print(Fore.RED + f"[{config.phone}] Auth key duplicated, delete session file")
                continue
            except Exception as e:
                print(Fore.RED + f"[{config.phone}] Failed to initialize: {e}")
                continue
                
        return self.session_clients

    async def close_sessions(self):
        for client in self.session_clients:
            try:
                await client.disconnect()
            except Exception as e:
                logger.error(f"Error disconnecting client: {e}")
        self.session_clients.clear()

    def get_healthy_clients(self) -> List[TelegramClient]:
        return [c for c in self.session_clients if c.is_connected()]

class EntityResolver:
    def __init__(self, client: TelegramClient):
        self.client = client
        self._cache = {}
    
    async def resolve(self, target: str) -> Optional[types.Entity]:
        try:
            if 't.me/' in target or 'telegram.me/' in target:
                target = target.split('/')[-1].split('?')[0]
            
            if target in self._cache:
                return self._cache[target]
            
            entity = await self.client.get_entity(target)
            
            if entity:
                self._cache[target] = entity
                return entity
                
        except (UsernameNotOccupiedError, UsernameInvalidError):
            logger.error(f"Username {target} not found or invalid")
        except PeerIdInvalidError:
            logger.error(f"Peer ID {target} invalid")
        except ValueError:
            try:
                if target.isdigit():
                    async for dialog in self.client.iter_dialogs(limit=1000):
                        if dialog.entity and getattr(dialog.entity, 'id', None) == int(target):
                            return dialog.entity
            except Exception as e:
                logger.error(f"Could not resolve entity {target}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error resolving {target}: {e}")
        
        return None
    
    def get_input_peer(self, entity: types.Entity) -> Optional[types.InputPeer]:
        if isinstance(entity, types.User):
            return InputPeerUser(entity.id, entity.access_hash)
        elif isinstance(entity, types.Chat):
            return InputPeerChat(entity.id)
        elif isinstance(entity, types.Channel):
            return InputPeerChannel(entity.id, entity.access_hash)
        return None

class AppReporter:
    def __init__(self, account_manager: AccountManager):
        self.account_manager = account_manager
        self.clients = account_manager.session_clients
        self.account_count = len(self.clients)
        self._semaphore = asyncio.Semaphore(MAX_CONCURRENT_REPORTS)
        self._flood_wait_until = {}
        self.rate_limiter = AdaptiveRateLimiter(30.0)

    async def report_entity(self, target: str, target_type: str, count: int) -> Dict:
        if count < MIN_REPORT_COUNT:
            count = MIN_REPORT_COUNT
        elif count > MAX_REPORT_COUNT:
            count = MAX_REPORT_COUNT

        reason_list = REASON_MAP_USER if target_type == "user" else REASON_MAP_GROUP_CHANNEL
        
        results = {
            "target": target,
            "target_type": target_type,
            "requested_count": count,
            "actual_count": 0,
            "successful": 0,
            "failed": 0,
            "flood_waited": 0,
            "reports": []
        }

        if not self.clients:
            logger.error("No clients available for reporting")
            return results
            
        resolver = EntityResolver(self.clients[0])
        entity = await resolver.resolve(target)
        
        if not entity:
            logger.error(f"Could not resolve entity: {target}")
            results["error"] = "Entity resolution failed"
            return results
            
        if target_type == "auto":
            if isinstance(entity, types.User):
                target_type = "user"
            elif isinstance(entity, (types.Chat, types.ChatForbidden)):
                target_type = "group"
            elif isinstance(entity, types.Channel):
                target_type = "channel" if entity.broadcast else "supergroup"
            else:
                target_type = "unknown"
        
        input_peer = resolver.get_input_peer(entity)
        if not input_peer:
            logger.error("Could not create input peer")
            return results

        reports_per_account = max(1, count // self.account_count)
        remainder = count % self.account_count
        
        tasks = []
        for idx, client in enumerate(self.clients):
            this_account_reports = reports_per_account + (1 if idx < remainder else 0)
            if this_account_reports > 0:
                task = self._report_with_client(
                    client, target, target_type, entity, input_peer, 
                    reason_list, this_account_reports, idx
                )
                tasks.append(task)
        
        report_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for res in report_results:
            if isinstance(res, Exception):
                results["failed"] += 1
                logger.error(f"Task failed with exception: {res}")
                continue
            for report in res:
                results["reports"].append(report)
                results["actual_count"] += 1
                if report.success:
                    results["successful"] += 1
                elif report.error and "Flood wait" in report.error:
                    results["flood_waited"] += 1
                else:
                    results["failed"] += 1
        
        return results

    async def _report_with_client(self, client: TelegramClient, target: str, 
                                  target_type: str, entity, input_peer,
                                  reason_list: List, count: int, client_idx: int) -> List[ReportResult]:
        results = []
        phone = getattr(client, '_account_phone', f'client_{client_idx}')
        
        if phone in self._flood_wait_until:
            if time.time() < self._flood_wait_until[phone]:
                logger.warning(f"[{phone}] Skipping due to active flood wait")
                return results
        
        async with self._semaphore:
            for i in range(count):
                reason_name, reason_obj = random.choice(reason_list)
                
                try:
                    await self.rate_limiter.acquire()
                    
                    if target_type == "user":
                        result = await client(account.ReportPeerRequest(
                            peer=input_peer,
                            reason=reason_obj,
                            message=f"Automated report: {reason_name} | Violation detected"
                        ))
                    else:
                        message_ids = []
                        try:
                            async for message in client.iter_messages(entity, limit=10):
                                if message.id:
                                    message_ids.append(message.id)
                        except Exception as e:
                            logger.debug(f"Could not fetch messages: {e}")
                        
                        result = await client(messages.ReportRequest(
                            peer=input_peer,
                            id=message_ids if message_ids else [1],
                            reason=reason_obj,
                            message=f"Automated report: {reason_name} | Community safety violation"
                        ))
                    
                    self.rate_limiter.adjust_rate(True)
                    
                    report = ReportResult(
                        account=phone,
                        reason=reason_name,
                        success=True
                    )
                    results.append(report)
                    print(Fore.GREEN + f"[{phone}] Reported {target} for {reason_name}")
                    
                    await asyncio.sleep(random.uniform(1.5, 3.5))
                    
                except FloodWaitError as e:
                    wait_time = e.seconds
                    self._flood_wait_until[phone] = time.time() + wait_time
                    self.rate_limiter.adjust_rate(False)
                    
                    report = ReportResult(
                        account=phone,
                        reason=reason_name,
                        success=False,
                        error=f"Flood wait {wait_time}s"
                    )
                    results.append(report)
                    print(Fore.RED + f"[{phone}] Flood wait {wait_time}s – backing off")
                    break
                    
                except FloodPremiumWaitError as e:
                    self._flood_wait_until[phone] = time.time() + e.seconds
                    self.rate_limiter.adjust_rate(False)
                    
                    report = ReportResult(
                        account=phone,
                        reason=reason_name,
                        success=False,
                        error=f"Premium flood wait {e.seconds}s"
                    )
                    results.append(report)
                    print(Fore.RED + f"[{phone}] Premium flood wait – backing off")
                    break
                    
                except UserDeactivatedError:
                    report = ReportResult(
                        account=phone,
                        reason=reason_name,
                        success=False,
                        error="Account deactivated"
                    )
                    results.append(report)
                    print(Fore.RED + f"[{phone}] Account deactivated")
                    break
                    
                except ChatAdminRequiredError:
                    report = ReportResult(
                        account=phone,
                        reason=reason_name,
                        success=False,
                        error="Admin rights required"
                    )
                    results.append(report)
                    print(Fore.RED + f"[{phone}] Admin rights required")
                    
                except ChannelPrivateError:
                    report = ReportResult(
                        account=phone,
                        reason=reason_name,
                        success=False,
                        error="Channel is private"
                    )
                    results.append(report)
                    print(Fore.RED + f"[{phone}] Private channel")
                    break
                    
                except Exception as e:
                    error_msg = str(e)
                    report = ReportResult(
                        account=phone,
                        reason=reason_name,
                        success=False,
                        error=error_msg
                    )
                    results.append(report)
                    print(Fore.RED + f"[{phone}] Failed: {error_msg[:50]}")
                    await asyncio.sleep(random.uniform(1, 2))
                
        return results

class AsyncEmailReporter:
    def __init__(self, account_manager: AccountManager):
        self.smtp_accounts = [
            acc.smtp for acc in account_manager.accounts 
            if acc.smtp and all(k in acc.smtp for k in ["host", "port", "user", "pass"])
        ]
        self._rate_limit = {}
        self._semaphore = asyncio.Semaphore(3)

    async def send_emails(self, target: str, subject: str, body_template: str, 
                    target_emails: Optional[List[str]] = None,
                    evidence_links: Optional[List[str]] = None) -> Dict:
        if target_emails is None:
            if Path("emails.txt").exists():
                with open("emails.txt", "r", encoding='utf-8') as f:
                    target_emails = [line.strip() for line in f if line.strip() and '@' in line]
            else:
                target_emails = TARGET_SUPPORT_EMAILS

        results = {
            "target": target,
            "sent": [],
            "failed": [],
            "total_attempts": 0
        }

        tasks = []
        for smtp in self.smtp_accounts:
            task = self._send_with_smtp(smtp, target, subject, body_template, target_emails, evidence_links)
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return results

    async def _send_with_smtp(self, smtp: Dict, target: str, subject: str, 
                              body_template: str, target_emails: List[str],
                              evidence_links: Optional[List[str]] = None):
        account_key = smtp["user"]
        if account_key in self._rate_limit:
            if time.time() - self._rate_limit[account_key] < 60:
                return
        
        try:
            import aiosmtplib
            await self._send_async_smtp(smtp, target, subject, body_template, target_emails, evidence_links)
            self._rate_limit[account_key] = time.time()
        except ImportError:
            await asyncio.to_thread(self._send_sync_smtp, smtp, target, subject, body_template, target_emails, evidence_links)
            self._rate_limit[account_key] = time.time()
    
    async def _send_async_smtp(self, smtp: Dict, target: str, subject: str,
                               body_template: str, target_emails: List[str],
                               evidence_links: Optional[List[str]] = None):
        try:
            import aiosmtplib
            
            for recipient in target_emails:
                try:
                    msg = MIMEMultipart()
                    msg["From"] = smtp["user"]
                    msg["To"] = recipient
                    msg["Subject"] = subject
                    msg["X-Priority"] = "1"
                    
                    body = body_template.format(target=target)
                    if evidence_links:
                        body += "\n\nEvidence Links:\n" + "\n".join(f"- {link}" for link in evidence_links)
                    
                    msg.attach(MIMEText(body, "plain", "utf-8"))
                    
                    await aiosmtplib.send(
                        msg,
                        hostname=smtp["host"],
                        port=smtp["port"],
                        start_tls=True,
                        username=smtp["user"],
                        password=smtp["pass"]
                    )
                    
                    print(Fore.GREEN + f"[EMAIL] Sent to {recipient} via {smtp['user']}")
                    await asyncio.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    print(Fore.RED + f"[EMAIL] Failed to {recipient}: {e}")
                    
        except ImportError:
            pass
    
    def _send_sync_smtp(self, smtp: Dict, target: str, subject: str,
                        body_template: str, target_emails: List[str],
                        evidence_links: Optional[List[str]] = None):
        try:
            server = smtplib.SMTP(smtp["host"], smtp["port"], timeout=10)
            server.starttls()
            server.login(smtp["user"], smtp["pass"])
            
            for recipient in target_emails:
                try:
                    msg = MIMEMultipart()
                    msg["From"] = smtp["user"]
                    msg["To"] = recipient
                    msg["Subject"] = subject
                    msg["X-Priority"] = "1"
                    
                    body = body_template.format(target=target)
                    if evidence_links:
                        body += "\n\nEvidence Links:\n" + "\n".join(f"- {link}" for link in evidence_links)
                    
                    msg.attach(MIMEText(body, "plain", "utf-8"))
                    
                    server.send_message(msg)
                    print(Fore.GREEN + f"[EMAIL] Sent to {recipient} via {smtp['user']}")
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    print(Fore.RED + f"[EMAIL] Failed to {recipient}: {e}")
            
            server.quit()
            
        except Exception as e:
            print(Fore.RED + f"[EMAIL] SMTP error for {smtp['user']}: {e}")

    def send_appeal_email(self, target: str, entity_type: str = "user", 
                          appeal_reason: str = "unfair restriction") -> Dict:
        templates = {
            "user": {
                "subject": f"Formal Appeal: Account Restoration Request for {target}",
                "body": """Dear Telegram Trust & Safety Team,

I am writing to formally appeal the restriction placed on the account {target}.

Account Details:
- Username/ID: {target}
- Issue: {reason}
- Date: {date}

Grounds for Appeal:
This account has been unjustly limited. The user has consistently adhered to Telegram's Terms of Service and Community Guidelines. We request a comprehensive review of the account activity and restoration of full functionality.

Supporting Information:
- No violations of ToS have occurred
- Account used for legitimate personal/business communications
- No spam or abusive behavior detected

Please investigate and restore the account at your earliest convenience.

Respectfully,
Account Recovery Team
Date: {date}"""
            },
            "group": {
                "subject": f"Formal Appeal: Group Reinstatement Request for {target}",
                "body": """Dear Telegram Support,

I am submitting a formal appeal for the reinstatement of the group {target}.

Group Details:
- Group Link/ID: {target}
- Restriction Type: Ban/Limitation
- Date: {date}

Justification:
This community group operates within Telegram's guidelines and serves as a legitimate discussion platform. The ban appears to be erroneous or the result of false reports.

We request immediate review and reinstatement.

Sincerely,
Community Manager"""
            },
            "channel": {
                "subject": f"Formal Appeal: Channel Reinstatement Request for {target}",
                "body": """Dear Telegram DMCA/Abuse Team,

Formal appeal regarding the suspension of channel {target}.

Channel Information:
- Channel: {target}
- Content Type: Educational/News/Entertainment
- Subscriber Count: [If known]

The channel complies with copyright laws and Telegram's terms. We believe this suspension resulted from malicious mass-reporting.

Request immediate review and restoration.

Best regards,
Channel Administrator"""
            }
        }

        template = templates.get(entity_type, templates["user"])
        body = template["body"].format(
            target=target, 
            reason=appeal_reason,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return self.send_emails(target, template["subject"], body)

class SpamBotAppealer:
    def __init__(self, clients: List[TelegramClient]):
        self.clients = clients
        self.spambot_username = "spambot"
        self._appeal_templates = [
            "Hello @spambot, I am appealing on behalf of user {target}. This account was unfairly restricted. Please review.",
            "Hi, user {target} needs help. False positive spam detection. Please check and restore.",
            "@spambot please review the case of {target}. Legitimate user blocked by error."
        ]

    async def appeal_for_user(self, target: str, custom_message: Optional[str] = None) -> Dict:
        results = {
            "target": target,
            "appeals": [],
            "successful": 0,
            "failed": 0
        }
        
        for idx, client in enumerate(self.clients):
            try:
                try:
                    spambot = await client.get_entity(self.spambot_username)
                except Exception:
                    spambot = await client.get_entity("@" + self.spambot_username)
                
                if custom_message:
                    msg = custom_message.format(target=target)
                else:
                    msg = random.choice(self._appeal_templates).format(target=target)
                
                sent_msg = await client.send_message(spambot, msg)
                
                await asyncio.sleep(2)
                try:
                    async for message in client.iter_messages(spambot, limit=5):
                        if message.buttons:
                            for row in message.buttons:
                                for button in row:
                                    if "mistake" in button.text.lower() or "wrong" in button.text.lower():
                                        await button.click()
                                        await asyncio.sleep(1)
                except Exception as e:
                    logger.debug(f"Button interaction failed: {e}")
                
                results["appeals"].append({
                    "account": getattr(client, '_account_phone', f'client_{idx}'),
                    "message_id": sent_msg.id,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                })
                results["successful"] += 1
                print(Fore.GREEN + f"[SpamBot] Appeal sent from {getattr(client, '_account_phone', idx)}")
                
                await asyncio.sleep(random.uniform(2, 4))
                
            except UserDeactivatedError:
                results["appeals"].append({
                    "account": getattr(client, '_account_phone', f'client_{idx}'),
                    "success": False,
                    "error": "Account deactivated"
                })
                results["failed"] += 1
            except Exception as e:
                error_msg = str(e)
                results["appeals"].append({
                    "account": getattr(client, '_account_phone', f'client_{idx}'),
                    "success": False,
                    "error": error_msg
                })
                results["failed"] += 1
                print(Fore.RED + f"[SpamBot] Failed: {error_msg[:50]}")
                await asyncio.sleep(random.uniform(1, 3))
        
        return results

class NotoScamReporter:
    def __init__(self, clients: List[TelegramClient]):
        self.clients = clients
        self.bot_username = "notoscam"
    
    async def report_scam(self, target: str, evidence: Optional[str] = None) -> Dict:
        results = {"target": target, "reports": []}
        
        for client in self.clients:
            try:
                bot = await client.get_entity(self.bot_username)
                
                report_text = f"Reporting scam account: {target}"
                if evidence:
                    report_text += f"\nEvidence: {evidence}"
                
                await client.send_message(bot, report_text)
                
                try:
                    entity = await client.get_entity(target)
                    async for message in client.iter_messages(entity, limit=5):
                        if message.text and any(word in message.text.lower() for word in ['scam', 'spam', 'fake', 'money', 'crypto', 'invest']):
                            await client.forward_messages(bot, message)
                            break
                except Exception:
                    pass
                
                results["reports"].append({
                    "account": getattr(client, '_account_phone', 'unknown'),
                    "success": True
                })
                print(Fore.GREEN + f"[NotoScam] Reported via {getattr(client, '_account_phone', 'unknown')}")
                
            except Exception as e:
                results["reports"].append({
                    "account": getattr(client, '_account_phone', 'unknown'),
                    "success": False,
                    "error": str(e)
                })
                print(Fore.RED + f"[NotoScam] Failed: {e}")
        
        return results

class AsyncWebReporter:
    def __init__(self):
        self.support_url = "https://telegram.org/support"
        self.ua = UserAgent()
        
    async def report(self, target: str, report_type: str = "spam", 
               description: Optional[str] = None, email: Optional[str] = None) -> Dict:
        result = {
            "target": target,
            "method": "web_form",
            "success": False,
            "details": {}
        }
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        timeout = aiohttp.ClientTimeout(total=15, connect=5, sock_read=10)
        
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                headers = {
                    "User-Agent": self.ua.random,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "DNT": "1",
                    "Connection": "keep-alive",
                }
                
                async with session.get(self.support_url, headers=headers, ssl=ssl_context) as resp:
                    result["details"]["fetch_status"] = resp.status
                    
                    if resp.status != 200:
                        result["details"]["error"] = f"HTTP {resp.status}"
                        return result
                    
                    html = await resp.text()
                    
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    if self._has_captcha(soup):
                        result["details"]["error"] = "CAPTCHA detected"
                        result["details"]["has_captcha"] = True
                        print(Fore.YELLOW + "[WEB] CAPTCHA detected")
                        return result
                    
                    form = soup.find('form')
                    if not form:
                        result["details"]["error"] = "No form found"
                        return result
                    
                    form_data = {}
                    for field in form.find_all(['input', 'textarea', 'select']):
                        name = field.get('name')
                        if not name:
                            continue
                        
                        field_type = field.get('type', 'text')
                        if field_type in ['submit', 'button', 'image', 'reset']:
                            continue
                        
                        if 'email' in name.lower() or 'from' in name.lower():
                            form_data[name] = email or "anonymous@protonmail.com"
                        elif 'message' in name.lower() or 'text' in name.lower() or 'description' in name.lower():
                            form_data[name] = description or self._generate_report_text(target, report_type)
                        elif 'subject' in name.lower() or 'topic' in name.lower():
                            form_data[name] = f"Abuse Report: {target}"
                        elif 'phone' in name.lower():
                            form_data[name] = "+1234567890"
                        else:
                            form_data[name] = field.get('value', '')
                    
                    action = form.get('action') or self.support_url
                    if action.startswith('/'):
                        from urllib.parse import urlparse
                        parsed = urlparse(self.support_url)
                        action = f"{parsed.scheme}://{parsed.netloc}{action}"
                    
                    async with session.post(action, data=form_data, headers=headers, ssl=ssl_context, allow_redirects=True) as submit_resp:
                        result["details"]["submit_status"] = submit_resp.status
                        
                        success_indicators = ['thank you', 'submitted', 'received', 'success', 'confirmation']
                        response_text = await submit_resp.text()
                        response_lower = response_text.lower()
                        
                        if submit_resp.status == 200 and any(ind in response_lower for ind in success_indicators):
                            result["success"] = True
                            result["details"]["confirmation"] = "Form submitted"
                            print(Fore.GREEN + "[WEB] Support form submitted")
                        else:
                            result["details"]["response_snippet"] = response_text[:200]
                            print(Fore.YELLOW + "[WEB] Form submitted but success unclear")
                        
        except Exception as e:
            result["details"]["error"] = str(e)
            print(Fore.RED + f"[WEB] Error: {e}")
        
        return result
    
    def _generate_report_text(self, target: str, report_type: str) -> str:
        templates = {
            "spam": f"I am reporting the account/channel {target} for spam and unsolicited messaging.",
            "scam": f"Urgent: {target} is operating a fraudulent scheme.",
            "abuse": f"I wish to report {target} for abusive behavior and harassment.",
            "child": f"CRITICAL: {target} is sharing illegal content involving minors.",
            "violence": f"Reporting {target} for promoting violence and extremist content."
        }
        return templates.get(report_type, templates["spam"])
    
    def _has_captcha(self, soup) -> bool:
        captcha_indicators = [
            ('div', {'class': 'g-recaptcha'}),
            ('iframe', {'src': lambda x: x and 'recaptcha' in x}),
            ('div', {'class': 'h-captcha'}),
        ]
        
        for tag, attrs in captcha_indicators:
            if soup.find(tag, attrs):
                return True
        
        if 'captcha' in soup.text.lower():
            return True
            
        return False

async def ban_user(target: str, count: int = DEFAULT_REPORT_COUNT, 
                   accounts_file: str = "accounts.json") -> Dict:
    mgr = AccountManager(accounts_file)
    await mgr.init_sessions()
    reporter = AppReporter(mgr)
    result = await reporter.report_entity(target, "user", count)
    await mgr.close_sessions()
    return result

async def ban_group(target: str, count: int = DEFAULT_REPORT_COUNT,
                    accounts_file: str = "accounts.json") -> Dict:
    mgr = AccountManager(accounts_file)
    await mgr.init_sessions()
    reporter = AppReporter(mgr)
    result = await reporter.report_entity(target, "group", count)
    await mgr.close_sessions()
    return result

async def ban_channel(target: str, count: int = DEFAULT_REPORT_COUNT,
                      accounts_file: str = "accounts.json") -> Dict:
    mgr = AccountManager(accounts_file)
    await mgr.init_sessions()
    reporter = AppReporter(mgr)
    result = await reporter.report_entity(target, "channel", count)
    await mgr.close_sessions()
    return result

async def max_ban(target: str, count: int = DEFAULT_REPORT_COUNT,
                  accounts_file: str = "accounts.json") -> Dict:
    results = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "methods": {}
    }
    
    mgr = AccountManager(accounts_file)
    await mgr.init_sessions()
    
    if not mgr.session_clients:
        results["error"] = "No valid sessions"
        return results
    
    try:
        resolver = EntityResolver(mgr.session_clients[0])
        entity = await resolver.resolve(target)
        
        if isinstance(entity, types.User):
            target_type = "user"
        elif isinstance(entity, (types.Chat, types.ChatForbidden)):
            target_type = "group"
        elif isinstance(entity, types.Channel):
            target_type = "channel" if entity.broadcast else "supergroup"
        else:
            target_type = "unknown"
            
        results["detected_type"] = target_type
    except Exception as e:
        target_type = "user"
        results["detection_error"] = str(e)
    
    try:
        reporter = AppReporter(mgr)
        results["methods"]["app_report"] = await reporter.report_entity(target, target_type, count)
    except Exception as e:
        results["methods"]["app_report"] = {"error": str(e)}
    
    try:
        email_reporter = AsyncEmailReporter(mgr)
        results["methods"]["email_report"] = await email_reporter.send_emails(
            target,
            f"Urgent Abuse Report: {target}",
            "This is a formal abuse report regarding {target} which violates Telegram Terms of Service.",
            evidence_links=[f"https://t.me/{target.replace('@', '')}" if not target.startswith('-') else None]
        )
    except Exception as e:
        results["methods"]["email_report"] = {"error": str(e)}
    
    try:
        web_reporter = AsyncWebReporter()
        results["methods"]["web_report"] = await web_reporter.report(
            target, 
            report_type="spam",
            description=f"Mass reporting {target} for spam and abuse"
        )
    except Exception as e:
        results["methods"]["web_report"] = {"error": str(e)}
    
    try:
        notoscam = NotoScamReporter(mgr.session_clients)
        results["methods"]["notoscam_report"] = await notoscam.report_scam(target)
    except Exception as e:
        results["methods"]["notoscam_report"] = {"error": str(e)}
    
    await mgr.close_sessions()
    return results

async def unfreeze_user(target: str, accounts_file: str = "accounts.json",
                        appeal_details: Optional[str] = None) -> Dict:
    results = {
        "target": target,
        "type": "user",
        "methods": {},
        "timestamp": datetime.now().isoformat()
    }
    
    mgr = AccountManager(accounts_file)
    await mgr.init_sessions()
    
    if not mgr.session_clients:
        results["error"] = "No valid sessions"
        return results
    
    try:
        email_reporter = AsyncEmailReporter(mgr)
        results["methods"]["email_appeal"] = await email_reporter.send_appeal_email(
            target, 
            entity_type="user",
            appeal_reason=appeal_details or "unfair restriction"
        )
    except Exception as e:
        results["methods"]["email_appeal"] = {"error": str(e)}
    
    try:
        appealler = SpamBotAppealer(mgr.session_clients)
        results["methods"]["spambot_appeal"] = await appealler.appeal_for_user(
            target, 
            custom_message=appeal_details
        )
    except Exception as e:
        results["methods"]["spambot_appeal"] = {"error": str(e)}
    
    try:
        support_results = []
        for client in mgr.session_clients[:2]:
            try:
                await client.send_message(
                    "support",
                    f"Appeal for account {target}: This user has been unfairly restricted. Please review the case urgently."
                )
                support_results.append({"account": getattr(client, '_account_phone', 'unknown'), "success": True})
            except Exception as e:
                support_results.append({"account": getattr(client, '_account_phone', 'unknown'), "error": str(e)})
        results["methods"]["direct_support"] = support_results
    except Exception as e:
        results["methods"]["direct_support"] = {"error": str(e)}
    
    await mgr.close_sessions()
    return results

async def unban_group(target: str, accounts_file: str = "accounts.json") -> Dict:
    results = {"target": target, "type": "group"}
    mgr = AccountManager(accounts_file)
    await mgr.init_sessions()
    
    if mgr.session_clients:
        email_reporter = AsyncEmailReporter(mgr)
        await email_reporter.send_appeal_email(target, entity_type="group")
        await mgr.close_sessions()
    
    return results

async def unban_channel(target: str, accounts_file: str = "accounts.json") -> Dict:
    results = {"target": target, "type": "channel"}
    mgr = AccountManager(accounts_file)
    await mgr.init_sessions()
    
    if mgr.session_clients:
        email_reporter = AsyncEmailReporter(mgr)
        await email_reporter.send_appeal_email(target, entity_type="channel")
        await mgr.close_sessions()
    
    return results

