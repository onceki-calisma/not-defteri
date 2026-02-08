// frontend/script/api.js
const API_BASE = 'http://127.0.0.1:5000';

export async function loadNote(id) {
  const res = await fetch(`${API_BASE}/notes/${id}`);
  if (!res.ok) throw new Error('Not bulunamadı');
  return res.json();
}

export async function updateNote(id, data) {
  await fetch(`${API_BASE}/notes/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
}

export async function createNote(type, title) {
  const res = await fetch(`${API_BASE}/notes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type, title })
  });
  return res.json();
}
