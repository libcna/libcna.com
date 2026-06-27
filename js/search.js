(function () {
  var input = document.getElementById('search-input');
  var resultsEl = document.getElementById('search-results');
  if (!input || !resultsEl) return;

  // Pre-fill from URL ?q= and run immediately
  var params = new URLSearchParams(window.location.search);
  var q = params.get('q') || '';
  if (q) {
    input.value = q;
    runSearch(q);
  }

  input.addEventListener('input', function () {
    runSearch(input.value);
  });

  function runSearch(query) {
    var q = query.trim().toLowerCase();
    if (q.length < 2) {
      resultsEl.innerHTML = q.length
        ? '<p class="search-hint">Type at least 2 characters.</p>'
        : '';
      return;
    }
    fetch('search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (index) {
        var terms = q.split(/\s+/).filter(Boolean);
        var results = index.filter(function (page) {
          var haystack = (
            page.title + ' ' +
            page.description + ' ' +
            (page.tags || []).join(' ')
          ).toLowerCase();
          return terms.every(function (t) { return haystack.includes(t); });
        });
        renderResults(results, q);
      })
      .catch(function () {
        resultsEl.innerHTML = '<p class="search-hint">Search index not available.</p>';
      });
  }

  function renderResults(results, q) {
    if (!results.length) {
      resultsEl.innerHTML =
        '<p class="search-hint">No results for <strong>' + esc(q) + '</strong>.</p>';
      return;
    }
    resultsEl.innerHTML =
      '<p class="search-count">' +
        results.length + ' result' + (results.length !== 1 ? 's' : '') +
      '</p>' +
      results.map(function (r) {
        return (
          '<a href="' + esc(r.url) + '" class="search-result-card">' +
            '<div class="search-result-title">' + highlight(esc(r.title), q) + '</div>' +
            '<div class="search-result-desc">' + highlight(esc(r.description), q) + '</div>' +
            '<div class="search-result-url">' + esc(r.url) + '</div>' +
          '</a>'
        );
      }).join('');
  }

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function highlight(text, q) {
    var terms = q.split(/\s+/).filter(Boolean);
    var out = text;
    terms.forEach(function (t) {
      var re = new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
      out = out.replace(re, function (m) { return '<mark>' + m + '</mark>'; });
    });
    return out;
  }
})();
