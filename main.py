
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers.start import register_start_handler
from handlers.add_record import register_add_handlers
from handlers.report import register_report_handlers
from handlers.settings import register_settings_handlers

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_start_handler(dp)
register_add_handlers(dp)
register_report_handlers(dp)
register_settings_handlers(dp)

if __name__ == "__main__":
    print("✅ Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
