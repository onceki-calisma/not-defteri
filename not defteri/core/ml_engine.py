# core/ml_engine.py
def generate_mindmap_from_text(text: str) -> dict:
    """
    Metinden zihin haritası üretir.
    Çıktı formatı:
    {
      "root": "Ana Konu",
      "children": [
        {"text": "Alt Konu 1", "children": []},
        {"text": "Alt Konu 2", "children": []}
      ]
    }
    """
    # Basit örnek (gerçek uygulamada NLP modeli kullanılır)
    return {
        "root": "Metin Özeti",
        "children": [
            {"text": "Anahtar Kelime 1", "children": []},
            {"text": "Anahtar Kelime 2", "children": []}
        ]
    }
