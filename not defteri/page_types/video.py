# page_types/video.py
from .base import PageType
import json

class VideoPage(PageType):
    type_id = "video"
    icon = "🎥"
    name = "Video Notu"

    def get_default_content(self) -> str:
        default = {
            "video_url": "",
            "transcript": "",
            "bookmarks": []  # [{"time": "1:23", "note": "Önemli nokta"}]
        }
        return json.dumps(default, ensure_ascii=False)

    def validate_content(self, content: str) -> bool:
        try:
            data = json.loads(content)
            required = ["video_url", "transcript", "bookmarks"]
            return all(key in data for key in required)
        except (json.JSONDecodeError, TypeError):
            return False

    def render_preview(self, content: str) -> str:
        if not self.validate_content(content):
            return "Geçersiz video notu"
        data = json.loads(content)
        bookmarks = len(data.get("bookmarks", []))
        return f"Video: {data['video_url'] or 'Yok'}, {bookmarks} işaret"
