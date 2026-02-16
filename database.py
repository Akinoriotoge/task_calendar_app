import sqlite3
import os

DB_PATH = os.path.join("data", "tasks.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        start_datetime TEXT,
        end_datetime TEXT
    )
    """)

    conn.commit()
    conn.close()
