
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN .env faylda topilmadi!")

print("✅ Config yuklandi: BOT_TOKEN va ADMIN_ID")
