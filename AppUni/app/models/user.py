import sqlite3

def init_db():
    conn = sqlite3.connect('app/models/database.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS database (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 fullname TEXT,
                 email TEXT UNIQUE,
                 password TEXT
                 )""")
    conn.commit()
    conn.close()

def create_user(fullname, email, password):
    try:
        conn = sqlite3.connect('app/models/database.db')
        conn.execute('INSERT INTO database (fullname, email, password) VALUES (?, ?, ?)', (fullname, email, password))
        conn.commit()
        conn.close()
        return False
    except sqlite3.IntegrityError:
        return True

def get_user_by_email(email):
    conn = sqlite3.connect('app/models/database.db')
    cursor = conn.execute('SELECT * FROM database WHERE email = ?', (email,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "fullname": row[1],
            "email": row[2],
            "password": row[3]
        }
    return None

def reset():
    conn = sqlite3.connect('app/models/database.db')
    conn.execute('DROP TABLE database')
    conn.close()
    conn.close()
# reset()