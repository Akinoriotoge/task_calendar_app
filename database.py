import sqlite3
import os
import sys

def get_connection():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(__file__)

    db_path = os.path.join(base_dir, "tasks.db")
    return sqlite3.connect(db_path)

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
