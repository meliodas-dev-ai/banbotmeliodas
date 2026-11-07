# Bahirava Bot

## Fixed Telegram errors

The two `BadRequest: Can't parse entities` failures were caused by:

- user names being inserted into Markdown without escaping;
- a support username containing an unescaped underscore in Markdown;
- malformed Telegram HTML: `<bᴄʟᴇᴀʀ ...</b>`;
- raw `&` characters inside HTML-formatted messages;
- a plain-text photo caption not explicitly disabling entity parsing.

The affected messages now escape user/API values, use valid Telegram HTML, and
disable parsing for the plain-text menu caption.

## Configuration

Copy `.env.example` to `.env` or add the same values to the hosting provider's
environment. At minimum, set `TELEGRAM_BOT_TOKEN` before starting the bot.
Credentials are intentionally not stored in `config.json`, `accounts.json`, or
the SMTP data files.

The original archive contained live-looking Telegram, GitHub, Hugging Face,
Groq, and SMTP credentials. Rotate those credentials before reusing them.