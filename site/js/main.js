/* Volcano Fitness — comportamiento calcado de go180.nl */
(function () {
  'use strict';

  /* ── 0 · Preloader: logo, luego cortina diagonal hacia arriba ── */
  var pre = document.getElementById('preloader');
  function dropCurtain() {
    if (!pre) return;
    pre.classList.add('is-out');
    setTimeout(function () { pre.classList.add('is-done'); }, 1200);
  }
  window.addEventListener('load', function () { setTimeout(dropCurtain, 900); });
  setTimeout(dropCurtain, 4000); // red lenta: no dejar la cortina colgada

  /* ── 1 · Menú overlay ── */
  var burger = document.getElementById('burger');
  var menu = document.getElementById('menu');

  function setMenu(open) {
    document.body.classList.toggle('is-menu-open', open);
    document.body.classList.toggle('is-locked', open);
    menu.classList.toggle('is-open', open);
    menu.setAttribute('aria-hidden', String(!open));
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  }

  burger.addEventListener('click', function () {
    setMenu(!menu.classList.contains('is-open'));
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu.classList.contains('is-open')) setMenu(false);
  });

  /* Submenú desplegable (el "Programs >" del original) */
  menu.querySelectorAll('.has-sub > a').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var li = a.parentElement;
      if (!li.classList.contains('is-open')) {
        e.preventDefault();
        li.classList.add('is-open');
      }
    });
  });

  /* Cerrar al navegar */
  menu.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function () {
      if (!a.parentElement.classList.contains('has-sub')) setMenu(false);
    });
  });

  /* ── 2 · Dots: sección activa + salto ── */
  var dots = Array.prototype.slice.call(document.querySelectorAll('.dots button'));
  var targets = dots.map(function (d) { return document.getElementById(d.dataset.go); });

  dots.forEach(function (d) {
    d.addEventListener('click', function () {
      var el = document.getElementById(d.dataset.go);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  /* Sección activa = la que cubre el centro del viewport */
  var ticking = false;
  function syncDots() {
    ticking = false;
    var mid = window.innerHeight / 2;
    var best = 0, bestD = Infinity;
    for (var k = 0; k < targets.length; k++) {
      if (!targets[k]) continue;
      var r = targets[k].getBoundingClientRect();
      var d = Math.abs((r.top + r.bottom) / 2 - mid);
      if (d < bestD) { bestD = d; best = k; }
    }
    for (var j = 0; j < dots.length; j++) {
      dots[j].classList.toggle('is-active', j === best);
    }
    /* Los dots sólo mientras estamos sobre los paneles */
    var last = targets[targets.length - 1];
    var past = last ? last.getBoundingClientRect().bottom < mid : false;
    document.body.classList.toggle('is-past-panels', past);
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(syncDots); }
  }, { passive: true });
  window.addEventListener('resize', syncDots, { passive: true });
  syncDots();

  /* ── 3 · Slideshow del hero ──
     Cruce suave entre imágenes. Cada una se acerca de a poco mientras está
     a la vista: eso es lo que da la sensación de movimiento. */
  var show = document.querySelector('[data-slideshow]');
  if (show) {
    var slides = show.querySelectorAll('.slide');
    if (slides.length > 1) {
      var i = 0;
      setInterval(function () {
        slides[i].classList.remove('is-activa');
        i = (i + 1) % slides.length;
        var s = slides[i];
        s.style.animation = 'none';
        void s.offsetWidth;          // fuerza el reinicio de la animación
        s.style.animation = '';
        s.classList.add('is-activa');
      }, 6500);
    }
  }

  /* ── 4 · Año del footer ── */
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
