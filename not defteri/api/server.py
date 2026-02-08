# api/server.py
from flask import Flask, jsonify, request
from core import NotDefteri
from page_types import get_page_type
import os

app = Flask(__name__)
not_defteri = NotDefteri(data_dir=os.path.join(os.path.dirname(__file__), "..", "data"))

# --- CORS ---
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# --- TÜM NOTLAR ---
@app.route('/notes', methods=['GET'])
def get_notes():
    tag = request.args.get('tag')
    notes = not_defteri.get_all_notes()
    if tag:
        notes = [n for n in notes if tag in (n.tags or [])]
    return jsonify([note.to_dict() for note in notes])

# --- TEK NOT ---
@app.route('/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    note = not_defteri.get_note(note_id)
    if not note:
        return jsonify({"error": "Not bulunamadı"}), 404
    return jsonify(note.to_dict())

# --- YENİ NOT ---
@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    note_type = data.get('type', 'text')
    title = data.get('title')

    if not get_page_type(note_type):
        return jsonify({"error": "Geçersiz sayfa türü"}), 400

    note_id = not_defteri.create_note(note_type, title)
    note = not_defteri.get_note(note_id)
    return jsonify(note.to_dict()), 201

# --- NOTU GÜNCELLE ---
@app.route('/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    note = not_defteri.get_note(note_id)
    if not note:
        return jsonify({"error": "Not bulunamadı"}), 404
    if note.locked:
        return jsonify({"error": "Kilitli not düzenlenemez"}), 403

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    tags = data.get('tags')

    if not not_defteri.update_note(note_id, title=title, content=content, tags=tags):
        return jsonify({"error": "Not güncellenemedi"}), 404

    updated_note = not_defteri.get_note(note_id)
    return jsonify(updated_note.to_dict())

# --- NOTU SİL ---
@app.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = not_defteri.get_note(note_id)
    if not note:
        return jsonify({"error": "Not bulunamadı"}), 404
    if note.locked:
        return jsonify({"error": "Kilitli not silinemez"}), 403

    if not_defteri.delete_note(note_id):
        return jsonify({"success": True})
    return jsonify({"error": "Not silinemedi"}), 404

# --- NOTU KİLİTLE / KİLİDİNİ AÇ ---
@app.route('/notes/<note_id>/lock', methods=['POST'])
def toggle_lock(note_id):
    note = not_defteri.get_note(note_id)
    if not note:
        return jsonify({"error": "Not bulunamadı"}), 404

    data = request.get_json()
    locked = data.get('locked', True)
    note.locked = locked
    not_defteri.save_all()
    return jsonify(note.to_dict())

# --- SAYFA TÜRLERİ ---
@app.route('/page-types', methods=['GET'])
def get_page_types():
    from page_types import PAGE_TYPES
    types = [
        {"id": pt.type_id, "name": pt.name, "icon": pt.icon}
        for pt in PAGE_TYPES.values()
    ]
    return jsonify(types)

@app.route('/')
def index():
    return "📓 Not Defteri API Çalışıyor!"

# --- AÇIK NOTLARI LİSTELE ---
@app.route('/public', methods=['GET'])
def list_public_notes():
    notes = not_defteri.get_all_notes()
    public_notes = [n.to_dict() for n in notes if n.public]
    return jsonify(public_notes)

# --- TEK AÇIK NOTU GETİR ---
@app.route('/public/<note_id>', methods=['GET'])
def get_public_note(note_id):
    note = not_defteri.get_note(note_id)
    if not note or not note.public:
        return jsonify({"error": "Açık not bulunamadı"}), 404
    return jsonify(note.to_dict())

# --- NOTU AÇIK YAP / KAPAT ---
@app.route('/notes/<note_id>/public', methods=['POST'])
def toggle_public(note_id):
    note = not_defteri.get_note(note_id)
    if not note:
        return jsonify({"error": "Not bulunamadı"}), 404

    data = request.get_json()
    public = data.get('public', True)
    note.public = public
    not_defteri.save_all()
    return jsonify(note.to_dict())

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
