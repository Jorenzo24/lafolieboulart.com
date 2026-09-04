/* La Folie Boulart — interactions */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- En-tête : état au défilement ---------- */
  var header = document.querySelector('.header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 40);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Panneau de navigation ---------- */
  var toggle = document.querySelector('.menu-toggle');
  var panel = document.getElementById('nav-panel');
  if (toggle && panel) {
    var lastFocus = null;
    var setNav = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      panel.classList.toggle('is-open', open);
      document.body.classList.toggle('nav-open', open);
      panel.setAttribute('aria-hidden', String(!open));
      if (open) {
        lastFocus = document.activeElement;
        var first = panel.querySelector('a, button');
        if (first) { first.focus(); }
      } else if (lastFocus) {
        lastFocus.focus();
      }
    };
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('is-open')) { setNav(false); }
    });

    /* Sous-menus */
    panel.querySelectorAll('.nav-sub-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        var sub = document.getElementById(btn.getAttribute('aria-controls'));
        btn.setAttribute('aria-expanded', String(!open));
        if (sub) { sub.classList.toggle('is-open', !open); }
      });
    });

    /* Aperçu visuel au survol des entrées */
    var media = panel.querySelector('.nav-panel__media');
    if (media) {
      var shots = media.querySelectorAll('img');
      panel.querySelectorAll('[data-shot]').forEach(function (link) {
        link.addEventListener('mouseenter', function () {
          var idx = parseInt(link.getAttribute('data-shot'), 10);
          shots.forEach(function (img, i) { img.classList.toggle('is-active', i === idx); });
        });
      });
    }

    /* Décalage progressif des entrées à l'ouverture */
    panel.querySelectorAll('.nav-list > li > .nav-list__row > a').forEach(function (a, i) {
      a.style.transitionDelay = (0.05 + i * 0.045) + 's';
    });
  }

  /* ---------- Carrousels ---------- */
  document.querySelectorAll('[data-slider]').forEach(function (root) {
    var track = root.querySelector('.slider__track');
    var slides = Array.prototype.slice.call(root.querySelectorAll('.slider__slide'));
    if (!track || slides.length < 2) { return; }

    var index = 0;
    var dotsWrap = root.querySelector('.slider__dots');
    var timer = null;
    var delay = parseInt(root.getAttribute('data-autoplay') || '0', 10);

    var dots = [];
    if (dotsWrap) {
      slides.forEach(function (_, i) {
        var d = document.createElement('button');
        d.className = 'slider__dot';
        d.type = 'button';
        d.setAttribute('aria-label', 'Vue ' + (i + 1));
        d.addEventListener('click', function () { go(i); restart(); });
        dotsWrap.appendChild(d);
        dots.push(d);
      });
    }

    function go(i) {
      index = (i + slides.length) % slides.length;
      track.style.transform = 'translateX(' + (-index * 100) + '%)';
      slides.forEach(function (s, n) { s.setAttribute('aria-hidden', String(n !== index)); });
      dots.forEach(function (d, n) { d.setAttribute('aria-current', String(n === index)); });
    }
    function next() { go(index + 1); }
    function prev() { go(index - 1); }
    function restart() {
      if (timer) { clearInterval(timer); }
      if (delay && !reduced) { timer = setInterval(next, delay); }
    }

    var btnPrev = root.querySelector('.slider__btn--prev');
    var btnNext = root.querySelector('.slider__btn--next');
    if (btnPrev) { btnPrev.addEventListener('click', function () { prev(); restart(); }); }
    if (btnNext) { btnNext.addEventListener('click', function () { next(); restart(); }); }

    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { prev(); restart(); }
      if (e.key === 'ArrowRight') { next(); restart(); }
    });

    /* Glissement tactile */
    var x0 = null;
    root.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    root.addEventListener('touchend', function (e) {
      if (x0 === null) { return; }
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) { dx < 0 ? next() : prev(); restart(); }
      x0 = null;
    }, { passive: true });

    root.addEventListener('mouseenter', function () { if (timer) { clearInterval(timer); } });
    root.addEventListener('mouseleave', restart);

    go(0);
    restart();
  });

  /* ---------- Visionneuse ---------- */
  var lbItems = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  if (lbItems.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Visionneuse');
    lb.innerHTML =
      '<img class="lightbox__img" alt="">' +
      '<button class="lightbox__btn lightbox__close" type="button" aria-label="Fermer">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 5l14 14M19 5L5 19"/></svg></button>' +
      '<button class="lightbox__btn lightbox__prev" type="button" aria-label="Image précédente">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M15 4l-8 8 8 8"/></svg></button>' +
      '<button class="lightbox__btn lightbox__next" type="button" aria-label="Image suivante">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 4l8 8-8 8"/></svg></button>' +
      '<p class="lightbox__count"></p>';
    document.body.appendChild(lb);

    var lbImg = lb.querySelector('.lightbox__img');
    var lbCount = lb.querySelector('.lightbox__count');
    var current = 0;
    var opener = null;

    function show(i) {
      current = (i + lbItems.length) % lbItems.length;
      var el = lbItems[current];
      var img = el.tagName === 'IMG' ? el : el.querySelector('img');
      lbImg.src = el.getAttribute('data-full') || (img ? img.currentSrc || img.src : '');
      lbImg.alt = img ? img.alt : '';
      lbCount.textContent = (current + 1) + ' / ' + lbItems.length;
    }
    function open(i) {
      opener = document.activeElement;
      show(i);
      lb.classList.add('is-open');
      document.body.classList.add('nav-open');
      lb.querySelector('.lightbox__close').focus();
    }
    function close() {
      lb.classList.remove('is-open');
      document.body.classList.remove('nav-open');
      if (opener) { opener.focus(); }
    }

    lbItems.forEach(function (el, i) {
      el.style.cursor = 'zoom-in';
      if (!el.hasAttribute('tabindex')) { el.setAttribute('tabindex', '0'); }
      if (!el.hasAttribute('role')) { el.setAttribute('role', 'button'); }
      el.addEventListener('click', function () { open(i); });
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); }
      });
    });

    lb.querySelector('.lightbox__close').addEventListener('click', close);
    lb.querySelector('.lightbox__prev').addEventListener('click', function () { show(current - 1); });
    lb.querySelector('.lightbox__next').addEventListener('click', function () { show(current + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) { close(); } });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) { return; }
      if (e.key === 'Escape') { close(); }
      if (e.key === 'ArrowLeft') { show(current - 1); }
      if (e.key === 'ArrowRight') { show(current + 1); }
    });
  }

  /* ---------- Apparition au défilement ---------- */
  var revealables = document.querySelectorAll('.reveal');
  if (revealables.length && 'IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- Vidéo du héros : lecture différée ---------- */
  var heroVideo = document.querySelector('[data-hero-video]');
  if (heroVideo) {
    var src = heroVideo.getAttribute('data-src');
    var load = function () {
      if (heroVideo.src) { return; }
      heroVideo.src = src;
      var p = heroVideo.play();
      if (p && p.catch) { p.catch(function () { /* lecture auto refusée */ }); }
    };
    if (reduced) { return; }
    if ('requestIdleCallback' in window) {
      requestIdleCallback(load, { timeout: 2500 });
    } else {
      window.addEventListener('load', load);
    }
  }
})();
