'use strict';

// ── Элементы DOM ──────────────────────────────────────────────────────────────
const audioFile   = document.getElementById('audioFile');
const player      = document.getElementById('player');
const fileNameEl  = document.getElementById('fileName');
const btnPlay     = document.getElementById('btnPlay');
const btnPause    = document.getElementById('btnPause');
const btnStop     = document.getElementById('btnStop');
const progressBar = document.getElementById('progressBar');
const currentTimeEl = document.getElementById('currentTime');
const durationEl  = document.getElementById('duration');
const volumeInput = document.getElementById('volume');

// ── Вспомогательная функция форматирования времени ────────────────────────────
function formatTime(seconds) {
  if (isNaN(seconds)) return '0:00';
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

// ── Выбор файла ───────────────────────────────────────────────────────────────
audioFile.addEventListener('change', function () {
  const file = this.files[0];
  if (!file) return;

  // Освобождаем предыдущий blob-URL, если был
  if (player.src && player.src.startsWith('blob:')) {
    URL.revokeObjectURL(player.src);
  }

  fileNameEl.textContent = file.name;

  // Создаём временный локальный URL и передаём плееру
  const objectURL = URL.createObjectURL(file);
  player.src = objectURL;
  player.load();

  // Сбрасываем прогресс-бар
  progressBar.value = 0;
  currentTimeEl.textContent = '0:00';
  durationEl.textContent = '0:00';
});

// ── Кнопки управления ─────────────────────────────────────────────────────────
btnPlay.addEventListener('click', () => {
  if (!player.src) return;
  player.play();
});

btnPause.addEventListener('click', () => {
  if (!player.src) return;
  player.pause();
});

btnStop.addEventListener('click', () => {
  if (!player.src) return;
  player.pause();
  player.currentTime = 0;
});

// ── Обновление прогресс-бара и времени ────────────────────────────────────────
player.addEventListener('timeupdate', () => {
  if (!player.duration) return;
  const pct = (player.currentTime / player.duration) * 100;
  progressBar.value = pct;
  currentTimeEl.textContent = formatTime(player.currentTime);
});

player.addEventListener('loadedmetadata', () => {
  progressBar.max = 100;
  durationEl.textContent = formatTime(player.duration);
});

// ── Перемотка через прогресс-бар ──────────────────────────────────────────────
progressBar.addEventListener('input', () => {
  if (!player.duration) return;
  player.currentTime = (progressBar.value / 100) * player.duration;
});

// ── Громкость ─────────────────────────────────────────────────────────────────
volumeInput.addEventListener('input', () => {
  player.volume = volumeInput.value;
});

// ── Автосброс по окончании трека ──────────────────────────────────────────────
player.addEventListener('ended', () => {
  player.currentTime = 0;
  progressBar.value = 0;
  currentTimeEl.textContent = '0:00';
});
