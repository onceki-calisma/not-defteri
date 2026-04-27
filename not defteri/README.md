# 📓 Not Defteri

Çok yönlü, modern ve akıllı bir not alma uygulaması. Hem **Komut Satırı (CLI)** hem de **Web Arayüzü** üzerinden notlarınızı yönetebilir, farklı formatlarda (metin, kod, görev, kanban, zihin haritası vb.) içerikler oluşturabilirsiniz.

## 🚀 Özellikler

-   **Çift Arayüz:** Aynı veri tabanını paylaşan güçlü bir CLI ve modern bir Web UI.
-   **Çeşitli Sayfa Türleri:**
    -   📝 Metin Notları
    -   💻 Kod Blokları
    -   ✅ Görev Listeleri (To-do)
    -   📋 Kanban Panoları
    -   🧠 Zihin Haritaları (Mindmap)
    -   📊 Diyagramlar
    -   🎬 Video ve 🎵 Ses Notları
-   **Akıllı Etiketleme:** ML tabanlı (SpaCy) otomatik anahtar kelime çıkarma ve kategorizasyon.
-   **Yerel Depolama:** Verileriniz tamamen kontrolünüz altında, yerel sisteminizde saklanır.

## 🛠️ Kurulum

### Gereksinimler

-   Python 3.8+
-   pip

### Adımlar

1.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

2.  NLP modellerini indirin (ML özellikleri için):
    ```bash
    python -m spacy download en_core_web_sm
    ```

## 📖 Kullanım

### Komut Satırı Arayüzü (CLI)

Uygulamayı `main.py` üzerinden çalıştırabilirsiniz:

-   **Yeni not oluştur:**
    ```bash
    python main.py new <tür> "<başlık>"
    # Örnek: python main.py new kanban "Proje Planı"
    ```
-   **Notları listele:**
    ```bash
    python main.py list
    ```
-   **Notu görüntüle:**
    ```bash
    python main.py view <note_id>
    ```
-   **Notu sil:**
    ```bash
    python main.py delete <note_id>
    ```

### Web Arayüzü

Web arayüzünü başlatmak için Flask sunucusunu çalıştırın:

```bash
python api/server.py
```

Ardından tarayıcınızda `http://localhost:5000` (veya sunucunun belirttiği adres) adresine gidin.

## 📂 Proje Yapısı

-   `main.py`: CLI giriş noktası.
-   `api/`: Flask sunucusu ve API endpointleri.
-   `core/`: Çekirdek mantık, veritabanı işlemleri ve ML motoru.
-   `frontend/`: Web arayüzü dosyaları (HTML/JS/CSS).
-   `page_types/`: Farklı not türlerinin tanımları.
-   `data/`: Notların ve veritabanının saklandığı dizin.

## 📄 Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakınız.