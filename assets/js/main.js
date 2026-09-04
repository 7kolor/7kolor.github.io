// 7Kolor Insights — shared site JS
(function () {
  document.documentElement.classList.remove('no-js');
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- Bilingual toggle ----
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

  // ---- Scroll reveal (fade-up, respects reduced motion) ----
  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    if (REDUCED || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('revealed'); });
      return;
    }
    // stagger: children with .reveal-item fan in sequentially
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var el = en.target;
          el.classList.add('revealed');
          io.unobserve(el);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  }

  // ---- Animated counters for .cred-value (data assets) ----
  function initCounters() {
    var RED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.querySelectorAll('.cred-value[data-count]').forEach(function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      var suffix = el.getAttribute('data-suffix') || '';
      var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          io.unobserve(el);
          if (RED || !target) {
            el.textContent = el.getAttribute('data-final') || format(target, decimals) + suffix;
            return;
          }
          var start = performance.now();
          var dur = 1200;
          function tick(now) {
            var k = Math.min(1, (now - start) / dur);
            k = 1 - Math.pow(1 - k, 3); // easeOutCubic
            el.textContent = format(target * k, decimals) + suffix;
            if (k < 1) requestAnimationFrame(tick);
          }
          requestAnimationFrame(tick);
        });
      }, { threshold: 0.4 });
      io.observe(el);
    });
    function format(n, d) {
      return n.toFixed(d).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
  }

  // ---- Header state on scroll ----
  function initHeader() {
    var h = document.querySelector('.header');
    if (!h) return;
    function onScroll() {
      h.classList.toggle('header-scrolled', window.scrollY > 8);
    }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // ---- Smooth scroll for in-page anchors ----
  function initSmooth() {
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        var target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth', block: 'start' });
        }
      });
    });
  }

  // ---- Hero slogan carousel ----
  function initCarousel() {
    var car = document.querySelector('[data-carousel]');
    if (!car) return;
    var items = car.querySelectorAll('.slogan-item');
    var dots = document.querySelectorAll('[data-carousel-dots] .dot');
    var idx = 0;
    var RED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function show(i) {
      items.forEach(function (el, k) {
        el.classList.toggle('show', k === i);
        el.classList.toggle('hide', k !== i);
      });
      dots.forEach(function (d, k) { d.classList.toggle('active', k === i); });
    }
    show(0);
    if (RED || items.length < 2) return;
    setInterval(function () {
      idx = (idx + 1) % items.length;
      show(idx);
    }, 3200);
  }

  // ---- Step boards: show ''暂无更多报告'' when fewer than 4 real reports ----
  function initStepHints() {
    var panels = document.querySelectorAll('.step-panel');
    if (!panels.length) return;
    panels.forEach(function (panel) {
      var grid = panel.querySelector('.step-grid');
      var hint = panel.querySelector('.step-empty-hint');
      if (!grid || !hint) return;
      var real = grid.querySelectorAll('.report-card:not(.report-card-soon)');
      if (real.length > 0 && real.length < 4) hint.style.display = 'block';
    });
  }

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
    initReveal();
    initCounters();
    initCarousel();
    initHeader();
    initSmooth();
    initStepHints();
  });

  // expose for pages that query reduced motion
  window.SITE_REDUCED = REDUCED;
})();
