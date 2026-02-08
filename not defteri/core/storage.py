# core/storage.py
import json
import os
from pathlib import Path
from typing import List, Dict, Any

class Storage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.notes_file = self.data_dir / "notes.json"

    def load_notes(self) -> List[Dict[str, Any]]:
        if not self.notes_file.exists():
            return []
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_notes(self, notes: List[Dict[str, Any]]) -> bool:
        try:
            with open(self.notes_file, "w", encoding="utf-8") as f:
                json.dump(notes, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False

    def get_last_opened_note_id(self) -> str:
        last_file = self.data_dir / "last_opened.txt"
        if last_file.exists():
            return last_file.read_text().strip()
        return ""

    def set_last_opened_note_id(self, note_id: str):
        last_file = self.data_dir / "last_opened.txt"
        last_file.write_text(note_id)
