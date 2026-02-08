# page_types/kanban.py
from .base import PageType
import json

class KanbanPage(PageType):
    type_id = "kanban"
    icon = "🗂️"
    name = "Kanban Panosu"

    def get_default_content(self) -> str:
        default = {
            "columns": ["Yapılacak", "Devam Ediyor", "Tamamlandı"],
            "cards": []
        }
        return json.dumps(default, ensure_ascii=False)

    def validate_content(self, content: str) -> bool:
        try:
            data = json.loads(content)
            if not isinstance(data, dict):
                return False
            if "columns" not in data or "cards" not in data:
                return False
            if not isinstance(data["columns"], list) or not isinstance(data["cards"], list):
                return False
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    def render_preview(self, content: str) -> str:
        if not self.validate_content(content):
            return "Geçersiz Kanban verisi"
        data = json.loads(content)
        total_cards = len(data["cards"])
        return f"{len(data['columns'])} sütun, {total_cards} kart"
