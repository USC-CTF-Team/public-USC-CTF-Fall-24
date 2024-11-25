import sqlite3
from werkzeug.security import generate_password_hash

FLAG = "CYBORG{Wh4t_h4pp3n3d_t0_my_p4ssw0rd!}"

def setup(db_id):
    conn = sqlite3.connect(str(db_id) + ".db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS flags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flag TEXT NOT NULL
                    )''')

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ('admin', generate_password_hash('Uncr4ck4bl3P4ss!!!')))
        cursor.execute("INSERT INTO flags (flag) VALUES (?)", (FLAG,))
        conn.commit()
        print("Database setup complete.")
    except sqlite3.IntegrityError:
        print("Admin user or flag already exists.")
    
    conn.close()

if __name__ == '__main__':
    setup()
