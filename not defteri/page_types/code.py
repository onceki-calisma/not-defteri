# page_types/code.py
from .base import PageType

class CodePage(PageType):
    type_id = "code"
    icon = "📓</>"
    name = "Kod Notu"

    def get_default_content(self) -> str:
        return "# Kodunuzu buraya yazın"

    def validate_content(self, content: str) -> bool:
        return isinstance(content, str)

    def render_preview(self, content: str) -> str:
        # Basit HTML escape
        escaped = (
            content
            .replace("&", "&amp;")
            .replace("<", "<")
            .replace(">", ">")
        )
        return f'<pre><code>{escaped}</code></pre>'
