# page_types/mindmap.py
from .base import PageType
import json

class MindMapPage(PageType):
    type_id = "mindmap"
    icon = "🧠"
    name = "Zihin Haritası"

    def get_default_content(self) -> str:
        default = {
            "root": "Ana Fikir",
            "children": [
                {"text": "Dal 1", "children": []},
                {"text": "Dal 2", "children": []}
            ]
        }
        return json.dumps(default, ensure_ascii=False)

    def validate_content(self, content: str) -> bool:
        try:
            data = json.loads(content)
            return "root" in data and "children" in data
        except (json.JSONDecodeError, TypeError):
            return False

    def render_preview(self, content: str) -> str:
        if not self.validate_content(content):
            return "Geçersiz zihin haritası"
        data = json.loads(content)
        def count_nodes(node):
            count = 1
            for child in node.get("children", []):
                count += count_nodes(child)
            return count
        total = count_nodes({"text": data["root"], "children": data["children"]})
        return f"Toplam {total} düğüm"
