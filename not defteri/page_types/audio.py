# page_types/audio.py
from .base import PageType
import json

class AudioPage(PageType):
    type_id = "audio"
    icon = "🎙️"
    name = "Ses Notu"

    def get_default_content(self) -> str:
        default = {
            "audio_file": "",
            "transcript": "",
            "timestamps": []  # [{"time": "0:45", "text": "Merhaba"}]
        }
        return json.dumps(default, ensure_ascii=False)

    def validate_content(self, content: str) -> bool:
        try:
            data = json.loads(content)
            required = ["audio_file", "transcript", "timestamps"]
            return all(key in data for key in required)
        except (json.JSONDecodeError, TypeError):
            return False

    def render_preview(self, content: str) -> str:
        if not self.validate_content(content):
            return "Geçersiz ses notu"
        data = json.loads(content)
        duration = "Bilinmiyor"
        if data["timestamps"]:
            last = data["timestamps"][-1]
            duration = last.get("time", "Bilinmiyor")
        return f"Ses: {data['audio_file'] or 'Yok'}, Süre: {duration}"
