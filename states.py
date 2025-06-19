from aiogram.dispatcher.filters.state import State, StatesGroup

class SettingsStates(StatesGroup):
    waiting_for_income = State()
    waiting_for_expense = State()
    waiting_for_name = State()       # ✅ Ismni o‘zgartirish uchun holat
    confirm_reset = State()          # ✅ Ma’lumotlarni tozalashni tasdiqlash

class AddRecord(StatesGroup):
    choosing_type = State()
    entering_amount = State()
    entering_note = State()