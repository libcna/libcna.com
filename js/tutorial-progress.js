(function () {
  const STORAGE_KEY = 'cna_tutorial_progress';

  function getProgress() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); }
    catch { return {}; }
  }
  function saveProgress(p) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(p)); } catch {}
  }
  function getTutorialId() {
    const m = location.pathname.match(/\/(\d+)-[^/]+\.html$/);
    return m ? parseInt(m[1], 10) : null;
  }

  // On tutorial pages: add a "Mark as done" checkbox
  function initTutorialPage() {
    const id = getTutorialId();
    if (!id) return;
    const progress = getProgress();
    const done = !!progress[id];

    const banner = document.createElement('div');
    banner.className = 'tutorial-progress-banner';
    banner.innerHTML = `
      <label class="tutorial-done-label">
        <input type="checkbox" id="tut-done-cb" ${done ? 'checked' : ''}>
        <span>${done ? '✓ Completed' : 'Mark as completed'}</span>
      </label>
      <a href="../../tutorials.html" class="tutorial-progress-link">← All tutorials</a>
    `;

    const article = document.querySelector('article.docs-content, .tutorial-layout article');
    if (article) article.prepend(banner);

    document.getElementById('tut-done-cb').addEventListener('change', function () {
      const p = getProgress();
      if (this.checked) { p[id] = 1; this.nextElementSibling.textContent = '✓ Completed'; }
      else { delete p[id]; this.nextElementSibling.textContent = 'Mark as completed'; }
      saveProgress(p);
    });
  }

  // On tutorials.html: show per-item checkmarks and overall progress bar
  function initTutorialsHub() {
    if (!document.querySelector('.tut-item')) return;
    const progress = getProgress();
    const total = 100;
    const done = Object.keys(progress).length;

    // Insert dynamic progress bar at top of page (after .page-header or first section)
    const header = document.querySelector('.page-header, .tutorials-header, h1');
    if (header) {
      const bar = document.createElement('div');
      bar.className = 'my-progress-bar-wrap';
      bar.innerHTML = `
        <div class="my-progress-label">Your progress: <strong>${done}</strong> / ${total} tutorials completed</div>
        <div class="my-progress-track"><div class="my-progress-fill" style="width:${Math.round(done/total*100)}%"></div></div>
        ${done > 0 ? `<button class="my-progress-reset" id="reset-progress">Reset progress</button>` : ''}
      `;
      header.after(bar);
      document.getElementById('reset-progress')?.addEventListener('click', () => {
        if (confirm('Reset all tutorial progress?')) { localStorage.removeItem(STORAGE_KEY); location.reload(); }
      });
    }

    // Add checkmark to completed tutorial items
    document.querySelectorAll('.tut-item').forEach(item => {
      const link = item.querySelector('a');
      if (!link) return;
      const m = link.href.match(/\/(\d+)-[^/]+\.html/);
      if (!m) return;
      const id = parseInt(m[1], 10);
      if (progress[id]) {
        item.classList.add('tut-done');
        const num = item.querySelector('.tut-num');
        if (num) num.textContent = '✓';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    if (location.pathname.includes('/tutorials/')) initTutorialPage();
    else initTutorialsHub();
  });
})();
