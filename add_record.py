from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states import AddRecord
from buttons import add_menu, cancel_menu, main_menu
from database import save_record

# ➕ Qo‘shish menyusiga kirish
async def add_start(message: types.Message):
    await message.answer("Daromad yoki Xarajatni tanlang:", reply_markup=add_menu())
    await AddRecord.choosing_type.set()

# 💰 Daromad yoki 💸 Xarajat tanlovi
async def choose_type(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("❌ Amal bekor qilindi.", reply_markup=main_menu())
        return await state.finish()
    if message.text == "🔙 Orqaga":
        return await back_to_main_menu(message, state)

    if message.text not in ["💰Daromad", "💸Xarajat"]:
        return await message.answer("Iltimos, tugmalardan foydalaning.")

    await state.update_data(record_type=message.text)
    await message.answer("Miqdorni kiriting:", reply_markup=cancel_menu())
    await AddRecord.entering_amount.set()

# 💵 Miqdorni kiritish
async def enter_amount(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("❌ Amal bekor qilindi.", reply_markup=add_menu())
        return await AddRecord.choosing_type.set()
    if message.text == "🔙 Orqaga":
        return await back_to_main_menu(message, state)

    try:
        amount = float(message.text)
    except ValueError:
        return await message.answer("❗️ Noto‘g‘ri format. Iltimos, raqam kiriting.")

    await state.update_data(amount=amount)
    await message.answer("Izoh kiriting (ixtiyoriy):", reply_markup=cancel_menu())
    await AddRecord.entering_note.set()

# 📝 Izoh kiritish
async def enter_note(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("❌ Amal bekor qilindi.", reply_markup=add_menu())
        return await AddRecord.choosing_type.set()
    if message.text == "🔙 Orqaga":
        return await back_to_main_menu(message, state)

    note = message.text
    data = await state.get_data()

    save_record(
        user_id=message.from_user.id,
        record_type=data['record_type'],
        amount=data['amount'],
        note=note
    )

    await message.answer("✅ Yozuv saqlandi!", reply_markup=main_menu())
    await state.finish()

# 🔙 Asosiy menyuga qaytarish
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await message.answer("🔙 Asosiy menyuga qaytdingiz.", reply_markup=main_menu())
    await state.finish()

# ✅ Barcha handlerlarni ro‘yxatdan o‘tkazish
def register_add_handlers(dp: Dispatcher):
    dp.register_message_handler(add_start, lambda m: m.text == "➕ Qo‘shish")
    dp.register_message_handler(choose_type, state=AddRecord.choosing_type)
    dp.register_message_handler(enter_amount, state=AddRecord.entering_amount)
    dp.register_message_handler(enter_note, state=AddRecord.entering_note)
    dp.register_message_handler(back_to_main_menu, text="🔙 Orqaga", state="*")