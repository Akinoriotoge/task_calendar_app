from database import get_connection
import sqlite3

def add_task(title, description, start, end):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO tasks (title, description, start_datetime, end_datetime)
    VALUES (?, ?, ?, ?)
    """, (title, description, start, end))

    conn.commit()
    conn.close()

def get_tasks():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()

    conn.close()
    return rows

def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    conn.close()

def get_task_by_id(task_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()

    conn.close()
    return row
