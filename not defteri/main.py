# main.py
import sys
import json
import argparse
from pathlib import Path

# Proje kökünü sys.path'e ekle (güvenlik önlemi)
sys.path.insert(0, str(Path(__file__).parent))

from core import NotDefteri
from page_types import get_page_type

def main():
    parser = argparse.ArgumentParser(
        prog="📓 Not Defteri",
        description="Çok yönlü komut satırı not defteri"
    )
    subparsers = parser.add_subparsers(dest="command", help="Komutlar")

    # --- new ---
    new_parser = subparsers.add_parser("new", help="Yeni not oluştur")
    new_parser.add_argument("type", choices=["text", "code", "task", "kanban", "video", "audio", "mindmap", "diagram"], help="Sayfa türü")
    new_parser.add_argument("title", nargs="?", default=None, help="Not başlığı")

    # --- list ---
    subparsers.add_parser("list", help="Tüm notları listele")

    # --- view ---
    view_parser = subparsers.add_parser("view", help="Notu görüntüle")
    view_parser.add_argument("note_id", help="Not ID'si")

    # --- delete ---
    delete_parser = subparsers.add_parser("delete", help="Notu sil")
    delete_parser.add_argument("note_id", help="Not ID'si")

    # --- current ---
    subparsers.add_parser("current", help="Son açık notu göster")

    args = parser.parse_args()

    # Not defterini başlat
    app = NotDefteri()

    if args.command == "new":
        note_id = app.create_note(args.type, args.title)
        print(f"✅ Yeni not oluşturuldu: {note_id}")

    elif args.command == "list":
        notes = app.get_all_notes()
        if not notes:
            print("Henüz hiç not yok.")
            return
        print(f"{'ID':<15} {'Başlık':<25} {'Tür':<15} {'Etiketler'}")
        print("-" * 60)
        for note in notes:
            tags = ", ".join(note.tags) if note.tags else "-"
            print(f"{note.id:<15} {note.title:<25} {note.type:<15} {tags}")

    elif args.command == "view":
        note = app.get_note(args.note_id)
        if not note:
            print(f"❌ Not bulunamadı: {args.note_id}")
            return
        print(f"\n📋 {note.title} ({note.type})")
        print(f"🆔 ID: {note.id}")
        print(f"🕒 Oluşturulma: {note.created_at}")
        print(f"🔖 Etiketler: {', '.join(note.tags) if note.tags else 'Yok'}")
        print("\n--- İçerik ---")
        print(note.content)

    elif args.command == "delete":
        if app.delete_note(args.note_id):
            print(f"🗑️ Not silindi: {args.note_id}")
        else:
            print(f"❌ Not bulunamadı: {args.note_id}")

    elif args.command == "current":
        note = app.get_current_note()
        if note:
            print(f" Şu anki not: {note.title} ({note.id})")
        else:
            print("Açık not yok.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
