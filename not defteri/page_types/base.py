# page_types/base.py
from abc import ABC, abstractmethod

class PageType(ABC):
    type_id: str
    icon: str
    name: str

    @abstractmethod
    def get_default_content(self) -> str:
        pass

    @abstractmethod
    def validate_content(self, content: str) -> bool:
        pass

    def render_preview(self, content: str) -> str:
        return content
