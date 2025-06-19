from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN

# 🟢 Handler importlari
from handlers.start import register_start_handler
from handlers.add_record import register_add_handlers
from handlers.report import register_report_handlers
from handlers.settings import register_settings_handlers  

# ✅ Sozlamalar handleri qo‘shildi

# 🔧 Bot va dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# 🔗 Handlerlarni ro‘yxatdan o‘tkazish
register_start_handler(dp)
register_add_handlers(dp)
register_report_handlers(dp)
register_settings_handlers(dp)  # ✅ Sozlamalar handleri ro‘yxatdan o‘tkazildi

# 🚀 Botni ishga tushurish
if __name__ == "__main__":
    print("✅ Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)