import sqlite3
from datetime import datetime, timedelta

# ✅ Foydalanuvchining ismini yangilash
def update_user_name(user_id, new_name):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users SET full_name = ? WHERE user_id = ?
    """, (new_name, user_id))

    conn.commit()
    conn.close()


# ✅ Foydalanuvchining barcha ma'lumotlarini o‘chirish
def delete_all_user_data(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # records jadvalidan o‘chirish
    cursor.execute("DELETE FROM records WHERE user_id = ?", (user_id,))
    # settingsdan o‘chirish
    cursor.execute("DELETE FROM user_settings WHERE user_id = ?", (user_id,))
    # foydalanuvchi ismini o‘chirish (xohlovcha)
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()


# ✅ Daromad/xarajat yozuvini bazaga saqlash
def save_record(user_id, record_type, amount, note):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            amount REAL,
            note TEXT,
            timestamp DATETIME DEFAULT (datetime('now', 'localtime'))
        )
    """)

    cursor.execute("""
        INSERT INTO records (user_id, type, amount, note)
        VALUES (?, ?, ?, ?)
    """, (user_id, record_type, amount, note))

    conn.commit()
    conn.close()


# ✅ Davr bo‘yicha yozuvlarni olish (hisobotlar uchun)
def get_records_by_period(user_id, period):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    now = datetime.now()

    if period == "Bugun":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == "Hafta":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == "Oy":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == "Ummumiy":
        start = None
        end = None
    else:
        conn.close()
        return []

    if start and end:
        cursor.execute("""
            SELECT timestamp, type, amount, note FROM records
            WHERE user_id = ? AND timestamp BETWEEN ? AND ?
        """, (user_id, start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S')))
    else:
        cursor.execute("""
            SELECT timestamp, type, amount, note FROM records
            WHERE user_id = ?
        """, (user_id,))

    results = cursor.fetchall()
    conn.close()
    return results


# ✅ Foydalanuvchini ro‘yxatga olish
def register_user(user_id, full_name):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, full_name)
        VALUES (?, ?)
    """, (user_id, full_name))

    conn.commit()
    conn.close()


# ✅ Foydalanuvchining oylik sozlamalarini saqlash
def save_user_settings(user_id, income=None, expense=None):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            monthly_income REAL DEFAULT 0,
            monthly_expense REAL DEFAULT 0
        )
    """)

    if income is not None:
        cursor.execute("""
            INSERT INTO user_settings (user_id, monthly_income)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET monthly_income=excluded.monthly_income
        """, (user_id, income))

    if expense is not None:
        cursor.execute("""
            INSERT INTO user_settings (user_id, monthly_expense)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET monthly_expense=excluded.monthly_expense
        """, (user_id, expense))

    conn.commit()
    conn.close()


# ✅ Sozlamalarni olish (hisobot uchun)
def get_user_settings(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT monthly_income, monthly_expense FROM user_settings
        WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    return {
        "monthly_income": row[0] if row else 0,
        "monthly_expense": row[1] if row else 0
    }