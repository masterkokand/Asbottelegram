from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# 🔘 Asosiy menyu
def main_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("➕ Qo‘shish"),
        KeyboardButton("📊 Hisobot")
    ).add(
        KeyboardButton("⚙️ Sozlamalar")
    )

# ➕ Qo‘shish menyusi
def add_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("💰Daromad"),
        KeyboardButton("💸Xarajat")
    ).add(
        KeyboardButton("🔙 Orqaga")
    )


def report_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Bugun"),
        KeyboardButton("Hafta"),
        KeyboardButton("Oy"),
        KeyboardButton("Umumiy"),
        KeyboardButton("🔙 Orqaga")
    )

# 📊 Hisobot menyusi

# ❌ Bekor qilish menyusi
def cancel_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("❌ Bekor qilish")
    )
    
    # ⚙️ Sozlamalar menyusi
def settings_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("🧾 Oylik daromad"),
        KeyboardButton("💸 Majburiy xarajatlar")
    ).add(
        KeyboardButton("📛 Ismni o‘zgartirish"),
        KeyboardButton("♻️ Ma'lumotlarni tozalash")
    ).add(
        KeyboardButton("🔙 Orqaga")
    )