import sqlite3
import os
from datetime import datetime

class RobotMemory:
    """Handles conversation history and persistent state storage in SQLite."""

    def __init__(self, db_path="../database/robot.db"):
        self.db_path = os.path.abspath(db_path)
        self._ensure_db()

    def _ensure_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_input TEXT,
                intent TEXT,
                bot_response TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS robot_memory (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def store_interaction(self, user_input: str, intent: str, bot_response: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversation_history (timestamp, user_input, intent, bot_response)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_input, intent, bot_response))
        conn.commit()
        conn.close()

    def set_memory(self, key: str, value: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO robot_memory (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
        """, (key, value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

    def get_memory(self, key: str, default=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM robot_memory WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else default

    def get_recent_conversations(self, limit=5):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, user_input, bot_response 
            FROM conversation_history 
            ORDER BY id DESC LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows
