import sqlite3
import csv

DB_NAME = "app.db"

def export_notes(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, content, category, created_at FROM notes WHERE user_id=?",
        (user_id,)
    )

    with open("notes_export.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Content", "Category", "Created At"])
        writer.writerows(cursor.fetchall())

    conn.close()

def export_tasks(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, priority, status, due_date FROM tasks WHERE user_id=?",
        (user_id,)
    )

    with open("tasks_export.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Task", "Priority", "Status", "Due Date"])
        writer.writerows(cursor.fetchall())

    conn.close()
