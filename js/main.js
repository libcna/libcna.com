/* CNA Website - Shared JS */
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

/* ---- #38 — Copy-to-clipboard button on code blocks ----------- */
function addCopyButtons() {
  document.querySelectorAll('pre code').forEach(function(codeEl) {
    var pre = codeEl.parentElement;
    pre.style.position = 'relative';
    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.addEventListener('click', function() {
      navigator.clipboard.writeText(codeEl.textContent).then(function() {
        btn.textContent = 'Copied!';
        setTimeout(function() { btn.textContent = 'Copy'; }, 2000);
      });
    });
    pre.appendChild(btn);
  });
}

/* ---- #41 — Back-to-top button -------------------------------- */
function addBackToTop() {
  var btn = document.createElement('button');
  btn.id = 'back-to-top';
  btn.textContent = '↑';
  btn.title = 'Back to top';
  document.body.appendChild(btn);
  window.addEventListener('scroll', function() {
    btn.style.display = window.scrollY > 400 ? 'block' : 'none';
  });
  btn.addEventListener('click', function() {
    window.scrollTo({top: 0, behavior: 'smooth'});
  });
}

/* ---- #69 — Anchor links on section headings ------------------ */
function addHeadingAnchors() {
  document.querySelectorAll('.docs-content h2, .docs-content h3, article h2, article h3').forEach(function(h) {
    if (!h.id) {
      h.id = h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    }
    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.className = 'heading-anchor';
    a.textContent = '#';
    a.title = 'Link to this section';
    h.appendChild(a);
  });
}

/* ---- #44/#45 — Code language labels -------------------------- */
function addCodeLanguageLabels() {
  document.querySelectorAll('pre code').forEach(function(codeEl) {
    var pre = codeEl.parentElement;
    var lang = '';
    /* Detect from existing class (e.g. class="language-cpp") */
    var match = codeEl.className.match(/language-(\w+)/);
    if (match) {
      lang = match[1];
    } else {
      /* Heuristic detection from content */
      var text = codeEl.textContent.trimStart();
      if (/^#include/.test(text)) {
        lang = 'C++';
      } else if (/^[\[{]/.test(text)) {
        lang = 'JSON';
      } else if (/^git clone|^cmake -S/.test(text)) {
        lang = 'Shell';
      } else if (/^cmake|^find_package/.test(text)) {
        lang = 'CMake';
      }
    }
    if (lang) {
      var label = document.createElement('span');
      label.className = 'code-lang-label';
      label.textContent = lang;
      pre.appendChild(label);
    }
  });
}

document.addEventListener('DOMContentLoaded', function() {
  addCopyButtons();
  addBackToTop();
  addHeadingAnchors();
  addCodeLanguageLabels();
});
