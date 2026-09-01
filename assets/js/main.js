// 7kolor Signals — shared site JS
// Bilingual toggle: elements carry data-zh / data-en attributes.
// Pages that are single-language set body[data-lang-page] and the toggle
// buttons are rendered as links instead (no JS switching needed).
(function () {
  function switchLang(lang, btn) {
    document.querySelectorAll('.lang-btn').forEach(function (b) { b.classList.remove('active'); });
    if (btn) btn.classList.add('active');
    document.querySelectorAll('[data-zh]').forEach(function (el) {
      var v = el.getAttribute('data-' + lang);
      if (v !== null) el.textContent = v;
    });
    try { localStorage.setItem('7kolor-lang', lang); } catch (e) {}
  }
  window.switchLang = switchLang;

  document.addEventListener('DOMContentLoaded', function () {
    // Restore preferred language on bilingual pages
    if (document.querySelector('[data-zh]') && !document.body.hasAttribute('data-lang-page')) {
      var saved = null;
      try { saved = localStorage.getItem('7kolor-lang'); } catch (e) {}
      if (saved === 'en' || saved === 'zh') {
        var btn = document.querySelector('.lang-btn[data-lang="' + saved + '"]');
        switchLang(saved, btn);
      }
    }
    // Smooth scroll for in-page anchors
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        var target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  });
})();
