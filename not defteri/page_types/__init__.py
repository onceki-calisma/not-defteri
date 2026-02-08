# page_types/__init__.py
from typing import Dict, Optional
from .base import PageType
from .text import TextPage
from .code import CodePage
from .task import TaskPage
from .kanban import KanbanPage
from .video import VideoPage
from .audio import AudioPage
from .mindmap import MindMapPage
from .diagram import DiagramPage

# Tüm sayfa türlerini kaydet
PAGE_TYPES: Dict[str, PageType] = {
    "text": TextPage(),
    "code": CodePage(),
    "task": TaskPage(),
    "kanban": KanbanPage(),
    "video": VideoPage(),
    "audio": AudioPage(),
    "mindmap": MindMapPage(),
    "diagram": DiagramPage(),
}

def get_page_type(type_id: str) -> Optional[PageType]:
    return PAGE_TYPES.get(type_id)
