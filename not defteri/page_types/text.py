# page_types/text.py
from .base import PageType

class TextPage(PageType):
    type_id = "text"
    icon = "📝"
    name = "Metin Notu"

    def get_default_content(self) -> str:
        return "Buraya yazmaya başlayın..."

    def validate_content(self, content: str) -> bool:
        return isinstance(content, str)
