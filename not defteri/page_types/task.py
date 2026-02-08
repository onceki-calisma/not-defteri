# page_types/task.py
from .base import PageType
import json

class TaskPage(PageType):
    type_id = "task"
    icon = "✅"
    name = "Görev Listesi"

    def get_default_content(self) -> str:
        return "[]"

    def validate_content(self, content: str) -> bool:
        try:
            tasks = json.loads(content)
            if not isinstance(tasks, list):
                return False
            for task in tasks:
                if not isinstance(task, dict):
                    return False
                if "text" not in task or "completed" not in task:
                    return False
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    def render_preview(self, content: str) -> str:
        if not self.validate_content(content):
            return "Geçersiz görev listesi"
        tasks = json.loads(content)
        completed = sum(1 for t in tasks if t.get("completed"))
        return f"{completed}/{len(tasks)} tamamlandı"
