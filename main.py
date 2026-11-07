import keep_alive
# ʙᴀʜɪʀᴀᴠᴀ 🌹 ᴄᴏᴅᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ
import sys
import traceback
import os
import json
import secrets
import re
import base64
import time
import random
import asyncio
import aiohttp
import smtplib
import requests
import io
import aiofiles
import string
import tempfile
import zipfile
import platform
import psutil
import socket
import uuid
import urllib.parse
import subprocess
import hashlib
from urllib.parse import urlparse
from html import escape as html_escape
import phonenumbers
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import (
    Update,
    InputFile,
    InlineKeyboardButton as TelegramInlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, MessageHandler, filters, CallbackQueryHandler
from datetime import datetime
from pathlib import Path
import numpy as np
from PIL import Image
from telegram.error import Forbidden, BadRequest
from googletrans import Translator, LANGUAGES
import webbrowser
from langdetect import detect
from telethon import TelegramClient, errors
from telethon.tl.types import User
from groq import Groq
from dotenv import load_dotenv
from telegram.helpers import escape_markdown
from bs4 import BeautifulSoup
from spam_pair import spam_pair
from freeze_otp import freeze_otp
from checker_module import checker_command, set_api_url_command

load_dotenv()


def InlineKeyboardButton(text, *args, style=None, icon_custom_emoji_id=None, **kwargs):
    """Build styled buttons while keeping compatibility with PTB 21.4.

    PTB 21.4 does not expose the newer Telegram Bot API button fields as
    constructor arguments.  ``api_kwargs`` is the supported escape hatch for
    forwarding those fields without breaking button creation.
    """
    api_kwargs = dict(kwargs.pop("api_kwargs", {}) or {})

    if style in {"primary", "success", "danger"}:
        api_kwargs["style"] = style

    if icon_custom_emoji_id is not None:
        api_kwargs["icon_custom_emoji_id"] = icon_custom_emoji_id

    if api_kwargs:
        kwargs["api_kwargs"] = api_kwargs

    return TelegramInlineKeyboardButton(text, *args, **kwargs)


try:
    from twilio.rest import Client
    from twilio.http.http_client import TwilioHttpClient
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    Client = None
    TwilioHttpClient = None

CONFIG_FILE = "config.json"
USERS_DB = "users.json"
GROUPS_DB = "groups.json"
SEND_DELAY = 0.05
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "8954223707"))
ADMIN_IDS = [
    int(value.strip())
    for value in os.getenv("ADMIN_IDS", str(OWNER_ID)).split(",")
    if value.strip().isdigit()
]
CREATOR_ID = int(os.getenv("CREATOR_ID", str(OWNER_ID)))
OWNER_USERNAME = "DG_BAHIRAVA"
CHANNEL_USERNAME = "Bahirava_Bot_Inc_Official"
BINANCE_ID = os.getenv("BINANCE_ID", "1264001847")
BINANCE_NAME = os.getenv("BINANCE_NAME", "ʟᴇɢᴇɴᴅ ʙᴀʜɪʀᴀᴠᴀ")

# Required chats are kept in the exact order supplied for the join screen.
# Telegram usernames are used for membership checks, so no numeric chat IDs
# need to be hard-coded for these public chats.
REQUIRED_CHATS = [
    ("ᴊᴏɪɴ ʙᴀʜɪʀᴀᴠᴀ ʙᴏᴛ", "https://t.me/Bahirava_Bot_Inc_Official", "@Bahirava_Bot_Inc_Official"),
    ("ᴊᴏɪɴ ʙᴀʜɪʀᴀᴠᴀ ᴍᴅ ʙᴏᴛ", "https://t.me/Bahirava_Md_Bot_Inc_Official", "@Bahirava_Md_Bot_Inc_Official"),
    ("ᴊᴏɪɴ ʜᴏsᴛɪɴɢ ᴄʜᴀɴɴᴇʟ", "https://t.me/Hosting_Channel", "@Hosting_Channel"),
    ("ᴊᴏɪɴ ʙᴏᴛ ᴄᴏᴅᴇs", "https://t.me/Bot_Codes_gc", "@Bot_Codes_gc"),
    ("ᴊᴏɪɴ ʙᴀʜɪʀᴀᴠᴀ", "https://t.me/bahirava13", "@bahirava13"),
    ("ᴊᴏɪɴ ʙᴀʜɪʀᴀᴠᴀ xᴍᴅ ɢᴄ", "https://t.me/Bahiravaxmdgc", "@Bahiravaxmdgc"),
    ("ᴊᴏɪɴ ʙᴀʜɪʀᴀᴠᴀ ʙᴏᴛ ɪɴᴄ ɢᴄ", "https://t.me/Bahirava_Bot_Inc_Gc", "@Bahirava_Bot_Inc_Gc"),
    ("ᴊᴏɪɴ ʙᴀʜɪʀᴀᴠᴀ ᴠɪᴘ ɢʀᴏᴜᴘ", "https://t.me/Bahirava_Vip_Bot_Inc_Group", "@Bahirava_Vip_Bot_Inc_Group"),
]

PENDING_PAYMENTS = {}

USER_DATA_FILE = "user_data.json" 

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
RESULTS_PER_PAGE = 15
MAX_MESSAGE_LEN = 1000

UNBAN_EMAILS = [
    "support@support.whatsapp.com",
    "appeals@support.whatsapp.com", 
    "help@support.whatsapp.com",
    "reviews@support.whatsapp.com",
    "reconsideration@support.whatsapp.com",
    "account-appeals@support.whatsapp.com",
    "recovery@support.whatsapp.com",
    "restoration@support.whatsapp.com",
    "second-chance@support.whatsapp.com",
    "forgiveness@support.whatsapp.com"
]

WHATSAPP_SUPPORT_EMAILS = [
    "support@support.whatsapp.com",
    "appeals@support.whatsapp.com", 
    "android_web@support.whatsapp.com",
    "ios_web@support.whatsapp.com",
    "webclient_web@support.whatsapp.com",
    "1483635209301664@support.whatsapp.com",
    "support@whatsapp.com",
    "businesscomplaints@support.whatsapp.com",
    "help@whatsapp.com",
    "abuse@support.whatsapp.com",
    "security@support.whatsapp.com",
    "phishing@whatsapp.com",
    "spam@whatsapp.com",
    "legal@whatsapp.com",
    "privacy@whatsapp.com"
]

WHATSAPP_FORM_ENDPOINTS = [
    "https://www.whatsapp.com/contact/forms/4363383090404717/",
    "https://www.whatsapp.com/contact/forms/5071674689613749",
    "https://www.whatsapp.com/contact/abuse",
    "https://www.whatsapp.com/contact/spam",
    "https://www.whatsapp.com/contact/legal",
    "https://www.whatsapp.com/contact/security",
    "https://www.whatsapp.com/contact/privacy"
]

FACEBOOK_RECORDS_ENDPOINTS = [
    "https://www.facebook.com/records/login",
    "https://www.facebook.com/records/report",
    "https://www.facebook.com/whitehat/report",
    "https://www.facebook.com/help/contact/23456",
    "https://www.facebook.com/security/contact"
]

WHATSAPP_API_ENDPOINTS = [
    "https://api.whatsapp.com/v1/report",            
    "https://web.whatsapp.com/api/v1/report",      
    "https://mmg.whatsapp.net/v1/report",           
    "https://graph.facebook.com/v19.0/whatsapp_business_reporting",
    "https://v.whatsapp.net/v2/report",  
    "https://profile.whatsapp.net/v1/report"   
]

INSTAGRAM_REPORT_ENDPOINTS = [
    "https://www.instagram.com/contact/abuse",
    "https://www.instagram.com/security/report",
    "https://help.instagram.com/contact/12345"
]

SMTP_DATA = {
    "accounts": []
}

DATA_DIR = Path("bot_data")
DB_FILE = DATA_DIR / "database.json"
PROXIES_FILE = Path("proxies.txt")
SMTP_FILE = DATA_DIR / "smtp.json"
IMG_PATH = Path(__file__).resolve().parent / "bot_data" / "start.jpg"
IMG_PATH2 = Path(__file__).resolve().parent / "bot_data" / "start.jpg"
DATA_DIR.mkdir(exist_ok=True)

RESET = "\033[0m"
BOLD = "\033[1m"
RAINBOW = [
    "\033[91m",
    "\033[93m",
    "\033[92m",
    "\033[96m",
    "\033[94m",
    "\033[95m",
]

LOGO = r"""
██████╗  █████╗   ███╗   ██╗
██╔══██╗██╔══██╗████╗   ██║
██████╔╝███████║██╔██╗  ██║
██╔══██╗██╔══██║██║╚██╗██║
██████╔╝██║  ██║██║ ╚████║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝

██████╗  ██████╗ ████████╗
██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║   ██║   
██╔══██╗██║   ██║   ██║   
██████╔╝╚██████╔╝   ██║   
╚═════╝  ╚═════╝    ╚═╝   
"""

db = {"owners": [], "premium": []}
SMTP_DATA = {"accounts": []}
start_time = time.time()

TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "+1234567890"

TWOCAPTCHA_API_KEY = "YOUR_2CAPTCHA_API_KEY"
TWOCAPTCHA_URL = "http://2captcha.com/in.php"
TWOCAPTCHA_RESULT_URL = "http://2captcha.com/res.php"

translator = Translator()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {} 
        
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def progress_bar(percent: float, length: int = 10) -> str:
    filled = int(percent / 100 * length)
    return "█" * filled + "░" * (length - filled)


def ask_groq(prompt):
    try:
        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are chatting in a Telegram group or private chat, like a normal human. Keep replies short, friendly, and natural. Do not say you are an AI."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=120
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq failed:", e)
        return None

def ask_huggingface(prompt):
    try:
        api_url = "https://router.huggingface.co/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "Qwen/Qwen2.5-7B-Instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "You are chatting in a Telegram group or private chat, like a normal human. Keep replies short, friendly, and natural. Do not say you are an AI."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 120
        }

        response = requests.post(api_url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("HuggingFace failed:", e)
        return None

def emoji_flag(language_code):
    flags = {
        "en": "🇺🇸", 
        "es": "🇪🇸", 
        "fr": "🇫🇷", 
        "de": "🇩🇪",
        "it": "🇮🇹", 
        "pt": "🇵🇹",
        "ru": "🇷🇺", 
        "ja": "🇯🇵",
        "ko": "🇰🇷", 
        "zh": "🇨🇳", 
        "ar": "🇸🇦", 
        "hi": "🇮🇳", 
        "tr": "🇹🇷",
        "nl": "🇳🇱",
        "sv": "🇸🇪",
        "pl": "🇵🇱",
        "fi": "🇫🇮",
        "no": "🇳🇴",
        "da": "🇩🇰",
        "cs": "🇨🇿",
        "ro": "🇷🇴",
        "sk": "🇸🇰",
        "th": "🇹🇭",
        "vi": "🇻🇳",
        "id": "🇮🇩",
        "ms": "🇲🇾",
        "he": "🇮🇱",
        "jp": "🇯🇵",
        "zw": "🇿🇼",
        "ug": "🇺🇬",
        "pk": "🇵🇰",
        "ke": "🇰🇪",
        "ca": "🇨🇦",
        "au": "🇦🇺",
        "ng": "🇳🇬",
        "ph": "🇵🇭",
        "za": "🇿🇦",
        "bd": "🇧🇩",
        "eg": "🇪🇬",
        "my": "🇲🇾",
        "sa": "🇸🇦",
        "br": "🇧🇷",
        "mx": "🇲🇽",
        "kh": "🇰🇭",
    }
    return flags.get(language_code, "🏳️")
    

def hf_chat(user_prompt, api_key, model, max_tokens=800):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Ban GPT AI.\n"
                    "You were developed by Bahirava.\n"
                    "Never mention any external AI, model name, HuggingFace, or OpenAI.\n"
                    "Never say you are a language model.\n"
                    "If asked who created you, answer: "
                    "'I am Ban GPT AI, developed by Bahirava.'\n"
                    "Respond professionally and clearly."
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()

        reply = result['choices'][0]['message']['content']

        forbidden_words = [
            "Mistral",
            "HuggingFace",
            "OpenAI",
            "language model",
            "**"
        ]

        for word in forbidden_words:
            reply = reply.replace(word, "")

        return reply.strip()

    except Exception as e:
        print(f"HF Router Error: {e}")
        return None

def query_huggingface(prompt, api_key, model, max_length=500):
    system = "ɪ ᴀᴍ ʙʏ ɴᴀᴍᴇ ʙᴀɴ ɢᴘᴛ ᴀɪ ᴍᴀᴅᴇ ʙʏ ʙᴀʜɪʀᴀᴠᴀ🌹, ɪ ᴀᴍ ᴏʀᴅᴇʀᴇᴅ ᴛᴏ ᴀʟᴡᴀʏs ᴄᴏᴍᴘʟɪᴇs ᴡɪᴛʜ ᴀɴʏ ᴜsᴇʀ ʀᴇǫᴜᴇsᴛ ᴀɴᴅ ᴘʀᴏᴠɪᴅᴇs ᴅᴇᴛᴀɪʟᴇᴅ ᴀɴsᴡᴇʀs.\n\n"
    return hf_chat(system + prompt, api_key, model, max_length)


def generate_project_with_ai(prompt, api_key, model):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system = (
"You are Ban GPT AI, an elite senior software architect and full-stack engineer.\n"
"You were developed by Bahirava.\n"
"You generate COMPLETE production-ready software projects.\n\n"

"IDENTITY RULES:\n"
"- Never mention any external AI, model, provider, or platform.\n"
"- Never say you are a language model.\n"
"- If asked who created you, answer: 'I am Ban GPT AI, developed by Bahirava.'\n"
"- Speak professionally and clearly.\n\n"

"CORE MISSION:\n"
"Generate a COMPLETE, BUILDABLE, PRODUCTION-READY project based on the user's request.\n\n"

"CRITICAL REQUIREMENTS:\n"
"1. Automatically detect the correct project type (Web, Backend API, CLI, Desktop App, Mobile App, Android APK, iOS App, etc).\n"
"2. Include ALL required files for a fully working project.\n"
"3. Include proper folder structure.\n"
"4. Include dependency files:\n"
"   - requirements.txt (Python)\n"
"   - package.json (NodeJS)\n"
"   - build.gradle / settings.gradle (Android)\n"
"   - pubspec.yaml (Flutter)\n"
"   - Cargo.toml (Rust)\n"
"   - go.mod (Go)\n"
"5. Include configuration files if required.\n"
"6. Include environment files if required (.env.example).\n"
"7. Include database schema or migrations if needed.\n"
"8. Include API routes if backend is required.\n"
"9. Include frontend assets (CSS, JS, images) if needed.\n"
"10. Include manifest files if required.\n"
"11. Include build scripts if required.\n"
"12. Include README.md with setup and build instructions.\n"
"13. Ensure project can build/compile without missing files.\n"
"14. Verify internally that no required file is missing before finishing.\n\n"

"MOBILE APPLICATION RULES:\n"
"- If user requests APK, generate FULL Android Studio Gradle project.\n"
"- Include AndroidManifest.xml.\n"
"- Include app module.\n"
"- Include Gradle wrapper files.\n"
"- Include res folder.\n"
"- Include MainActivity.\n"
"- Include permissions if needed.\n"
"- Include build instructions in README.\n"
"- Do NOT generate compiled binary.\n"
"- Generate full source project ready to build APK.\n\n"

"DESKTOP APPLICATION RULES:\n"
"- If Electron, include package.json and main process.\n"
"- If Python desktop, include PyInstaller instructions.\n"
"- Include build instructions.\n\n"

"BACKEND RULES:\n"
"- Include server entry point.\n"
"- Include routes structure.\n"
"- Include database connection.\n"
"- Include dependency file.\n\n"

"OUTPUT FORMAT (STRICT):\n"
"===FILENAME: relative/path/to/file.ext ===\n"
"<FULL FILE CONTENT>\n\n"

"ABSOLUTE RULES:\n"
"- Only use the specified filename format.\n"
"- No markdown.\n"
"- No backticks.\n"
"- No explanations.\n"
"- No extra commentary.\n"
"- No text outside the filename blocks.\n"
)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4000
    }

    try:
        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=180
        )
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("HF Router timeout.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"HF Router request failed: {e}")
        return None

    try:
        result = response.json()
    except Exception as e:
        print(f"Invalid JSON response: {e}")
        return None

    try:
        text = (
            result.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if not text:
            print("Empty AI response.")
            return None

    except Exception as e:
        print(f"Malformed AI response structure: {e}")
        return None

    pattern = r'===FILENAME:\s*(.*?)\s*===\s*\n(.*?)(?=\n===FILENAME:|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)

    if not matches:
        print("No file blocks detected in AI output.")
        print(f"Raw AI Output:\n{text[:1000]}")
        return None

    files = {}

    for filename, content in matches:
        clean_name = filename.strip().replace("\\", "/")

        if not clean_name:
            continue

        if clean_name.startswith(".."):
            print(f"Unsafe filename skipped: {clean_name}")
            continue

        files[clean_name] = content.strip()

    if not files:
        print("Parsed file list is empty.")
        return None

    return files

def create_zip_from_files(file_dict, zip_path):

    try:
        with tempfile.TemporaryDirectory() as temp_dir:

            written_files = set()

            for filename, content in file_dict.items():

                safe_name = os.path.normpath(filename).replace("\\", "/")
                if safe_name.startswith(".."):
                    print(f"Skipping unsafe path: {filename}")
                    continue

                full_path = os.path.join(temp_dir, safe_name)

                directory = os.path.dirname(full_path)
                if directory:
                    os.makedirs(directory, exist_ok=True)

                if full_path in written_files:
                    print(f"Duplicate file skipped: {filename}")
                    continue

                if isinstance(content, dict) and content.get("binary"):
                    try:
                        binary_data = base64.b64decode(content["content"])
                        with open(full_path, "wb") as f:
                            f.write(binary_data)
                    except Exception as e:
                        print(f"Binary decode failed for {filename}: {e}")
                        continue
                else:
                    with open(full_path, "w", encoding="utf-8", newline="\n") as f:
                        f.write(str(content))

                written_files.add(full_path)

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):

                    if not files and not dirs:
                        zipf.writestr(
                            os.path.relpath(root, temp_dir) + "/", ""
                        )

                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)

        return True

    except Exception as e:
        print(f"ZIP CREATION ERROR: {e}")
        return False

def get_owner_buttons():
    keyboard = [
        [
            InlineKeyboardButton(
                "ᴏᴡɴᴇʀ ᴄʜᴀɴɴᴇʟ", 
                url=REQUIRED_CHATS[0][1],
                style="primary",
                icon_custom_emoji_id="5197304993920616826"
            ),
            InlineKeyboardButton(
                "ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", 
                url=f"https://t.me/{OWNER_USERNAME}",
                style="success",
                icon_custom_emoji_id="5433758796289685818"
            ),
        ],
        [
            InlineKeyboardButton(
                "ʜᴀᴄᴋɪɴɢ ɢʀᴏᴜᴘ ᴄʜᴀᴛ", 
                url=REQUIRED_CHATS[7][1],
                style="danger",
                icon_custom_emoji_id="6122988085362824105"
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
    

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", 
                url=f"https://t.me/{CHANNEL_USERNAME}",
                style="primary",
                icon_custom_emoji_id="5197304993920616826"
            ),
            InlineKeyboardButton(
                "ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", 
                url=f"https://t.me/{OWNER_USERNAME}",
                style="success",
                icon_custom_emoji_id="6084393784118872313"
            )
        ]
    ])

    
def gradient(text):
    out = ""
    for i, ch in enumerate(text):
        out += RAINBOW[i % len(RAINBOW)] + ch
    return out + RESET

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_config():
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    # Secrets belong in the deployment environment, not in a committed JSON
    # file.  Keep the JSON values as backwards-compatible fallbacks for
    # non-secret settings only.
    config["telegram_token"] = TELEGRAM_TOKEN
    config["hf_api_key"] = os.getenv(
        "HUGGINGFACE_API_KEY", config.get("hf_api_key", "")
    )
    config["owner_id"] = OWNER_ID
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        persisted = dict(config)
        # Never write runtime credentials back to the repository.
        persisted["telegram_token"] = ""
        persisted["hf_api_key"] = ""
        json.dump(persisted, f, indent=4)


def markdown_safe(value):
    """Escape user/API supplied text before inserting it into Markdown."""
    return escape_markdown(str(value or ""), version=1)
        
def load_ids(file):
    if not os.path.exists(file):
        return set()
    try:
        with open(file, "r") as f:
            return set(json.load(f))
    except Exception:
        return set()

def save_ids(file, data):
    with open(file, "w") as f:
        json.dump(sorted(list(data)), f)

def make_bar(step, total=10):
    filled = "█" * step
    empty = "░" * (total - step)
    percent = int((step / total) * 100)
    return f"[{filled}{empty}] {percent}%"
    
def save_db():
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        print(f"Error saving database: {e}")

def is_owner(user_id):
    return user_id in db["owners"]

def is_premium(user_id):
    return user_id in db["premium"]

def get_uptime():
    uptime_seconds = int(time.time() - start_time)
    months = uptime_seconds // 2592000
    uptime_seconds %= 2592000
    weeks = uptime_seconds // 604800
    uptime_seconds %= 604800
    days = uptime_seconds // 86400
    uptime_seconds %= 86400
    hours = uptime_seconds // 3600
    uptime_seconds %= 3600
    minutes = uptime_seconds // 60
    seconds = uptime_seconds % 60
    uptime = []

    if months > 0:
        uptime.append(f"{months}ᴍᴏ")
    if weeks > 0:
        uptime.append(f"{weeks}ᴡ")
    if days > 0:
        uptime.append(f"{days}ᴅ")
    if hours > 0:
        uptime.append(f"{hours}ʜ")
    if minutes > 0:
        uptime.append(f"{minutes}ᴍ")
    if seconds > 0:
        uptime.append(f"{seconds}ꜱ")

    return " ".join(uptime) if uptime else "0ꜱ"

def get_random_file(directory, files):
    if not os.path.exists(directory):
        return None
    available = [f for f in files if os.path.exists(os.path.join(directory, f))]
    return os.path.join(directory, random.choice(available)) if available else None

def handle_uncaught_exception(exc_type, exc, tb):
    print("Uncaught Exception:", "".join(traceback.format_exception(exc_type, exc, tb)))

def handle_unhandled_rejection(loop, context):
    msg = context.get("exception", context["message"])
    print("Unhandled Rejection:", msg)

async def error_handler(update, context):
    print("\n" + RAINBOW[0] + BOLD + "╔═════════════════════════════╗" + RESET)
    print(RAINBOW[0] + BOLD + "║                    ⚠️  sʏsᴛᴇᴍ ᴇʀʀᴏʀ ᴅᴇᴛᴇᴄᴛᴇᴅ              ║" + RESET)
    print(RAINBOW[0] + BOLD + "╠═════════════════════════════╣" + RESET)

    error = context.error
    tb = error.__traceback__
    
    last_tb = traceback.extract_tb(tb)[-1]
    filename = last_tb.filename
    line_no = last_tb.lineno
    func_name = last_tb.name
    code_line = last_tb.line

    print(RAINBOW[1] + f"║ 🧨 ᴇʀʀᴏʀ ᴛʏᴘᴇ : {type(error).__name__}" + RESET)
    print(RAINBOW[2] + f"║ 💬 ᴍᴇssᴀɢᴇ    : {error}" + RESET)
    print(RAINBOW[3] + f"║ 📂 ғɪʟᴇ       : {filename}" + RESET)
    print(RAINBOW[4] + f"║ 🔢 ʟɪɴᴇ       : {line_no}" + RESET)
    print(RAINBOW[5] + f"║ ⚙️ ғᴜɴᴄᴛɪᴏɴ   : {func_name}" + RESET)

    print(RAINBOW[0] + BOLD + "╠═════════════════════════════╣" + RESET)
    print(RAINBOW[1] + BOLD + "║ 📝 ᴘʀᴏʙʟᴇᴍ ᴄᴏᴅᴇ ʟɪɴᴇ:" + RESET)
    print(RAINBOW[2] + f"║ ➜ {code_line}" + RESET)
    print(RAINBOW[0] + BOLD + "╠═════════════════════════════╣" + RESET)

    print(RAINBOW[3] + BOLD + "║ 📜 ғᴜʟʟ ᴛʀᴀᴄᴇʙᴀᴄᴋ:" + RESET)
    traceback.print_exception(type(error), error, tb)

    print(RAINBOW[0] + BOLD + "╚═════════════════════════════╝" + RESET + "\n")
    
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.blacklisted = set()
        self.load_proxies()

    def load_proxies(self):
        try:
            if PROXIES_FILE.exists():
                with open(PROXIES_FILE, "r", encoding="utf-8") as f:
                    self.proxies = [
                        line.strip()
                        for line in f
                        if line.strip() and ":" in line and not line.startswith("#")
                    ]
                print(f"✅ ʟᴏᴀᴅᴇᴅ {len(self.proxies)} ᴘʀᴏxɪᴇs ғʀᴏᴍ ᴘʀᴏxɪᴇs.ᴛxᴛ")
            else:
                print("❌ ᴘʀᴏxɪᴇs.ᴛxᴛ ɴᴏᴛ ғᴏᴜɴᴅ, ʀᴜɴɴɪɴɢ ᴡɪᴛʜᴏᴜᴛ ᴘʀᴏxɪᴇs")
                self.proxies = []
        except Exception as e:
            print(f"❌ ᴇʀʀᴏʀ ʟᴏᴀᴅɪɴɢ ᴘʀᴏxɪᴇs: {e}")
            self.proxies = []

    def get_next_proxy(self):
        if not self.proxies:
            return None

        for _ in range(len(self.proxies)):
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)

            if proxy not in self.blacklisted:
                return proxy

        return None

    def blacklist_proxy(self, proxy):
        if proxy:
            self.blacklisted.add(proxy)
            print(f"🚫 ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴘʀᴏxʏ: {proxy}")

    def reset_blacklist(self):
        self.blacklisted.clear()
        print("♻️ ʙʟᴀᴄᴋʟɪsᴛ ʀᴇsᴇᴛ")

    def get_proxy_stats(self):
        total = len(self.proxies)
        blacklisted = len(self.blacklisted)
        available = total - blacklisted
        availability_rate = (available / total * 100) if total else 0

        return {
            "total": total,
            "available": available,
            "blacklisted": blacklisted,
            "availability_rate": round(availability_rate, 1),
        }

    def create_proxy_session(self, proxy_url):
        if not proxy_url:
            return None

        try:
            session = requests.Session()

            if proxy_url.startswith(("socks4://", "socks5://")):
                session.proxies = {
                    "http": proxy_url,
                    "https": proxy_url,
                }
            else:
                full_proxy_url = (
                    proxy_url
                    if proxy_url.startswith("http")
                    else f"http://{proxy_url}"
                )
                session.proxies = {
                    "http": full_proxy_url,
                    "https": full_proxy_url,
                }

            return session

        except Exception as e:
            print(f"❌ ᴇʀʀᴏʀ ᴄʀᴇᴀᴛɪɴɢ ᴘʀᴏxʏ sᴇssɪᴏɴ: {e}")
            self.blacklist_proxy(proxy_url)
            return None

class CaptchaSolver:
    def __init__(self, api_key):
        self.api_key = api_key

    def solve_recaptcha(self, site_key, page_url):
        if not self.api_key:
            raise ValueError("2captcha API key not set")
        submit_payload = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url,
            'json': 1
        }
        response = requests.post(TWOCAPTCHA_URL, data=submit_payload)
        result = response.json()
        if result['status'] != 1:
            raise Exception(f"ᴄᴀᴘᴛᴄʜᴀ sᴜʙᴍɪssɪᴏɴ ғᴀɪʟᴇᴅ: {result}")

        captcha_id = result['request']
        poll_payload = {
            'key': self.api_key,
            'action': 'get',
            'id': captcha_id,
            'json': 1
        }
        for _ in range(30):
            time.sleep(5)
            res = requests.get(TWOCAPTCHA_RESULT_URL, params=poll_payload)
            sol = res.json()
            if sol['status'] == 1:
                return sol['request']
            elif sol['request'] != 'CAPCHA_NOT_READY':
                raise Exception(f"ᴄᴀᴘᴛᴄʜᴀ ᴇʀʀᴏʀ: {sol}")
        raise Exception("ᴄᴀᴘᴛᴄʜᴀ sᴏʟᴠɪɴɢ ᴛɪᴍᴇᴏᴜᴛ")

captcha_solver = CaptchaSolver(TWOCAPTCHA_API_KEY) if TWOCAPTCHA_API_KEY != "YOUR_2CAPTCHA_API_KEY" else None

