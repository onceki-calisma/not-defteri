# page_types/diagram.py
from .base import PageType
import json

class DiagramPage(PageType):
    type_id = "diagram"
    icon = "📐"
    name = "Şema / Akış Çizimi"

    def get_default_content(self) -> str:
        default = {
            "nodes": [
                {"id": "1", "type": "start", "text": "Başla", "x": 100, "y": 100},
                {"id": "2", "type": "process", "text": "İşlem", "x": 100, "y": 200}
            ],
            "edges": [
                {"from": "1", "to": "2"}
            ]
        }
        return json.dumps(default, ensure_ascii=False)

    def validate_content(self, content: str) -> bool:
        try:
            data = json.loads(content)
            return "nodes" in data and "edges" in data
        except (json.JSONDecodeError, TypeError):
            return False

    def render_preview(self, content: str) -> str:
        if not self.validate_content(content):
            return "Geçersiz şema"
        data = json.loads(content)
        nodes = len(data.get("nodes", []))
        edges = len(data.get("edges", []))
        return f"{nodes} öğe, {edges} bağlantı"
