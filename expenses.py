import sqlite3

def add_expense(user_id, amount, category, date, description):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, amount, category, date, description))
    conn.commit()
    conn.close()


def get_expenses(user_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT amount, category, date, description FROM expenses WHERE user_id=?", (user_id,))
    data = c.fetchall()
    conn.close()
    return data