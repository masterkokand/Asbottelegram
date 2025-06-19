from aiogram import types, Dispatcher
from buttons import main_menu
from texts import texts  # Agar `texts` yo‘q bo‘lsa, oddiy matn yozing

async def start_handler(message: types.Message):
    await message.answer(
        f"👋 Assalomu alaykum, {message.from_user.full_name}!\nMoliyaviy hisob-kitoblar uchun menyudan foydalaning.",
        reply_markup=main_menu()
    )
def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])