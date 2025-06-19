from aiogram import types, Dispatcher
from buttons import report_menu
from database import get_records_by_period, get_user_settings

# 📊 Hisobot menyusi
async def show_report_menu(message: types.Message):
    await message.answer("📊 Qaysi davr uchun hisobotni ko‘rmoqchisiz?", reply_markup=report_menu())

# 🗓 Har bir davr bo‘yicha handlerlar
async def today_report(message: types.Message):
    await send_report(message, "Bugun")

async def week_report(message: types.Message):
    await send_report(message, "Hafta")

async def month_report(message: types.Message):
    await send_report(message, "Oy")

async def all_time_report(message: types.Message):
    await send_report(message, "Ummumiy")

# 📥 Umumiy hisobot funksiyasi
async def send_report(message: types.Message, period: str):
    user_id = message.from_user.id
    records = get_records_by_period(user_id, period)
    settings = get_user_settings(user_id)

    if not records and not settings:
        await message.answer(f"🔍 {period} uchun hech qanday yozuv topilmadi.")
        return

    income = 0
    expense = 0
    income_lines = []
    expense_lines = []

    for timestamp, record_type, amount, note in records:
        record_type = record_type.lower().strip()
        line = f"{amount:.2f} so'm - {note} ({timestamp[:16]})"
        if record_type == "💰daromad" or record_type == "daromad":
            income += amount
            income_lines.append("✅ " + line)  # ✅ Daromad emoji
        elif record_type == "💸xarajat" or record_type == "xarajat":
            expense += amount
            expense_lines.append("❌ " + line)  # ❌ Xarajat qizil emoji

    # 🧮 Sozlamalardan majburiy daromad/xarajat qo‘shish
    monthly_income = settings.get("monthly_income", 0)
    monthly_expense = settings.get("monthly_expense", 0)

    if monthly_income:
        income += monthly_income
        income_lines.append(f"✅ <i>Majburiy daromad (sozlamadan): {monthly_income:.2f} so'm</i>")
    if monthly_expense:
        expense += monthly_expense
        expense_lines.append(f"❌ <i>Majburiy xarajat (sozlamadan): {monthly_expense:.2f} so'm</i>")

    report_text = f"📊 <b>{period} uchun hisobot</b>:\n\n"

    if income_lines:
        report_text += "✅ <b>Daromadlar:</b>\n" + "\n".join(income_lines) + "\n\n"
    if expense_lines:
        report_text += "❌ <b>Xarajatlar:</b>\n" + "\n".join(expense_lines) + "\n\n"

    report_text += (
        f"🟢 <b>Umumiy daromad:</b> {income:.2f} so'm\n"
        f"🔴 <b>Umumiy xarajat:</b> {expense:.2f} so'm\n"
        f"💵 <b>Qolgan balans:</b> {income - expense:.2f} so'm"
    )

    await message.answer(report_text, parse_mode="HTML")

# 🔄 Handlerlarni ro‘yxatdan o‘tkazish
def register_report_handlers(dp: Dispatcher):
    dp.register_message_handler(show_report_menu, lambda msg: msg.text == "📊 Hisobot")
    dp.register_message_handler(today_report, text="Bugun")
    dp.register_message_handler(week_report, text="Hafta")
    dp.register_message_handler(month_report, text="Oy")
    dp.register_message_handler(all_time_report, text="Umumiy")  # ✅ TUZATILGAN QATOR