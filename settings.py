from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from buttons import settings_menu, main_menu, cancel_menu
from states import SettingsStates
from database import (
    save_user_settings,
    delete_all_user_data,
    update_user_name
)

# ⚙️ Sozlamalar menyusi
async def settings_menu_handler(message: types.Message):
    await message.answer("⚙️ Sozlamalarni tanlang:", reply_markup=settings_menu())

# 🧾 Oylik daromad
async def ask_income(message: types.Message):
    await message.answer("🧾 Oylik daromadni so‘mda kiriting:", reply_markup=cancel_menu())
    await SettingsStates.waiting_for_income.set()

async def save_income(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("❌ Amaliyot bekor qilindi.", reply_markup=settings_menu())
        await state.finish()
        return
    try:
        income = float(message.text)
        save_user_settings(message.from_user.id, income=income)
        await message.answer(f"✅ Oylik daromad saqlandi: {income:.2f} so'm", reply_markup=settings_menu())
        await state.finish()
    except ValueError:
        await message.answer("❌ Noto‘g‘ri format. Son kiriting.")

# 💸 Majburiy xarajat
async def ask_expense(message: types.Message):
    await message.answer("💸 Majburiy xarajatni so‘mda kiriting:", reply_markup=cancel_menu())
    await SettingsStates.waiting_for_expense.set()

async def save_expense(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("❌ Amaliyot bekor qilindi.", reply_markup=settings_menu())
        await state.finish()
        return
    try:
        expense = float(message.text)
        save_user_settings(message.from_user.id, expense=expense)
        await message.answer(f"✅ Majburiy xarajat saqlandi: {expense:.2f} so'm", reply_markup=settings_menu())
        await state.finish()
    except ValueError:
        await message.answer("❌ Noto‘g‘ri format. Son kiriting.")

# 📛 Ismni o‘zgartirish
async def ask_name_change(message: types.Message):
    await message.answer("✍️ Yangi ismingizni kiriting:", reply_markup=cancel_menu())
    await SettingsStates.waiting_for_name.set()

async def save_new_name(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("❌ Amaliyot bekor qilindi.", reply_markup=settings_menu())
        await state.finish()
        return
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("❗️ Ism juda qisqa. Qayta kiriting.")
        return
    update_user_name(message.from_user.id, name)
    await message.answer(f"✅ Ismingiz yangilandi: {name}", reply_markup=settings_menu())
    await state.finish()

# ♻️ Barcha ma'lumotlarni o‘chirish
async def confirm_reset(message: types.Message):
    await message.answer("⚠️ Barcha ma'lumotlaringiz o‘chiriladi. Tasdiqlaysizmi? (Ha / Yo‘q)", reply_markup=cancel_menu())
    await SettingsStates.confirm_reset.set()

async def process_reset_confirmation(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("❌ Amaliyot bekor qilindi.", reply_markup=settings_menu())
        await state.finish()
        return
    if message.text.lower() in ["ha", "xa", "yes"]:
        delete_all_user_data(message.from_user.id)
        await message.answer("♻️ Ma'lumotlaringiz tozalandi. Endi yangidan boshlashingiz mumkin.", reply_markup=main_menu())
        await state.finish()
    else:
        await message.answer("❌ Bekor qilindi.", reply_markup=settings_menu())
        await state.finish()

# 🔙 Orqaga
async def back_to_menu(message: types.Message, state: FSMContext):
    await message.answer("🔙 Sozlamalar menyusiga qaytdingiz.", reply_markup=settings_menu())
    await state.finish()

# ✅ Ro‘yxatdan o‘tkazish
def register_settings_handlers(dp: Dispatcher):
    dp.register_message_handler(settings_menu_handler, lambda msg: msg.text == "⚙️ Sozlamalar")
    dp.register_message_handler(ask_income, lambda msg: msg.text == "🧾 Oylik daromad")
    dp.register_message_handler(save_income, state=SettingsStates.waiting_for_income)

    dp.register_message_handler(ask_expense, lambda msg: msg.text == "💸 Majburiy xarajatlar")
    dp.register_message_handler(save_expense, state=SettingsStates.waiting_for_expense)

    dp.register_message_handler(ask_name_change, lambda msg: msg.text == "📛 Ismni o‘zgartirish")
    dp.register_message_handler(save_new_name, state=SettingsStates.waiting_for_name)

    dp.register_message_handler(confirm_reset, lambda msg: msg.text == "♻️ Ma'lumotlarni tozalash")
    dp.register_message_handler(process_reset_confirmation, state=SettingsStates.confirm_reset)

    dp.register_message_handler(back_to_menu, text="🔙 Orqaga", state="*")
    dp.register_message_handler(back_to_menu, text="❌ Bekor qilish", state="*")