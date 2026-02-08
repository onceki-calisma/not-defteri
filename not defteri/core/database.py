# core/database.py
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any

class Database:
    def __init__(self, db_path: str = "data/notes.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    type TEXT NOT NULL,
                    tags TEXT,
                    locked BOOLEAN DEFAULT 0,
                    public BOOLEAN DEFAULT 0,  -- 👈 YENİ SÜTUN
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            conn.commit()

    def save_note(self, note: Dict[str, Any]):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO notes
                (id, title, content, type, tags, locked, public, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                note["id"],
                note["title"],
                note["content"],
                note["type"],
                json.dumps(note.get("tags", [])),
                int(note.get("locked", False)),
                int(note.get("public", False)),  # 👈 KAYDEDİLİYOR
                note["created_at"],
                note["updated_at"]
            ))
            conn.commit()

    def load_notes(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM notes")
            rows = cursor.fetchall()
            notes = []
            for row in rows:
                notes.append({
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "type": row[3],
                    "tags": json.loads(row[4]) if row[4] else [],
                    "locked": bool(row[5]),
                    "public": bool(row[6]),  # 👈 YÜKLENİYOR
                    "created_at": row[7],
                    "updated_at": row[8]
                })
            return notes

    def delete_note(self, note_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()
