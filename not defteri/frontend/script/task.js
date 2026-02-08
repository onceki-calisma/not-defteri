// frontend/script/task.js
import { loadNote, updateNote } from './api.js';

// URL'den not ID'sini al
const urlParams = new URLSearchParams(window.location.search);
const noteId = urlParams.get('id');

if (!noteId) {
  alert('Not ID eksik!');
  window.location.href = '../index.html';
}

// Notu yükle
let currentTasks = [];
loadNote(noteId).then(note => {
  document.querySelector('.note-title').textContent = note.title;
  renderTasks(note.content);
  currentTasks = JSON.parse(note.content || '[]');
});

function renderTasks(content) {
  try {
    const tasks = JSON.parse(content);
    const container = document.querySelector('.task-container');
    container.innerHTML = tasks.map((task, i) => `
      <div class="task-item">
        <input type="checkbox" ${task.completed ? 'checked' : ''} data-index="${i}">
        <span contenteditable="true">${task.text}</span>
        <button class="delete-task" data-index="${i}">🗑️</button>
      </div>
    `).join('');

    // Etkileşimleri bağla
    container.querySelectorAll('input[type="checkbox"]').forEach(input => {
      input.addEventListener('change', (e) => {
        const index = e.target.dataset.index;
        currentTasks[index].completed = e.target.checked;
        saveTasks();
      });
    });

    container.querySelectorAll('.delete-task').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = e.target.dataset.index;
        currentTasks.splice(index, 1);
        saveTasks();
      });
    });

    container.querySelectorAll('span[contenteditable]').forEach(span => {
      span.addEventListener('blur', (e) => {
        const index = e.target.closest('.task-item').querySelector('input').dataset.index;
        currentTasks[index].text = e.target.textContent;
        saveTasks();
      });
    });
  } catch (e) {
    document.querySelector('.task-container').innerHTML = '<p>Geçersiz görev verisi</p>';
  }
}

async function saveTasks() {
  const title = document.querySelector('.note-title').textContent;
  await updateNote(noteId, { title, content: JSON.stringify(currentTasks) });
}

// Manuel kaydetme
document.getElementById('saveBtn').addEventListener('click', saveTasks);
