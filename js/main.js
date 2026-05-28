/* CNA Website — Shared JS */
(function () {
  'use strict';

  /* Mobile nav toggle */
  const toggle = document.querySelector('.nav-toggle');
  const menu   = document.querySelector('.nav-menu');

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      menu.classList.toggle('open');
      const open = menu.classList.contains('open');
      toggle.setAttribute('aria-expanded', open);
    });

    /* Close on outside click */
    document.addEventListener('click', function (e) {
      if (!toggle.contains(e.target) && !menu.contains(e.target)) {
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded', false);
      }
    });
  }

  /* Mark active nav link */
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(function (a) {
    if (a.getAttribute('href') === path) {
      a.classList.add('active');
    }
  });

  /* FAQ accordion */
  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const item = btn.closest('.faq-item');
      item.classList.toggle('open');
    });
  });

})();
