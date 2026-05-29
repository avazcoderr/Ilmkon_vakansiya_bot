import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_GROUP_ID: int = int(os.getenv("ADMIN_GROUP_ID", "0"))
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///ilmkon.db")
REMINDER_HOURS: int = int(os.getenv("REMINDER_HOURS", "24"))

_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: list[int] = [int(x.strip()) for x in _raw.split(",") if x.strip().isdigit()]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylida ko'rsatilmagan!")
