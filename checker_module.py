
""" 
ᴄᴏᴅᴇᴅ ʙʏ ʙᴀʜɪʀᴀᴠᴀ🌹
ʙᴀɴ ᴄʜᴇᴄᴋᴇʀ
"""
import os
import re
import asyncio
import requests
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

BAILEYS_API_URL = os.getenv("BAILEYS_API_URL", "")


def markdown_safe(value):
    return escape_markdown(str(value or ""), version=1)

class WhatsAppStatus(Enum):
    ONLINE_ACTIVE = "online_active"
    TEMP_RESTRICTED = "temp_restricted"
    PERMANENT_BAN = "permanent_ban"
    NOT_REGISTERED = "not_registered"
    UNKNOWN = "unknown"
    ERROR = "error"
    DISCONNECTED = "disconnected"

@dataclass
class CheckResult:
    status: WhatsAppStatus
    message: str
    details: str
    icon: str
    raw_data: dict

def check_number_via_api(phone: str) -> dict:
    try:
        clean_phone = re.sub(r'[^\d]', '', phone)
        url = f"{BAILEYS_API_URL}/check/{clean_phone}"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.ConnectionError:
        return {"error": "ᴄᴀɴɴᴏᴛ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ʙᴀɪʟᴇʏs sᴇʀᴠᴇʀ", "status": "disconnected"}
    except requests.exceptions.Timeout:
        return {"error": "ʀᴇǫᴜᴇsᴛ ᴛɪᴍᴇᴏᴜᴛ", "status": "timeout"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

def interpret_result(data: dict) -> CheckResult:
    
    if data.get("status") == "disconnected" or data.get("error") == "ᴡʜᴀᴛsᴀᴘᴘ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ":
        return CheckResult(
            status=WhatsAppStatus.DISCONNECTED,
            message="🔴 sᴇʀᴠᴇʀ ᴏғғʟɪɴᴇ",
            details="ʙᴀɪʟᴇʏs sᴇʀᴠᴇʀ is ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ. ᴄʜᴇᴄᴋ ʏᴏᴜʀ Node.js sᴇʀᴠᴇʀ.",
            icon="🔴",
            raw_data=data
        )
    
    if data.get("status") == "not_registered":
        return CheckResult(
            status=WhatsAppStatus.NOT_REGISTERED,
            message="❌ ɴᴏᴛ ᴏɴ ᴡʜᴀᴛsᴀᴘᴘ",
            details="ᴛʜɪs ɴᴜᴍʙᴇʀ is ɴᴏᴛ ʀᴇɢɪsᴛᴇʀᴇᴅ ᴏɴ ᴡʜᴀᴛsᴀᴘᴘ.",
            icon="❌",
            raw_data=data
        )
    
    if data.get("error"):
        return CheckResult(
            status=WhatsAppStatus.ERROR,
            message="⚠️ ᴄʜᴇᴄᴋ ғᴀɪʟᴇᴅ",
            details=f"ᴇʀʀᴏʀ: {data.get('error')}",
            icon="⚠️",
            raw_data=data
        )
    
    status = data.get("status", "unknown")
    checks = data.get("checks", {})
    confidence = data.get("confidence", "low")
    analysis = data.get("analysis", {})
    
    if status == "active":
        last_seen = checks.get("lastSeen")
        online_text = f"ʟᴀsᴛ sᴇᴇɴ: {format_last_seen(last_seen)}" if last_seen else "ᴄᴜʀʀᴇɴᴛʟʏ ᴏɴʟɪɴᴇ ᴏʀ ʜɪᴅᴅᴇɴ"
        
        return CheckResult(
            status=WhatsAppStatus.ONLINE_ACTIVE,
            message="✅ ᴏɴʟɪɴᴇ ᴏʀ ᴀᴄᴛɪᴠᴇ",
            details=f"{analysis.get('description', 'Account is healthy')}\n\n"
                   f"📊 ɪɴᴅɪᴄᴀᴛᴏʀs:\n"
                   f"• ᴘʀᴏғɪʟᴇ ᴘɪᴄᴛᴜʀᴇ: {'Yes' if checks.get('hasProfilePicture') else 'No'}\n"
                   f"• sᴛᴀᴛᴜs ᴛᴇxᴛ: {checks.get('statusText') or 'ɴᴏᴛ sᴇᴛ'}\n"
                   f"• {online_text}\n"
                   f"• ᴄᴏɴғɪᴅᴇɴᴄᴇ: {confidence.upper()}\n\n"
                   f"💡 {analysis.get('recommendation', 'sᴀғᴇ ᴛᴏ ᴍᴇssᴀɢᴇ')}",
            icon="✅",
            raw_data=data
        )
    
    if status in ["temp_restricted", "suspicious"]:
        return CheckResult(
            status=WhatsAppStatus.TEMP_RESTRICTED,
            message="⚠️ ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ʀᴇsᴛʀɪᴄᴛᴇᴅ",
            details=f"{analysis.get('description', 'ᴀᴄᴄᴏᴜɴᴛ ʟɪᴍɪᴛᴇᴅ')}\n\n"
                   f"📊 ɪɴᴅɪᴄᴀᴛᴏʀs:\n"
                   f"• ᴘʀᴏғɪʟᴇ ᴀᴄᴄᴇssɪʙʟᴇ: {'Yes' if checks.get('hasProfilePicture') else 'ɴᴏ/ʙʟᴏᴄᴋᴇᴅ'}\n"
                   f"• sᴛᴀᴛᴜs ᴀᴄᴄᴇssɪʙʟᴇ: {'Yes' if checks.get('hasStatus') else 'ɴᴏ/ʙʟᴏᴄᴋᴇᴅ'}\n"
                   f"• ᴘʀᴇsᴇɴᴄᴇ: {'Received' if checks.get('hasPresence') else 'ɴᴏᴛ ʀᴇᴄᴇɪᴠᴇᴅ'}\n"
                   f"• ᴄᴏɴғɪᴅᴇɴᴄᴇ: {confidence.upper()}\n\n"
                   f"⚠️ {analysis.get('recommendation', 'ᴡᴀɪᴛ ʙᴇғᴏʀᴇ ᴍᴇssᴀɢɪɴɢ')}",
            icon="⚠️",
            raw_data=data
        )
    
    if status == "permanent_ban":
        return CheckResult(
            status=WhatsAppStatus.PERMANENT_BAN,
            message="🚫 ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ ʙᴀɴɴᴇᴅ",
            details=f"{analysis.get('description', 'ᴀᴄᴄᴏᴜɴᴛ ʙᴀɴɴᴇᴅ')}\n\n"
                   f"📊 ɪɴᴅɪᴄᴀᴛᴏʀs:\n"
                   f"• ᴘʀᴏғɪʟᴇ ᴀᴄᴄᴇss: ᴅᴇɴɪᴇᴅ\n"
                   f"• sᴛᴀᴛᴜs Access: ᴅᴇɴɪᴇᴅ\n"
                   f"• ᴀʟʟ ᴅᴀᴛᴀ: ɪɴᴀᴄᴄᴇssɪʙʟᴇ\n"
                   f"• ᴄᴏɴғɪᴅᴇɴᴄᴇ: {confidence.upper()}\n\n"
                   f"🚫 {analysis.get('recommendation', 'ᴅᴏ ɴᴏᴛ ᴍᴇssᴀɢᴇ')}",
            icon="🚫",
            raw_data=data
        )
    
    return CheckResult(
        status=WhatsAppStatus.UNKNOWN,
        message="❓ ᴜɴᴋɴᴏᴡɴ sᴛᴀᴛᴜs",
        details="ᴄᴏᴜʟᴅ ɴᴏᴛ ᴅᴇᴛᴇʀᴍɪɴᴇ ᴀᴄᴄᴏᴜɴᴛ sᴛᴀᴛᴜs.",
        icon="❓",
        raw_data=data
    )

def format_last_seen(timestamp: int) -> str:
    try:
        from datetime import datetime
        dt = datetime.fromtimestamp(timestamp / 1000)
        diff = datetime.now() - dt
        
        seconds = diff.total_seconds()
        if seconds < 60:
            return "ᴊᴜsᴛ ɴᴏᴡ"
        elif seconds < 3600:
            return f"{int(seconds/60)} ᴍɪɴᴜᴛᴇs ᴀɢᴏ"
        elif seconds < 86400:
            return f"{int(seconds/3600)} ʜᴏᴜʀs ᴀɢᴏ"
        else:
            return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return "Unknown"

async def checker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "❌ ᴜsᴀɢᴇ: `/ban_checker +234801234567`\n\n"
            "ᴜsᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴡʜᴀᴛsᴀᴘᴘ ɴᴜᴍʙᴇʀs.",
            parse_mode='Markdown'
        )
        return
    
    phone = context.args[0].strip()
    
    if not re.match(r'^\+\d{10,15}$', phone):
        await update.message.reply_text(
            "❌ ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ\n"
            "Use: `+2346407640464`",
            parse_mode='Markdown'
        )
        return
    
    msg = await update.message.reply_text(
        f"🔍 ᴄʜᴇᴄᴋɪɴɢ `{markdown_safe(phone)}`...\n`[{'░'*10}]` 0%",
        parse_mode='Markdown'
    )
    
    steps = [
        ("ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ʙᴀɪʟᴇʏs...", 25),
        ("ǫᴜᴇʀʏɪɴɢ ᴡʜᴀᴛsᴀᴘᴘ...", 50),
        ("ᴀɴᴀʟʏᴢɪɴɢ ʀᴇsᴘᴏɴsᴇ...", 75),
        ("ᴄᴏᴍᴘɪʟɪɴɢ ʀᴇsᴜʟᴛs...", 100)
    ]
    
    for text, pct in steps:
        await asyncio.sleep(0.8)
        filled = int(pct / 10)
        bar = "█" * filled + "░" * (10 - filled)
        try:
            await msg.edit_text(
                f"🔍 ᴄʜᴇᴄᴋɪɴɢ `{markdown_safe(phone)}`...\n`[{bar}]` {pct}%\n{text}",
                parse_mode='Markdown'
            )
        except:
            pass
 
    api_response = check_number_via_api(phone)
    result = interpret_result(api_response)
    
    output = f"""
┏❏ 🔍 ᴡʜᴀᴛsᴀᴘᴘ ɴᴜᴍʙᴇʀ ᴄʜᴇᴄᴋ ❐┓
┃
║ ❏📱 ɴᴜᴍʙᴇʀ: `{markdown_safe(phone)}`
┃
║ ❐ {markdown_safe(result.icon)} sᴛᴀᴛᴜs: {markdown_safe(result.message)}
┃
║ ❏ {markdown_safe(result.details)}
┃
║ ❐ ⏰ ᴄʜᴇᴄᴋᴇᴅ: {datetime.now().strftime('%H:%M:%S')}
┃
┗❐ 🔗 sᴏᴜʀᴄᴇ ᴜsᴇᴅ : ʙᴀɪʟᴇʏs ᴀᴘɪ ❐┛
"""
    
    if result.status in [WhatsAppStatus.ERROR, WhatsAppStatus.DISCONNECTED]:
        output += f"\n\n`ᴅᴇʙᴜɢ: {markdown_safe(str(result.raw_data)[:200])}`"
    
    await msg.edit_text(output, parse_mode='Markdown')

async def set_api_url_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BAILEYS_API_URL
    
    if not context.args:
        await update.message.reply_text(
            f"ᴄᴜʀʀᴇɴᴛ ᴀᴘɪ ᴜʀʟ: `{markdown_safe(BAILEYS_API_URL)}`\n\n"
            "ᴛᴏ ᴄʜᴀɴɢᴇ: `/setapi https://newurlxxxxxxx`",
            parse_mode='Markdown'
        )
        return
    
    new_url = context.args[0].strip().rstrip('/')
    BAILEYS_API_URL = new_url
    os.environ["BAILEYS_API_URL"] = new_url
    
    await update.message.reply_text(
        f"✅ ᴀᴘɪ ᴜʀʟ ᴜᴘᴅᴀᴛᴇᴅ ᴛᴏ:\n`{markdown_safe(new_url)}`",
        parse_mode='Markdown'
    )
