import sqlite3
from app.models.set_up import get_connection

def create_user(fullname, email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)',
            (fullname, email, password))
        new_user_id = cursor.lastrowid
        cursor.execute(
            'INSERT INTO students (user_id, fullname) VALUES (?, ?)',
            (new_user_id, fullname))
        conn.commit()
        conn.close()
        return new_user_id          # trả về id thay vì False
    except sqlite3.IntegrityError:
        return None                  # trả về None thay vì True (báo email trùng)

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    if row:
        return {
            "id": row[0],
            "fullname": row[1],
            "email": row[2],
            "password": row[3]
        }
    return None