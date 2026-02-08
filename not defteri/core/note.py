# core/note.py
import json
from datetime import datetime
from typing import Any, Dict, List, Optional,data

class Note:
    def __init__(
        self,
        id: str,
        title: str,
        content: str,
        type: str,
        tags: Optional[List[str]] = None,
        locked: bool = False,
        public: bool = False
    ):
        self.id = id
        self.title = title
        self.content = content
        self.type = type
        self.tags = tags or []
        self.locked = locked
        self.public = public
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def to_dict(self) -> Dict[str,data, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "type": self.type,
            "tags": self.tags,
            "locked": self.locked,
            "public": self.public,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls) -> Dict[str,data, Any]):
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            type=data["type"],
            tags=data.get("tags", []),
            locked=data.get("locked", False),
            public=data.get("public", False)
        )
