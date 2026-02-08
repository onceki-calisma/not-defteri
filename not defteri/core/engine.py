# core/engine.py
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from .note import Note

# JSON depolama (eski sistem)
class Storage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.notes_file = os.path.join(self.data_dir, "notes.json")

    def load_notes(self):
        if not os.path.exists(self.notes_file):
            return []
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                import json
                return json.load(f)
        except (ValueError, IOError):
            return []

    def save_notes(self, notes):
        with open(self.notes_file, "w", encoding="utf-8") as f:
            import json
            json.dump(notes, f, ensure_ascii=False, indent=2)

    def delete_note(self, note_id):
        notes = self.load_notes()
        notes = [n for n in notes if n["id"] != note_id]
        self.save_notes(notes)

# SQLite depolama (yeni sistem)
from .database import Database

class NotDefteri:
    def __init__(self, db_path: str = None, data_dir: str = None):
        """
        İki modda çalışır:
        - Eğer db_path verilirse → SQLite kullanır
        - Eğer data_dir verilirse → JSON kullanır (eski sistem)
        - Hiçbiri verilmezse → varsayılan SQLite kullanır
        """
        if db_path is not None:
            # Yeni sistem: SQLite
            self.storage_type = "sqlite"
            self.db = Database(db_path)
            self.notes = []
            self._load_notes_sqlite()
        elif data_dir is not None:
            # Eski sistem: JSON
            self.storage_type = "json"
            self.storage = Storage(data_dir)
            self.notes = []
            self._load_notes_json()
        else:
            # Varsayılan: SQLite
            default_db = os.path.join("data", "notes.db")
            self.storage_type = "sqlite"
            self.db = Database(default_db)
            self.notes = []
            self._load_notes_sqlite()

        self.current_note_id = None

    # --- SQLITE YÜKLEME ---
    def _load_notes_sqlite(self):
        raw_notes = self.db.load_notes()
        self.notes = [Note.from_dict(n) for n in raw_notes]
        if not self.notes:
            self._create_default_note()

    # --- JSON YÜKLEME ---
    def _load_notes_json(self):
        raw_notes = self.storage.load_notes()
        self.notes = [Note.from_dict(n) for n in raw_notes]
        if not self.notes:
            self._create_default_note()

    def _create_default_note(self):
        default = Note(
            id="note-1",
            title="Başlıksız Not",
            content="Buraya yazmaya başlayın...",
            type="text"
        )
        self.notes = [default]
        self.save_all()

    def save_all(self):
        if self.storage_type == "sqlite":
            for note in self.notes:
                self.db.save_note(note.to_dict())
        else:  # json
            raw_notes = [note.to_dict() for note in self.notes]
            self.storage.save_notes(raw_notes)

    def create_note(self, note_type: str, title: str = None) -> str:
        from page_types import get_page_type
        page_type = get_page_type(note_type)
        if not page_type:
            raise ValueError(f"Bilinmeyen sayfa türü: {note_type}")

        note_id = f"note-{len(self.notes) + 1}"
        default_title = title or f"Yeni {page_type.name}"
        default_content = page_type.get_default_content()

        note = Note(
            id=note_id,
            title=default_title,
            content=default_content,
            type=note_type
        )
        self.notes.append(note)
        self.save_all()
        return note_id

    def delete_note(self, note_id: str) -> bool:
        note_to_delete = None
        for note in self.notes:
            if note.id == note_id:
                if note.locked:
                    raise ValueError("Kilitli not silinemez")
                note_to_delete = note
                break

        if note_to_delete:
            self.notes = [n for n in self.notes if n.id != note_id]
            if self.storage_type == "sqlite":
                self.db.delete_note(note_id)
            else:
                self.storage.delete_note(note_id)
            if self.current_note_id == note_id:
                self.current_note_id = self.notes[0].id if self.notes else None
            return True
        return False

    def update_note(self, note_id: str, title: str = None, content: str = None, tags: list = None, locked: bool = None):
        for note in self.notes:
            if note.id == note_id:
                if note.locked and (title is not None or content is not None or tags is not None):
                    raise ValueError("Kilitli not düzenlenemez")

                if title is not None:
                    note.title = title
                if content is not None:
                    from page_types import get_page_type
                    page_type = get_page_type(note.type)
                    if page_type and not page_type.validate_content(content):
                        raise ValueError("Geçersiz içerik formatı")
                    note.content = content
                if tags is not None:
                    note.tags = tags
                if locked is not None:
                    note.locked = locked
                note.updated_at = datetime.now().isoformat()
                self.save_all()
                return True
        return False

    def get_note(self, note_id: str) -> Optional[Note]:
        return next((n for n in self.notes if n.id == note_id), None)

    def get_all_notes(self) -> List[Note]:
        return self.notes