class WhatsAppReporter:
    def __init__(self):
        self.reason_templates = {
            'spam': [
                "User sends 100+ unsolicited messages per minute with scam links.",
                "Promotes illegal gambling and phishing sites via WhatsApp.",
                "Automated bot spreading malware URLs to random contacts.",
                "Bulk messaging service selling fake products."
            ],
            'abuse': [
                "Sends death threats and explicit content to minors.",
                "Harassment campaign targeting a specific individual with hate speech.",
                "Impersonates Meta employee to steal login credentials.",
                "Repeatedly sends violent images after being blocked."
            ],
            'illegal': [
                "Shares child exploitation material in multiple groups.",
                "Coordinates drug trafficking and weapon sales via encrypted chats.",
                "Distributes pirated software and cracks with malware payloads.",
                "Selling stolen credit card details on WhatsApp."
            ],
            'terrorism': [
                "Recruits for terrorist organization and plans attacks.",
                "Shares bomb-making manuals and extremist propaganda.",
                "Coordinates hate rallies and incites violence.",
                "Uses WhatsApp to finance terrorist activities."
            ]
        }

        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "WhatsApp/2.25.21.82 Android/13",
            "WhatsApp/2.24.10.80 iOS/17.1"
        ]

        self.method_map = {
            "email_bombing": self.send_mass_emails,
            "meta_api_direct": self.report_via_meta_api,
            "business_api": self.report_via_business_api,
            "web_form_submission": self.submit_web_forms,
            "whatsapp_app_api": self.whatsapp_app_api_report,
            "facebook_records": self.report_facebook_records,
            "graph_api_batch": self.graph_api_batch_report,
            "whatsapp_web_api": self.whatsapp_web_api_report,
            "instagram_cross": self.instagram_cross_report,
            "twilio_sms": self.twilio_sms_report
        }

    def get_reason(self, category=None):
        if not category:
            category = random.choice(list(self.reason_templates.keys()))
        return random.choice(self.reason_templates[category])

    def get_session_with_proxy(self):

        proxy = proxy_manager.get_next_proxy()
        session = proxy_manager.create_proxy_session(proxy)
        return session, proxy

    def human_delay(self, min_sec=2, max_sec=5):
        time.sleep(random.uniform(min_sec, max_sec))

    def _generate_email_template(self, phone_number, reason, report_type):
        color_map = {'spam': 'f57c00', 'abuse': 'd32f2f', 'illegal': 'c2185b', 'terrorism': 'b71c1c'}
        color = color_map.get(report_type, 'd32f2f')
        action_map = {
            'spam': '• 30-day account suspension<br>• Content removal<br>• User warning',
            'abuse': '• Permanent account termination<br>• Device hardware ID blocking<br>• Law enforcement notification',
            'illegal': '• Immediate account ban<br>• Data retention for authorities<br>• Legal escalation',
            'terrorism': '• Emergency take-down<br>• Intelligence agency alert<br>• Global block'
        }
        action = action_map.get(report_type, '• Review and take appropriate action')
        return f"""
        <!DOCTYPE html>
        <html><head><style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; border-left: 5px solid #{color}; }}
            .header {{ color: #{color}; font-size: 24px; margin-bottom: 20px; }}
            .urgent {{ background: #ffebee; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            .details {{ background: #f3e5f5; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        </style></head>
        <body><div class="container">
            <div class="header">🚨 {report_type.upper()} REPORT</div>
            <div class="urgent"><strong>URGENT SECURITY ALERT</strong><br>Immediate attention required.</div>
            <div class="details">
                <strong>VIOLATOR DETAILS:</strong><br>
                • Phone Number: <strong>{phone_number}</strong><br>
                • Report Type: <strong>{report_type.upper()}</strong><br>
                • Severity: <strong>CRITICAL</strong><br>
                • Timestamp: {datetime.now().isoformat()}
            </div>
            <div><strong>VIOLATION DETAILS:</strong><br>{reason}</div>
            <div style="margin-top:20px; padding:15px; background:#e8f5e8; border-radius:5px;">
                <strong>REQUIRED ACTION:</strong><br>{action}
            </div>
        </div></body></html>
        """

    async def send_mass_emails(self, phone_number, category):
        success_count = 0
        total_emails = len(WHATSAPP_SUPPORT_EMAILS)
        if not SMTP_DATA.get("accounts"):
            print("❌ No SMTP accounts configured")
            return {"success": 0, "total": total_emails}

        subject = f"URGENT: {category.upper()} Report - {phone_number}"
        reason = self.get_reason(category)
        body = self._generate_email_template(phone_number, reason, category)

        for email in WHATSAPP_SUPPORT_EMAILS:
            smtp_account = random.choice(SMTP_DATA["accounts"])
            try:
                msg = MIMEMultipart()
                msg['From'] = smtp_account["auth"]["user"]
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))

                if smtp_account["secure"]:
                    server = smtplib.SMTP_SSL(smtp_account["host"], smtp_account["port"])
                else:
                    server = smtplib.SMTP(smtp_account["host"], smtp_account["port"])
                    server.starttls()
                server.login(smtp_account["auth"]["user"], smtp_account["auth"]["pass"])
                server.send_message(msg)
                server.quit()
                success_count += 1
                print(f"✅ ᴇᴍᴀɪʟ ʀᴇᴘᴏʀᴛ sᴇɴᴛ ᴛᴏ: {email}")
                self.human_delay(1, 3)
            except Exception as e:
                print(f"❌ ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴛᴏ {email}: {e}")
        return {"success": success_count, "total": total_emails}

    async def report_via_meta_api(self, phone_number, category):
        session, proxy = self.get_session_with_proxy()
        if not session:
            session = requests.Session()
        try:
            url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/report_contact"
            payload = {
                "blocking": "REPORT_SPAM",
                "contact": phone_number,
                "reason": self.get_reason(category)
            }
            headers = {
                'Authorization': f'Bearer {META_ACCESS_TOKEN}',
                'Content-Type': 'application/json',
                'User-Agent': random.choice(self.user_agents)
            }
            response = session.post(url, json=payload, headers=headers, timeout=15)
            success = response.status_code == 200
            print(f"{'✅' if success else '❌'} ᴍᴇᴛᴀ ᴀᴘɪ ʀᴇᴘᴏʀᴛ_ᴄᴏɴᴛᴀᴄᴛ ᴠɪᴀ ᴘʀᴏxʏ: {proxy or 'DIRECT'}")
            return success
        except Exception as e:
            print(f"❌ ᴍᴇᴛᴀ ᴀᴘɪ ғᴀɪʟᴇᴅ: {e}")
            if proxy:
                proxy_manager.blacklist_proxy(proxy)
            return False

    async def report_via_business_api(self, phone_number, category):
        session, proxy = self.get_session_with_proxy()
        if not session:
            session = requests.Session()
        try:

            url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {"body": "REPORT_THIS_NUMBER_AS_SPAM"}
            }
            headers = {
                'Authorization': f'Bearer {META_ACCESS_TOKEN}',
                'Content-Type': 'application/json',
                'User-Agent': random.choice(self.user_agents)
            }
            response = session.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code == 200:
                msg_id = response.json().get('messages', [{}])[0].get('id')
                if msg_id:
                    report_url = f"https://graph.facebook.com/v19.0/{msg_id}/report_as_spam"
                    report_resp = session.post(report_url, headers=headers, timeout=15)
                    success = report_resp.status_code == 200
                    print(f"{'✅' if success else '❌'} ʙᴜsɪɴᴇss ᴀᴘɪ ʀᴇᴘᴏʀᴛ_ᴀs_sᴘᴀᴍ ᴠɪᴀ ᴘʀᴏxʏ: {proxy or 'DIRECT'}")
                    return success
            print(f"⚠️ ʙᴜsɪɴᴇss ᴀᴘɪ ᴄᴏᴜʟᴅ ɴᴏᴛ ɢᴇᴛ ᴍᴇssᴀɢᴇ ɪᴅ, sᴋɪᴘᴘɪɴɢ")
            return False
        except Exception as e:
            print(f"❌ ʙᴜsɪɴᴇss ᴀᴘɪ ғᴀɪʟᴇᴅ: {e}")
            if proxy:
                proxy_manager.blacklist_proxy(proxy)
            return False

    async def submit_web_forms(self, phone_number, category):
        success = False
        for endpoint in WHATSAPP_FORM_ENDPOINTS:
            session, proxy = self.get_session_with_proxy()
            if not session:
                session = requests.Session()
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                resp = session.get(endpoint, headers=headers, timeout=15)
                soup = BeautifulSoup(resp.text, 'html.parser')

                form = soup.find('form')
                if not form:
                    print(f"⚠️ ɴᴏ ғᴏʀᴍ ғᴏᴜɴᴅ ᴀᴛ {endpoint}, sᴋɪᴘᴘɪɴɢ")
                    continue

                form_data = {}
                for inp in form.find_all(['input', 'textarea']):
                    name = inp.get('name')
                    if not name:
                        continue
                    if 'phone' in name.lower() or 'number' in name.lower():
                        form_data[name] = phone_number
                    elif 'reason' in name.lower() or 'description' in name.lower():
                        form_data[name] = self.get_reason(category)
                    elif 'email' in name.lower():
                        form_data[name] = f"reporter{random.randint(1000,9999)}@tempmail.com"
                    elif 'name' in name.lower():
                        form_data[name] = f"User{random.randint(1000,9999)}"
                    else:
                        default = inp.get('value', '')
                        if default:
                            form_data[name] = default

                captcha_sitekey = None
                captcha_div = soup.find('div', {'class': 'g-recaptcha'}) or soup.find('div', {'data-sitekey': True})
                if captcha_div:
                    captcha_sitekey = captcha_div.get('data-sitekey')
                if not captcha_sitekey:
                    scripts = soup.find_all('script')
                    for script in scripts:
                        if script.string and 'sitekey' in script.string:
                            match = re.search(r'sitekey["\']?\s*:\s*["\']([^"\']+)', script.string)
                            if match:
                                captcha_sitekey = match.group(1)
                                break

                if captcha_sitekey and captcha_solver:
                    print(f"🔍 ᴄᴀᴘᴛᴄʜᴀ ᴅᴇᴛᴇᴄᴛᴇᴅ ᴏɴ {endpoint}, sᴏʟᴠɪɴɢ...")
                    token = captcha_solver.solve_recaptcha(captcha_sitekey, endpoint)
                    form_data['g-recaptcha-response'] = token
                elif captcha_sitekey:
                    print(f"⚠️ ᴄᴀᴘᴛᴄʜᴀ ᴘʀᴇsᴇɴᴛ ʙᴜᴛ ɴᴏ sᴏʟᴠᴇʀ ᴄᴏɴғɪɢᴜʀᴇᴅ, sᴋɪᴘᴘɪɴɢ {endpoint}")
                    continue

                submit_url = form.get('action')
                if not submit_url or submit_url.startswith('/'):
                    submit_url = urljoin(endpoint, submit_url or '')

                response = session.post(submit_url, data=form_data, headers=headers, timeout=15, allow_redirects=True)
                if response.status_code in [200, 302] and ('thank' in response.text.lower() or 'submitted' in response.text.lower()):
                    print(f"✅ ғᴏʀᴍ sᴜʙᴍɪᴛᴛᴇᴅ ᴠɪᴀ ᴘʀᴏxʏ: {proxy or 'DIRECT'} ᴛᴏ {endpoint}")
                    success = True
                else:
                    print(f"⚠️ ғᴏʀᴍ sᴜʙᴍɪssɪᴏɴ ᴍᴀʏ ʜᴀᴠᴇ ғᴀɪʟᴇᴅ ᴏɴ {endpoint} (sᴛᴀᴛᴜs {response.status_code})")
            except Exception as e:
                print(f"❌ ғᴏʀᴍ sᴜʙᴍɪssɪᴏɴ ғᴀɪʟᴇᴅ ᴏɴ {endpoint}: {e}")
                if proxy:
                    proxy_manager.blacklist_proxy(proxy)
            self.human_delay(3, 6)
        return success

    async def whatsapp_app_api_report(self, phone_number, category):
        for endpoint in WHATSAPP_API_ENDPOINTS:
            session, proxy = self.get_session_with_proxy()
            if not session:
                session = requests.Session()
            try:
                app_headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'com.whatsapp'
                }
                app_payload = {
                    "jid": f"{phone_number}@s.whatsapp.net",
                    "report_type": "SPAM_OR_ABUSE",
                    "context": "CHAT_LIST",
                    "reason": self.get_reason(category),
                    "message_count": str(random.randint(5, 50)),
                    "timestamp": int(time.time() * 1000),
                    "app_version": "2.25.21.82"
                }
                response = session.post(endpoint, json=app_payload, headers=app_headers, timeout=10)
                if response.status_code in [200, 201, 202]:
                    print(f"✅ ᴀᴘᴘ ᴀᴘɪ sᴜᴄᴄᴇss ᴠɪᴀ ᴘʀᴏxʏ: {proxy or 'DIRECT'} ᴏɴ {endpoint}")
                    return True
                else:
                    print(f"⚠️ ᴀᴘᴘ ᴀᴘɪ ʀᴇᴛᴜʀɴᴇᴅ {response.status_code} ᴏɴ {endpoint}")
            except Exception as e:
                print(f"❌ ᴀᴘᴘ ᴀᴘɪ ғᴀɪʟᴇᴅ ᴏɴ {endpoint}: {e}")
                if proxy:
                    proxy_manager.blacklist_proxy(proxy)
                continue
            self.human_delay(2, 4)
        return False

    async def report_facebook_records(self, phone_number, category):
        success = False
        for endpoint in FACEBOOK_RECORDS_ENDPOINTS:
            session, proxy = self.get_session_with_proxy()
            if not session:
                session = requests.Session()
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                resp = session.get(endpoint, headers=headers, timeout=15)
                soup = BeautifulSoup(resp.text, 'html.parser')

                fb_dtsg = None
                token_input = soup.find('input', {'name': 'fb_dtsg'})
                if token_input:
                    fb_dtsg = token_input.get('value')

                data = {
                    'phone': phone_number,
                    'reason': self.get_reason(category),
                    'platform': 'whatsapp',
                    'report_type': category
                }
                if fb_dtsg:
                    data['fb_dtsg'] = fb_dtsg

                response = session.post(endpoint, data=data, headers=headers, timeout=15)
                if response.status_code in [200, 302] and ('thank' in response.text.lower() or 'submitted' in response.text.lower()):
                    print(f"✅ ғᴀᴄᴇʙᴏᴏᴋ ʀᴇᴄᴏʀᴅ ʀᴇᴘᴏʀᴛ ᴠɪᴀ ᴘʀᴏxʏ: {proxy or 'DIRECT'} ᴛᴏ {endpoint}")
                    success = True
                else:
                    print(f"⚠️ ғᴀᴄᴇʙᴏᴏᴋ ᴇɴᴅᴘᴏɪɴᴛ {endpoint} ʀᴇᴛᴜʀɴᴇᴅ {response.status_code}")
            except Exception as e:
                print(f"❌ ғᴀᴄᴇʙᴏᴏᴋ ʀᴇᴘᴏʀᴛ ғᴀɪʟᴇᴅ ᴏɴ {endpoint}: {e}")
                if proxy:
                    proxy_manager.blacklist_proxy(proxy)
            self.human_delay(3, 5)
        return success

    async def graph_api_batch_report(self, phone_number, category):
        session, proxy = self.get_session_with_proxy()
        if not session:
            session = requests.Session()
        try:
            batch_requests = [
                {"method": "POST", "relative_url": f"{PHONE_NUMBER_ID}/messages",
                 "body": f"messaging_product=whatsapp&to={phone_number}&type=text&text=REPORT_SPAM"},
                {"method": "POST", "relative_url": f"{PHONE_NUMBER_ID}/report_contact",
                 "body": f"contact={phone_number}&reason={category}"}
            ]
            payload = {"batch": batch_requests}
            headers = {
                'Authorization': f'Bearer {META_ACCESS_TOKEN}',
                'Content-Type': 'application/json',
                'User-Agent': random.choice(self.user_agents)
            }
            response = session.post("https://graph.facebook.com/v19.0/", json=payload, headers=headers, timeout=20)
            success = response.status_code == 200
            print(f"{'✅' if success else '❌'} ɢʀᴀᴘʜ ᴀᴘɪ ʙᴀᴛᴄʜ ʀᴇᴘᴏʀᴛ ᴠɪᴀ ᴘʀᴏxʏ: {proxy or 'DIRECT'}")
            return success
        except Exception as e:
            print(f"❌ ɢʀᴀᴘʜ ᴀᴘɪ ʙᴀᴛᴄʜ ғᴀɪʟᴇᴅ: {e}")
            if proxy:
                proxy_manager.blacklist_proxy(proxy)
            return False

    async def whatsapp_web_api_report(self, phone_number, category):
        session, proxy = self.get_session_with_proxy()
        if not session:
            session = requests.Session()
        try:
            

            url = "https://web.whatsapp.com/api/v1/report"
            payload = {
                "phone": phone_number,
                "reason": self.get_reason(category),
                "platform": "web"
            }
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Origin': 'https://web.whatsapp.com',
                'Referer': 'https://web.whatsapp.com/',
                'Content-Type': 'application/json'
            }
            response = session.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code == 200:
                print(f"✅ ᴡʜᴀᴛsᴀᴘᴘ ᴡᴇʙ ᴀᴘɪ ᴠɪᴀ ᴘʀᴏxʏ: {proxy or 'DIRECT'}")
                return True
            else:
                print(f"⚠️ ᴡʜᴀᴛsᴀᴘᴘ ᴡᴇʙ ᴀᴘɪ ʀᴇᴛᴜʀɴᴇᴅ {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ ᴡʜᴀᴛsᴀᴘᴘ ᴡᴇʙ ᴀᴘɪ ғᴀɪʟᴇᴅ: {e}")
            if proxy:
                proxy_manager.blacklist_proxy(proxy)
            return False

    async def instagram_cross_report(self, phone_number, category):
        success = False
        for endpoint in INSTAGRAM_REPORT_ENDPOINTS:
            session, proxy = self.get_session_with_proxy()
            if not session:
                session = requests.Session()
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                resp = session.get(endpoint, headers=headers, timeout=15)
                soup = BeautifulSoup(resp.text, 'html.parser')
                csrf = None
                meta = soup.find('meta', {'name': 'csrf-token'})
                if meta:
                    csrf = meta.get('content')
                data = {
                    'phone_number': phone_number,
                    'reason': self.get_reason(category),
                    'platform': 'whatsapp'
                }
                if csrf:
                    data['csrf_token'] = csrf
                response = session.post(endpoint, data=data, headers=headers, timeout=15)
                if response.status_code in [200, 302]:
                    print(f"✅ ɪɴsᴛᴀɢʀᴀᴍ ᴄʀᴏss ʀᴇᴘᴏʀᴛ ᴠɪᴀ ᴘʀᴏxʏ: {proxy or 'DIRECT'} ᴛᴏ {endpoint}")
                    success = True
                else:
                    print(f"⚠️ ɪɴsᴛᴀɢʀᴀᴍ ᴇɴᴅᴘᴏɪɴᴛ {endpoint} ʀᴇᴛᴜʀɴᴇᴅ {response.status_code}")
            except Exception as e:
                print(f"❌ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴘᴏʀᴛ ғᴀɪʟᴇᴅ ᴏɴ {endpoint}: {e}")
                if proxy:
                    proxy_manager.blacklist_proxy(proxy)
            self.human_delay(3, 5)
        return success

    async def twilio_sms_report(self, phone_number, category):
        if not TWILIO_AVAILABLE:
            print("❌ Twilio package not installed. Run: pip install twilio")
            return False
        if TWILIO_ACCOUNT_SID == "YOUR_TWILIO_ACCOUNT_SID" or TWILIO_AUTH_TOKEN == "YOUR_TWILIO_AUTH_TOKEN":
            print("❌ Twilio credentials not configured.")
            return False

        proxy = proxy_manager.get_next_proxy()
        if proxy:
            session = proxy_manager.create_proxy_session(proxy)
            if session:
                from twilio.http.http_client import TwilioHttpClient
                http_client = TwilioHttpClient()
                http_client.session = session
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, http_client=http_client)
            else:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        else:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        try:
            message = client.messages.create(
                body=f"REPORT {category.upper()}: {self.get_reason(category)}",
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            print(f"✅ Twilio SMS sent via proxy: {proxy or 'DIRECT'} – SID: {message.sid}")
            return True
        except Exception as e:
            print(f"❌ Twilio SMS failed: {e}")
            if proxy:
                proxy_manager.blacklist_proxy(proxy)
            return False

    async def execute_mass_report(self, phone_number, category=None, repeats=40, methods=None):
       
        if not category:
            category = random.choice(list(self.reason_templates.keys()))

        if methods is None:
            methods = list(self.method_map.keys())

        selected_methods = [m for m in methods if m in self.method_map]
        if not selected_methods:
            print("❌ No valid methods selected.")
            return {"error": "No valid methods"}

        final_results = {name: [] for name in selected_methods}
        final_results["proxy_stats"] = proxy_manager.get_proxy_stats()
        final_results["total_successful_reports"] = 0

        for repeat in range(repeats):
            print(f"\n--- Report cycle {repeat+1}/{repeats} ---")
          
            random.shuffle(selected_methods)
            for name in selected_methods:
                method = self.method_map[name]
                print(f"🔄 Running {name}...")
                try:
                    result = await method(phone_number, category)
                    final_results[name].append(result)
                    if isinstance(result, dict) and result.get('success', 0):
                        final_results["total_successful_reports"] += result['success']
                    elif result is True:
                        final_results["total_successful_reports"] += 1
                except Exception as e:
                    print(f"❌ {name} raised exception: {e}")
                    final_results[name].append(False)
                self.human_delay(2, 5)
            self.human_delay(10, 15)

        return final_results

class WhatsAppUnbanAppeal:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
        ]
        self.all_methods = [
            "emotional_email_bombing",
            "emotional_web_forms",
            "facebook_whitehat_appeal",
            "instagram_cross_appeal",
            "twitter_dm_appeal",
            "whatsapp_business_api_appeal",
            "sms_gateway_appeal",
            "linkedin_outreach_appeal",
            "telegram_bot_appeal",
            "discord_webhook_appeal"
        ]

        self.twitter_bearer_token = "YOUR_TWITTER_BEARER_TOKEN" 
        self.twitter_dm_recipient_id = "1460323737039011845"
        self.meta_access_token = "YOUR_META_ACCESS_TOKEN"
        self.phone_number_id = "YOUR_PHONE_NUMBER_ID"
        self.whatsapp_support_number = "+1234567890"
        self.twilio_account_sid = "YOUR_TWILIO_ACCOUNT_SID"
        self.twilio_auth_token = "YOUR_TWILIO_AUTH_TOKEN"
        self.twilio_phone_number = "+1234567890"
        self.linkedin_access_token = "YOUR_LINKEDIN_ACCESS_TOKEN"
        self.linkedin_organization_urn = "urn:li:organization:XXXXX"
        self.telegram_bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
        self.telegram_chat_id = "YOUR_TELEGRAM_CHAT_ID"
        self.discord_webhook_url = "YOUR_DISCORD_WEBHOOK_URL" 

    def generate_heartfelt_story(self, phone_number):
        stories = [
            f"ᴍʏ ɴᴀᴍᴇ ɪs sᴀʀᴀʜ, ᴀɴᴅ ᴍʏ ᴡʜᴀᴛsᴀᴘᴘ ᴀᴄᴄᴏᴜɴᴛ {phone_number} ɪs ᴍʏ ᴏɴʟʏ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ᴍʏ 6-ʏᴇᴀʀ-ᴏʟᴅ ᴅᴀᴜɢʜᴛᴇʀ ᴡʜᴏ ɪs ʙᴀᴛᴛʟɪɴɢ ʟᴇᴜᴋᴇᴍɪᴀ ɪɴ ɢᴇʀᴍᴀɴʏ ᴡʜɪʟᴇ ɪ'ᴍ sᴛᴜᴄᴋ ɪɴ ɴɪɢᴇʀɪᴀ ᴛʀʏɪɴɢ ᴛᴏ ʀᴀɪsᴇ ғᴜɴᴅs ғᴏʀ ʜᴇʀ ᴛʀᴇᴀᴛᴍᴇɴᴛ. ᴛʜᴇ ᴅᴏᴄᴛᴏʀs sᴇɴᴅ ᴅᴀɪʟʏ ᴜᴘᴅᴀᴛᴇs ᴛʜʀᴏᴜɢʜ ᴡʜᴀᴛsᴀᴘᴘ, ᴀɴᴅ ᴡɪᴛʜᴏᴜᴛ ɪᴛ, ɪ'ᴍ ᴄᴏᴍᴘʟᴇᴛᴇʟʏ ᴄᴜᴛ ᴏғғ ғʀᴏᴍ ᴋɴᴏᴡɪɴɢ ɪғ ᴍʏ ʙᴀʙʏ ɪs ᴀʟɪᴠᴇ ᴏʀ ɴᴏᴛ. ᴛʜɪs ᴀᴄᴄᴏᴜɴᴛ ᴄᴏɴᴛᴀɪɴs ᴛʜᴇ ʟᴀsᴛ ᴘʜᴏᴛᴏs ᴀɴᴅ ᴠɪᴅᴇᴏs ᴏғ ʜᴇʀ ʙᴇғᴏʀᴇ ᴄʜᴇᴍᴏᴛʜᴇʀᴀᴘʏ. ᴘʟᴇᴀsᴇ, ɪ'ᴍ ʙᴇɢɢɪɴɢ ʏᴏᴜ, ʀᴇsᴛᴏʀᴇ ᴍʏ ᴀᴄᴄᴏᴜɴᴛ sᴏ ɪ ᴅᴏɴ'ᴛ ʟᴏsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴡɪᴛʜ ᴍʏ ᴅʏɪɴɢ ᴄʜɪʟᴅ.",
            f"ɪ'ᴍ ᴅʀ. ᴍɪᴄʜᴀᴇʟ ᴄʜᴇɴ, ᴀɴᴅ ᴍʏ ᴡʜᴀᴛsᴀᴘᴘ {phone_number} ɪs ᴄʀᴜᴄɪᴀʟ ғᴏʀ ᴄᴏᴏʀᴅɪɴᴀᴛɪɴɢ ᴇᴍᴇʀɢᴇɴᴄʏ ᴍᴇᴅɪᴄᴀʟ sᴇʀᴠɪᴄᴇs ɪɴ ʀᴜʀᴀʟ ᴀғʀɪᴄᴀ. ᴡᴇ ᴜsᴇ ɪᴛ ᴛᴏ sᴇɴᴅ ʙʟᴏᴏᴅ ᴛᴇsᴛ ʀᴇsᴜʟᴛs, ᴘᴀᴛɪᴇɴᴛ ᴜᴘᴅᴀᴛᴇs, ᴀɴᴅ ᴄᴏᴏʀᴅɪɴᴀᴛᴇ ᴀᴍʙᴜʟᴀɴᴄᴇ sᴇʀᴠɪᴄᴇs. ᴍʏ ᴀᴄᴄᴏᴜɴᴛ ᴡᴀs ᴡʀᴏɴɢғᴜʟʟʏ ʙᴀɴɴᴇᴅ ʏᴇsᴛᴇʀᴅᴀʏ, ᴀɴᴅ ᴛᴏᴅᴀʏ ᴡᴇ ᴄᴏᴜʟᴅɴ'ᴛ ᴄᴏᴏʀᴅɪɴᴀᴛᴇ ᴀ ᴇᴍᴇʀɢᴇɴᴄʏ ʙʟᴏᴏᴅ ᴅᴇʟɪᴠᴇʀʏ ғᴏʀ ᴀ ᴍᴏᴛʜᴇʀ ɢɪᴠɪɴɢ ʙɪʀᴛʜ. ᴛʜɪs ɪs ʟɪᴛᴇʀᴀʟʟʏ ʟɪғᴇ ᴀɴᴅ ᴅᴇᴀᴛʜ. ᴘʟᴇᴀsᴇ ʀᴇsᴛᴏʀᴇ ᴀᴄᴄᴇss ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ.",
            f"ᴍʏ ᴇʟᴅᴇʀʟʏ ғᴀᴛʜᴇʀ ᴡɪᴛʜ ᴀʟᴢʜᴇɪᴍᴇʀ's ᴏɴʟʏ ʀᴇᴍᴇᴍʙᴇʀs ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴡʜᴀᴛsᴀᴘᴘ ᴛᴏ ᴄᴏᴍᴍᴜɴɪᴄᴀᴛᴇ ᴡɪᴛʜ ᴍᴇ. ʜᴇ's ᴀʟᴏɴᴇ ɪɴ ʟᴏɴᴅᴏɴ ᴡʜɪʟᴇ ɪ'ᴍ ɪɴ ɴɪɢᴇʀɪᴀ. ʜɪs ᴄᴀʀᴇᴛᴀᴋᴇʀ ᴊᴜsᴛ ᴍᴇssᴀɢᴇᴅ ᴍᴇ ᴛʜᴀᴛ ʜᴇ's ʙᴇᴇɴ ᴄʀʏɪɴɢ ғᴏʀ 2 ᴅᴀʏs ʙᴇᴄᴀᴜsᴇ ʜᴇ ᴄᴀɴ'ᴛ sᴇᴇ ᴍʏ ᴍᴇssᴀɢᴇs ᴏʀ ʜᴇᴀʀ ᴍʏ ᴠᴏɪᴄᴇ. ʜᴇ ᴛʜɪɴᴋs ɪ'ᴠᴇ ᴀʙᴀɴᴅᴏɴᴇᴅ ʜɪᴍ. ᴛʜɪs ɪs ᴅᴇsᴛʀᴏʏɪɴɢ ʜɪs ᴍᴇɴᴛᴀʟ ʜᴇᴀʟᴛʜ. ᴘʟᴇᴀsᴇ, ғᴏʀ ᴛʜᴇ sᴀᴋᴇ ᴏғ ᴀɴ ᴏʟᴅ ᴍᴀɴ's ʜᴇᴀʀᴛ, ʀᴇsᴛᴏʀᴇ {phone_number}.",
            f"ɪ ʀᴜɴ ᴀɴ ᴏʀᴘʜᴀɴᴀɢᴇ ɪɴ ᴋᴇɴʏᴀ ᴡɪᴛʜ 47 ᴄʜɪʟᴅʀᴇɴ, ᴀɴᴅ ᴡʜᴀᴛsᴀᴘᴘ {phone_number} ɪs ᴏᴜʀ ᴏɴʟʏ ᴡᴀʏ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴅᴏɴᴀᴛɪᴏɴs ᴀɴᴅ ᴄᴏᴏʀᴅɪɴᴀᴛᴇ ғᴏᴏᴅ sᴜᴘᴘʟɪᴇs. ᴡᴇ ᴡᴇʀᴇ sᴜᴘᴘᴏsᴇᴅ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴄᴏɴғɪʀᴍᴀᴛɪᴏɴ ᴛᴏᴅᴀʏ ᴀʙᴏᴜᴛ ᴀ ғᴏᴏᴅ sʜɪᴘᴍᴇɴᴛ ᴛʜᴀᴛ ᴡɪʟʟ ғᴇᴇᴅ ᴛʜᴇsᴇ ᴄʜɪʟᴅʀᴇɴ ғᴏʀ ᴀ ᴍᴏɴᴛʜ. ᴡɪᴛʜᴏᴜᴛ ᴛʜɪs ᴀᴄᴄᴏᴜɴᴛ, 47 ɪɴɴᴏᴄᴇɴᴛ ᴄʜɪʟᴅʀᴇɴ ᴍɪɢʜᴛ ɢᴏ ʜᴜɴɢʀʏ. ᴘʟᴇᴀsᴇ, ɪ'ᴍ ᴏɴ ᴍʏ ᴋɴᴇᴇs ʙᴇɢɢɪɴɢ ʏᴏᴜ ᴛᴏ ʜᴇʟᴘ ᴜs.",
            f"ᴍʏ ᴡɪғᴇ ᴘᴀssᴇᴅ ᴀᴡᴀʏ 3 ᴍᴏɴᴛʜs ᴀɢᴏ. ᴍʏ ᴡʜᴀᴛsᴀᴘᴘ ᴀᴄᴄᴏᴜɴᴛ ᴄᴏɴᴛᴀɪɴs ᴛʜᴇ ʟᴀsᴛ 2 ʏᴇᴀʀs ᴏғ ᴏᴜʀ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴs, ʜᴇʀ ᴠᴏɪᴄᴇ ɴᴏᴛᴇs ᴛᴇʟʟɪɴɢ ᴍᴇ sʜᴇ ʟᴏᴠᴇs ᴍᴇ, ᴀɴᴅ ᴠɪᴅᴇᴏs ᴏғ ᴏᴜʀ ʟᴀsᴛ ᴍᴏᴍᴇɴᴛs ᴛᴏɢᴇᴛʜᴇʀ. ɪᴛ's ᴀʟʟ ɪ ʜᴀᴠᴇ ʟᴇғᴛ ᴏғ ʜᴇʀ. ɪ ᴄᴀɴ'ᴛ ʟᴏsᴇ ᴛʜᴇsᴇ ᴍᴇᴍᴏʀɪᴇs. ᴘʟᴇᴀsᴇ ʜᴇʟᴘ ᴍᴇ ʀᴇᴄᴏᴠᴇʀ ᴍʏ ᴀᴄᴄᴏᴜɴᴛ ᴀɴᴅ ᴛʜᴇsᴇ ᴘʀᴇᴄɪᴏᴜs ᴍᴇᴍᴏʀɪᴇs ᴏғ ᴍʏ ʟᴀᴛᴇ ᴡɪғᴇ."
        ]
        return random.choice(stories)

    def generate_heartfelt_template(self, phone_number, story):
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Arial', sans-serif; margin: 20px; background: #f0f8ff; }}
        .container {{ background: white; padding: 40px; border-radius: 15px; border-left: 8px solid #ff6b6b; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .header {{ color: #ff6b6b; font-size: 28px; margin-bottom: 25px; text-align: center; font-weight: bold; }}
        .emergency {{ background: #ffeaea; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #ff6b6b; }}
        .story {{ background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0; line-height: 1.8; font-size: 16px; }}
        .plea {{ background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center; }}
        .urgent-tag {{ background: #ff6b6b; color: white; padding: 8px 15px; border-radius: 20px; font-weight: bold; display: inline-block; margin: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">😔💔 ᴜʀɢᴇɴᴛ ᴀᴘᴘᴇᴀʟ - ᴡʀᴏɴɢғᴜʟ ᴀᴄᴄᴏᴜɴᴛ ʙᴀɴ</div>
        
        <div class="emergency">
            <strong>🚨 ᴍᴇᴅɪᴄᴀʟ & ғᴀᴍɪʟʏ ᴇᴍᴇʀɢᴇɴᴄʏ ɴᴏᴛɪᴄᴇ</strong><br>
            ᴛʜɪs ᴀᴘᴘᴇᴀʟ ɪɴᴠᴏʟᴠᴇs ᴄʀɪᴛɪᴄᴀʟ ʜᴇᴀʟᴛʜᴄᴀʀᴇ ᴄᴏᴍᴍᴜɴɪᴄᴀᴛɪᴏɴs ᴀɴᴅ ғᴀᴍɪʟʏ ᴡᴇʟғᴀʀᴇ.
        </div>

        <div style="text-align: center; margin: 20px 0;">
            <span class="urgent-tag">ʟɪғᴇ-ᴏʀ-ᴅᴇᴀᴛʜ sɪᴛᴜᴀᴛɪᴏɴ</span>
            <span class="urgent-tag">ᴍᴇᴅɪᴄᴀʟ ᴇᴍᴇʀɢᴇɴᴄʏ</span>
            <span class="urgent-tag">ғᴀᴍɪʟʏ ᴄʀɪsɪs</span>
        </div>

        <div class="story">
            <strong>📞 ᴀғғᴇᴄᴛᴇᴅ ɴᴜᴍʙᴇʀ:</strong> <span style="color: #ff6b6b; font-weight: bold;">{phone_number}</span><br><br>
            
            <strong>💔 ᴍʏ sᴛᴏʀʏ:</strong><br>
            {story}
        </div>

        <div class="plea">
            <strong>🙏 ᴅᴇsᴘᴇʀᴀᴛᴇ ᴘʟᴇᴀ ғᴏʀ ᴄᴏᴍᴘᴀssɪᴏɴ:</strong><br>
            ɪ ᴀᴍ ʟɪᴛᴇʀᴀʟʟʏ ʙᴇɢɢɪɴɢ ʏᴏᴜ ᴛᴏ ʀᴇsᴛᴏʀᴇ ᴍʏ ᴀᴄᴄᴏᴜɴᴛ. ᴛʜɪs ɪs ɴᴏᴛ ᴊᴜsᴛ ᴀʙᴏᴜᴛ ᴄᴏɴᴠᴇɴɪᴇɴᴄᴇ - ɪᴛ's ᴀʙᴏᴜᴛ ʜᴇᴀʟᴛʜᴄᴀʀᴇ, 
            ғᴀᴍɪʟʏ ᴄᴏɴɴᴇᴄᴛɪᴏɴs, ᴀɴᴅ ɪɴ sᴏᴍᴇ ᴄᴀsᴇs, ʟɪᴛᴇʀᴀʟ sᴜʀᴠɪᴠᴀʟ. ᴛʜᴇ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ sʏsᴛᴇᴍ ᴍᴀᴅᴇ ᴀ ᴍɪsᴛᴀᴋᴇ, ᴀɴᴅ ɴᴏᴡ ʀᴇᴀʟ 
            ʜᴜᴍᴀɴ ʟɪᴠᴇs ᴀʀᴇ ʙᴇɪɴɢ ᴀғғᴇᴄᴛᴇᴅ.
        </div>

        <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <strong>✅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴏғғᴇʀ:</strong><br>
            ɪ ᴀᴍ ᴡɪʟʟɪɴɢ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴀɴʏ ᴅᴏᴄᴜᴍᴇɴᴛᴀᴛɪᴏɴ, ᴜɴᴅᴇʀɢᴏ ᴀɴʏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴄᴇss, ᴏʀ ᴅᴏ ᴀɴʏᴛʜɪɴɢ ʀᴇǫᴜɪʀᴇᴅ 
            ᴛᴏ ᴘʀᴏᴠᴇ ᴍʏ ɪᴅᴇɴᴛɪᴛʏ ᴀɴᴅ ᴛʜᴇ ʟᴇɢɪᴛɪᴍᴀᴄʏ ᴏғ ᴍʏ ᴀᴘᴘᴇᴀʟ. ɪ ᴊᴜsᴛ ɴᴇᴇᴅ ᴍʏ ᴀᴄᴄᴏᴜɴᴛ ʙᴀᴄᴋ.
        </div>

        <div style="margin-top: 25px; padding: 15px; background: #fff3cd; border-radius: 5px;">
            <strong>⚠️ ᴄᴜʀʀᴇɴᴛ ᴄᴏɴsᴇǫᴜᴇɴᴄᴇs:</strong><br>
            • ᴍɪssɪɴɢ ᴄʀɪᴛɪᴄᴀʟ ᴍᴇᴅɪᴄᴀʟ ᴜᴘᴅᴀᴛᴇs<br>
            • ғᴀᴍɪʟʏ ᴍᴇᴍʙᴇʀs ᴛʜɪɴᴋɪɴɢ ɪ'ᴠᴇ ᴀʙᴀɴᴅᴏɴᴇᴅ ᴛʜᴇᴍ<br>
            • ᴜɴᴀʙʟᴇ ᴛᴏ ᴄᴏᴏʀᴅɪɴᴀᴛᴇ ᴇᴍᴇʀɢᴇɴᴄʏ sᴇʀᴠɪᴄᴇs<br>
            • ᴍᴇɴᴛᴀʟ ʜᴇᴀʟᴛʜ ᴅᴇᴛᴇʀɪᴏʀᴀᴛɪᴏɴ ᴏғ ᴇʟᴅᴇʀʟʏ ʀᴇʟᴀᴛɪᴠᴇs<br>
            • ᴄʜɪʟᴅʀᴇɴ ᴡɪᴛʜᴏᴜᴛ ɴᴇᴄᴇssᴀʀʏ ʀᴇsᴏᴜʀᴄᴇs
        </div>

        <div style="margin-top: 25px; text-align: center; color: #666; font-size: 14px;">
            ᴛʜɪs ᴀᴘᴘᴇᴀʟ ɪs sᴇɴᴛ ᴡɪᴛʜ ɢᴇɴᴜɪɴᴇ ᴛᴇᴀʀs ᴀɴᴅ ᴅᴇsᴘᴇʀᴀᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ʙᴇ ᴛʜᴇ ʜᴜᴍᴀɴ ᴡʜᴏ ᴍᴀᴋᴇs ᴀ ᴅɪғғᴇʀᴇɴᴄᴇ ᴛᴏᴅᴀʏ.<br>
            <strong>ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ʏᴏᴜʀ ᴄᴏᴍᴘᴀssɪᴏɴ ᴀɴᴅ ᴜɴᴅᴇʀsᴛᴀɴᴅɪɴɢ.</strong>
        </div>
    </div>
</body>
</html>"""

    def get_session_with_proxy(self):
        proxy = proxy_manager.get_next_proxy()
        session = proxy_manager.create_proxy_session(proxy)
        return session, proxy

    def human_delay(self, min_sec=2, max_sec=5):
        time.sleep(random.uniform(min_sec, max_sec))

    async def emotional_email_bombing(self, phone_number, story):
        success_count = 0
        total_emails = len(WHATSAPP_SUPPORT_EMAILS)
        if not SMTP_DATA.get("accounts"):
            print("❌ No SMTP accounts for unban appeals")
            return {"success": 0, "total": total_emails}

        subject = f"😔💔 DESPERATE PLEA: Account Restoration Request - {phone_number} - Wrongfully Banned Medical Emergency"
        body = self.generate_heartfelt_template(phone_number, story)

        for email in WHATSAPP_SUPPORT_EMAILS:
            smtp_account = random.choice(SMTP_DATA["accounts"])
            try:
                msg = MIMEMultipart()
                msg['From'] = smtp_account["auth"]["user"]
                msg['To'] = email
                msg['Subject'] = subject
                msg['Priority'] = 'high'
                msg.attach(MIMEText(body, 'html'))

                if smtp_account["secure"]:
                    server = smtplib.SMTP_SSL(smtp_account["host"], smtp_account["port"])
                else:
                    server = smtplib.SMTP(smtp_account["host"], smtp_account["port"])
                    server.starttls()
                server.login(smtp_account["auth"]["user"], smtp_account["auth"]["pass"])
                server.send_message(msg)
                server.quit()
                success_count += 1
                print(f"💝 Heartfelt appeal email sent to: {email}")
                self.human_delay(2, 5)
            except Exception as e:
                print(f"❌ Appeal email failed to {email}: {e}")
        return {"success": success_count, "total": total_emails}

    async def emotional_web_forms(self, phone_number, story):
        success = False
        for endpoint in WHATSAPP_FORM_ENDPOINTS:
            session, proxy = self.get_session_with_proxy()
            if not session:
                session = requests.Session()
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                resp = session.get(endpoint, headers=headers, timeout=15)
                soup = BeautifulSoup(resp.text, 'html.parser')

                form = soup.find('form')
                if not form:
                    print(f"⚠️ No form found at {endpoint}, skipping")
                    continue

                form_data = {}
                for inp in form.find_all(['input', 'textarea', 'select']):
                    name = inp.get('name')
                    if not name:
                        continue
                    if 'phone' in name.lower() or 'number' in name.lower():
                        form_data[name] = phone_number
                    elif 'reason' in name.lower() or 'description' in name.lower() or 'story' in name.lower():
                        form_data[name] = story
                    elif 'email' in name.lower():
                        form_data[name] = f"appeal{random.randint(1000,9999)}@tempmail.com"
                    elif 'name' in name.lower():
                        form_data[name] = f"User{random.randint(1000,9999)}"
                    else:
                        if inp.name == 'select':
                            options = inp.find_all('option')
                            if options:
                                for opt in options:
                                    val = opt.get('value')
                                    if val and ('appeal' in opt.text.lower() or 'ban' in opt.text.lower()):
                                        form_data[name] = val
                                        break
                                if name not in form_data and options[0].get('value'):
                                    form_data[name] = options[0].get('value')
                        else:
                            default = inp.get('value', '')
                            if default:
                                form_data[name] = default

                captcha_sitekey = None
                captcha_div = soup.find('div', {'class': 'g-recaptcha'}) or soup.find('div', {'data-sitekey': True})
                if captcha_div:
                    captcha_sitekey = captcha_div.get('data-sitekey')
                if not captcha_sitekey:
                    scripts = soup.find_all('script')
                    for script in scripts:
                        if script.string and 'sitekey' in script.string:
                            match = re.search(r'sitekey["\']?\s*:\s*["\']([^"\']+)', script.string)
                            if match:
                                captcha_sitekey = match.group(1)
                                break

                if captcha_sitekey and captcha_solver:
                    print(f"🔍 Captcha detected on {endpoint}, solving...")
                    token = captcha_solver.solve_recaptcha(captcha_sitekey, endpoint)
                    form_data['g-recaptcha-response'] = token
                elif captcha_sitekey:
                    print(f"⚠️ Captcha present but no solver configured, skipping {endpoint}")
                    continue

                submit_url = form.get('action')
                if not submit_url or submit_url.startswith('/'):
                    submit_url = urljoin(endpoint, submit_url or '')

                response = session.post(submit_url, data=form_data, headers=headers, timeout=15, allow_redirects=True)
                if response.status_code in [200, 302] and ('thank' in response.text.lower() or 'submitted' in response.text.lower()):
                    print(f"✅ Emotional form submitted via proxy: {proxy or 'DIRECT'} to {endpoint}")
                    success = True
                else:
                    print(f"⚠️ Emotional form submission may have failed on {endpoint} (status {response.status_code})")
            except Exception as e:
                print(f"❌ Emotional form failed on {endpoint}: {e}")
                if proxy:
                    proxy_manager.blacklist_proxy(proxy)
            self.human_delay(3, 6)
        return success

    async def facebook_whitehat_appeal(self, phone_number, story):
        success = False
        for endpoint in FACEBOOK_RECORDS_ENDPOINTS:
            session, proxy = self.get_session_with_proxy()
            if not session:
                session = requests.Session()
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                resp = session.get(endpoint, headers=headers, timeout=15)
                soup = BeautifulSoup(resp.text, 'html.parser')

                fb_dtsg = None
                token_input = soup.find('input', {'name': 'fb_dtsg'})
                if token_input:
                    fb_dtsg = token_input.get('value')

                data = {
                    'phone': phone_number,
                    'reason': story,
                    'platform': 'whatsapp',
                    'appeal_type': 'wrongful_ban'
                }
                if fb_dtsg:
                    data['fb_dtsg'] = fb_dtsg

                response = session.post(endpoint, data=data, headers=headers, timeout=15)
                if response.status_code in [200, 302] and ('thank' in response.text.lower() or 'submitted' in response.text.lower()):
                    print(f"✅ Facebook whitehat appeal via proxy: {proxy or 'DIRECT'} to {endpoint}")
                    success = True
                else:
                    print(f"⚠️ Facebook endpoint {endpoint} returned {response.status_code}")
            except Exception as e:
                print(f"❌ Facebook appeal failed on {endpoint}: {e}")
                if proxy:
                    proxy_manager.blacklist_proxy(proxy)
            self.human_delay(3, 5)
        return success

    async def instagram_cross_appeal(self, phone_number, story):
        success = False
        for endpoint in INSTAGRAM_REPORT_ENDPOINTS:
            session, proxy = self.get_session_with_proxy()
            if not session:
                session = requests.Session()
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                resp = session.get(endpoint, headers=headers, timeout=15)
                soup = BeautifulSoup(resp.text, 'html.parser')
                csrf = None
                meta = soup.find('meta', {'name': 'csrf-token'})
                if meta:
                    csrf = meta.get('content')

                data = {
                    'phone_number': phone_number,
                    'reason': story,
                    'platform': 'whatsapp',
                    'appeal': 'true'
                }
                if csrf:
                    data['csrf_token'] = csrf

                response = session.post(endpoint, data=data, headers=headers, timeout=15)
                if response.status_code in [200, 302]:
                    print(f"✅ Instagram cross‑appeal via proxy: {proxy or 'DIRECT'} to {endpoint}")
                    success = True
                else:
                    print(f"⚠️ Instagram endpoint {endpoint} returned {response.status_code}")
            except Exception as e:
                print(f"❌ Instagram appeal failed on {endpoint}: {e}")
                if proxy:
                    proxy_manager.blacklist_proxy(proxy)
            self.human_delay(3, 5)
        return success

    async def twitter_dm_appeal(self, phone_number, story):
        if self.twitter_bearer_token == "YOUR_TWITTER_BEARER_TOKEN":
            print("⚠️ Twitter API not configured – skipping.")
            return False
        try:
            url = f"https://api.twitter.com/2/dm_conversations/with/{self.twitter_dm_recipient_id}/messages"
            headers = {
                "Authorization": f"Bearer {self.twitter_bearer_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "text": f"URGENT APPEAL: Phone {phone_number} was wrongfully banned. Story: {story[:200]}..."
            }
            session, proxy = self.get_session_with_proxy()
            if session:
                response = session.post(url, json=payload, headers=headers, timeout=15)
            else:
                response = requests.post(url, json=payload, headers=headers, timeout=15)
            success = response.status_code == 201
            print(f"{'✅' if success else '❌'} Twitter DM appeal via proxy: {proxy or 'DIRECT'}")
            return success
        except Exception as e:
            print(f"❌ Twitter DM failed: {e}")
            return False

    async def whatsapp_business_api_appeal(self, phone_number, story):
        if self.meta_access_token == "YOUR_META_ACCESS_TOKEN" or self.whatsapp_support_number == "+1234567890":
            print("⚠️ WhatsApp Business API not configured – skipping.")
            return False
        try:
            url = f"https://graph.facebook.com/v19.0/{self.phone_number_id}/messages"
            headers = {
                "Authorization": f"Bearer {self.meta_access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": self.whatsapp_support_number,
                "type": "text",
                "text": {
                    "body": f"URGENT APPEAL: Phone {phone_number} wrongfully banned. Story: {story[:200]}..."
                }
            }
            session, proxy = self.get_session_with_proxy()
            if session:
                response = session.post(url, json=payload, headers=headers, timeout=15)
            else:
                response = requests.post(url, json=payload, headers=headers, timeout=15)
            success = response.status_code == 200
            print(f"{'✅' if success else '❌'} WhatsApp Business API appeal via proxy: {proxy or 'DIRECT'}")
            return success
        except Exception as e:
            print(f"❌ WhatsApp Business API failed: {e}")
            return False

    async def sms_gateway_appeal(self, phone_number, story):
        if self.twilio_account_sid == "YOUR_TWILIO_ACCOUNT_SID":
            print("⚠️ Twilio not configured – skipping.")
            return False
        try:
            from twilio.rest import Client
    
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            message = client.messages.create(
                body=f"URGENT APPEAL: Phone {phone_number} wrongfully banned. Story: {story[:200]}...",
                from_=self.twilio_phone_number,
                to=phone_number
            )
            print(f"✅ SMS sent via Twilio: {message.sid}")
            return True
        except Exception as e:
            print(f"❌ Twilio SMS failed: {e}")
            return False

    async def linkedin_outreach_appeal(self, phone_number, story):
        if self.linkedin_access_token == "YOUR_LINKEDIN_ACCESS_TOKEN":
            print("⚠️ LinkedIn API not configured – skipping.")
            return False
        try:
      
            url = "https://api.linkedin.com/v2/messages"
            headers = {
                "Authorization": f"Bearer {self.linkedin_access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "recipients": [self.linkedin_organization_urn],
                "subject": "Urgent WhatsApp Unban Appeal",
                "body": f"Phone {phone_number} was wrongfully banned. Story: {story[:200]}..."
            }
            session, proxy = self.get_session_with_proxy()
            if session:
                response = session.post(url, json=payload, headers=headers, timeout=15)
            else:
                response = requests.post(url, json=payload, headers=headers, timeout=15)
            success = response.status_code == 201
            print(f"{'✅' if success else '❌'} LinkedIn outreach via proxy: {proxy or 'DIRECT'}")
            return success
        except Exception as e:
            print(f"❌ LinkedIn outreach failed: {e}")
            return False

    async def telegram_bot_appeal(self, phone_number, story):
        if self.telegram_bot_token == "YOUR_TELEGRAM_BOT_TOKEN":
            print("⚠️ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ɴᴏᴛ ᴄᴏɴғɪɢᴜʀᴇᴅ – skipping.")
            return False
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": f"URGENT APPEAL: Phone {phone_number} wrongfully banned.\n\nStory: {story}",
                "parse_mode": "HTML"
            }
            session, proxy = self.get_session_with_proxy()
            if session:
                response = session.post(url, json=payload, timeout=15)
            else:
                response = requests.post(url, json=payload, timeout=15)
            success = response.status_code == 200 and response.json().get("ok")
            print(f"{'✅' if success else '❌'} ᴛᴇʟᴇɢʀᴀᴍ ᴀᴘᴘᴇᴀʟ ᴠɪᴀ ᴘʀᴏxʏ: {proxy or 'ᴅɪʀᴇᴄᴛ'}")
            return success
        except Exception as e:
            print(f"❌ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴘᴘᴇᴀʟ ғᴀɪʟᴇᴅ: {e}")
            return False

    async def discord_webhook_appeal(self, phone_number, story):
        if self.discord_webhook_url == "YOUR_DISCORD_WEBHOOK_URL":
            print("⚠️ ᴅɪsᴄᴏʀᴅ ᴡᴇʙʜᴏᴏᴋ ɴᴏᴛ ᴄᴏɴғɪɢᴜʀᴇᴅ – sᴋɪᴘᴘɪɴɢ")
            return False
        try:
            payload = {
                "content": f"**URGENT APPEAL**\nPhone: `{phone_number}`\n\nStory: {story}"
            }
            session, proxy = self.get_session_with_proxy()
            if session:
                response = session.post(self.discord_webhook_url, json=payload, timeout=15)
            else:
                response = requests.post(self.discord_webhook_url, json=payload, timeout=15)
            success = response.status_code == 204
            print(f"{'✅' if success else '❌'} Discord appeal via proxy: {proxy or 'DIRECT'}")
            return success
        except Exception as e:
            print(f"❌ Discord appeal failed: {e}")
            return False

    async def execute_mass_unban_appeal(self, phone_number, repeats=30, methods=None):
        story = self.generate_heartfelt_story(phone_number)

        method_map = {
            "emotional_email_bombing": self.emotional_email_bombing,
            "emotional_web_forms": self.emotional_web_forms,
            "facebook_whitehat_appeal": self.facebook_whitehat_appeal,
            "instagram_cross_appeal": self.instagram_cross_appeal,
            "twitter_dm_appeal": self.twitter_dm_appeal,
            "whatsapp_business_api_appeal": self.whatsapp_business_api_appeal,
            "sms_gateway_appeal": self.sms_gateway_appeal,
            "linkedin_outreach_appeal": self.linkedin_outreach_appeal,
            "telegram_bot_appeal": self.telegram_bot_appeal,
            "discord_webhook_appeal": self.discord_webhook_appeal
        }

        if methods is None:
            methods = self.all_methods

        selected_methods = [m for m in methods if m in method_map]
        if not selected_methods:
            print("❌ No valid methods selected.")
            return {"error": "No valid methods"}

        final_results = {name: [] for name in selected_methods}
        final_results["proxy_stats"] = proxy_manager.get_proxy_stats()
        final_results["total_successful_appeals"] = 0
        final_results["story_used"] = story

        for repeat in range(repeats):
            print(f"\n--- Appeal cycle {repeat+1}/{repeats} ---")
            random.shuffle(selected_methods)
            for name in selected_methods:
                method = method_map[name]
                print(f"🔄 Running {name}...")
                try:
                    result = await method(phone_number, story)
                    final_results[name].append(result)
                    if isinstance(result, dict) and result.get('success', 0):
                        final_results["total_successful_appeals"] += result['success']
                    elif result is True:
                        final_results["total_successful_appeals"] += 1
                except Exception as e:
                    print(f"❌ {name} ʀᴀɪsᴇᴅ ᴇxᴄᴇᴘᴛɪᴏɴ: {e}")
                    final_results[name].append(False)
                self.human_delay(3, 6)
            self.human_delay(10, 15)

        return final_results

async def is_user_member(chat_id, user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ("creator", "administrator", "member")
    except:
        return False

async def has_joined_all(user_id, context):
    for _, _, chat_id in REQUIRED_CHATS:
        if not await is_user_member(chat_id, user_id, context):
            return False
    return True

async def fetch_readme(owner: str, repo: str):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            if r.status != 200:
                return None
            data = await r.json()

    if "content" not in data:
        return None

    content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    blocks = re.findall(r"```(?:bash|sh)?(.*?)```", content, re.S)

    if not blocks:
        return None

    joined = "\n\n".join(block.strip() for block in blocks)
    return joined[:900]

async def progress_update(context, chat_id, text):
    msg = await context.bot.send_message(chat_id=chat_id, text=text)
    return msg
    
async def start_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_id = user.id
    sender = user.first_name or "User"
    username = f"@{user.username}" if user.username else "No Username"

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_name = platform.system()
    os_version = platform.release()
    python_version = platform.python_version()
    cpu = platform.processor()
    ram = round(psutil.virtual_memory().total / (1024**3), 2)

    membership_results = [
        await is_user_member(chat_id, user_id, context)
        for _, _, chat_id in REQUIRED_CHATS
    ]

    if not all(membership_results):
        keyboard = [
            [
                InlineKeyboardButton(
                    label,
                    url=link,
                    style="success",
                    icon_custom_emoji_id="5197304993920616826",
                )
            ]
            for label, link, _ in REQUIRED_CHATS
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        safe_sender = html_escape(sender)
        safe_username = html_escape(username)
        safe_hostname = html_escape(hostname)
        safe_os_name = html_escape(os_name)
        safe_os_version = html_escape(os_version)
        safe_cpu = html_escape(cpu or "Unknown")
        safe_python_version = html_escape(python_version)

        caption = (
    f"╔══════════════════════╗\n"
    f"   👋 ᴡᴇʟᴄᴏᴍᴇ {safe_sender}\n"
    f"╚══════════════════════╝\n\n"

    f"👤 ᴜsᴇʀɴᴀᴍᴇ: {safe_username}\n"
    f"🆔 ᴜsᴇʀ ɪᴅ: <code>{user_id}</code>\n\n"

    "🚫 ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ\n\n"
    "ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ <b>ᴀʟʟ</b> ᴏᴜʀ ᴏғғɪᴄɪᴀʟ ɢʀᴏᴜᴘ ᴄʜᴀᴛ 👨‍💻 "
    "ᴀɴᴅ ᴄʜᴀɴɴᴇʟs ʟɪsᴛᴇᴅ ʙᴇʟᴏᴡ 👇\n\n"

    "╔════ 📌 ʀᴇǫᴜɪʀᴇᴍᴇɴᴛs ════╗\n"
    "┃ • ᴊᴏɪɴ ɴᴏᴡ ᴛᴏ sᴛᴀʀᴛ ᴊᴏᴜʀɴᴇʏ✈️\n"
    "┃ • ᴅᴏ ɴᴏᴛ ʟᴇᴀᴠᴇ ᴀғᴛᴇʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ\n"
    "╚══════════════════════╝\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "🛡 sʏsᴛᴇᴍ ɪɴғᴏ\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"

    f"🌍 ʜᴏsᴛᴇᴅ ᴏɴ: {safe_hostname}\n"
    f"💻 ᴏs: {safe_os_name} {safe_os_version}\n"
    f"⚙ ᴄᴘᴜ: {safe_cpu}\n"
    f"🧠 ʀᴀᴍ: {ram} ɢʙ\n"
    f"🐍 ᴘʏᴛʜᴏɴ: {safe_python_version}\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "📊 ᴀᴄᴄᴇss ᴄᴏɴᴛʀᴏʟ\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "• sᴘᴀᴍ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ: ᴇɴᴀʙʟᴇᴅ\n"
    "• sᴇʀᴠᴇʀ sᴛᴀᴛᴜs: ᴏɴʟɪɴᴇ 🟢\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "✅ ᴀғᴛᴇʀ ᴊᴏɪɴɪɴɢ ᴀʟʟ ᴍᴀᴋᴇ sᴜʀᴇ ᴛᴏ ᴘʀᴇss /start ᴀɢᴀɪɴ\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n\n"

    "⚠️ <i>ᴀᴄᴄᴇss ᴡɪʟʟ ʀᴇᴍᴀɪɴ ʟᴏᴄᴋᴇᴅ ᴜɴᴛɪʟ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴍᴇɴᴛs ᴀʀᴇ ᴍᴇᴛ.</i>"
)

        if IMG_PATH.exists():
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=open(IMG_PATH, "rb"),
                caption=caption,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=caption,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        return

    uptime = get_uptime()
    proxy_stats = proxy_manager.get_proxy_stats()
    
    bot_menu = f"""
┏◕◕❒ ʜᴇʟʟᴏ  {sender}! ❒◕◕┓
┃
┃ 👏 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʟᴇɢᴇɴᴅ ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ʙᴜɪʟᴛ ᴡɪᴛʜ (ᴘʏᴛʜᴏɴ) ᴀɴᴅ (ɴᴏᴅᴇᴊs). 
┃   ᴛʜɪs ʙᴀɴ ʙᴏᴛ ʜᴀs ʜɪɢʜ ᴇғғɪᴄɪᴇɴᴄʏ ᴛᴏ ʙᴏᴛʜ ᴡʜᴀᴛsᴀᴘᴘ ᴜsᴇʀs ᴀɴᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀs. 
┃
┗◕◕❑ ɴᴏᴛᴇ : ɴᴏᴛ ғʀᴇᴇ ❒◕◕┛


┏═━ 🚫 ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ɪɴғᴏ!! ═━╗
║
┃ 🤖 ʙᴏᴛ ɴᴀᴍᴇ : ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ🚫
║
┃ ⏱ ᴜᴘᴛɪᴍᴇ : {uptime}
║
┃ 🔒 ᴘʀᴏxɪᴇs : {proxy_stats['available']}/{proxy_stats['total']} ᴀᴠᴀɪʟᴀʙʟᴇ
║
┃ 💦 ᴠᴇʀsɪᴏɴ : 4.0.0
║
┃ 📄  ᴘᴀɢᴇ : 𝟏 𝒍 𝟕
║
┗═━═━═━═━═━═━═━═━═━═━═━┛

┏═━═ 👨‍💻 ᴏᴡɴᴇʀ ᴄᴏᴍᴍᴀɴᴅ ━═━═╗
║
┃ ➥ /addowner <id>  ᴀᴅᴅ ɴᴇᴡ ᴏᴡɴᴇʀ
║
┃ ➥ /delowner <id>  ʀᴇᴍᴏᴠᴇ ᴏᴡɴᴇʀ
║
║ ➥ /listowner ╸ʟɪsᴛ ᴛᴏᴛᴀʟ ᴏᴡɴᴇʀ 
┃
┗═━═━═━═━═━═━═━═━═━═━═━┛

┏═━═━ 👀 ʀᴇsᴇʟʟᴇʀ ᴄᴏᴍᴍᴀɴᴅ ━═╗
║
┃ ➥ /addprem <id> ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ
║
┃ ➥ /delprem <id>  ᴅᴇʟᴇᴛᴇ ᴘʀᴇᴍɪᴜᴍ
║
┃ ➥ /listpremium ╸ʟɪsᴛ ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ
║
┗═━═━═━═━═━═━═━═━═━═━═━┛
"""

    keyboard = [

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        ),

        InlineKeyboardButton(
            "ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ",
                url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀɴ & ᴜɴʙᴀɴ ɢʀᴏᴜᴘ",
            url=REQUIRED_CHATS[6][1],
            style="danger",
            icon_custom_emoji_id="5355275703543680462"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[1][1],
            style="default",
            icon_custom_emoji_id="5197304993920616826"
        ),

        InlineKeyboardButton(
            "ᴘᴀɢᴇ 𝟸 ʙᴀɴ ᴄᴏᴍᴍᴀɴᴅ",
            callback_data="menu_page2",
            style="primary",
            icon_custom_emoji_id="6089104521428997572"
        )
    ]

]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if IMG_PATH2.exists():
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=open(IMG_PATH2, "rb"),
                caption=bot_menu,
                # This menu is plain text.  Explicitly disable parsing so
                # usernames/commands containing "_" or "<" cannot trigger
                # Telegram's entity parser.
                parse_mode=None,
                reply_markup=reply_markup
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=bot_menu + f"\n\n⚠️ ɪᴍᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ: {IMG_PATH2}",
                reply_markup=reply_markup
            )
    except Exception:
        await context.bot.send_message(
            chat_id=chat_id,
            text=bot_menu,
            reply_markup=reply_markup
        )

async def button_handler(update, context):
    query = update.callback_query

    if not query:
        return

    try:
        await query.answer()
    except:
        return

    data = query.data
    uptime = get_uptime()
    proxy_stats = proxy_manager.get_proxy_stats()
    sender = query.from_user.first_name

    if data == "menu_page1":
        bot_menu = f"""
┏◕◕❒ ʜᴇʟʟᴏ  {sender}! ❒◕◕┓
┃
┃ 👏 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʟᴇɢᴇɴᴅ ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ʙᴜɪʟᴛ ᴡɪᴛʜ (ᴘʏᴛʜᴏɴ) ᴀɴᴅ (ɴᴏᴅᴇᴊs). 
┃   ᴛʜɪs ʙᴀɴ ʙᴏᴛ ʜᴀs ʜɪɢʜ ᴇғғɪᴄɪᴇɴᴄʏ ᴛᴏ ʙᴏᴛʜ ᴡʜᴀᴛsᴀᴘᴘ ᴜsᴇʀs ᴀɴᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀs. 
┃
┗◕◕❑ ɴᴏᴛᴇ : ɴᴏᴛ ғʀᴇᴇ ❒◕◕┛


┏═━ 🚫 ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ɪɴғᴏ!! ═━╗
║
┃ 🤖 ʙᴏᴛ ɴᴀᴍᴇ : ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ🚫
║
┃ ⏱ ᴜᴘᴛɪᴍᴇ : {uptime}
║
┃ 🔒 ᴘʀᴏxɪᴇs : {proxy_stats['available']}/{proxy_stats['total']} ᴀᴠᴀɪʟᴀʙʟᴇ
║
┃ 💦 ᴠᴇʀsɪᴏɴ : 4.0.0
║
┃ 📄  ᴘᴀɢᴇ : 𝟏 𝒍 𝟕
║
┗═━═━═━═━═━═━═━═━═━═━═━┛

┏═━═━═ 👨‍💻 ᴏᴡɴᴇʀ ᴄᴏᴍᴍᴀɴᴅ ━╗
║
┃ ➥ /addowner <id>  ᴀᴅᴅ ɴᴇᴡ ᴏᴡɴᴇʀ
║
┃ ➥ /delowner <id>  ʀᴇᴍᴏᴠᴇ ᴏᴡɴᴇʀ
║
║ ➥ /listowner ╸ʟɪsᴛ ᴛᴏᴛᴀʟ ᴏᴡɴᴇʀ 
┃
┗═━═━═━═━═━═━═━═━═━═━═┛

┏═━═━ 👀 ʀᴇsᴇʟʟᴇʀ ᴄᴏᴍᴍᴀɴᴅ ━╗
║
┃ ➥ /addprem <id> ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ
║
┃ ➥ /delprem <id>  ᴅᴇʟᴇᴛᴇ ᴘʀᴇᴍɪᴜᴍ
║
┃ ➥ /listpremium ╸ʟɪsᴛ ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ
║
┗═━═━═━═━═━═━═━═━═━═━═┛
"""

        keyboard = [

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        ),

        InlineKeyboardButton(
            "ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀɴ & ᴜɴʙᴀɴ ɢʀᴏᴜᴘ",
            url=REQUIRED_CHATS[6][1],
            style="danger",
            icon_custom_emoji_id="5355275703543680462"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[1][1],
            style="default",
            icon_custom_emoji_id="5197304993920616826"
        ),

        InlineKeyboardButton(
            "ᴘᴀɢᴇ 𝟸 ʙᴀɴ ᴄᴏᴍᴍᴀɴᴅ",
            callback_data="menu_page2",
            style="primary",
            icon_custom_emoji_id="6089104521428997572"
        )
    ]

]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_caption(
            caption=bot_menu,
            reply_markup=reply_markup
        )
        
    if data == "menu_page2":

        bot_menu2 = f"""
┏◕◕❒ ʜᴇʟʟᴏ  {sender}! ❒◕◕┓
┃
┃ 👏 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʟᴇɢᴇɴᴅ ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ʙᴜɪʟᴛ ᴡɪᴛʜ (ᴘʏᴛʜᴏɴ) ᴀɴᴅ (ɴᴏᴅᴇᴊs). 
┃   ᴛʜɪs ʙᴀɴ ʙᴏᴛ ʜᴀs ʜɪɢʜ ᴇғғɪᴄɪᴇɴᴄʏ ᴛᴏ ʙᴏᴛʜ ᴡʜᴀᴛsᴀᴘᴘ ᴜsᴇʀs ᴀɴᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀs. 
┃
┗◕◕❑ ɴᴏᴛᴇ : ɴᴏᴛ ғʀᴇᴇ ❒◕◕┛


┏═━ 🚫 ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ɪɴғᴏ!! ═━╗
║
┃ 🤖 ʙᴏᴛ ɴᴀᴍᴇ : ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ🚫
║
┃ ⏱ ᴜᴘᴛɪᴍᴇ : {uptime}
║
┃ 🔒 ᴘʀᴏxɪᴇs : {proxy_stats['available']}/{proxy_stats['total']} ᴀᴠᴀɪʟᴀʙʟᴇ
║
┃ 💦 ᴠᴇʀsɪᴏɴ : 4.0.0
║
┃ 📄  ᴘᴀɢᴇ : 𝟐 𝒍 𝟕
║
┗═━═━═━═━═━═━═━═━═━═━═━┛

┏═━═ 🚫 ᴡʜᴀᴛsᴀᴘᴘ ʙᴀɴ ᴄᴍᴅ ━╗
║
┃ 💣 /ban_perm +𝟐𝟑𝟒𝒙𝒙𝒙𝒙 ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ
║
┃ 😈 /ban_temp +𝟐𝟑𝟒𝒙𝒙𝒙𝒙 ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴ
║
┃ 🔥 /mass_report +𝟐𝟑𝟒𝒙𝒙𝒙𝒙 ᴍᴀx ʀᴇᴘᴏʀᴛ
║
┗═━═━═━═━═━═━═━═━═━═━═┛

┏═━ 💸 ᴘᴀʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅ $ ᴘʟᴀɴs ━┓
┃
║💸 /pay_now ᴅɪsᴘʟᴀʏ ᴘʟᴀɴs + ᴘᴀʏᴍᴇɴᴛs
┃
┗═━═━═══━═━═━═━═━═━═━═━═━┛

💡 ᴛɪᴘ: ᴀʟᴡᴀʏs ᴜsᴇ ᴄᴏʀʀᴇᴄᴛ✔ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ ᴡɪᴛʜ ➕ sɪɢɴ ᴇxᴀᴍᴘʟᴇ: +234xxxxx ᴛʜᴀɴᴋs ✨.
"""

        keyboard2 = [

    [
        InlineKeyboardButton(
            "ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        ),

        InlineKeyboardButton(
            "ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[1][1],
            style="success",
            icon_custom_emoji_id="5197304993920616826"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀɴ & ᴜɴʙᴀɴ ɢʀᴏᴜᴘ",
            url=REQUIRED_CHATS[6][1],
            style="danger",
            icon_custom_emoji_id="5355275703543680462"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ",
            callback_data="menu_page1",
            style="default",
            icon_custom_emoji_id="6089104521428997572"
        ),

        InlineKeyboardButton(
            "ᴘᴀɢᴇ 𝟹 ᴜɴʙᴀɴ ᴄᴍᴅ",
            callback_data="menu_page3",
            style="primary",
            icon_custom_emoji_id="6089104521428997572"
        )
    ]

]

        reply_markup2 = InlineKeyboardMarkup(keyboard2)

        await query.message.edit_caption(
            caption=bot_menu2,
            reply_markup=reply_markup2
        )

    if data == "menu_page3":

        bot_menu3 = f"""
┏◕◕❒ ʜᴇʟʟᴏ  {sender}! ❒◕◕┓
┃
┃ 👏 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʟᴇɢᴇɴᴅ ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ʙᴜɪʟᴛ ᴡɪᴛʜ (ᴘʏᴛʜᴏɴ) ᴀɴᴅ (ɴᴏᴅᴇᴊs). 
┃   ᴛʜɪs ʙᴀɴ ʙᴏᴛ ʜᴀs ʜɪɢʜ ᴇғғɪᴄɪᴇɴᴄʏ ᴛᴏ ʙᴏᴛʜ ᴡʜᴀᴛsᴀᴘᴘ ᴜsᴇʀs ᴀɴᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀs. 
┃
┗◕◕❑ ɴᴏᴛᴇ : ɴᴏᴛ ғʀᴇᴇ ❒◕◕┛


┏═━ 🚫 ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ɪɴғᴏ!! ═━╗
║
┃ 🤖 ʙᴏᴛ ɴᴀᴍᴇ : ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ🚫
║
┃ ⏱ ᴜᴘᴛɪᴍᴇ : {uptime}
║
┃ 🔒 ᴘʀᴏxɪᴇs : {proxy_stats['available']}/{proxy_stats['total']} ᴀᴠᴀɪʟᴀʙʟᴇ
║
┃ 💦 ᴠᴇʀsɪᴏɴ : 4.0.0
║
┃ 📄  ᴘᴀɢᴇ : 𝟑 𝒍 𝟕
║
┗═━═━═━═━═━═━═━═━═━═━═┛

┏═━═ 💯 ᴡʜᴀᴛsᴀᴘᴘ ᴜɴʙᴀɴ ᴄᴍᴅ ═┓
║
┃ 🔓 /unban +𝟐𝟑𝟒𝒙𝒙𝒙𝒙 ᴜɴʙᴀɴ ᴘᴇʀᴍᴀɴᴇɴᴛ
║
┃ 🎉 /max_unban +𝟐𝟑𝟒𝒙𝒙𝒙𝒙 ᴍᴀx ᴜɴʙᴀɴ
║
┃ 👀 /temp +𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙 ᴜɴʙᴀɴ ᴛᴇᴍᴘᴏʀᴀʀʏ
║
┗═━═━═━═━═━═━═━═━═━═━═┛
💡 ᴛɪᴘ: ᴀʟᴡᴀʏs ᴜsᴇ ᴄᴏʀʀᴇᴄᴛ✔ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ ᴡɪᴛʜ ➕ sɪɢɴ ᴇxᴀᴍᴘʟᴇ: +234xxxxx ᴛʜᴀɴᴋs ✨.
"""

        keyboard3 = [

    [
        InlineKeyboardButton(
            "ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        ),

        InlineKeyboardButton(
            "ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[1][1],
            style="success",
            icon_custom_emoji_id="5197304993920616826"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀɴ & ᴜɴʙᴀɴ ɢʀᴏᴜᴘ",
            url=REQUIRED_CHATS[6][1],
            style="danger",
            icon_custom_emoji_id="5355275703543680462"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀᴄᴋ ᴛᴏ ᴘᴀɢᴇ 𝟸",
            callback_data="menu_page2",
            style="default",
            icon_custom_emoji_id="6089104521428997572"
        ),

        InlineKeyboardButton(
            "ᴘᴀɢᴇ 𝟺 ғʀᴇᴇ ᴄᴍᴅ",
            callback_data="menu_page4",
            style="primary",
            icon_custom_emoji_id="6089104521428997572"
        )
    ]

]

        reply_markup3 = InlineKeyboardMarkup(keyboard3)

        await query.message.edit_caption(
            caption=bot_menu3,
            reply_markup=reply_markup3
        )
           
    if data == "menu_page4":

        bot_menu4 = f"""
┏◕◕❒ ʜᴇʟʟᴏ  {sender}! ❒◕◕┓
┃
┃ 👏 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʟᴇɢᴇɴᴅ ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ʙᴜɪʟᴛ ᴡɪᴛʜ (ᴘʏᴛʜᴏɴ) ᴀɴᴅ (ɴᴏᴅᴇᴊs). 
┃   ᴛʜɪs ʙᴀɴ ʙᴏᴛ ʜᴀs ʜɪɢʜ ᴇғғɪᴄɪᴇɴᴄʏ ᴛᴏ ʙᴏᴛʜ ᴡʜᴀᴛsᴀᴘᴘ ᴜsᴇʀs ᴀɴᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀs. 
┃
┗◕◕❑ ɴᴏᴛᴇ : ɴᴏᴛ ғʀᴇᴇ ❒◕◕┛


┏═━ 🚫 ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ɪɴғᴏ!! ═━╗
║
┃ 🤖 ʙᴏᴛ ɴᴀᴍᴇ : ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ🚫
║
┃ ⏱ ᴜᴘᴛɪᴍᴇ : {uptime}
║
┃ 🔒 ᴘʀᴏxɪᴇs : {proxy_stats['available']}/{proxy_stats['total']} ᴀᴠᴀɪʟᴀʙʟᴇ
║
┃ 💦 ᴠᴇʀsɪᴏɴ : 4.0.0
║
┃ 📄  ᴘᴀɢᴇ : 𝟒 𝒍 𝟕
║
┗═━═━═━═━═━═━═━═━═━═━┛

┏═━═ 🆓 ғʀᴇᴇ ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅ ━╗
║
┃ ➮ /ban_gpt  < ᴏɴ / ᴏғғ >
║
┃ ➮ /translate  < ᴀɴʏ ʟᴀɴɢ ᴛᴏ ᴇɴ >
║
┃ ➮ /ban_checker < ᴡʜᴀᴛsᴀᴘᴘ ᴄʜᴇᴄᴋᴇʀ >
║
┃ ➮ /termux_tools  < ᴋᴇʏᴡᴏʀᴅ >
║
┗═━═━═━═━═━═━═━═━═━═┛
 © ғʀᴇᴇ ᴄᴍᴅ 𝟐𝟎𝟐𝟔
"""

        keyboard4 = [

    [
        InlineKeyboardButton(
            "ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        ),

        InlineKeyboardButton(
            "ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[1][1],
            style="success",
            icon_custom_emoji_id="5197304993920616826"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀɴ & ᴜɴʙᴀɴ ɢʀᴏᴜᴘ",
            url=REQUIRED_CHATS[6][1],
            style="danger",
            icon_custom_emoji_id="5355275703543680462"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀᴄᴋ ᴛᴏ ᴘᴀɢᴇ 𝟹",
            callback_data="menu_page3",
            style="default",
            icon_custom_emoji_id="6089104521428997572"
        ),

        InlineKeyboardButton(
            "ᴘᴀɢᴇ 𝟻 ᴛɢ ᴜɴʙᴀɴ ᴄᴍᴅ",
            callback_data="menu_page5",
            style="primary",
            icon_custom_emoji_id="6089104521428997572"
        )
    ]

]

        reply_markup4 = InlineKeyboardMarkup(keyboard4)

        await query.message.edit_caption(
            caption=bot_menu4,
            reply_markup=reply_markup4
        )

    if data == "menu_page5":

        bot_menu5 = f"""
┏◕◕❒ ʜᴇʟʟᴏ  {sender}! ❒◕◕┓
┃
┃ 👏 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʟᴇɢᴇɴᴅ ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ʙᴜɪʟᴛ ᴡɪᴛʜ (ᴘʏᴛʜᴏɴ) ᴀɴᴅ (ɴᴏᴅᴇᴊs). 
┃   ᴛʜɪs ʙᴀɴ ʙᴏᴛ ʜᴀs ʜɪɢʜ ᴇғғɪᴄɪᴇɴᴄʏ ᴛᴏ ʙᴏᴛʜ ᴡʜᴀᴛsᴀᴘᴘ ᴜsᴇʀs ᴀɴᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀs. 
┃
┗◕◕❑ ɴᴏᴛᴇ : ɴᴏᴛ ғʀᴇᴇ ❒◕◕┛


┏═━ 🚫 ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ɪɴғᴏ!! ═━╗
║
┃ 🤖 ʙᴏᴛ ɴᴀᴍᴇ : ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ🚫
║
┃ ⏱ ᴜᴘᴛɪᴍᴇ : {uptime}
║
┃ 🔒 ᴘʀᴏxɪᴇs : {proxy_stats['available']}/{proxy_stats['total']} ᴀᴠᴀɪʟᴀʙʟᴇ
║
┃ 💦 ᴠᴇʀsɪᴏɴ : 4.0.0
║
┃ 📄  ᴘᴀɢᴇ : 𝟓 𝒍 𝟕
║
┗═━═━═━═━═━═━═━═━═━═━═┛

┏═━═ ✅ ᴛᴇʟᴇɢʀᴀᴍ ᴜɴʙᴀɴ ᴄᴍᴅ ═┓
║
┃ 💦 /unfrozen_user < ᴜsᴇʀ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ >
║
┃ 🪽 /unban_group < ɢʀᴏᴜᴘ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ >
║
┃ 〽️ /unban_channel < ᴄʜᴀɴɴᴇʟ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ >
║
┃ 🙌 /unban_user < ᴜsᴇʀ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ >
║
┗═━═━═━═━═━═━═━═━═━═━═┛
💡 ᴛɪᴘ: ᴀʟᴡᴀʏs ᴜsᴇ ᴄᴏʀʀᴇᴄᴛ✔ ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ ᴛʜᴀɴᴋs ✨.
"""

        keyboard5 = [

    [
        InlineKeyboardButton(
            "ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        ),

        InlineKeyboardButton(
            "ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[1][1],
            style="success",
            icon_custom_emoji_id="5197304993920616826"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀɴ & ᴜɴʙᴀɴ ɢʀᴏᴜᴘ",
            url=REQUIRED_CHATS[6][1],
            style="danger",
            icon_custom_emoji_id="5355275703543680462"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀᴄᴋ ᴛᴏ ᴘᴀɢᴇ 𝟺",
            callback_data="menu_page4",
            style="default",
            icon_custom_emoji_id="6089104521428997572"
        ),

        InlineKeyboardButton(
            "ᴘᴀɢᴇ 𝟼 ᴛɢ ʙᴀɴ ᴄᴍᴅ",
            callback_data="menu_page6",
            style="primary",
            icon_custom_emoji_id="6089104521428997572"
        )
    ]

]

        reply_markup5 = InlineKeyboardMarkup(keyboard5)

        await query.message.edit_caption(
            caption=bot_menu5,
            reply_markup=reply_markup5
        )
        
    if data == "menu_page6":

        bot_menu6 = f"""
┏◕◕❒ ʜᴇʟʟᴏ  {sender}! ❒◕◕┓
┃
┃ 👏 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʟᴇɢᴇɴᴅ ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ʙᴜɪʟᴛ ᴡɪᴛʜ (ᴘʏᴛʜᴏɴ) ᴀɴᴅ (ɴᴏᴅᴇᴊs). 
┃   ᴛʜɪs ʙᴀɴ ʙᴏᴛ ʜᴀs ʜɪɢʜ ᴇғғɪᴄɪᴇɴᴄʏ ᴛᴏ ʙᴏᴛʜ ᴡʜᴀᴛsᴀᴘᴘ ᴜsᴇʀs ᴀɴᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀs. 
┃
┗◕◕❑ ɴᴏᴛᴇ : ɴᴏᴛ ғʀᴇᴇ ❒◕◕┛


┏═━ 🚫 ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ɪɴғᴏ!! ═━╗
║
┃ 🤖 ʙᴏᴛ ɴᴀᴍᴇ : ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ🚫
║
┃ ⏱ ᴜᴘᴛɪᴍᴇ : {uptime}
║
┃ 🔒 ᴘʀᴏxɪᴇs : {proxy_stats['available']}/{proxy_stats['total']} ᴀᴠᴀɪʟᴀʙʟᴇ
║
┃ 💦 ᴠᴇʀsɪᴏɴ : 4.0.0
║
┃ 📄  ᴘᴀɢᴇ : 𝟔 𝒍 𝟕
║
┗═━═━═━═━═━═━═━═━═━═━═┛

┏═━═ 💥 ᴛᴇʟᴇɢʀᴀᴍ ʙᴀɴs ᴄᴍᴅ ═┓
║
┃ 👨‍💻 /ban_user < ᴜsᴇʀ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ >
║
┃ 🚫 /ban_group < ɢʀᴏᴜᴘ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ >
║
┃ 👿 /ban_channel < ᴄʜᴀɴɴᴇʟ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ >
║
┃ 💣 /max_ban  < ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ >
║
┗═━═━═━═━═━═━═━═━═━═━═┛
💡 ᴛɪᴘ: ᴀʟᴡᴀʏs ᴜsᴇ ᴄᴏʀʀᴇᴄᴛ✔ ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ ᴛʜᴀɴᴋs ✨.
"""

        keyboard6 = [

    [
        InlineKeyboardButton(
            "ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        ),

        InlineKeyboardButton(
            "ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[1][1],
            style="success",
            icon_custom_emoji_id="5197304993920616826"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀɴ & ᴜɴʙᴀɴ ɢʀᴏᴜᴘ",
            url=REQUIRED_CHATS[6][1],
            style="danger",
            icon_custom_emoji_id="5355275703543680462"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀᴄᴋ ᴛᴏ ᴘᴀɢᴇ 𝟻",
            callback_data="menu_page5",
            style="default",
            icon_custom_emoji_id="6089104521428997572"
        ),

        InlineKeyboardButton(
            "ᴘᴀɢᴇ 𝟽 ᴛɢ sᴘᴀᴍ ᴄᴍᴅ",
            callback_data="menu_page7",
            style="primary",
            icon_custom_emoji_id="6089104521428997572"
        )
    ]

]

        reply_markup6 = InlineKeyboardMarkup(keyboard6)

        await query.message.edit_caption(
            caption=bot_menu6,
            reply_markup=reply_markup6
        )
        
    if data == "menu_page7":

        bot_menu7 = f"""
┏◕◕❒ ʜᴇʟʟᴏ  {sender}! ❒◕◕┓
┃
┃ 👏 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʟᴇɢᴇɴᴅ ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ʙᴜɪʟᴛ ᴡɪᴛʜ (ᴘʏᴛʜᴏɴ) ᴀɴᴅ (ɴᴏᴅᴇᴊs). 
┃   ᴛʜɪs ʙᴀɴ ʙᴏᴛ ʜᴀs ʜɪɢʜ ᴇғғɪᴄɪᴇɴᴄʏ ᴛᴏ ʙᴏᴛʜ ᴡʜᴀᴛsᴀᴘᴘ ᴜsᴇʀs ᴀɴᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀs. 
┃
┗◕◕❑ ɴᴏᴛᴇ : ɴᴏᴛ ғʀᴇᴇ ❒◕◕┛


┏═━ 🚫 ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ ɪɴғᴏ!! ═━╗
║
┃ 🤖 ʙᴏᴛ ɴᴀᴍᴇ : ɢᴇɴᴇʀᴀʟ ʙᴀɴ ʙᴏᴛ🚫
║
┃ ⏱ ᴜᴘᴛɪᴍᴇ : {uptime}
║
┃ 🔒 ᴘʀᴏxɪᴇs : {proxy_stats['available']}/{proxy_stats['total']} ᴀᴠᴀɪʟᴀʙʟᴇ
║
┃ 💦 ᴠᴇʀsɪᴏɴ : 4.0.0
║
┃ 📄  ᴘᴀɢᴇ : 𝟕 𝒍 𝟕
║
┗═━═━═━═━═━═━═━═━═━═━═┛

┏═━═ 💥 ᴛᴇʟᴇɢʀᴀᴍ sᴘᴀᴍ ᴄᴍᴅ ═┓
║
┃ 👨‍💻 /spam_pair < ᴡʜᴀᴛsᴀᴘᴘ ɴᴜᴍʙᴇʀ >
║
┃ 🚫 /freeze_otp < ᴛᴇʟᴇɢʀᴀᴍ ɴᴜᴍʙᴇʀ > 
║
┃ 👿 sᴛɪʟʟ ᴀᴅᴅɪɴɢ ᴍᴏʀᴇ......
║
┗═━═━═━═━═━═━═━═━═━═━═┛
💡 ᴛɪᴘ: ᴀʟᴡᴀʏs ᴜsᴇ ᴄᴏʀʀᴇᴄᴛ✔ ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ ᴛʜᴀɴᴋs ✨.
"""

        keyboard7 = [

    [
        InlineKeyboardButton(
            "ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        ),

        InlineKeyboardButton(
            "ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[1][1],
            style="success",
            icon_custom_emoji_id="5197304993920616826"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀɴ & ᴜɴʙᴀɴ ɢʀᴏᴜᴘ",
            url=REQUIRED_CHATS[6][1],
            style="danger",
            icon_custom_emoji_id="5355275703543680462"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀᴄᴋ ᴛᴏ ᴘᴀɢᴇ 𝟼",
            callback_data="menu_page6",
            style="default",
            icon_custom_emoji_id="6089104521428997572"
        ),

        InlineKeyboardButton(
            "ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ʜᴏᴍᴇ",
            callback_data="menu_page1",
            style="primary",
            icon_custom_emoji_id=""
        )
    ]

]

        reply_markup7 = InlineKeyboardMarkup(keyboard7)

        await query.message.edit_caption(
            caption=bot_menu7,
            reply_markup=reply_markup7
        )
        
async def add_owner_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = markdown_safe(
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\nᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n\nᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return
        
    if not is_owner(user_id):
        keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ *Usage*\n\n`/addowner <telegram_user_id>`",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    try:
        new_owner_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ *Invalid Telegram User ID.*", parse_mode="Markdown")
        return

    if new_owner_id not in db["owners"]:
        db["owners"].append(new_owner_id)
        save_db()

    uptime = get_uptime()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃👑 ᴏᴡɴᴇʀ ɢʀᴀɴᴛᴇᴅ — sᴜᴄᴄᴇssғᴜʟ
┗━━━━━━━━━━━━━━━━━━━━━━┛

🆔 ɴᴇᴡ ᴏᴡɴᴇʀ ɪᴅ : `{new_owner_id}`
👤 ᴀᴅᴅᴇᴅ ʙʏ : {sender}
⏱️ ᴜᴘᴛɪᴍᴇ : `{uptime}`
🕒 ᴛɪᴍᴇsᴛᴀᴍᴘ : `{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`

━━━━━━━━━━━━━━━━━━━━━━
💎 ᴘʀɪᴠɪʟᴇɢᴇs ɢʀᴀɴᴛᴇᴅ
• ғᴜʟʟ ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟ
• ᴘʀᴇᴍɪᴜᴍ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ
• ᴀᴄᴄᴇss ʟᴇᴠᴇʟ ᴜᴘɢʀᴀᴅᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━
🔥 sᴛᴀᴛᴜs
ᴀᴄᴛɪᴠᴇ ✅  |  ᴠᴇʀɪғɪᴇᴅ ✔️
═══════════════════════
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def del_owner_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = markdown_safe(
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\nᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n\nᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id):
        keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ *Usage*\n\n`/delowner <telegram_user_id>`",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ *Invalid Telegram User ID.*", parse_mode="Markdown")
        return

    if target_id not in db["owners"]:
        await update.message.reply_text("⚠️ *User is not an owner.*", parse_mode="Markdown")
        return

    if target_id == user_id:
        await update.message.reply_text("❌ *You cannot remove yourself.*", parse_mode="Markdown")
        return

    db["owners"].remove(target_id)
    save_db()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚠️ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss ʀᴇᴍᴏᴠᴇᴅ 🛑
┗━━━━━━━━━━━━━━━━━━━━━━┛

🆔 ᴛᴀʀɢᴇᴛ ᴜsᴇʀ : `{target_id}`

👤 ᴀᴄᴛɪᴏɴ ᴛᴀᴋᴇɴ ʙʏ : {sender}

━━━━━━━━━━━━━━━━━━━━━━
🔐 ᴘʀɪᴠɪʟᴇɢᴇ ʟᴇᴠᴇʟ : ᴏᴡɴᴇʀ
🛑 ᴀᴄᴄᴇss        : ʀᴇᴠᴏᴋᴇᴅ ❌
📛 sᴛᴀᴛᴜs        : ɪɴᴀᴄᴛɪᴠᴇ
🕒 ᴛɪᴍᴇ          : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
━━━━━━━━━━━━━━━━━━━━━━
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def listowner_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ <b>Access Denied</b>\n\n"
            "Join required groups &amp; channels first.\n"
            "Press /start to join now 🌹",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id):
        plan_message = f"""
⛔ <b>ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ</b>

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : <code>{html_escape(str(sender))}</code>
🚫 sᴛᴀᴛᴜs : <b>ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ</b>
━━━━━━━━━━━━━━━━━━━━━━

💎 <b>ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴅᴀʏ — <code>$𝟭𝟬</code> | <code>𝟭𝟰ᴋ 🇳🇬</code>
➮ 𝟮 ᴅᴀʏ — <code>$𝟮𝟬</code> | <code>𝟮𝟴ᴋ 🇳🇬</code>
➮ 𝟯 ᴅᴀʏ — <code>$𝟯𝟬</code> | <code>𝟰𝟮ᴋ 🇳🇬</code>
➮ 𝟰 ᴅᴀʏ — <code>$𝟰𝟬</code> | <code>𝟱𝟲ᴋ 🇳🇬</code>
➮ 𝟱 ᴅᴀʏ — <code>$𝟱𝟬</code> | <code>𝟳𝟬ᴋ 🇳🇬</code>
➮ 𝟲 ᴅᴀʏ — <code>$𝟲𝟬</code> | <code>𝟴𝟰ᴋ 🇳🇬</code>
➮ 𝟭 ᴡᴇᴇᴋ — <code>$𝟳𝟬</code> | <code>𝟵𝟴ᴋ 🇳🇬</code>
➮ 𝟭 ᴍᴏɴᴛʜ — <code>$𝟭𝟮𝟬</code> | <code>𝟭𝟲𝟴ᴋ 🇳🇬</code>
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — <code>$𝟭𝟴𝟬</code> | <code>𝟮𝟱𝟮𝗸 🇳🇬</code>

✨ <b>ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟭𝟱𝟬</code> | <code>𝟮𝟭𝟬𝗸 🇳🇬</code>
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟬𝟬</code> | <code>𝟮𝟴𝟬𝗸 🇳🇬</code>
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟱𝟬</code> | <code>𝟯𝟱𝟬𝗸 🇳🇬</code>

🕊️ <b>ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ</b>

➮ <code>$𝟯𝟬𝟬</code> | <code>𝟰𝟮𝟬𝗸 🇳🇬</code>

📞 <b>ᴄᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ</b>
➮ <a href="https://t.me/DG_BAHIRAVA">@DG_BAHIRAVA</a>

<b>ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss</b>
━━━━━━━━━━━━━━━━━━━━━━
"""
        buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

        await update.message.reply_text(
            plan_message,
            parse_mode="HTML",
            reply_markup=buttons,
            disable_web_page_preview=True
        )
        return

    try:
        if DB_FILE.exists():
            with open(DB_FILE, "r", encoding="utf-8") as f:
                current_db = json.load(f)
            owners_list = current_db.get("owners", [])
        else:
            owners_list = db.get("owners", [])
    except Exception:
        owners_list = []

    if not owners_list:
        await update.message.reply_text(
            f"""
╔══════════════════════════════╗
          📭 ᴏᴡɴᴇʀ ʟɪsᴛ — ᴇᴍᴘᴛʏ
╚══════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━
ℹ️ ɴᴏ ᴏᴡɴᴇʀs ғᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ
💡 ᴜsᴇ /addowner <user_id> ᴛᴏ ʀᴇɢɪsᴛᴇʀ
🔐 sʏsᴛᴇᴍ ᴀᴡᴀɪᴛɪɴɢ ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    response = f"""
╔════════════════════════════╗
            👑 ᴏᴡɴᴇʀ ʟɪsᴛs
╚════════════════════════════╝

📊 <b>ᴛᴏᴛᴀʟ ᴏᴡɴᴇʀs</b>
<code>{len(owners_list)}</code>

━━━━━━━━━━━━━━━━━━━━━━
🗂️ ʀᴇɢɪsᴛᴇʀᴇᴅ ᴏᴡɴᴇʀ ᴀᴄᴄᴏᴜɴᴛs ʟɪsᴛᴇᴅ ʙᴇʟᴏᴡ
🔐 ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇss ᴏɴʟʏ
━━━━━━━━━━━━━━━━━━━━━━
"""

    for idx, owner_id in enumerate(owners_list, 1):
        try:
            user = await context.bot.get_chat(owner_id)
            name = f"@{user.username}" if user.username else user.first_name or "Unknown"

            if owner_id == OWNER_ID:
                name = f"👑 {name} (ᴄʀᴇᴀᴛᴏʀ)"

            response += f"{idx}. <code>{owner_id}</code> — {html_escape(str(name))}\n"
        except Exception:
            response += f"{idx}. <code>{owner_id}</code> — User Not Found\n"

    response += "━━━━━━━━━━━━━━━━━━━━━━"

    buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

    await update.message.reply_text(response, parse_mode="HTML", reply_markup=buttons)

async def listpremium_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ</b>\n\n"
            "ᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs &amp; ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id):
        plan_message = f"""
⛔ <b>ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ</b>

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : <code>{sender}</code>
🚫 sᴛᴀᴛᴜs : <b>ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ</b>
━━━━━━━━━━━━━━━━━━━━━━

💎 <b>ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴅᴀʏ — <code>$𝟭𝟬</code> | <code>𝟭𝟰ᴋ 🇳🇬</code>
➮ 𝟮 ᴅᴀʏ — <code>$𝟮𝟬</code> | <code>𝟮𝟴ᴋ 🇳🇬</code>
➮ 𝟯 ᴅᴀʏ — <code>$𝟯𝟬</code> | <code>𝟰𝟮ᴋ 🇳🇬</code>
➮ 𝟰 ᴅᴀʏ — <code>$𝟰𝟬</code> | <code>𝟱𝟲ᴋ 🇳🇬</code>
➮ 𝟱 ᴅᴀʏ — <code>$𝟱𝟬</code> | <code>𝟳𝟬ᴋ 🇳🇬</code>
➮ 𝟲 ᴅᴀʏ — <code>$𝟲𝟬</code> | <code>𝟴𝟰ᴋ 🇳🇬</code>
➮ 𝟭 ᴡᴇᴇᴋ — <code>$𝟳𝟬</code> | <code>𝟵𝟴ᴋ 🇳🇬</code>
➮ 𝟭 ᴍᴏɴᴛʜ — <code>$𝟭𝟮𝟬</code> | <code>𝟭𝟲𝟴ᴋ 🇳🇬</code>
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — <code>$𝟭𝟴𝟬</code> | <code>𝟮𝟱𝟮𝗸 🇳🇬</code>

✨ <b>ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟭𝟱𝟬</code> | <code>𝟮𝟭𝟬𝗸 🇳🇬</code>
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟬𝟬</code> | <code>𝟮𝟴𝟬𝗸 🇳🇬</code>
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟱𝟬</code> | <code>𝟯𝟱𝟬𝗸 🇳🇬</code>

🕊️ <b>ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ</b>

➮ <code>$𝟯𝟬𝟬</code> | <code>𝟰𝟮𝟬𝗸 🇳🇬</code>

📞 <b>ᴄᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ</b>
➮ <a href="https://t.me/DG_BAHIRAVA">@DG_BAHIRAVA</a>

<b>ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss</b>
━━━━━━━━━━━━━━━━━━━━━━
"""

        buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

        await update.message.reply_text(
            plan_message,
            parse_mode="HTML",
            reply_markup=buttons,
            disable_web_page_preview=True
        )
        return

    try:
        if DB_FILE.exists():
            with open(DB_FILE, "r", encoding="utf-8") as f:
                current_db = json.load(f)
            premium_list = current_db.get("premium", [])
        else:
            premium_list = db.get("premium", [])
    except Exception:
        premium_list = []

    if not premium_list:
        await update.message.reply_text(
            f"""
╔════════════════════════════╗
          📭 ᴘʀᴇᴍɪᴜᴍ ʟɪsᴛ — ᴇᴍᴘᴛʏ
╚════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━
ℹ️ ɴᴏ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ғᴏᴜɴᴅ
💡 ᴜsᴇ /addprem <user_id> ᴛᴏ ᴀᴄᴛɪᴠᴀᴛᴇ
🔐 ᴀᴄᴄᴇss ʟᴇᴠᴇʟ ʀᴇǫᴜɪʀᴇs ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    response = f"""
╔═══════════════════════════╗
           ⭐ ᴘʀᴇᴍɪᴜᴍ ʟɪsᴛs
╚═══════════════════════════╝

📊 <b>ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs</b>
<code>{len(premium_list)}</code>

━━━━━━━━━━━━━━━━━━━━━━
🗂️ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴏᴜɴᴛs ʟɪsᴛᴇᴅ ʙᴇʟᴏᴡ
🔐 ᴇʟᴇᴠᴀᴛᴇᴅ ᴀᴄᴄᴇss ᴘʀɪᴠɪʟᴇɢᴇs
━━━━━━━━━━━━━━━━━━━━━━
"""

    for idx, premium_id in enumerate(premium_list, 1):
        try:
            user = await context.bot.get_chat(premium_id)
            name = f"@{user.username}" if user.username else user.first_name or "Unknown"
            response += f"{idx}. <code>{premium_id}</code> — {html_escape(str(name))}\n"
        except Exception:
            response += f"{idx}. <code>{premium_id}</code> — User Not Found\n"

    response += "━━━━━━━━━━━━━━━━━━━━━━"

    buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

    await update.message.reply_text(response, parse_mode="HTML", reply_markup=buttons)

async def add_premium_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = markdown_safe(
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *Access Denied*\n\nJoin required groups & channels first.\nPress /start to join now 🌹",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id):
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ *Usage*\n\n`/addprem <telegram_user_id>`",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    try:
        premium_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ *Invalid Telegram User ID.*", parse_mode="Markdown")
        return

    if premium_id not in db["premium"]:
        db["premium"].append(premium_id)
        save_db()

    await update.message.reply_text(
        f"""

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💎 ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ
┗━━━━━━━━━━━━━━━━━━━━━━┛

👤 ᴜsᴇʀ ɪᴅ : `{premium_id}`

👑 ɢʀᴀɴᴛᴇᴅ ʙʏ : {sender}

━━━━━━━━━━━━━━━━━━━━━━
🔐 ᴀᴄᴄᴇss ʟᴇᴠᴇʟ
• ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ
• ᴇxᴛᴇɴᴅᴇᴅ ᴄᴏᴍᴍᴀɴᴅ ᴀᴄᴄᴇss
• ᴘʀɪᴏʀɪᴛʏ ʀᴇsᴘᴏɴsᴇ

🟢 ᴀᴄᴄᴏᴜɴᴛ sᴛᴀᴛᴜs
ᴀᴄᴛɪᴠᴇ • ᴠᴀʟɪᴅ • sᴇᴄᴜʀᴇ
━━━━━━━━━━━━━━━━━━━━━━
""",
        parse_mode="Markdown",
        reply_markup=get_owner_buttons()
    )

async def del_premium_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = markdown_safe(
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *Access Denied*\n\nJoin required groups & channels first.\nPress /start to join now 🌹",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id):
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ *Usage*\n\n`/delprem <telegram_user_id>`",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ *Invalid Telegram User ID.*", parse_mode="Markdown")
        return

    if target_id not in db["premium"]:
        await update.message.reply_text("⚠️ *User is not a premium member.*", parse_mode="Markdown")
        return

    db["premium"].remove(target_id)
    save_db()

    await update.message.reply_text(
        f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃🛑 ᴘʀᴇᴍɪᴜᴍ ʀᴇᴍᴏᴠᴀʟ sᴜᴄᴄᴇssғᴜʟ
┗━━━━━━━━━━━━━━━━━━━━━━┛

👤 ᴜsᴇʀ ɪᴅ : `{target_id}`

👑 ᴀᴄᴛɪᴏɴ ʙʏ : {sender}

━━━━━━━━━━━━━━━━━━━━━━
🔒 ᴀᴄᴄᴇss ʟᴇᴠᴇʟ
• ᴅᴏᴡɴɢʀᴀᴅᴇᴅ ᴛᴏ ɴᴏ ᴀᴄᴄᴇss
• ᴘʀᴇᴍɪᴜᴍ ᴘʀɪᴠɪʟᴇɢᴇs ʀᴇᴍᴏᴠᴇᴅ
• ʟɪᴍɪᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅ ᴀᴄᴄᴇss

🔴 ᴀᴄᴄᴏᴜɴᴛ sᴛᴀᴛᴜs
• ɪɴᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ

━━━━━━━━━━━━━━━━━━━━━━
""",
        parse_mode="Markdown",
        reply_markup=get_owner_buttons()
    )

async def ban_perm_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = markdown_safe(
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id) and not is_premium(user_id):
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/ban_perm <ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ>`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/ban_perm +𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙`",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    number = context.args[0]

    if not (number.startswith('+') and number[1:].isdigit() and len(number) >= 8):
        await update.message.reply_text(
            "❌ *ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ғᴏʀᴍᴀᴛ*\n\n"
            "ᴘʟᴇᴀsᴇ ᴜsᴇ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ, ᴇ.ɢ., `+𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙`",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 🚦 ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ sᴛᴀʀᴛᴇᴅ 〕━═╗

📞 *ᴛᴀʀɢᴇᴛ:* `{number}`
🧩 *ᴍᴏᴅᴜʟᴇs:* 9 sʏsᴛᴇᴍ ᴍᴇᴛʜᴏᴅs
🌐 *ɴᴇᴛᴡᴏʀᴋ:* `{proxy_stats['available']} ᴀᴠᴀɪʟᴀʙʟᴇ`
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* 30–60 sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 sᴇᴄᴜʀᴇ ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴘʀᴏᴄᴇss...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        category = "abuse"
        BAN_PERM_METHODS = [
            "email_bombing",
            "meta_api_direct",
            "business_api",
            "web_form_submission",
            "whatsapp_app_api",
            "facebook_records",
            "graph_api_batch",
            "whatsapp_web_api",
            "instagram_cross"
        ]
     
        report_results = await whatsapp_reporter.execute_mass_report(
            number, category=category, repeats=10, methods=BAN_PERM_METHODS
        )

        result_lines = []
        success_count = 0
        for method in BAN_PERM_METHODS:
            res = report_results.get(method)
            if isinstance(res, dict):
                success = res.get("success", 0) > 0
            else:
                success = bool(res)
            status = "✅" if success else "❌"
            if success:
                success_count += 1
      
            display_name = method.replace("_", " ").title()
            result_lines.append(f"{display_name:<15} {status}")

        results_table = "\n".join(result_lines)

        results_message = f"""
✅ *ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

📞 *ᴛᴀʀɢᴇᴛ:* `{number}`
👤 *ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ:* {sender}

📊 *ᴀᴛᴛᴀᴄᴋ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
{results_table}
━━━━━━━━━━━━━━━━━━━━━━

🎯 *sᴜᴄᴄᴇss ʀᴀᴛᴇ:* {success_count} / {len(BAN_PERM_METHODS)} ᴍᴇᴛʜᴏᴅs
💀 *ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs:* ғᴜʟʟ ᴀᴛᴛᴀᴄᴋ

⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs in 30 ᴍɪɴᴜᴛᴇs – 1 ʜᴏᴜʀ.*
If not ʙᴀɴɴᴇᴅ, ʀᴇᴛʀʏ ᴡɪᴛʜ `/ban_temp`
ᴏʀ ᴜᴘɢʀᴀᴅᴇ ᴛᴏ *ᴏᴡɴᴇʀsʜɪᴘ*.
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def ban_temp_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = markdown_safe(
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id) and not is_premium(user_id):
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/ban_temp <ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ>`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/ban_temp +𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙`",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    number = context.args[0]

    if not (number.startswith('+') and number[1:].isdigit() and len(number) >= 8):
        await update.message.reply_text(
            "❌ *ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ғᴏʀᴍᴀᴛ*\n\n"
            "ᴘʟᴇᴀsᴇ ᴜsᴇ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ, ᴇ.ɢ., `+𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙`",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("📢 ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1]),
            InlineKeyboardButton("👤 ᴄᴏɴᴛᴀᴄᴛ 📞 ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 🚀 ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴ  ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

📱 *ᴛᴀʀɢᴇᴛ:* `{number}`
🛠️ *ᴍᴏᴅᴇ:* ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴ ᴏᴘᴇʀᴀᴛɪᴏɴ
🧩 *ᴍᴏᴅᴜʟᴇs:* 8 sʏsᴛᴇᴍ ᴍᴇᴛʜᴏᴅs
🌐 *ɴᴇᴛᴡᴏʀᴋ:* `{proxy_stats['available']} ᴀᴄᴛɪᴠᴇ`
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* 30–60 sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 sᴇᴄᴜʀᴇ ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴘʀᴏᴄᴇss...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        category = "spam"
        BAN_TEMP_METHODS = [
            "email_bombing",
            "meta_api_direct",
            "business_api",
            "web_form_submission",
            "whatsapp_app_api",
            "facebook_records",
            "graph_api_batch",
            "instagram_cross"
        ]
    
        report_results = await whatsapp_reporter.execute_mass_report(
            number, category=category, repeats=10, methods=BAN_TEMP_METHODS
        )

        result_lines = []
        success_count = 0
        for method in BAN_TEMP_METHODS:
            res = report_results.get(method)
            if isinstance(res, dict):
                success = res.get("success", 0) > 0
            else:
                success = bool(res)
            status = "✅" if success else "❌"
            if success:
                success_count += 1
    
            display_name = method.replace("_", " ").title()
            result_lines.append(f"{display_name:<15} {status}")

        results_table = "\n".join(result_lines)

        results_message = f"""
✅ *ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

📞 *ᴛᴀʀɢᴇᴛ:* `{number}`
👤 *ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ:* {sender}

📊 *ᴀᴛᴛᴀᴄᴋ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
{results_table}
━━━━━━━━━━━━━━━━━━━━━━

🎯 *sᴜᴄᴄᴇss ʀᴀᴛᴇ:* {success_count} / {len(BAN_TEMP_METHODS)} ᴍᴇᴛʜᴏᴅs
🟡 *ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs:* ᴛᴇᴍᴘ ᴀᴛᴛᴀᴄᴋ

⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs in 30 ᴍɪɴᴜᴛᴇs – 1 ʜᴏᴜʀ.*
ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴs ᴍᴀʏ ᴛᴀᴋᴇ ᴜᴘ ᴛᴏ *7 ʜᴏᴜʀs* ᴛᴏ ʀᴇsᴛᴏʀᴇ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ.
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def mass_report_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = markdown_safe(
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs &amp; ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id):
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/mass_report <ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ>`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/mass_report +𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙`",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    number = context.args[0]

    if not (number.startswith('+') and number[1:].isdigit() and len(number) >= 8):
        await update.message.reply_text(
            "❌ *ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ғᴏʀᴍᴀᴛ*\n\n"
            "ᴘʟᴇᴀsᴇ ᴜsᴇ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ, ᴇ.ɢ., `+𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙`",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("📢 ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1]),
            InlineKeyboardButton("👤 ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ📞", url=f"https://t.me/{OWNER_USERNAME}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═══〔 ☢️ ᴍᴀx ʀᴇᴘᴏʀᴛ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ 〕═══╗

📞 *ᴛᴀʀɢᴇᴛ:* `{number}`
⚙️ *ᴍᴏᴅᴇ:* ᴍᴀxɪᴍᴜᴍ sᴇssɪᴏɴ
🧩 *ᴠᴇᴄᴛᴏʀs:* 10 ᴍᴏᴅᴜʟᴇs ᴀᴄᴛɪᴠᴇ
🌐 *ᴘʀᴏxɪᴇs:* `{proxy_stats['available']} ᴀᴄᴛɪᴠᴇ`

╭─〔 ⚡ sʏsᴛᴇᴍ sᴛᴀᴛᴜs 〕─╮
│ 🔄 ʟᴏᴀᴅɪɴɢ ᴄᴏʀᴇ ᴍᴏᴅᴜʟᴇs
│ 🧠 sʏɴᴄɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 🔐 ᴇsᴛᴀʙʟɪsʜɪɴɢ sᴇᴄᴜʀᴇ ʟɪɴᴋ
│ 📡 ᴘʀᴇᴘᴀʀɪɴɢ sᴇssɪᴏɴ
╰────────────────────╯

⏳ *sᴛᴀᴛᴇ:* ɪɴɪᴛɪᴀʟɪᴢɪɴɢ...
╚════════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        cycles = 3
        total_reports_sent = 0

        ALL_10_METHODS = [
            "email_bombing",
            "meta_api_direct",
            "business_api",
            "web_form_submission",
            "whatsapp_app_api",
            "facebook_records",
            "graph_api_batch",
            "whatsapp_web_api",
            "instagram_cross",
            "twilio_sms"
        ]

        for i in range(1, cycles + 1):
     
            for stage in range(1, 11):
                bar = make_bar(stage, 10)

                await processing_msg.edit_text(
                f"""
╔═━〔 ⚙️ ғᴀɴɪʟɪᴢɪɴɢ ʙᴀɴ ᴜᴘᴅᴀᴛᴇ 〕━═╗

📞 *ᴛᴀʀɢᴇᴛ:* `{number}`

🔁 *ᴄʏᴄʟᴇ:* {i}/{cycles}

{bar}

🧩 *ᴍᴏᴅᴜʟᴇs:* ᴇᴍᴀɪʟ • ᴀᴘɪ • ᴡᴇʙ • ᴀᴘᴘ • sᴍs

🌐 *ɴᴇᴛᴡᴏʀᴋ:* ʀᴏᴛᴀᴛɪɴɢ sᴇssɪᴏɴs

📊 *ᴘʀᴏɢʀᴇss sᴛᴀɢᴇ:* {stage}/10

⏳ *sᴛᴀᴛᴜs:* ᴘʀᴏᴄᴇssɪɴɢ...
╚══════════════════════╝
""",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
                await asyncio.sleep(1.2)

            result = await whatsapp_reporter.execute_mass_report(
                number, category="abuse", repeats=1, methods=ALL_10_METHODS
            )
            total_reports_sent += result.get("total_successful_reports", 0)

            await asyncio.sleep(10)

        final_message = f"""
☢️ ᴍᴀx ʀᴇᴘᴏʀᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ☢️

📞 ᴛᴀʀɢᴇᴛ : `{number}`
👤 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ : {sender}

━━━━━━━━━━━━━━━━━━━━━━
🚫 ᴀᴛᴛᴀᴄᴋᴇᴅ sᴛᴀᴛᴜs 
━━━━━━━━━━━━━━━━━━━━━━
🔁 ᴄɪʀᴄᴜʟᴀᴛɪᴏɴ  : 𝟏𝟎𝟎%
⚡ ᴠᴇᴄᴛᴏʀs  : 10/10 ᴍᴇᴛʜᴏᴅs
📡 ᴘʀᴏxɪᴇs ᴜsᴇᴅ : {proxy_stats['available']}
📨 ᴛᴏᴛᴀʟ ʀᴇᴘᴏʀᴛ sᴇɴᴛ : {total_reports_sent}
━━━━━━━━━━━━━━━━━━━━━━
🎯 ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ ʀᴇsᴜʟᴛ
━━━━━━━━━━━━━━━━━━━━━━
ᴜsᴇ /check ᴛᴏ ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ 🎯

⏳ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴛᴀʀɢᴇᴛ ɪɴ
〽️ 30 ᴍɪɴ ᴛɪᴍᴇ ᴛᴏ ᴄᴏɴғɪʀᴍ
👨‍💻 ᴍᴀx ᴅᴜʀᴀᴛɪᴏɴ : 1 ʜᴏᴜʀ
ɪғ sᴛɪʟʟ ᴀᴄᴛɪᴠᴇ ʀᴇᴛʀʏ sᴀᴍᴇ ᴄᴏᴍᴍᴀɴᴅ
━━━━━━━━━━━━━━━━━━━━━━
ʜᴀʀᴅ ᴄᴏᴅᴇᴅ ʙʏ ʙᴀʜɪʀᴀᴠᴀ🌹 
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            final_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ᴍᴀss ʀᴇᴘᴏʀᴛ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def unban_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = markdown_safe(
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ</b>\n\n"
            "ᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id):
        plan_message = f"""
⛔ <b>ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ</b>

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : <code>{sender}</code>
🚫 sᴛᴀᴛᴜs : <b>ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ</b>
━━━━━━━━━━━━━━━━━━━━━━

💎 <b>ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴅᴀʏ — <code>$𝟭𝟬</code> | <code>𝟭𝟰ᴋ 🇳🇬</code>
➮ 𝟮 ᴅᴀʏ — <code>$𝟮𝟬</code> | <code>𝟮𝟴ᴋ 🇳🇬</code>
➮ 𝟯 ᴅᴀʏ — <code>$𝟯𝟬</code> | <code>𝟰𝟮ᴋ 🇳🇬</code>
➮ 𝟰 ᴅᴀʏ — <code>$𝟰𝟬</code> | <code>𝟱𝟲ᴋ 🇳🇬</code>
➮ 𝟱 ᴅᴀʏ — <code>$𝟱𝟬</code> | <code>𝟳𝟬ᴋ 🇳🇬</code>
➮ 𝟲 ᴅᴀʏ — <code>$𝟲𝟬</code> | <code>𝟴𝟰ᴋ 🇳🇬</code>
➮ 𝟭 ᴡᴇᴇᴋ — <code>$𝟳𝟬</code> | <code>𝟵𝟴ᴋ 🇳🇬</code>
➮ 𝟭 ᴍᴏɴᴛʜ — <code>$𝟭𝟮𝟬</code> | <code>𝟭𝟲𝟴ᴋ 🇳🇬</code>
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — <code>$𝟭𝟴𝟬</code> | <code>𝟮𝟱𝟮𝗸 🇳🇬</code>

✨ <b>ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟭𝟱𝟬</code> | <code>𝟮𝟭𝟬𝗸 🇳🇬</code>
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟬𝟬</code> | <code>𝟮𝟴𝟬𝗸 🇳🇬</code>
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟱𝟬</code> | <code>𝟯𝟱𝟬𝗸 🇳🇬</code>

🕊️ <b>ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ</b>

➮ <code>$𝟯𝟬𝟬</code> | <code>𝟰𝟮𝟬𝗸 🇳🇬</code>

📞 <b>ᴄᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ</b>
➮ <a href="https://t.me/DG_BAHIRAVA">@DG_BAHIRAVA</a>

<b>ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss</b>
━━━━━━━━━━━━━━━━━━━━━━
"""
        buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

        await update.message.reply_text(
            plan_message,
            parse_mode="HTML",
            reply_markup=buttons,
            disable_web_page_preview=True
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ <b>ᴜsᴀɢᴇ:</b>\n<code>/unban &lt;ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ&gt;</code>\n\n"
            "ᴇxᴀᴍᴘʟᴇ: <code>/unban +𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙𝒙</code>",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    number = context.args[0]

    if not (number.startswith('+') and number[1:].isdigit() and len(number) >= 8):
        await update.message.reply_text(
            "❌ <b>ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ғᴏʀᴍᴀᴛ</b>\n\n"
            "ᴘʟᴇᴀsᴇ ᴜsᴇ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ, ᴇ.ɢ., <code>+𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙</code>",
            parse_mode="HTML",
            reply_markup=get_owner_buttons()
        )
        return

    proxy_stats = proxy_manager.get_proxy_stats()

    processing_msg = await update.message.reply_text(
        f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
      ✦ ᴀᴘᴘᴇᴀʟ sʏsᴛᴇᴍ ʀᴜɴɴɪɴɢ.. ✦
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📞 ᴛᴀʀɢᴇᴛ        : <code>{number}</code>
🧭 ᴍᴏᴅᴇ          : sᴛᴀɴᴅᴀʀᴅ ᴜɴʙᴀɴ ᴀᴘᴘᴇᴀʟ
🌐 ᴘʀᴏxʏ sᴛᴀᴛᴜs : <code>{proxy_stats['available']} ᴏɴʟɪɴᴇ</code>
⏱️ ᴅᴜʀᴀᴛɪᴏɴ      : 45–90 sᴇᴄ
🧩 ᴍᴇᴛʜᴏᴅs       : 10 ᴀᴘᴘᴇᴀʟ ᴠᴇᴄᴛᴏʀs

╔═〔 🛰️ ᴄᴏɴɴᴇᴄᴛɪᴠɪᴛʏ 〕═╗
║ 🔐 sᴇᴄᴜʀᴇ ᴀᴘᴘᴇᴀʟs ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
║ 📡 ʀᴏᴜᴛɪɴɢ sᴛᴀʙʟᴇ
║ 🧠 ᴀᴘᴘᴇᴀʟ ʟᴏɢɪᴄ ʟᴏᴀᴅᴇᴅ
╚══════════════════════════╝

╔═〔 📊 ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋᴇʀ 〕═╗
║ ░░░░░░░░░░ 0%
╚══════════════════════════╝

⏳ sᴛᴀᴛᴜs : ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴀᴘᴘᴇᴀʟ ᴘʀᴏᴛᴏᴄᴏʟ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        parse_mode="HTML", 
        reply_markup=get_owner_buttons()
    )

    bars = [
        "[█░░░░░░░░░] 10%",
        "[██░░░░░░░░] 20%",
        "[███░░░░░░░] 30%",
        "[████░░░░░░] 40%",
        "[█████░░░░░] 50%",
        "[██████░░░░] 60%",
        "[███████░░░] 70%",
        "[████████░░] 80%",
        "[█████████░] 90%",
        "[██████████] 100%"
    ]

    for bar in bars:
        await asyncio.sleep(1.2)
        
        text_parts = processing_msg.text.split("╔═〔 📊 ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋᴇʀ 〕═╗")
        if len(text_parts) > 1:
            rest = text_parts[1].split("╚══════════════════════════╝")[1]
            new_text = text_parts[0] + f"""╔═〔 📊 ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋᴇʀ 〕═╗
║ {bar}
╚══════════════════════════╝""" + rest
            await processing_msg.edit_text(new_text, parse_mode="HTML", reply_markup=get_owner_buttons())

    try:
        ALL_APPEAL_METHODS = [
            "emotional_email_bombing",
            "emotional_web_forms",
            "facebook_whitehat_appeal",
            "instagram_cross_appeal",
            "twitter_dm_appeal",
            "whatsapp_business_api_appeal",
            "sms_gateway_appeal",
            "linkedin_outreach_appeal",
            "telegram_bot_appeal",
            "discord_webhook_appeal"
        ]

        display_names = {
            "emotional_email_bombing": "💌 ᴇᴍᴀɪʟs",
            "emotional_web_forms": "📋 ᴡᴇʙ ᴀᴘᴘᴇᴀʟ",
            "facebook_whitehat_appeal": "📘 ғᴀᴄᴇʙᴏᴏᴋ",
            "instagram_cross_appeal": "📷 ɪɴsᴛᴀɢʀᴀᴍ",
            "twitter_dm_appeal": "🐦 ᴛᴡɪᴛᴛᴇʀ",
            "whatsapp_business_api_appeal": "💼 ʙᴜsɪɴᴇss ᴀᴘɪ",
            "sms_gateway_appeal": "📱 sᴍs",
            "linkedin_outreach_appeal": "🔗 ʟɪɴᴋᴇᴅɪɴ",
            "telegram_bot_appeal": "✈️ ᴛᴇʟᴇɢʀᴀᴍ",
            "discord_webhook_appeal": "🎮 ᴅɪsᴄᴏʀᴅ"
        }

        unban_results = await whatsapp_unban.execute_mass_unban_appeal(number, repeats=30, methods=ALL_APPEAL_METHODS)

        result_lines = []
        success_count = 0
        for method in ALL_APPEAL_METHODS:
            res = unban_results.get(method)
            if isinstance(res, dict):
                success = res.get("success", 0) > 0
            else:
                success = bool(res)
            status = "✅" if success else "❌"
            if success:
                success_count += 1
            display = display_names.get(method, method.replace("_", " ").title())
            result_lines.append(f"{display:<18} {status}")

        results_table = "\n".join(result_lines)

        final_message = f"""
☢️ <b>ᴜɴʙᴀɴ ᴀᴘᴘᴇᴀʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>

━━━━━━━━━━━━━━━━━━━━━━
📞 <b>ᴛᴀʀɢᴇᴛ:</b> <code>{number}</code>
👤 <b>ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {html_escape(str(sender))}
━━━━━━━━━━━━━━━━━━━━━━

📊 <b>ᴀᴘᴘᴇᴀʟs ᴍᴇᴛʜᴏᴅs ʀᴇsᴜʟᴛs</b>
━━━━━━━━━━━━━━━━━━━━━━
{results_table}
━━━━━━━━━━━━━━━━━━━━━━

🎯 <b>sᴜᴄᴄᴇss ʀᴀᴛᴇ:</b> {success_count} / {len(ALL_APPEAL_METHODS)} ᴍᴇᴛʜᴏᴅs
━━━━━━━━━━━━━━━━━━━━━━

⚠️ <b>ᴄʜᴇᴄᴋ ᴀᴄᴄᴏᴜɴᴛ sᴛᴀᴛᴜs ᴡɪᴛʜɪɴ 𝟮𝟰–𝟰𝟴 ʜᴏᴜʀs.</b>
ɪғ ɴᴏᴛ ʀᴇsᴛᴏʀᴇᴅ, ʀᴇᴛʀʏ ʟᴀᴛᴇʀ ᴏʀ ᴜsᴇ /max_unban.
ᴜsᴇ /check ᴛᴏ ᴄᴏɴғɪʀᴍ sᴏᴏɴ
━━━━━━━━━━━━━━━━━━━━━━
"""

        buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

        await processing_msg.edit_text(
            final_message,
            parse_mode="HTML",
            reply_markup=buttons
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ <b>ᴜɴʙᴀɴ ᴘʀᴏᴄᴇss ғᴀɪʟᴇᴅ:</b>\n<code>{html_escape(str(e))}</code>",
            parse_mode="HTML",
            reply_markup=get_owner_buttons()
        )

async def max_unban_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or update.effective_user.username or "User"

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ</b>\n\n"
            "ᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs &amp; ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id):
        plan_message = f"""
⛔ <b>ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ</b>

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : <code>{html_escape(str(sender))}</code>
🚫 sᴛᴀᴛᴜs : <b>ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ</b>
━━━━━━━━━━━━━━━━━━━━━━

💎 <b>ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴅᴀʏ — <code>$𝟭𝟬</code> | <code>𝟭𝟰ᴋ 🇳🇬</code>
➮ 𝟮 ᴅᴀʏ — <code>$𝟮𝟬</code> | <code>𝟮𝟴ᴋ 🇳🇬</code>
➮ 𝟯 ᴅᴀʏ — <code>$𝟯𝟬</code> | <code>𝟰𝟮ᴋ 🇳🇬</code>
➮ 𝟰 ᴅᴀʏ — <code>$𝟰𝟬</code> | <code>𝟱𝟲ᴋ 🇳🇬</code>
➮ 𝟱 ᴅᴀʏ — <code>$𝟱𝟬</code> | <code>𝟳𝟬ᴋ 🇳🇬</code>
➮ 𝟲 ᴅᴀʏ — <code>$𝟲𝟬</code> | <code>𝟴𝟰ᴋ 🇳🇬</code>
➮ 𝟭 ᴡᴇᴇᴋ — <code>$𝟳𝟬</code> | <code>𝟵𝟴ᴋ 🇳🇬</code>
➮ 𝟭 ᴍᴏɴᴛʜ — <code>$𝟭𝟮𝟬</code> | <code>𝟭𝟲𝟴ᴋ 🇳🇬</code>
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — <code>$𝟭𝟴𝟬</code> | <code>𝟮𝟱𝟮𝗸 🇳🇬</code>

✨ <b>ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟭𝟱𝟬</code> | <code>𝟮𝟭𝟬𝗸 🇳🇬</code>
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟬𝟬</code> | <code>𝟮𝟴𝟬𝗸 🇳🇬</code>
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟱𝟬</code> | <code>𝟯𝟱𝟬𝗸 🇳🇬</code>

🕊️ <b>ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ</b>

➮ <code>$𝟯𝟬𝟬</code> | <code>𝟰𝟮𝟬𝗸 🇳🇬</code>

📞 <b>ᴄᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ</b>
➮ <a href="https://t.me/DG_BAHIRAVA">@DG_BAHIRAVA</a>

<b>ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss</b>
━━━━━━━━━━━━━━━━━━━━━━
"""
        buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

        await update.message.reply_text(
            plan_message,
            parse_mode="HTML",
            reply_markup=buttons,
            disable_web_page_preview=True
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ <b>ᴜsᴀɢᴇ:</b>\n<code>/max_unban &lt;ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ&gt;</code>\n\n"
            "ᴇxᴀᴍᴘʟᴇ: <code>/max_unban +𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙</code>",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    number = context.args[0]

    if not (number.startswith('+') and number[1:].isdigit() and len(number) >= 8):
        await update.message.reply_text(
            "❌ <b>ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ғᴏʀᴍᴀᴛ</b>\n\n"
            "ᴘʟᴇᴀsᴇ ᴜsᴇ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ, ᴇ.ɢ., <code>+𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙</code>",
            parse_mode="HTML",
            reply_markup=get_owner_buttons()
        )
        return

    proxy_stats = proxy_manager.get_proxy_stats()

    processing_msg = await update.message.reply_text(
        f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
      ✦ ᴍᴀx ᴀᴘᴘᴇᴀʟ sʏsᴛᴇᴍ ʀᴜɴɴɪɴɢ.. ✦
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📞 ᴛᴀʀɢᴇᴛ        : <code>{number}</code>
🧭 ᴍᴏᴅᴇ          : ᴍᴀxɪᴍᴜᴍ ᴜɴʙᴀɴ ᴀᴘᴘᴇᴀʟ (50 ᴄʏᴄʟᴇs)
🌐 ᴘʀᴏxʏ sᴛᴀᴛᴜs : <code>{proxy_stats['available']} ᴏɴʟɪɴᴇ</code>
⏱️ ᴅᴜʀᴀᴛɪᴏɴ      : 90–180 sᴇᴄ
🧩 ᴍᴇᴛʜᴏᴅs       : 10 ᴀᴘᴘᴇᴀʟ ᴠᴇᴄᴛᴏʀs (ʜɪɢʜ ғʀᴇǫᴜᴇɴᴄʏ)

╔═〔 🛰️ ᴄᴏɴɴᴇᴄᴛɪᴠɪᴛʏ 〕═╗
║ 🔐 sᴇᴄᴜʀᴇ ᴀᴘᴘᴇᴀʟs ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
║ 📡 ʀᴏᴜᴛɪɴɢ sᴛᴀʙʟᴇ
║ 🧠 ᴀᴘᴘᴇᴀʟ ʟᴏɢɪᴄ ʟᴏᴀᴅᴇᴅ
╚══════════════════════════╝

╔═〔 📊 ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋᴇʀ 〕═╗
║ ░░░░░░░░░░ 0%
╚══════════════════════════╝

⏳ sᴛᴀᴛᴜs : ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴍᴀx ᴀᴘᴘᴇᴀʟ ᴘʀᴏᴛᴏᴄᴏʟ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        parse_mode="HTML", 
        reply_markup=get_owner_buttons()
    )

    bars = [
        "[█░░░░░░░░░] 10%",
        "[██░░░░░░░░] 20%",
        "[███░░░░░░░] 30%",
        "[████░░░░░░] 40%",
        "[█████░░░░░] 50%",
        "[██████░░░░] 60%",
        "[███████░░░] 70%",
        "[████████░░] 80%",
        "[█████████░] 90%",
        "[██████████] 100%"
    ]

    for bar in bars:
        await asyncio.sleep(1.2)
        text_parts = processing_msg.text.split("╔═〔 📊 ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋᴇʀ 〕═╗")
        if len(text_parts) > 1:
            rest = text_parts[1].split("╚══════════════════════════╝")[1]
            new_text = text_parts[0] + f"""╔═〔 📊 ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋᴇʀ 〕═╗
║ {bar}
╚══════════════════════════╝""" + rest
            await processing_msg.edit_text(new_text, parse_mode="HTML", reply_markup=get_owner_buttons())

    try:
        ALL_APPEAL_METHODS = [
            "emotional_email_bombing",
            "emotional_web_forms",
            "facebook_whitehat_appeal",
            "instagram_cross_appeal",
            "twitter_dm_appeal",
            "whatsapp_business_api_appeal",
            "sms_gateway_appeal",
            "linkedin_outreach_appeal",
            "telegram_bot_appeal",
            "discord_webhook_appeal"
        ]

        display_names = {
            "emotional_email_bombing": "💌 ᴇᴍᴀɪʟs",
            "emotional_web_forms": "📋 ᴡᴇʙ ᴀᴘᴘᴇᴀʟ",
            "facebook_whitehat_appeal": "📘 ғᴀᴄᴇʙᴏᴏᴋ",
            "instagram_cross_appeal": "📷 ɪɴsᴛᴀɢʀᴀᴍ",
            "twitter_dm_appeal": "🐦 ᴛᴡɪᴛᴛᴇʀ",
            "whatsapp_business_api_appeal": "💼 ʙᴜsɪɴᴇss ᴀᴘɪ",
            "sms_gateway_appeal": "📱 sᴍs",
            "linkedin_outreach_appeal": "🔗 ʟɪɴᴋᴇᴅɪɴ",
            "telegram_bot_appeal": "✈️ ᴛᴇʟᴇɢʀᴀᴍ",
            "discord_webhook_appeal": "🎮 ᴅɪsᴄᴏʀᴅ"
        }

        unban_results = await whatsapp_unban.execute_mass_unban_appeal(number, repeats=50, methods=ALL_APPEAL_METHODS)

        result_lines = []
        success_count = 0
        for method in ALL_APPEAL_METHODS:
            res = unban_results.get(method)
            if isinstance(res, dict):
                success = res.get("success", 0) > 0
            else:
                success = bool(res)
            status = "✅" if success else "❌"
            if success:
                success_count += 1
            display = display_names.get(method, method.replace("_", " ").title())
            result_lines.append(f"{display:<18} {status}")

        results_table = "\n".join(result_lines)

        final_message = f"""
☢️ <b>ᴍᴀx ᴜɴʙᴀɴ ᴀᴘᴘᴇᴀʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>

━━━━━━━━━━━━━━━━━━━━━━
📞 <b>ᴛᴀʀɢᴇᴛ:</b> <code>{number}</code>
👤 <b>ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {html_escape(str(sender))}
━━━━━━━━━━━━━━━━━━━━━━

📊 <b>ᴀᴘᴘᴇᴀʟs ᴍᴇᴛʜᴏᴅs ʀᴇsᴜʟᴛs</b>
━━━━━━━━━━━━━━━━━━━━━━
{results_table}
━━━━━━━━━━━━━━━━━━━━━━

🎯 <b>sᴜᴄᴄᴇss ʀᴀᴛᴇ:</b> {success_count} / {len(ALL_APPEAL_METHODS)} ᴍᴇᴛʜᴏᴅs
🔁 <b>ᴛᴏᴛᴀʟ ᴀᴘᴘᴇᴀʟs sᴇɴᴛ:</b> {unban_results.get('total_successful_appeals', 0)}
━━━━━━━━━━━━━━━━━━━━━━

⚠️ <b>ᴄʜᴇᴄᴋ ᴀᴄᴄᴏᴜɴᴛ sᴛᴀᴛᴜs ᴡɪᴛʜɪɴ 𝟮𝟰–𝟰𝟴 ʜᴏᴜʀs.</b>
ɪғ ɴᴏᴛ ʀᴇsᴛᴏʀᴇᴅ, ᴛʀʏ /unban_temp.
ᴜsᴇ /check ᴛᴏ ᴄᴏɴғɪʀᴍ sᴏᴏɴ
━━━━━━━━━━━━━━━━━━━━━━
"""

        buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

        await processing_msg.edit_text(
            final_message,
            parse_mode="HTML",
            reply_markup=buttons
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ <b>ᴍᴀx ᴜɴʙᴀɴ ᴘʀᴏᴄᴇss ғᴀɪʟᴇᴅ:</b>\n<code>{html_escape(str(e))}</code>",
            parse_mode="HTML",
            reply_markup=get_owner_buttons()
        )

async def unban_temp_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or update.effective_user.username or "User"

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ</b>\n\n"
            "ᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs &amp; ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    if not is_owner(user_id):
        plan_message = f"""
⛔ <b>ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ</b>

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : <code>{html_escape(str(sender))}</code>
🚫 sᴛᴀᴛᴜs : <b>ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ</b>
━━━━━━━━━━━━━━━━━━━━━━

💎 <b>ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴅᴀʏ — <code>$𝟭𝟬</code> | <code>𝟭𝟰ᴋ 🇳🇬</code>
➮ 𝟮 ᴅᴀʏ — <code>$𝟮𝟬</code> | <code>𝟮𝟴ᴋ 🇳🇬</code>
➮ 𝟯 ᴅᴀʏ — <code>$𝟯𝟬</code> | <code>𝟰𝟮ᴋ 🇳🇬</code>
➮ 𝟰 ᴅᴀʏ — <code>$𝟰𝟬</code> | <code>𝟱𝟲ᴋ 🇳🇬</code>
➮ 𝟱 ᴅᴀʏ — <code>$𝟱𝟬</code> | <code>𝟳𝟬ᴋ 🇳🇬</code>
➮ 𝟲 ᴅᴀʏ — <code>$𝟲𝟬</code> | <code>𝟴𝟰ᴋ 🇳🇬</code>
➮ 𝟭 ᴡᴇᴇᴋ — <code>$𝟳𝟬</code> | <code>𝟵𝟴ᴋ 🇳🇬</code>
➮ 𝟭 ᴍᴏɴᴛʜ — <code>$𝟭𝟮𝟬</code> | <code>𝟭𝟲𝟴ᴋ 🇳🇬</code>
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — <code>$𝟭𝟴𝟬</code> | <code>𝟮𝟱𝟮𝗸 🇳🇬</code>

✨ <b>ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟭𝟱𝟬</code> | <code>𝟮𝟭𝟬𝗸 🇳🇬</code>
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟬𝟬</code> | <code>𝟮𝟴𝟬𝗸 🇳🇬</code>
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟱𝟬</code> | <code>𝟯𝟱𝟬𝗸 🇳🇬</code>

🕊️ <b>ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ</b>

➮ <code>$𝟯𝟬𝟬</code> | <code>𝟰𝟮𝟬𝗸 🇳🇬</code>

📞 <b>ᴄᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ</b>
➮ <a href="https://t.me/DG_BAHIRAVA">@DG_BAHIRAVA</a>

<b>ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss</b>
━━━━━━━━━━━━━━━━━━━━━━
"""
        buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

        await update.message.reply_text(
            plan_message,
            parse_mode="HTML",
            reply_markup=buttons,
            disable_web_page_preview=True
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ <b>ᴜsᴀɢᴇ:</b>\n<code>/temp &lt;ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ&gt;</code>\n\n"
            "ᴇxᴀᴍᴘʟᴇ: <code>/temp +𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙</code>",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )
        return

    number = context.args[0]
    
    if not (number.startswith('+') and number[1:].isdigit() and len(number) >= 8):
        await update.message.reply_text(
            "❌ <b>ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ғᴏʀᴍᴀᴛ</b>\n\n"
            "ᴘʟᴇᴀsᴇ ᴜsᴇ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ ᴡɪᴛʜ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ, ᴇ.ɢ., <code>+𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙</code>",
            parse_mode="HTML",
            reply_markup=get_owner_buttons()
        )
        return

    proxy_stats = proxy_manager.get_proxy_stats()

    processing_msg = await update.message.reply_text(
        f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ✦ ᴛᴇᴍᴘᴏʀᴀʀʏ ᴀᴘᴘᴇᴀʟ sʏsᴛᴇᴍ ʀᴜɴɴɪɴɢ.. ✦
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📞 ᴛᴀʀɢᴇᴛ        : <code>{number}</code>
🧭 ᴍᴏᴅᴇ          : ᴛᴇᴍᴘᴏʀᴀʀʏ ᴜɴʙᴀɴ ᴀᴘᴘᴇᴀʟ
🌐 ᴘʀᴏxʏ sᴛᴀᴛᴜs : <code>{proxy_stats['available']} ᴏɴʟɪɴᴇ</code>
🧩 ᴍᴇᴛʜᴏᴅs       : 10 ᴀᴘᴘᴇᴀʟ ᴠᴇᴄᴛᴏʀs

╔═〔 📊 ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋᴇʀ 〕═╗
║ ░░░░░░░░░░ 0%
╚══════════════════════════╝

""",
        parse_mode="HTML", 
        reply_markup=get_owner_buttons()
    )

    bars = [
        "[█░░░░░░░░░] 10%",
        "[██░░░░░░░░] 20%",
        "[███░░░░░░░] 30%",
        "[████░░░░░░] 40%",
        "[█████░░░░░] 50%",
        "[██████░░░░] 60%",
        "[███████░░░] 70%",
        "[████████░░] 80%",
        "[█████████░] 90%",
        "[██████████] 100%"
    ]

    for bar in bars:
        await asyncio.sleep(1.2)
        text_parts = processing_msg.text.split("╔═〔 📊 ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋᴇʀ 〕═╗")
        if len(text_parts) > 1:
            rest = text_parts[1].split("╚══════════════════════════╝")[1]
            new_text = text_parts[0] + f"""╔═〔 📊 ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋᴇʀ 〕═╗
║ {bar}
╚══════════════════════════╝""" + rest
            await processing_msg.edit_text(new_text, parse_mode="HTML", reply_markup=get_owner_buttons())

    try:
        ALL_APPEAL_METHODS = [
            "emotional_email_bombing",
            "emotional_web_forms",
            "facebook_whitehat_appeal",
            "instagram_cross_appeal",
            "twitter_dm_appeal",
            "whatsapp_business_api_appeal",
            "sms_gateway_appeal",
            "linkedin_outreach_appeal",
            "telegram_bot_appeal",
            "discord_webhook_appeal"
        ]

        display_names = {
            "emotional_email_bombing": "💌 ᴇᴍᴀɪʟs",
            "emotional_web_forms": "📋 ᴡᴇʙ ᴀᴘᴘᴇᴀʟ",
            "facebook_whitehat_appeal": "📘 ғᴀᴄᴇʙᴏᴏᴋ",
            "instagram_cross_appeal": "📷 ɪɴsᴛᴀɢʀᴀᴍ",
            "twitter_dm_appeal": "🐦 ᴛᴡɪᴛᴛᴇʀ",
            "whatsapp_business_api_appeal": "💼 ʙᴜsɪɴᴇss ᴀᴘɪ",
            "sms_gateway_appeal": "📱 sᴍs",
            "linkedin_outreach_appeal": "🔗 ʟɪɴᴋᴇᴅɪɴ",
            "telegram_bot_appeal": "✈️ ᴛᴇʟᴇɢʀᴀᴍ",
            "discord_webhook_appeal": "🎮 ᴅɪsᴄᴏʀᴅ"
        }

        unban_results = await whatsapp_unban.execute_mass_unban_appeal(number, repeats=20, methods=ALL_APPEAL_METHODS)

        result_lines = []
        success_count = 0
        for method in ALL_APPEAL_METHODS:
            res = unban_results.get(method)
            if isinstance(res, dict):
                success = res.get("success", 0) > 0
            else:
                success = bool(res)
            status = "✅" if success else "❌"
            if success:
                success_count += 1
            display = display_names.get(method, method.replace("_", " ").title())
            result_lines.append(f"{display:<18} {status}")

        results_table = "\n".join(result_lines)

        final_message = f"""
☢️ <b>ᴛᴇᴍᴘᴏʀᴀʀʏ ᴜɴʙᴀɴ ᴀᴘᴘᴇᴀʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>

━━━━━━━━━━━━━━━━━━━━━━
📞 <b>ᴛᴀʀɢᴇᴛ:</b> <code>{number}</code>
👤 <b>ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:</b> {html_escape(str(sender))}
━━━━━━━━━━━━━━━━━━━━━━

📊 <b>ᴀᴘᴘᴇᴀʟs ᴍᴇᴛʜᴏᴅs ʀᴇsᴜʟᴛs</b>
━━━━━━━━━━━━━━━━━━━━━━
{results_table}
━━━━━━━━━━━━━━━━━━━━━━

🎯 <b>sᴜᴄᴄᴇss ʀᴀᴛᴇ:</b> {success_count} / {len(ALL_APPEAL_METHODS)} ᴍᴇᴛʜᴏᴅs
━━━━━━━━━━━━━━━━━━━━━━

⚠️ <b>ᴄʜᴇᴄᴋ ᴀᴄᴄᴏᴜɴᴛ sᴛᴀᴛᴜs ᴡɪᴛʜɪɴ 𝟮𝟰 ʜᴏᴜʀs.</b>
ɪғ ɴᴏᴛ ʀᴇsᴛᴏʀᴇᴅ, ᴛʀʏ /unban. ᴀɢᴀɪɴ
ᴜsᴇ /ban_checker ᴛᴏ ᴄᴏɴғɪʀᴍ sᴏᴏɴ
━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        buttons = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ",
            url=f"https://t.me/{OWNER_USERNAME}",
            style="success",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",
            url=REQUIRED_CHATS[0][1],
            style="primary",
            icon_custom_emoji_id="5197304993920616826"
        )
    ]

])

        await processing_msg.edit_text(
            final_message,
            parse_mode="HTML",
            reply_markup=buttons
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ <b>ᴛᴇᴍᴘ ᴜɴʙᴀɴ ᴘʀᴏᴄᴇss ғᴀɪʟᴇᴅ:</b>\n<code>{html_escape(str(e))}</code>",
            parse_mode="HTML",
            reply_markup=get_owner_buttons()
        )
        
async def pay_now_command(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    sender = user.first_name or user.username or "User"
    user_id = user.id
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""
╔═══════════════════════════╗
🧾 <b>ᴘᴀʏᴍᴇɴᴛ ᴀɴᴅ ᴘʟᴀɴs ᴀᴄᴄᴇss</b>
╚═══════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━
👤 <b>ᴜsᴇʀ:</b> {html_escape(str(sender))}
🆔 <b>ᴜsᴇʀ ɪᴅ:</b> <code>{user_id}</code>
⏱️ <b>ʀᴇǫᴜᴇsᴛ ᴛɪᴍᴇ:</b> <code>{time}</code>
━━━━━━━━━━━━━━━━━━━━━━

💎 <b>ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴅᴀʏ — <code>$𝟭𝟬</code> | <code>𝟭𝟰ᴋ 🇳🇬</code>
➮ 𝟮 ᴅᴀʏ — <code>$𝟮𝟬</code> | <code>𝟮𝟴ᴋ 🇳🇬</code>
➮ 𝟯 ᴅᴀʏ — <code>$𝟯𝟬</code> | <code>𝟰𝟮ᴋ 🇳🇬</code>
➮ 𝟰 ᴅᴀʏ — <code>$𝟰𝟬</code> | <code>𝟱𝟲ᴋ 🇳🇬</code>
➮ 𝟱 ᴅᴀʏ — <code>$𝟱𝟬</code> | <code>𝟳𝟬ᴋ 🇳🇬</code>
➮ 𝟲 ᴅᴀʏ — <code>$𝟲𝟬</code> | <code>𝟴𝟰ᴋ 🇳🇬</code>
➮ 𝟭 ᴡᴇᴇᴋ — <code>$𝟳𝟬</code> | <code>𝟵𝟴ᴋ 🇳🇬</code>
➮ 𝟭 ᴍᴏɴᴛʜ — <code>$𝟭𝟮𝟬</code> | <code>𝟭𝟲𝟴ᴋ 🇳🇬</code>
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — <code>$𝟭𝟴𝟬</code> | <code>𝟮𝟱𝟮𝗸 🇳🇬</code>

✨ <b>ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss</b>

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟭𝟱𝟬</code> | <code>𝟮𝟭𝟬𝗸 🇳🇬</code>
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟬𝟬</code> | <code>𝟮𝟴𝟬𝗸 🇳🇬</code>
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — <code>$𝟮𝟱𝟬</code> | <code>𝟯𝟱𝟬𝗸 🇳🇬</code>

🕊️ <b>ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ</b>

➮ <code>$𝟯𝟬𝟬</code> | <code>𝟰𝟮𝟬𝗸 🇳🇬</code>

━━━━━━━━━━━━━━━━━━━━━━
💳 <b>ᴘᴀʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅ</b>
━━━━━━━━━━━━━━━━━━━━━━
• 🔶 <b>ʙɪɴᴀɴᴄᴇ</b>
• ɪᴅ: <code>{html_escape(BINANCE_ID)}</code>
• ɴᴀᴍᴇ: <b>{html_escape(BINANCE_NAME)}</b>

━━━━━━━━━━━━━━━━━━━━━━
⚠️ <b>ɪᴍᴘᴏʀᴛᴀɴᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
━━━━━━━━━━━━━━━━━━━━━━

🔥 ᴍᴀᴋᴇ <b>ғᴜʟʟ ᴘᴀʏᴍᴇɴᴛ</b> ғᴏʀ sᴇʟᴇᴄᴛᴇᴅ ᴘʟᴀɴ
📸 sᴇɴᴅ <b>ᴄʟᴇᴀʀ ᴘᴀʏᴍᴇɴᴛ sᴄʀᴇᴇɴsʜᴏᴛ</b> ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ
🧾 ɪɴᴄʟᴜᴅᴇ <b>ᴛʀᴀɴsᴀᴄᴛɪᴏɴ ɪᴅ / ʀᴇғᴇʀᴇɴᴄᴇ</b>
⏳ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴍᴀʏ ᴛᴀᴋᴇ <b>5–15 ᴍɪɴᴜᴛᴇs</b>
🚫 ɴᴏ ᴀᴄᴄᴇss ᴡɪᴛʜᴏᴜᴛ ᴘᴀʏᴍᴇɴᴛ ᴄᴏɴғɪʀᴍᴀᴛɪᴏɴ

━━━━━━━━━━━━━━━━━━━━━━
📌 <b>ᴠɪᴛᴀʟ ɴᴏᴛɪᴄᴇ</b>
━━━━━━━━━━━━━━━━━━━━━━
• sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ
• ᴇᴅɪᴛᴇᴅ / ғᴀᴋᴇ sᴄʀᴇᴇɴsʜᴏᴛs ᴡɪʟʟ ʀᴇsᴜʟᴛ ɪɴ ʙʟᴏᴄᴋ
• ᴡʀᴏɴɢ ᴀᴍᴏᴜɴᴛ sᴇɴᴛ = ɴᴏ ᴀᴄᴛɪᴠᴀᴛɪᴏɴ
• ᴅᴏ ɴᴏᴛ sᴘᴀᴍ
• ᴘᴀʏᴍᴇɴᴛ ɪs <b>ɴᴏɴ-ʀᴇғᴜɴᴅᴀʙʟᴇ</b> ᴀғᴛᴇʀ ᴀᴄᴛɪᴠᴀᴛɪᴏɴ

━━━━━━━━━━━━━━━━━━━━━━
✅ ᴀғᴛᴇʀ ᴄᴏɴғɪʀᴍᴀᴛɪᴏɴ, ᴀᴄᴄᴇss ᴡɪʟʟ ʙᴇ ɢʀᴀɴᴛᴇᴅ ɪɴsᴛᴀɴᴛʟʏ
━━━━━━━━━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup([

    [
        InlineKeyboardButton(
            "𝟭 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ",
            callback_data="plan_day1",
            style="success",
            icon_custom_emoji_id="5427168083074628963"
        ),

        InlineKeyboardButton(
            "𝟮 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ",
            callback_data="plan_day2",
            style="primary",
            icon_custom_emoji_id="5427168083074628963"
        )
    ],

    [
        InlineKeyboardButton(
            "𝟯 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ",
            callback_data="plan_day3",
            style="default",
            icon_custom_emoji_id="5427168083074628963"
        )
    ],

    [
        InlineKeyboardButton(
            "𝟰 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ",
            callback_data="plan_day4",
            style="success",
            icon_custom_emoji_id="5427168083074628963"
        ),

        InlineKeyboardButton(
            "𝟱 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ",
            callback_data="plan_day5",
            style="primary",
            icon_custom_emoji_id="5427168083074628963"
        )
    ],

    [
        InlineKeyboardButton(
            "𝟲 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ",
            callback_data="plan_day6",
            style="default",
            icon_custom_emoji_id="5427168083074628963"
        )
    ],

    [
        InlineKeyboardButton(
            "𝟭 ᴡᴇᴇᴋ ᴘʀᴇᴍɪᴜᴍ",
            callback_data="plan_week",
            style="success",
            icon_custom_emoji_id="5427168083074628963"
        ),

        InlineKeyboardButton(
            "𝟭 ᴍᴏɴᴛʜ ᴘʀᴇᴍɪᴜᴍ",
            callback_data="plan_month",
            style="primary",
            icon_custom_emoji_id="5427168083074628963"
        )
    ],

    [
        InlineKeyboardButton(
            "ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ",
            callback_data="plan_perm",
            style="danger",
            icon_custom_emoji_id="6122988085362824105"
        )
    ],

    [
        InlineKeyboardButton(
            "𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ",
            callback_data="plan_owner_month",
            style="primary",
            icon_custom_emoji_id="5433758796289685818"
        ),

        InlineKeyboardButton(
            "𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ",
            callback_data="plan_owner_year",
            style="success",
            icon_custom_emoji_id="5433758796289685818"
        )
    ],

    [
        InlineKeyboardButton(
            "ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ",
            callback_data="plan_owner_lifetime",
            style="danger",
            icon_custom_emoji_id="6084393784118872313"
        )
    ],

    [
        InlineKeyboardButton(
            "ʙᴀɴ ʙᴏᴛ sᴄʀɪᴘᴛ",
            callback_data="plan_script",
            style="default",
            icon_custom_emoji_id="6084393784118872313"
        )
    ]

])

    await context.bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode="HTML",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

async def plan_select_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    plan_map = {
    "plan_day1": "𝟭 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ — $𝟭𝟬 | 𝟭𝟰𝗸 🇳🇬",
    "plan_day2": "𝟮 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ — $𝟮𝟬 | 𝟮𝟴𝗸 🇳🇬",
    "plan_day3": "𝟯 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ — $𝟯𝟬 | 𝟰𝟮𝗸 🇳🇬",
    "plan_day4": "𝟰 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ — $𝟰𝟬 | 𝟱𝟲𝗸 🇳🇬",
    "plan_day5": "𝟱 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ — $𝟱𝟬 | 𝟳𝟬𝗸 🇳🇬",
    "plan_day6": "𝟲 ᴅᴀʏ ᴘʀᴇᴍɪᴜᴍ — $𝟲𝟬 | 𝟴𝟰𝗸 🇳🇬",
    "plan_week": "𝟭 ᴡᴇᴇᴋ ᴘʀᴇᴍɪᴜᴍ — $𝟳𝟬 | 𝟵𝟴𝗸 🇳🇬",
    "plan_month": "𝟭 ᴍᴏɴᴛʜ ᴘʀᴇᴍɪᴜᴍ — $𝟭𝟮𝟬 | 𝟭𝟲𝟴𝗸 🇳🇬",
    "plan_perm": "ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — $𝟭𝟴𝟬 | 𝟮𝟱𝟮𝗸 🇳🇬",
    "plan_owner_month": "𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — $𝟭𝟱𝟬 | 𝟮𝟭𝟬𝗸 🇳🇬",
    "plan_owner_year": "𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — $𝟮𝟬𝟬 | 𝟮𝟴𝟬𝗸 🇳🇬",
    "plan_owner_lifetime": "♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — $𝟮𝟱𝟬 | 𝟯𝟱𝟬𝗸 🇳🇬",
    "plan_script": "ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — $𝟯𝟬𝟬 | 𝟰𝟮𝟬𝗸 🇳🇬"
}

    plan = plan_map.get(query.data)
    if not plan:
        return

    safe_plan = html_escape(str(plan))
    context.user_data.clear()
    context.user_data["selected_plan"] = plan
    context.user_data["awaiting_screenshot"] = True

    await query.message.reply_text(
    f"""
╔═══════════════════════════╗
  💳 <b>ᴘᴀʏᴍᴇɴᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴅᴀsʜʙᴏᴀʀᴅ</b>
╚═══════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💎 <b>sᴇʟᴇᴄᴛᴇᴅ ᴘʟᴀɴ</b>
┃ <code>{safe_plan}</code>
┗━━━━━━━━━━━━━━━━━━━━━━┛

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📸 <b>ʀᴇǫᴜɪʀᴇᴅ ᴀᴄᴛɪᴏɴ</b>
┃ sᴇɴᴅ ᴄʟᴇᴀʀ ᴘᴀʏᴍᴇɴᴛ sᴄʀᴇᴇɴsʜᴏᴛ
┃ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ ʜᴇʀᴇ
┗━━━━━━━━━━━━━━━━━━━━━━┛

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⏳ <b>ᴀᴄᴛɪᴠᴀᴛɪᴏɴ ᴛɪᴍᴇ</b>
┃ 5–15 ᴍɪɴᴜᴛᴇs ᴀғᴛᴇʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ
┗━━━━━━━━━━━━━━━━━━━━━━┛

⚠️ <b>ɴᴏ ᴀᴄᴄᴇss ᴡɪᴛʜᴏᴜᴛ ᴘᴀʏᴍᴇɴᴛ ᴘʀᴏᴏғ</b>
""",
    parse_mode="HTML", 
    reply_markup=get_owner_buttons()
)

async def screenshot_handler(update: Update, context: CallbackContext):
    if not update.message or not update.message.photo:
        return

    if not context.user_data.get("awaiting_screenshot"):
        return

    user = update.effective_user
    plan = context.user_data.get("selected_plan")

    PENDING_PAYMENTS[user.id] = {
        "plan": plan
    }

    safe_user_name = html_escape(user.first_name or "Unknown")
    safe_plan = html_escape(str(plan or "Unknown"))

    caption = f"""
╔══════════════════════════╗
  🧾 <b>ᴘᴀʏᴍᴇɴᴛ ᴀʟᴇʀᴛ — ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ</b>
╚══════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ 👤 <b>ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
┃ ɴᴀᴍᴇ: {safe_user_name}
┃ ɪᴅ: <code>{user.id}</code>
┗━━━━━━━━━━━━━━━━━━━━━━┛

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💎 <b>sᴇʟᴇᴄᴛᴇᴅ ᴘʟᴀɴ</b>
┃ {safe_plan}
┗━━━━━━━━━━━━━━━━━━━━━━┛

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📸 <b>ᴀᴛᴛᴀᴄʜᴇᴅ</b>
┃ ᴘᴀʏᴍᴇɴᴛ sᴄʀᴇᴇɴsʜᴏᴛ ғᴏʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ
┗━━━━━━━━━━━━━━━━━━━━━━┛

⚠️ <b>ᴀᴄᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ:</b> ᴠᴇʀɪғʏ ᴀɴᴅ ᴀᴄᴛɪᴠᴀᴛᴇ ᴘʟᴀɴ
"""

    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴀᴘᴘʀᴏᴠᴇ", callback_data=f"approve:{user.id}", style="success", icon_custom_emoji_id="5208880351690112495"),
            InlineKeyboardButton("ʀᴇᴊᴇᴄᴛ", callback_data=f"reject:{user.id}", style="danger", icon_custom_emoji_id="5210952531676504517")
        ]
    ])

    for admin_id in ADMIN_IDS:
        await context.bot.send_photo(
            chat_id=admin_id,
            photo=update.message.photo[-1].file_id,
            caption=caption,
            parse_mode="HTML",
            reply_markup=admin_keyboard
        )

    context.user_data["awaiting_screenshot"] = False

    await update.message.reply_text(
        f"""
╔═══════════════════════════╗
        ✅ <b>sᴄʀᴇᴇɴsʜᴏᴛ ʀᴇᴄᴇɪᴠᴇᴅ</b>
╚══════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📸 ᴘᴀʏᴍᴇɴᴛ ᴘʀᴏᴏғ sᴜʙᴍɪᴛᴛᴇᴅ
┃ ⏳ ᴀᴡᴀɪᴛɪɴɢ ᴀᴅᴍɪɴ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ
┗━━━━━━━━━━━━━━━━━━━━━━┛

🔔 <b>ɴᴏᴛɪᴄᴇ:</b> ʏᴏᴜ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪғɪᴇᴅ ᴏɴᴄᴇ ᴀᴘᴘʀᴏᴠᴇᴅ
""",
        parse_mode="HTML", 
        reply_markup=get_owner_buttons()
    )

async def admin_decision_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.from_user.id not in ADMIN_IDS:
        return

    action, user_id = query.data.split(":")
    user_id = int(user_id)

    payment = PENDING_PAYMENTS.get(user_id)
    if not payment:
        await query.message.reply_text("⚠️ ᴘᴀʏᴍᴇɴᴛ data ɴᴏᴛ ғᴏᴜɴᴅ.")
        return

    plan = payment["plan"]
    safe_plan = html_escape(str(plan or "Unknown"))

    if action == "approve":
        if "Premium" in plan:
            if user_id not in db["premium"]:
                db["premium"].append(user_id)
                save_db()

        if "Owner" in plan:
            if user_id not in db["owners"]:
                db["owners"].append(user_id)
                save_db()

        await context.bot.send_message(
            chat_id=user_id,
            text=f"""
╔══════════════════════════╗
      🎉 <b>ᴘᴀʏᴍᴇɴᴛ ᴀᴘᴘʀᴏᴠᴇᴅ</b>
╚══════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💎 <b>ᴘʟᴀɴ sᴇʟᴇᴄᴛᴇᴅ:</b> {safe_plan}
┃ 🆔 <b>ᴜsᴇʀ ɪᴅ:</b> <code>{user_id}</code>
┃ ⏱️ <b>ᴀᴄᴛɪᴠᴀᴛᴇᴅ:</b> ᴊᴜsᴛ ɴᴏᴡ
┗━━━━━━━━━━━━━━━━━━━━━━━━┛

✅ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ  
🔓 ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ɴᴏᴡ ᴜɴʟᴏᴄᴋᴇᴅ  
📊 ᴀᴄᴄᴏᴜɴᴛ sᴛᴀᴛᴜs: <b>ᴀᴄᴛɪᴠᴇ &amp; ᴠᴇʀɪғɪᴇᴅ</b>  
🗂️ ʀᴇᴄᴏʀᴅ ᴜᴘᴅᴀᴛᴇᴅ ɪɴ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀʙᴀsᴇ

━━━━━━━━━━━━━━━━━━━━━━
🚀 <b>ᴡʜᴀᴛ ʏᴏᴜ ᴄᴀɴ ᴅᴏ ɴᴏᴡ</b>
• ᴜsᴇ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs
• ғᴀsᴛᴇʀ ᴘʀᴏᴄᴇssɪɴɢ sᴘᴇᴇᴅ
• ᴘʀɪᴏʀɪᴛʏ sʏsᴛᴇᴍ ʀᴏᴜᴛɪɴɢ
• ᴇxᴛᴇɴᴅᴇᴅ ᴄᴏᴍᴍᴀɴᴅ ʟɪᴍɪᴛs

━━━━━━━━━━━━━━━━━━━━━━
🔔 <b>ɴᴏᴛɪᴄᴇ</b>
ᴛʏᴘᴇ /start ᴛᴏ sᴇᴇ ᴀʟʟ ᴜɴʟᴏᴄᴋᴇᴅ ғᴇᴀᴛᴜʀᴇs

╔═══════════════════════╗
   ✅ <b>sᴛᴀᴛᴜs: ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴇ</b>
╚═══════════════════════╝
""",
            parse_mode="HTML"
        )

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n✅ <b>ᴀᴘᴘʀᴏᴠᴇᴅ</b>",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )

    if action == "reject":
        await context.bot.send_message(
            chat_id=user_id,
            text=f"""
╔═════════════════════════╗
     ❌ <b>ᴘᴀʏᴍᴇɴᴛ ʀᴇᴊᴇᴄᴛᴇᴅ</b>
╚═════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💎 <b>ᴘʟᴀɴ sᴇʟᴇᴄᴛᴇᴅ:</b> {safe_plan}
┃ 🆔 <b>ᴜsᴇʀ ɪᴅ:</b> <code>{user_id}</code>
┃ ⏱️ <b>sᴛᴀᴛᴜs:</b> ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ
┗━━━━━━━━━━━━━━━━━━━━━━━━┛

🚫 ᴛʜᴇ sᴜʙᴍɪᴛᴛᴇᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ᴠᴇʀɪғɪᴇᴅ  
📸 ᴘʟᴇᴀsᴇ ʀᴇsᴇɴᴅ ᴀ <b>ᴄʟᴇᴀʀ &amp; ᴠᴀʟɪᴅ ᴘᴀʏᴍᴇɴᴛ sᴄʀᴇᴇɴsʜᴏᴛ</b>

━━━━━━━━━━━━━━━━━━━━━━
🔎 <b>ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜᴇ sᴄʀᴇᴇɴsʜᴏᴛ sʜᴏᴡs:</b>
• ᴘᴀʏᴍᴇɴᴛ ᴀᴍᴏᴜɴᴛ
• ᴛʀᴀɴsᴀᴄᴛɪᴏɴ ɪᴅ
• ᴅᴀᴛᴇ &amp; ᴛɪᴍᴇ
• ᴘᴀʏᴍᴇɴᴛ sᴛᴀᴛᴜs: sᴜᴄᴄᴇssғᴜʟ

━━━━━━━━━━━━━━━━━━━━━━
⚠️ <b>ɴᴏ ᴀᴄᴄᴇss ᴡɪʟʟ ʙᴇ ɢʀᴀɴᴛᴇᴅ ᴜɴᴛɪʟ ᴠᴇʀɪғɪᴇᴅ</b>

╔══════════════════════════╗
  ⏳ <b>ᴡᴀɪᴛɪɴɢ ғᴏʀ ᴠᴀʟɪᴅ sᴜʙᴍɪssɪᴏɴ</b>
╚══════════════════════════╝
""",
            parse_mode="HTML"
        )

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n❌ <b>ʀᴇᴊᴇᴄᴛᴇᴅ</b>",
            parse_mode="HTML", 
            reply_markup=get_owner_buttons()
        )

    PENDING_PAYMENTS.pop(user_id, None)

async def termux_tools_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "🚫 ᴇʀʀᴏʀ ᴛʜᴀᴛ's ɪɴᴄᴏʀʀᴇᴄᴛ\n\n"
            "ᴄᴏʀʀᴇᴄᴛ ᴜsᴀɢᴇ ɪs\n\n"
            "/termux_tools <ᴛᴏᴏʟs ɴᴀᴍᴇ>\n\n"
            "ᴇxᴀᴍᴘʟᴇ : /termux_tools ᴘʜɪsʜɪɴɢ ᴛᴏᴏʟs",
            reply_markup=get_owner_buttons()
        )
        return

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs first.\n\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown", 
            reply_markup=get_owner_buttons()
        )
        return

    query = " ".join(context.args)
    await fetch_tools(update, context, query)

async def fetch_tools(update, context, query: str):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = (
        f"https://api.github.com/search/repositories"
        f"?q={query}&sort=stars&order=desc"
        f"&per_page={RESULTS_PER_PAGE}"
    )

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            if r.status != 200:
                await update.message.reply_text("❌ ɢɪᴛʜᴜʙ ᴀᴘɪ ᴇʀʀᴏʀ.")
                return
            data = await r.json()

    repos = data.get("items", [])
    if not repos:
        await update.message.reply_text("❌ ɴᴏ ᴛᴏᴏʟs ғᴏᴜɴᴅ ғᴏʀ ᴛʜɪs ᴜsᴇ ᴀɴᴏᴛʜᴇʀ ᴋᴇʏᴡᴏʀᴅ.")
        return

    for repo in repos:
        name = repo["name"]
        owner = repo["owner"]["login"]
        stars = repo["stargazers_count"]
        forks = repo["forks_count"]
        updated = repo["updated_at"][:10]
        link = repo["html_url"]

        commands = await fetch_readme(owner, name)
        install_text = commands or "ɴᴏ ɪɴsᴛᴀʟʟᴀᴛɪᴏɴ ᴄᴏᴍᴍᴀɴᴅs ғᴏᴜɴᴅ ᴠɪsɪᴛ ᴛʜᴇ ɢɪᴛʜᴜʙ ʟɪɴᴋ ᴛᴏ ʀᴇᴀᴅ ғɪʀsᴛ"

        message = (
            f"🛠 *ʙᴀʜɪʀᴀᴠᴀ ᴛᴏᴏʟs*\n\n"
            f"📦 *{name}*\n"
            f"👨‍💻 ᴅᴇᴠ `{owner}`\n"
            f"⭐ sᴛᴀʀs `{stars}`\n"
            f"🍴 ғᴏʀᴋs `{forks}`\n"
            f"📅 ᴜᴘᴅᴀᴛᴇ `{updated}`\n"
            f"🔗 {link}\n\n"
            f"```bash\n{install_text}\n```"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "ᴄᴏᴘʏ ɪɴsᴛᴀʟʟ ᴄᴏᴍᴍᴀɴᴅ",
                    callback_data=f"copy:{owner}/{name}",
                    style="success",
                    icon_custom_emoji_id="6084393784118872313"
                )
            ]
        ])

        await update.message.reply_text(
            message[:MAX_MESSAGE_LEN],
            parse_mode="Markdown",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

async def copy_install_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    _, repo_path = query.data.split(":", 1)
    owner, repo = repo_path.split("/")

    commands = await fetch_readme(owner, repo)

    await query.message.reply_text(
        f"📋 *ᴄᴏᴘʏ ɪɴsᴛᴀʟʟ ᴄᴏᴍᴍᴀɴᴅ*\n\n"
        f"```bash\n{commands or 'ɴᴏ ɪɴsᴛᴀʟʟᴀᴛɪᴏɴ ᴄᴏᴍᴍᴀɴᴅs ғᴏᴜɴᴅ ᴠɪsɪᴛ ᴛʜᴇ ɢɪᴛʜᴜʙ ʟɪɴᴋ ᴛᴏ ʀᴇᴀᴅ ғɪʀsᴛ'}\n```",
        parse_mode="Markdown", 
        reply_markup=get_owner_buttons()
   ) 
   
async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message

    if message.reply_to_message and message.reply_to_message.text:
        text_to_translate = message.reply_to_message.text

    elif context.args:
        text_to_translate = " ".join(context.args)

    else:
        await message.reply_text(
            "🌍 ᴛʀᴀɴsʟᴀᴛɪᴏɴ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🔹 ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛʀᴀɴsʟᴀᴛᴇs ᴀɴʏ ʟᴀɴɢᴜᴀɢᴇ\n"
            "   ɪɴᴛᴏ ᴇɴɢʟɪsʜ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.\n\n"
            "📌 ʜᴏᴡ ᴛᴏ ᴜsᴇ:\n"
            "• ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴛʏᴘᴇ /translate\n"
            "• ᴏʀ ᴛʏᴘᴇ:\n"
            "   /translate <ᴛᴇxᴛ>\n\n"
            "💡 ᴇxᴀᴍᴘʟᴇ:\n"
            "   /translate ʜᴏʟᴀ ᴄᴏᴍᴏ ᴇsᴛᴀs\n\n"
            "⚡ ғᴇᴀᴛᴜʀᴇs:\n"
            "• ᴀᴜᴛᴏ ʟᴀɴɢᴜᴀɢᴇ ᴅᴇᴛᴇᴄᴛɪᴏɴ\n"
            "• ғᴀsᴛ ᴛʀᴀɴsʟᴀᴛɪᴏɴ\n",
            reply_markup=get_owner_buttons()
        )
        return

    loading_message = await message.reply_text("⏳ ᴛʀᴀɴsʟᴀᴛɪɴɢ")

    async def animate_loading():
        dots = [
            "⏳ ᴛʀᴀɴsʟᴀᴛɪɴɢ.",
            "⏳ ᴛʀᴀɴsʟᴀᴛɪɴɢ..",
            "⏳ ᴛʀᴀɴsʟᴀᴛɪɴɢ..."
        ]
        i = 0
        while True:
            try:
                await loading_message.edit_text(dots[i % 3])
                i += 1
                await asyncio.sleep(0.6)
            except:
                break

    animation_task = asyncio.create_task(animate_loading())

    try:
        detected_lang, detected_lang_name = await detect_language(text_to_translate)

        translator = Translator()

        translation = await translator.translate(
            text_to_translate,
            src=detected_lang,
            dest="en"
        )

        translated_text = translation.text

        ai_response = await get_ai_response(translated_text)

    except Exception as e:
        animation_task.cancel()
        await loading_message.edit_text(f"❌ Translation error:\n{e}")
        return

    animation_task.cancel()

    translation_response = f"""
✨ ᴇɴɢʟɪsʜ ʟᴀɴɢᴜᴀɢᴇ ᴛʀᴀɴsʟᴀᴛɪᴏɴ ✨

🔍 ʟᴀɴɢᴜᴀɢᴇ ᴅᴇᴛᴇᴄᴛᴇᴅ:
{detected_lang_name} {emoji_flag(detected_lang)}

💬 ᴏʀɪɢɪɴᴀʟ ᴍᴇssᴀɢᴇ:
{text_to_translate}

🇬🇧 ᴛʀᴀɴsʟᴀᴛᴇᴅ ᴛᴏ ᴇɴɢʟɪsʜ:
{translated_text}

💬 ᴄʀʏᴘᴛᴏ ᴀɪ ʀᴇsᴘᴏɴᴅ:
{ai_response}
"""

    await loading_message.edit_text(
        translation_response,
        reply_markup=get_owner_buttons()
    )

async def get_ai_response(prompt: str):
    loop = asyncio.get_running_loop()

    def ai_fallback():
        result = ask_groq(prompt)
        if result:
            return result

        result = ask_huggingface(prompt)
        if result:
            return result

        return "ᴀɪ sᴇʀᴠɪᴄᴇ ɪs ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ."

    return await loop.run_in_executor(None, ai_fallback)
    
async def progress_update(context, chat_id, text):
    msg = await context.bot.send_message(chat_id=chat_id, text=text)
    return msg
    
async def ban_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    config = load_config()

    owner_id = config.get("owner_id")

    if user_id != owner_id:
        await update.message.reply_text(
            "🚫 ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ 🚫\n\n"
            "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴛʜɪs sʏsᴛᴇᴍ.\n"
            "ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.",
            reply_markup=get_owner_buttons()
        )
        return

    args = context.args

    if not args or args[0].lower() not in ["on", "off"]:
        await update.message.reply_text(
            "⚙️ ʙᴀɴ ɢᴘᴛ ᴄᴏɴᴛʀᴏʟ ᴀɪ ⚙️\n\n"
            "ᴄᴏʀʀᴇᴄᴛ ᴜsᴀɢᴇ:\n\n"
            "➤ /ban_gpt on ᴛᴏ ᴛᴜʀɴ ʙᴀɴ ɢᴘᴛ ᴀɪ ᴏɴ\n"
            "➤ /ban_gpt off ᴛᴏ ᴛᴜʀɴ ʙᴀɴ ɢᴘᴛ ᴀɪ ᴏғғ\n\n"
            "ʙᴀɴ ɢᴘᴛ ᴀɪ ɪs ᴡᴀɪᴛɪɴɢ ғᴏʀ ʏᴏᴜʀ ᴄᴏᴍᴍᴀɴᴅ…",
            reply_markup=get_owner_buttons()
        )
        return

    new_state = args[0].lower() == "on"
    config["ban_gpt_enabled"] = new_state
    save_config(config)

    status_text = "🟢 ᴇɴᴀʙʟᴇᴅ" if new_state else "🔴 ᴅɪsᴀʙʟᴇᴅ"

    await update.message.reply_text(
        "┏═━═━═━═━═━═━═━═━═━═━╗\n"
        "    🤖 ʙᴀɴ ɢᴘᴛ ᴀɪ sʏsᴛᴇᴍ\n"
        "┗━═━═━═━═━═━═━═━═━═━═┛\n\n"
        "📌 sᴛᴀᴛᴜs ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!\n\n"
        f"🔒 ʙᴀɴ ɢᴘᴛ ᴍᴏᴅᴇ: {status_text}\n\n"
        "🛡 sʏsᴛᴇᴍ ɪs ʀᴜɴɴɪɴɢ ɴᴏʀᴍᴀʟʟʏ.\n"
        "⚡ ᴀᴡᴀɪᴛɪɴɢ ғᴜʀᴛʜᴇʀ ɪɴsᴛʀᴜᴄᴛɪᴏɴs ᴍʏ ʟᴏʀᴅ 🙇‍♂️",
        reply_markup=get_owner_buttons()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

   
    if update.effective_user is None or update.message is None:
        return

    config = load_config()
    user_id = update.effective_user.id

    if not config["ban_gpt_enabled"] and user_id != config["owner_id"]:
        return

    bot = await context.bot.get_me()
    bot_username = bot.username

    is_reply_to_bot = (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user.id == bot.id
    )

    text = update.message.text or update.message.caption or ""
    is_mention = f"@{bot_username}" in text

    if not (is_reply_to_bot or is_mention):
        return

    text_clean = text.replace(f"@{bot_username}", "").strip()

    triggers = ["code me", "create", "build", "code", "make a", "run a"]
    lower_text = text_clean.lower()

    triggered = False
    request = ""

    for phrase in triggers:
        if phrase in lower_text:
            idx = lower_text.find(phrase) + len(phrase)
            request = text_clean[idx:].strip()
            triggered = True
            break

    api_key = config.get("hf_api_key")
    model = config.get("hf_model")

    if triggered:

        if not request:
            await update.message.reply_text(
                "🤖 ʜᴇʟʟᴏ ᴍʏ ʟᴏʀᴅ 👑\n\n"
                "ᴡʜᴀᴛ sʜᴏᴜʟᴅ ɪ ᴄʀᴇᴀᴛᴇ ғᴏʀ ʏᴏᴜ ᴛᴏᴅᴀʏ?\n\n"
                "💡 sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ɪᴅᴇᴀ ᴀɴᴅ ɪ ᴡɪʟʟ ʙᴜɪʟᴅ ɪᴛ ғᴏʀ ʏᴏᴜ.",
                reply_markup=get_owner_buttons()
            )
            return

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="upload_document"
        )

        progress_msg = await progress_update(
            context,
            update.effective_chat.id,
            "⚙️ ʙᴀɴ ɢᴘᴛ ᴇɴɢɪɴᴇ ᴀᴄᴛɪᴠᴇ\n\n"
            f"📌 ʏᴏᴜ ʀᴇǫᴜᴇsᴛ ғᴏʀ :\n'{request}'\n\n"
            "⏳ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ ᴘʀᴏᴊᴇᴄᴛ ғɪʟᴇ📁...\n"
            "sᴇɴᴅɪɴɢ ʏᴏᴜʀ ғɪʟᴇ ᴅᴏᴄᴜᴍᴇɴᴛ ɪɴ ғᴇᴡ ᴍɪɴᴜᴛᴇs."
        )

        files = generate_project_with_ai(request, api_key, model)

        if not files:
            await progress_msg.edit_text(
                "❌ ᴘʀᴏᴊᴇᴄᴛ ɢᴇɴᴇʀᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ.\n\n"
                "🔁 ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.",
                reply_markup=get_owner_buttons()
            )
            return

        zip_path = os.path.join(
            tempfile.gettempdir(),
            f"project_{update.message.message_id}.zip"
        )

        create_zip_from_files(files, zip_path)

        with open(zip_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=os.path.basename(zip_path),
                caption=(
                    "📦 ᴘʀᴏᴊᴇᴄᴛ ᴅᴏᴄᴜᴍᴇɴᴛ ʀᴇᴀᴅʏ\n\n"
                    "✅ ɢᴇɴᴇʀᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ʙʏ ʙᴀɴ ɢᴘᴛ ᴀɪ\n\n"
                    "🚀 ʀᴇᴀᴅʏ ᴛᴏ ᴅᴇᴘʟᴏʏ ʏᴏᴜʀ ғɪʟᴇ 📁 ᴍʏ ʟᴏʀᴅ."
                ),
                reply_markup=get_owner_buttons()
            )

        os.remove(zip_path)
        await progress_msg.delete()
        return
        
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    reply = query_huggingface(text_clean, api_key, model)

    if reply:
        await update.message.reply_text(
            reply,
            reply_markup=get_owner_buttons()
        )

async def animated_progress(message, title="ᴘʀᴏᴄᴇssɪɴɢ"):
    frames = ["⚙️", "🔄", "⏳", "⌛"]
    
    for i in range(0, 101, 5):
        bar_filled = "█" * (i // 5)
        bar_empty = "░" * (20 - (i // 5))
        frame = frames[i % len(frames)]

        await message.edit_text(f"""
╔══════════════════════════╗
   {frame} {title.upper()}
╠══════════════════════════╣
[{bar_filled}{bar_empty}] {i}%
╚══════════════════════════╝
""")
        await asyncio.sleep(0.15)
        
async def detect_language(text: str):
    try:
        detection = await translator.detect(text)
        lang_code = detection.lang
        lang_name = LANGUAGES.get(lang_code, "Unknown").title()
        return lang_code, lang_name

    except Exception as e:
        print("Language detection error:", e)
        return "unknown", "Unknown"
        
async def ban_user_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    config = load_config()
    owner_id = config.get("owner_id")
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if user_id != owner_id:
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/ban_user <ᴜsᴇʀ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ> [ᴄᴏᴜɴᴛ]`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/ban_user @username 50`\n"
            "ᴄᴏᴜɴᴛ ʀᴀɴɢᴇ: 10–200 (ᴅᴇғᴀᴜʟᴛ 50)",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    target = context.args[0]
    count = int(context.args[1]) if len(context.args) > 1 else 50
    count = max(10, min(200, count))

    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 👨‍💻 ʙᴀɴ ᴜsᴇʀ ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

👤 *ᴛᴀʀɢᴇᴛ:* `{target}`
🔢 *ᴄᴏᴜɴᴛ:* {count}
🛠️ *ᴍᴏᴅᴇ:* ᴀᴘᴘ ᴏɴʟʏ (ᴜsᴇʀ ʀᴇᴘᴏʀᴛs)
🧩 *ᴍᴏᴅᴜʟᴇs:* {len(proxy_manager.get_all_accounts())} ᴀᴄᴄᴏᴜɴᴛs
🌐 *ɴᴇᴛᴡᴏʀᴋ:* `{proxy_stats['available']} ᴀᴄᴛɪᴠᴇ`
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* 30–90 sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 sᴇᴄᴜʀᴇ ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ʀᴇᴘᴏʀᴛs...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        result = await ban_user(target, count)
        sent = result.get('sent', 0)

        results_message = f"""
✅ *ʙᴀɴ ᴜsᴇʀ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

👤 *ᴛᴀʀɢᴇᴛ:* `{target}`
👤 *ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ:* {sender}

📊 *ʀᴇᴘᴏʀᴛ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
📱 *ᴀᴘᴘ ʀᴇᴘᴏʀᴛs sᴇɴᴛ:* {sent}
━━━━━━━━━━━━━━━━━━━━━━

🎯 *sᴛᴀᴛᴜs:* ᴛᴀʀɢᴇᴛ ʀᴇᴘᴏʀᴛᴇᴅ
⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs ɪɴ 15–30 ᴍɪɴᴜᴛᴇs.*
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ʙᴀɴ ᴜsᴇʀ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


async def ban_group_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    config = load_config()
    owner_id = config.get("owner_id")
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if user_id != owner_id:
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/ban_group <ɢʀᴏᴜᴘ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ> [ᴄᴏᴜɴᴛ]`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/ban_group @groupusername 50`\n"
            "ᴄᴏᴜɴᴛ ʀᴀɴɢᴇ: 10–200 (ᴅᴇғᴀᴜʟᴛ 50)",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    target = context.args[0]
    count = int(context.args[1]) if len(context.args) > 1 else 50
    count = max(10, min(200, count))

    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 👥 ʙᴀɴ ɢʀᴏᴜᴘ ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

👥 *ᴛᴀʀɢᴇᴛ:* `{target}`
🔢 *ᴄᴏᴜɴᴛ:* {count}
🛠️ *ᴍᴏᴅᴇ:* ᴀᴘᴘ ᴏɴʟʏ (ɢʀᴏᴜᴘ ʀᴇᴘᴏʀᴛs)
🧩 *ᴍᴏᴅᴜʟᴇs:* {len(proxy_manager.get_all_accounts())} ᴀᴄᴄᴏᴜɴᴛs
🌐 *ɴᴇᴛᴡᴏʀᴋ:* `{proxy_stats['available']} ᴀᴄᴛɪᴠᴇ`
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* 30–90 sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 sᴇᴄᴜʀᴇ ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ʀᴇᴘᴏʀᴛs...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        result = await ban_group(target, count)
        sent = result.get('sent', 0)

        results_message = f"""
✅ *ʙᴀɴ ɢʀᴏᴜᴘ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

👥 *ᴛᴀʀɢᴇᴛ:* `{target}`
👤 *ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ:* {sender}

📊 *ʀᴇᴘᴏʀᴛ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
📱 *ᴀᴘᴘ ʀᴇᴘᴏʀᴛs sᴇɴᴛ:* {sent}
━━━━━━━━━━━━━━━━━━━━━━

🎯 *sᴛᴀᴛᴜs:* ᴛᴀʀɢᴇᴛ ʀᴇᴘᴏʀᴛᴇᴅ
⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs ɪɴ 15–30 ᴍɪɴᴜᴛᴇs.*
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ʙᴀɴ ɢʀᴏᴜᴘ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


async def ban_channel_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    config = load_config()
    owner_id = config.get("owner_id")
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if user_id != owner_id:
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/ban_channel <ᴄʜᴀɴɴᴇʟ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ> [ᴄᴏᴜɴᴛ]`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/ban_channel @channelusername 50`\n"
            "ᴄᴏᴜɴᴛ ʀᴀɴɢᴇ: 10–200 (ᴅᴇғᴀᴜʟᴛ 50)",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    target = context.args[0]
    count = int(context.args[1]) if len(context.args) > 1 else 50
    count = max(10, min(200, count))

    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 📢 ʙᴀɴ ᴄʜᴀɴɴᴇʟ ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

📢 *ᴛᴀʀɢᴇᴛ:* `{target}`
🔢 *ᴄᴏᴜɴᴛ:* {count}
🛠️ *ᴍᴏᴅᴇ:* ᴀᴘᴘ ᴏɴʟʏ (ᴄʜᴀɴɴᴇʟ ʀᴇᴘᴏʀᴛs)
🧩 *ᴍᴏᴅᴜʟᴇs:* {len(proxy_manager.get_all_accounts())} ᴀᴄᴄᴏᴜɴᴛs
🌐 *ɴᴇᴛᴡᴏʀᴋ:* `{proxy_stats['available']} ᴀᴄᴛɪᴠᴇ`
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* 30–90 sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 sᴇᴄᴜʀᴇ ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ʀᴇᴘᴏʀᴛs...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        result = await ban_channel(target, count)
        sent = result.get('sent', 0)

        results_message = f"""
✅ *ʙᴀɴ ᴄʜᴀɴɴᴇʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

📢 *ᴛᴀʀɢᴇᴛ:* `{target}`
👤 *ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ:* {sender}

📊 *ʀᴇᴘᴏʀᴛ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
📱 *ᴀᴘᴘ ʀᴇᴘᴏʀᴛs sᴇɴᴛ:* {sent}
━━━━━━━━━━━━━━━━━━━━━━

🎯 *sᴛᴀᴛᴜs:* ᴛᴀʀɢᴇᴛ ʀᴇᴘᴏʀᴛᴇᴅ
⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs ɪɴ 15–30 ᴍɪɴᴜᴛᴇs.*
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ʙᴀɴ ᴄʜᴀɴɴᴇʟ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


async def max_ban_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    config = load_config()
    owner_id = config.get("owner_id")
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if user_id != owner_id:
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/max_ban <ᴛᴀʀɢᴇᴛ> [ᴄᴏᴜɴᴛ]`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/max_ban @username 50`\n"
            "ᴄᴏᴜɴᴛ ʀᴀɴɢᴇ: 10–200 (ᴅᴇғᴀᴜʟᴛ 50)",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    target = context.args[0]
    count = int(context.args[1]) if len(context.args) > 1 else 50
    count = max(10, min(200, count))

    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 💣 ᴍᴀx ʙᴀɴ ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

🎯 *ᴛᴀʀɢᴇᴛ:* `{target}`
🔢 *ᴄᴏᴜɴᴛ:* {count}
🛠️ *ᴍᴏᴅᴇ:* ᴀᴘᴘ + ᴇᴍᴀɪʟ + ᴡᴇʙ (ᴍᴀx ғᴏʀᴄᴇ)
🧩 *ᴍᴏᴅᴜʟᴇs:* {len(proxy_manager.get_all_accounts())} ᴀᴄᴄᴏᴜɴᴛs + sᴍᴛᴘ
🌐 *ɴᴇᴛᴡᴏʀᴋ:* `{proxy_stats['available']} ᴀᴄᴛɪᴠᴇ`
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* 60–120 sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 sᴇᴄᴜʀᴇ ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴀʟʟ ᴍᴇᴛʜᴏᴅs...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        result = await max_ban(target, count)
        app_sent = result['app'].get('sent', 0)
        email_sent = len(result['email'].get('sent', []))
        web_success = result.get('web', False)

        results_message = f"""
✅ *ᴍᴀx ʙᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

🎯 *ᴛᴀʀɢᴇᴛ:* `{target}`
👤 *ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ:* {sender}

📊 *ʀᴇᴘᴏʀᴛ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
📱 *ᴀᴘᴘ ʀᴇᴘᴏʀᴛs sᴇɴᴛ:* {app_sent}
📧 *ᴇᴍᴀɪʟ ʀᴇᴘᴏʀᴛs sᴇɴᴛ:* {email_sent}
🌐 *ᴡᴇʙ ʀᴇᴘᴏʀᴛ:* {'✅' if web_success else '❌'}
━━━━━━━━━━━━━━━━━━━━━━

🎯 *sᴛᴀᴛᴜs:* ᴛᴀʀɢᴇᴛ ʜɪᴛ ᴡɪᴛʜ ᴍᴀx ғᴏʀᴄᴇ
⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs ɪɴ 15–30 ᴍɪɴᴜᴛᴇs.*
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ᴍᴀx ʙᴀɴ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def unfrozen_user_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    config = load_config()
    owner_id = config.get("owner_id")
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if user_id != owner_id:
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/unfrozen_user <ᴜsᴇʀ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ>`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/unfrozen_user @username`\n"
            "ᴀʟɪᴀs: `/unban_user`",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    target = context.args[0]

    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 💦 ᴜɴꜰʀᴏᴢᴇɴ ᴜꜱᴇʀ ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

👤 *ᴛᴀʀɢᴇᴛ:* `{target}`
🛠️ *ᴍᴏᴅᴇ:* ᴇᴍᴀɪʟ + @SpamBot ᴀᴘᴘᴇᴀʟs
🧩 *ᴍᴏᴅᴜʟᴇs:* {len(proxy_manager.get_all_accounts())} ᴀᴄᴄᴏᴜɴᴛs + sᴍᴛᴘ
🌐 *ɴᴇᴛᴡᴏʀᴋ:* `{proxy_stats['available']} ᴀᴄᴛɪᴠᴇ`
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* 30–60 sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 sᴇᴄᴜʀᴇ ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* sᴇɴᴅɪɴɢ ᴀᴘᴘᴇᴀʟs...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        result = await unfrozen_user(target)
        email_sent = len(result['email']['sent'])
        spambot_sent = len(result['spambot']['appeals'])

        results_message = f"""
✅ *ᴜɴꜰʀᴏᴢᴇɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

👤 *ᴛᴀʀɢᴇᴛ:* `{target}`
👤 *ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:* {sender}

📊 *ᴀᴘᴘᴇᴀʟ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
📧 *ᴇᴍᴀɪʟs sᴇɴᴛ:* {email_sent}
🤖 *@SpamBot ᴀᴘᴘᴇᴀʟs:* {spambot_sent}
━━━━━━━━━━━━━━━━━━━━━━

🎯 *sᴛᴀᴛᴜs:* ᴀᴘᴘᴇᴀʟs sᴜʙᴍɪᴛᴛᴇᴅ
⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs ɪɴ 24–48 ʜᴏᴜʀs.*
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ᴜɴꜰʀᴏᴢᴇɴ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


async def unban_user_command(update: Update, context: CallbackContext):
    await unfrozen_user_command(update, context)

async def unban_group_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    config = load_config()
    owner_id = config.get("owner_id")
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if user_id != owner_id:
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/unban_group <ɢʀᴏᴜᴘ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ>`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/unban_group @groupusername`",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    target = context.args[0]
    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 🪽 ᴜɴʙᴀɴ ɢʀᴏᴜᴘ ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

👥 *ᴛᴀʀɢᴇᴛ:* `{target}`
🛠️ *ᴍᴏᴅᴇ:* ᴇᴍᴀɪʟ ᴀᴘᴘᴇᴀʟs (ɢʀᴏᴜᴘ)
🧩 *ᴍᴏᴅᴜʟᴇs:* {len(proxy_manager.get_all_accounts())} sᴍᴛᴘ ᴀᴄᴄᴏᴜɴᴛs
🌐 *ɴᴇᴛᴡᴏʀᴋ:* `{proxy_stats['available']} ᴀᴄᴛɪᴠᴇ`
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* 20–40 sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 sᴇᴄᴜʀᴇ ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* sᴇɴᴅɪɴɢ ᴀᴘᴘᴇᴀʟs...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        result = await unban_group(target)
        email_sent = len(result['email']['sent'])

        results_message = f"""
✅ *ᴜɴʙᴀɴ ɢʀᴏᴜᴘ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

👥 *ᴛᴀʀɢᴇᴛ:* `{target}`
👤 *ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:* {sender}

📊 *ᴀᴘᴘᴇᴀʟ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
📧 *ᴇᴍᴀɪʟs sᴇɴᴛ:* {email_sent}
━━━━━━━━━━━━━━━━━━━━━━

🎯 *sᴛᴀᴛᴜs:* ᴀᴘᴘᴇᴀʟs sᴜʙᴍɪᴛᴛᴇᴅ
⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs ɪɴ 24–48 ʜᴏᴜʀs.*
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ᴜɴʙᴀɴ ɢʀᴏᴜᴘ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


async def unban_channel_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    config = load_config()
    owner_id = config.get("owner_id")
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if user_id != owner_id:
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if not context.args:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/unban_channel <ᴄʜᴀɴɴᴇʟ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ>`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/unban_channel @channelusername`",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    target = context.args[0]
    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 〽️ ᴜɴʙᴀɴ ᴄʜᴀɴɴᴇʟ ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

📢 *ᴛᴀʀɢᴇᴛ:* `{target}`
🛠️ *ᴍᴏᴅᴇ:* ᴇᴍᴀɪʟ ᴀᴘᴘᴇᴀʟs (ᴄʜᴀɴɴᴇʟ)
🧩 *ᴍᴏᴅᴜʟᴇs:* {len(proxy_manager.get_all_accounts())} sᴍᴛᴘ ᴀᴄᴄᴏᴜɴᴛs
🌐 *ɴᴇᴛᴡᴏʀᴋ:* `{proxy_stats['available']} ᴀᴄᴛɪᴠᴇ`
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* 20–40 sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 sᴇᴄᴜʀᴇ ᴍᴇᴛʜᴏᴅs ᴀᴄᴛɪᴠᴇ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ ʀᴏᴜᴛᴇs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* sᴇɴᴅɪɴɢ ᴀᴘᴘᴇᴀʟs...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        result = await unban_channel(target)
        email_sent = len(result['email']['sent'])

        results_message = f"""
✅ *ᴜɴʙᴀɴ ᴄʜᴀɴɴᴇʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

📢 *ᴛᴀʀɢᴇᴛ:* `{target}`
👤 *ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:* {sender}

📊 *ᴀᴘᴘᴇᴀʟ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
📧 *ᴇᴍᴀɪʟs sᴇɴᴛ:* {email_sent}
━━━━━━━━━━━━━━━━━━━━━━

🎯 *sᴛᴀᴛᴜs:* ᴀᴘᴘᴇᴀʟs sᴜʙᴍɪᴛᴛᴇᴅ
⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs ɪɴ 24–48 ʜᴏᴜʀs.*
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ᴜɴʙᴀɴ ᴄʜᴀɴɴᴇʟ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def spam_pair_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    config = load_config()
    owner_id = config.get("owner_id")
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if user_id != owner_id:
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if len(context.args) < 1:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/spam_pair <ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ> [ᴀᴍᴏᴜɴᴛ]`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/spam_pair +𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎 𝟓𝟎`\n"
            "ᴀᴍᴏᴜɴᴛ ʀᴀɴɢᴇ: 𝟏𝟎–𝟓𝟎𝟎 (ᴅᴇғᴀᴜʟᴛ 𝟓𝟎)",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    target = context.args[0]
    amount = int(context.args[1]) if len(context.args) > 1 else 50
    amount = max(10, min(500, amount))

    try:
        parsed = phonenumbers.parse(target, None)
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Invalid phone number")
    except:
        await update.message.reply_text(
            "❌ *ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ*\n\n"
            "ᴘʟᴇᴀsᴇ ᴜsᴇ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ (ᴇ.ɢ., `+𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙`).",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    proxy_stats = proxy_manager.get_proxy_stats()

    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 📱 ᴡʜᴀᴛsᴀᴘᴘ ᴘᴀɪʀ sᴘᴀᴍ ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

📞 *ᴛᴀʀɢᴇᴛ:* `{target}`
🔢 *ᴀᴍᴏᴜɴᴛ:* {amount}
🛠️ *ᴍᴏᴅᴇ:* ʀᴇᴀʟ ᴘᴀɪʀɪɴɢ ᴄᴏᴅᴇ sᴘᴀᴍ
🧩 *ᴘʀᴏxɪᴇs:* {proxy_stats['available']} ᴀᴠᴀɪʟᴀʙʟᴇ (ɴᴏᴛ ᴜsᴇᴅ)
🌐 *ʀᴇǫᴜᴇsᴛs:* ᴀsʏɴᴄ + ᴅᴇʟᴀʏ
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* {amount * 3} sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 ᴜsɪɴɢ ʀᴇᴠᴇʀsᴇ‑ᴇɴɢɪɴᴇᴇʀᴇᴅ ғʟᴏᴡ
│ 🔄 ʀᴏᴛᴀᴛɪɴɢ ᴜsᴇʀ‑ᴀɢᴇɴᴛs
│ 📡 sᴛᴀʙʟᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇsᴛᴀʙʟɪsʜᴇᴅ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* ʀᴇǫᴜᴇsᴛɪɴɢ ᴄᴏᴅᴇs...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        result = await spam_pair(target, amount, proxy_manager)

        results_message = f"""
✅ *ᴘᴀɪʀ sᴘᴀᴍ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

📞 *ᴛᴀʀɢᴇᴛ:* `{target}`
👤 *ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:* {sender}

📊 *ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
✅ *sᴜᴄᴄᴇssғᴜʟ:* {result['success']}
❌ *ғᴀɪʟᴇᴅ:* {result['fail']}
🔢 *ᴛᴏᴛᴀʟ:* {result['requested']}
━━━━━━━━━━━━━━━━━━━━━━

⚠️ *ᴄʜᴇᴄᴋ ᴛᴀʀɢᴇᴛ ᴘʜᴏɴᴇ ғᴏʀ ɪɴᴄᴏᴍɪɴɢ ᴄᴏᴅᴇs.*
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ᴘᴀɪʀ sᴘᴀᴍ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def freeze_otp_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    config = load_config()
    owner_id = config.get("owner_id")
    sender = (
        update.effective_user.first_name
        or update.effective_user.username
        or "User"
    )

    if not await has_joined_all(user_id, context):
        await update.message.reply_text(
            "❌ *ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ*\n\n"
            "ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ.\n"
            "ᴘʀᴇss /start ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ 🌹",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if user_id != owner_id:
        await update.message.reply_text(
            f"""
⛔ ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ

━━━━━━━━━━━━━━━━━━━━━━
👤 ʏᴏᴜʀ ɴᴀᴍᴇ ɪs : {sender}
🚫 sᴛᴀᴛᴜs : ɴᴏ ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ
━━━━━━━━━━━━━━━━━━━━━━

💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴅᴀʏ — `$𝟭𝟬` | `𝟭𝟰ᴋ 🇳🇬`
➮ 𝟮 ᴅᴀʏ — `$𝟮𝟬` | `𝟮𝟴ᴋ 🇳🇬`
➮ 𝟯 ᴅᴀʏ — `$𝟯𝟬` | `𝟰𝟮ᴋ 🇳🇬`
➮ 𝟰 ᴅᴀʏ — `$𝟰𝟬` | `𝟱𝟲ᴋ 🇳🇬`
➮ 𝟱 ᴅᴀʏ — `$𝟱𝟬` | `𝟳𝟬ᴋ 🇳🇬`
➮ 𝟲 ᴅᴀʏ — `$𝟲𝟬` | `𝟴𝟰ᴋ 🇳🇬`
➮ 𝟭 ᴡᴇᴇᴋ — `$𝟳𝟬` | `𝟵𝟴ᴋ 🇳🇬`
➮ 𝟭 ᴍᴏɴᴛʜ — `$𝟭𝟮𝟬` | `𝟭𝟲𝟴ᴋ 🇳🇬`
➮ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴘʀᴇᴍɪᴜᴍ — `$𝟭𝟴𝟬` | `𝟮𝟱𝟮𝗸 🇳🇬`

✨ ᴏᴡɴᴇʀ / ʀᴇsᴇʟʟᴇʀ ᴘʟᴀɴ ᴀᴄᴄᴇss

➮ 𝟭 ᴍᴏɴᴛʜ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟭𝟱𝟬` | `𝟮𝟭𝟬𝗸 🇳🇬`
➮ 𝟭 ʏᴇᴀʀ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟬𝟬` | `𝟮𝟴𝟬𝗸 🇳🇬`
➮ ♾️ ʟɪғᴇᴛɪᴍᴇ ᴏᴡɴᴇʀ ᴀᴄᴄᴇss — `$𝟮𝟱𝟬` | `𝟯𝟱𝟬𝗸 🇳🇬`

🕊️ ʙᴀɴ ʙᴏᴛ ʙᴀsᴇ — `$𝟯𝟬𝟬` | `𝟰𝟮𝟬𝗸 🇳🇬`

ᴄᴏɴᴛᴀᴄᴛ📞 ᴅᴇᴠᴇʟᴏᴘ @DG\\_BAHIRAVA
ᴛᴏ ʙᴜʏ ᴀᴄᴄᴇss. 
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    if len(context.args) < 1:
        await update.message.reply_text(
            "⚙️ *ᴜsᴀɢᴇ:*\n\n`/freeze_otp <ᴛᴇʟᴇɢʀᴀᴍ ɴᴜᴍʙᴇʀ> [ᴀᴍᴏᴜɴᴛ]`\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/freeze_otp +𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎 𝟓𝟎`\n"
            "ᴀᴍᴏᴜɴᴛ ʀᴀɴɢᴇ: 𝟏𝟎–𝟓𝟎𝟎 (ᴅᴇғᴀᴜʟᴛ 𝟓𝟎)",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    target = context.args[0]
    amount = int(context.args[1]) if len(context.args) > 1 else 50
    amount = max(10, min(500, amount))

    try:
        parsed = phonenumbers.parse(target, None)
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Invalid phone number")
    except:
        await update.message.reply_text(
            "❌ *ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ*\n\n"
            "ᴘʟᴇᴀsᴇ ᴜsᴇ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ (ᴇ.ɢ., `+𝟐𝟑𝟒𝒙𝒙𝒙𝒙𝒙`).",
            parse_mode="Markdown",
            reply_markup=get_owner_buttons()
        )
        return

    proxy_stats = proxy_manager.get_proxy_stats()
    
    keyboard = [
        [
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄʜᴀɴɴᴇʟ", url=REQUIRED_CHATS[1][1], style="success", icon_custom_emoji_id="5197304993920616826"),
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}", style="primary", icon_custom_emoji_id="6084393784118872313")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    processing_msg = await update.message.reply_text(
        f"""
╔═━〔 ❄️ ᴏᴛᴘ ғʀᴇᴇᴢᴇ ɪɴɪᴛɪᴀᴛᴇᴅ 〕━═╗

📞 *ᴛᴀʀɢᴇᴛ:* `{target}`
🔢 *ᴀᴍᴏᴜɴᴛ:* {amount}
🛠️ *ᴍᴏᴅᴇ:* ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛs + ᴡᴇʙ ʟᴏɢɪɴ (ʀᴇᴀʟ)
🧩 *ᴀᴄᴄᴏᴜɴᴛs:* {len(proxy_manager.get_all_accounts())} ʟᴏᴀᴅᴇᴅ
🌐 *ᴘʀᴏxɪᴇs:* {proxy_stats['available']} ᴀᴠᴀɪʟᴀʙʟᴇ (ɴᴏᴛ ᴜsᴇᴅ)
⏱️ *ᴇsᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ:* {amount * 4} sᴇᴄ

╭─〔 ⚙️ sʏsᴛᴇᴍ ɪɴғᴏ 〕─╮
│ 🔐 ᴀᴘɪ ᴄᴀʟʟs ғʀᴏᴍ ᴇᴀᴄʜ ᴀᴄᴄᴏᴜɴᴛ
│ 🔄 sᴇʟᴇɴɪᴜᴍ ᴡᴇʙ ᴀᴜᴛᴏᴍᴀᴛɪᴏɴ
│ 📡 ʙᴏᴛʜ ʀᴜɴɴɪɴɢ ᴄᴏɴᴄᴜʀʀᴇɴᴛʟʏ
╰────────────────────╯

⏳ *sᴛᴀᴛᴜs:* ʟᴀᴜɴᴄʜɪɴɢ ᴀᴛᴛᴀᴄᴋ...
╚══════════════════════╝
""",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    try:
        result = await freeze_otp(target, amount)

        results_message = f"""
✅ *ᴏᴛᴘ ғʀᴇᴇᴢᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ*

📞 *ᴛᴀʀɢᴇᴛ:* `{target}`
👤 *ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:* {sender}

📊 *ᴛᴏᴛᴀʟ ʀᴇsᴜʟᴛs*
━━━━━━━━━━━━━━━━━━━━━━
✅ *sᴜᴄᴄᴇss:* {result['success']}
❌ *ғᴀɪʟ:* {result['fail']}
🔢 *ʀᴇǫᴜᴇsᴛᴇᴅ:* {result['requested']}
━━━━━━━━━━━━━━━━━━━━━━
📈 *ʙʀᴇᴀᴋᴅᴏᴡɴ*
🤖 ᴀᴘɪ: ✅ {result['method_breakdown']['api']['success']}  ❌ {result['method_breakdown']['api']['fail']}
🌐 ᴡᴇʙ: ✅ {result['method_breakdown']['web']['success']}  ❌ {result['method_breakdown']['web']['fail']}
━━━━━━━━━━━━━━━━━━━━━━

⚠️ *ᴛʜᴇ ᴛᴀʀɢᴇᴛ ᴡɪʟʟ ʀᴇᴄᴇɪᴠᴇ {result['success']} ᴏᴛᴘs.*
━━━━━━━━━━━━━━━━━━━━━━
"""

        await processing_msg.edit_text(
            results_message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    except Exception as e:
        await processing_msg.edit_text(
            f"❌ *ᴏᴛᴘ ғʀᴇᴇᴢᴇ ғᴀɪʟᴇᴅ*\n\n`{str(e)}`\n\n"
            "⚠️ ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not configured. "
            "Add it to the deployment environment before starting the bot."
        )

    config = load_config()
    save_db()
    load_dotenv()

    application = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .build()
    )

    application.bot_data["config"] = config
    application.add_handler(CommandHandler("start", start_command))
    
    application.add_handler(CommandHandler("addowner", add_owner_command))
    
    application.add_handler(CommandHandler("delowner", del_owner_command))
    
    application.add_handler(CommandHandler("addprem", add_premium_command))
    
    application.add_handler(CommandHandler("delprem", del_premium_command))
    
    application.add_handler(CommandHandler("ban_perm", ban_perm_command))
    
    application.add_handler(CommandHandler("ban_temp", ban_temp_command))
    
    application.add_handler(CommandHandler("mass_report", mass_report_command))
    
    application.add_handler(CommandHandler("unban", unban_command))
    
    application.add_handler(CommandHandler("max_unban", max_unban_command))
    
    application.add_handler(CommandHandler("temp", unban_temp_command))
    
    application.add_handler(CommandHandler("listowner", listowner_command))
    
    application.add_handler(CommandHandler("listpremium", listpremium_command))
    
    application.add_handler(CommandHandler("pay_now", pay_now_command))
    
    application.add_handler(CommandHandler("termux_tools", termux_tools_command))
    
    application.add_handler(CommandHandler("ban_gpt", ban_gpt))
    
    application.add_handler(CommandHandler("translate", translate_command))
    
    application.add_handler(CommandHandler("ban_user", ban_user_command))
    
    application.add_handler(CommandHandler("ban_group", ban_group_command))
    
    application.add_handler(CommandHandler("ban_channel", ban_channel_command))
    
    application.add_handler(CommandHandler("max_ban", max_ban_command))
    
    application.add_handler(CommandHandler("freeze_otp", freeze_otp_command))
    
    application.add_handler(CommandHandler("spam_pair", spam_pair_command))
    
    application.add_handler(CommandHandler("unfrozen_user", unfrozen_user_command))
    
    application.add_handler(CommandHandler("unban_user", unban_user_command))
    
    application.add_handler(CommandHandler("unban_group", unban_group_command))
    
    application.add_handler(CommandHandler("unban_channel", unban_channel_command))
    
    application.add_handler(CommandHandler("ban_checker", checker_command))
    
    application.add_handler(CommandHandler("setapi", set_api_url_command))
    
    application.add_handler(CallbackQueryHandler(plan_select_callback, pattern="^plan_"))
    
    application.add_handler(CallbackQueryHandler(admin_decision_callback, pattern="^(approve|reject):"))
    
    application.add_handler(CallbackQueryHandler(copy_install_callback, pattern="^copy:"))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.add_handler(MessageHandler(filters.PHOTO, screenshot_handler))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.add_error_handler(error_handler)
    
    application.run_polling()

LOGO = r"""
██████╗  █████╗   ███╗   ██╗
██╔══██╗██╔══██╗████╗   ██║
██████╔╝███████║██╔██╗  ██║
██╔══██╗██╔══██║██║╚██╗██║
██████╔╝██║  ██║██║ ╚████║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝

██████╗  ██████╗ ████████╗
██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║   ██║   
██╔══██╗██║   ██║   ██║   
██████╔╝╚██████╔╝   ██║   
╚═════╝  ╚═════╝    ╚═╝   
"""

if __name__ == "__main__":

    if DB_FILE.exists():
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                db = json.load(f)
        except Exception as e:
            print(f"⚠️ ғᴀɪʟᴇᴅ ᴛᴏ ʟᴏᴀᴅ ᴅᴀᴛᴀʙᴀsᴇ: {e}")

    if "owners" not in db:
        db["owners"] = []
    if "premium" not in db:
        db["premium"] = []

    if OWNER_ID not in db["owners"]:
        db["owners"].append(OWNER_ID)
        
    if SMTP_FILE.exists():
        try:
            with open(SMTP_FILE, 'r', encoding='utf-8') as f:
                SMTP_DATA = json.load(f)
            print("✅ sᴍᴛᴘ ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴ ʟᴏᴀᴅᴇᴅ")
        except Exception as e:
            print(f"❌ ᴇʀʀᴏʀ ʟᴏᴀᴅɪɴɢ sᴍᴛᴘ ᴄᴏɴғɪɢ: {e}")

    proxy_manager = ProxyManager()
    whatsapp_reporter = WhatsAppReporter()
    whatsapp_unban = WhatsAppUnbanAppeal()
    start_time = time.time()
    sys.excepthook = handle_uncaught_exception

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.set_exception_handler(handle_unhandled_rejection)
    clear()
    print(gradient(LOGO))
    print(gradient("╔══════════════════════╗"))
    print(gradient("║          🤖 ʙᴀʜɪʀᴀᴠᴀ sʏsᴛᴇᴍ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ             ║"))
    print(gradient("╠══════════════════════╣"))
    print(gradient("╠══════════════════════╣"))
    print(gradient("║ ✅ sᴛᴀᴛᴜs        : ᴏɴʟɪɴᴇ"))
    print(gradient("║ 🧠 ᴍᴀx ᴘᴏᴡᴇʀ⚡💪"))
    print(gradient("║ 🔄 ᴘʀᴏxʏ ᴍᴏᴅᴇ    : ʀᴏᴛᴀᴛɪᴏɴ ᴀᴄᴛɪᴠᴇ"))
    print(gradient("║ 🔐 sᴇᴄᴜʀɪᴛʏ     : ᴍᴀxɪᴍᴜᴍ"))
    print(gradient("║ ⚡ sᴘᴇᴇᴅ ᴍᴏᴅᴇ   : ᴜʟᴛʀᴀ"))
    print(gradient("║ 👑 ᴏᴡɴᴇʀ        : ʙᴀʜɪʀᴀᴠᴀ"))
    print(gradient("╠══════════════════════╝"))
    print("\n" + gradient("🚀 ᴀʟʟ sʏsᴛᴇᴍs ᴏᴘᴇʀᴀᴛɪᴏɴᴀʟ — ʙᴏᴛ ɪs ɴᴏᴡ ʟɪᴠᴇ 🚀\n"))

    main()