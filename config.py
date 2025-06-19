from dotenv import load_dotenv
import os

# .env fayldan o'zgaruvchilarni yuklaydi
load_dotenv()

# Token va admin ID ni olamiz
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # agar yo'q bo‘lsa 0 bo‘lib ketsin

# Tekshiruv: token bo‘sh bo‘lsa xato chiqarsin
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN .env faylda topilmadi!")

# Ixtiyoriy: Chop etish (debug maqsadida)
print("✅ Config yuklandi: BOT_TOKEN va ADMIN_ID")