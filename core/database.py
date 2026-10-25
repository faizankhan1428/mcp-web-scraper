import sqlite3
import os
from datetime import datetime

def init_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scrapes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            url TEXT,
            title TEXT,
            file_path TEXT,
            file_type TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_to_database(db_path: str, url: str, title: str, file_path: str, file_type: str):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scrapes (timestamp, url, title, file_path, file_type) VALUES (?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), url, title, file_path, file_type)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

def search_database(db_path: str, keyword: str) -> str:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, url, title, file_path, file_type FROM scrapes WHERE title LIKE ? OR url LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return f"No records found matching '{keyword}'."

        result = f"Found {len(rows)} matching record(s):\n"
        for row in rows:
            result += f"- [{row[0]}] {row[2]} ({row[4]})\n  URL: {row[1]}\n  Path: {row[3]}\n\n"
        return result
    except Exception as e:
        return f"Database search failed: {str(e)}"