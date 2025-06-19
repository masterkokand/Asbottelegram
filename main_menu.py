from aiogram import types, Dispatcher
from buttons import add_menu, report_menu, settings_menu

async def handle_add(message: types.Message):
    await message.answer("➕ Iltimos, Daromad yoki Xarajatni tanlang:", reply_markup=add_menu())

async def handle_report(message: types.Message):
    await message.answer("📊 Qaysi davr uchun hisobot kerak?", reply_markup=report_menu())

async def handle_settings(message: types.Message):
    await message.answer("⚙️ Sozlamalardan birini tanlang:", reply_markup=settings_menu())

def register_main_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_add, lambda msg: msg.text == "➕ Qo‘shish")
    dp.register_message_handler(handle_report, lambda msg: msg.text == "📊 Hisobot")
    dp.register_message_handler(handle_settings, lambda msg: msg.text == "⚙️ Sozlamalar")
    
   