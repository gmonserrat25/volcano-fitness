/* Volcano Fitness · v2
   Comportamiento de la maquetación calcada del shot de Dribbble:
   menú de celular, pestañas, acordeón, testimonios y entradas al scrollear. */
(function () {
  'use strict';

  /* ── Año del pie ── */
  var anio = document.getElementById('anio');
  if (anio) anio.textContent = new Date().getFullYear();

  /* ── Cabecera: sombra al despegarse de arriba ── */
  var cab = document.getElementById('cab');
  if (cab) {
    var pegar = function () { cab.classList.toggle('is-pegada', window.scrollY > 8); };
    pegar();
    window.addEventListener('scroll', pegar, { passive: true });
  }

  /* ── Menú del celular ── */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var abierto = nav.classList.toggle('is-abierto');
      burger.classList.toggle('is-abierto', abierto);
      burger.setAttribute('aria-expanded', abierto ? 'true' : 'false');
      burger.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
    });
    // al elegir una sección, el menú se cierra solo
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('is-abierto');
        burger.classList.remove('is-abierto');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ── Pestañas de "Más sobre nosotros" ── */
  var pest = document.querySelector('.pest');
  if (pest) {
    pest.addEventListener('click', function (e) {
      var btn = e.target.closest('[role="tab"]');
      if (!btn) return;
      pest.querySelectorAll('[role="tab"]').forEach(function (b) {
        var activo = b === btn;
        b.setAttribute('aria-selected', activo ? 'true' : 'false');
        var panel = document.getElementById(b.getAttribute('aria-controls'));
        if (!panel) return;
        panel.classList.toggle('is-activo', activo);
        if (activo) panel.removeAttribute('hidden'); else panel.setAttribute('hidden', '');
      });
    });
  }

  /* ── Acordeones ──
     Se abren de a uno, como en la referencia. Hay uno en la home y otro en
     varias páginas internas, así que se enganchan todos. */
  document.querySelectorAll('.acordeon').forEach(function (acordeon) {
    acordeon.addEventListener('click', function (e) {
      var cabAcor = e.target.closest('.acor__cab');
      if (!cabAcor) return;
      var item = cabAcor.parentElement;
      var abrir = !item.classList.contains('is-abierto');
      acordeon.querySelectorAll('.acor').forEach(function (a) {
        a.classList.remove('is-abierto');
        a.querySelector('.acor__cab').setAttribute('aria-expanded', 'false');
      });
      if (abrir) {
        item.classList.add('is-abierto');
        cabAcor.setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* ── Testimonios: los tres nombres cambian la cita ── */
  var nombres = document.querySelector('.testi__nombres');
  var cita = document.getElementById('testi-txt');
  if (nombres && cita) {
    nombres.addEventListener('click', function (e) {
      var btn = e.target.closest('[role="tab"]');
      if (!btn) return;
      nombres.querySelectorAll('[role="tab"]').forEach(function (b) {
        b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
      });
      cita.textContent = btn.getAttribute('data-cita') || cita.textContent;
    });
  }

  /* ── Las tres tarjetas blancas: la que tocás queda "activa" ── */
  var incluye = document.querySelector('.incluye__grid');
  if (incluye) {
    incluye.addEventListener('mouseover', function (e) {
      var tarjeta = e.target.closest('.inc');
      if (!tarjeta) return;
      incluye.querySelectorAll('.inc').forEach(function (i) {
        i.classList.toggle('is-activa', i === tarjeta);
      });
    });
  }

  /* ── Carrusel del hero ──
     Las portadas se pasan solas, sin controles: las pastillas PREV/NEXT del
     diseño original se dieron de baja. Antes esto se frenaba mientras el
     mouse estaba sobre el hero, y como el hero ocupa la pantalla entera
     bastaba con dejar el puntero quieto para que no girara nunca.
     Las diapositivas salen del HTML: para cambiarlas no hace falta tocar
     esto. Lo único que lo detiene es la pestaña en segundo plano, y no
     arranca si el sistema pide menos movimiento. */
  var hero = document.querySelector('.hero');
  var slides = hero ? [].slice.call(hero.querySelectorAll('.hero__slide')) : [];

  if (hero && slides.length > 1) {
    var actual = 0;
    var solo = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var reloj = null;
    var ESPERA = 7000;

    function mostrar(i) {
      actual = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        var activa = n === actual;
        s.classList.toggle('is-activa', activa);
        // la de atrás no debería quedar leyéndose ni consumiendo CPU
        s.setAttribute('aria-hidden', activa ? 'false' : 'true');
        var v = s.querySelector('video');
        if (!v) return;
        if (activa) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else v.pause();
      });
    }

    function arrancar() {
      if (solo || reloj) return;
      reloj = setInterval(function () { mostrar(actual + 1); }, ESPERA);
    }
    function frenar() {
      if (!reloj) return;
      clearInterval(reloj);
      reloj = null;
    }

    // con la pestaña en segundo plano no tiene sentido que siga girando
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) frenar(); else arrancar();
    });

    mostrar(0);
    arrancar();
  }

  /* ── Entradas al scrollear ── */
  var animables = document.querySelectorAll('[data-sube]');
  if (!('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    animables.forEach(function (el) { el.classList.add('is-visible'); });
    return;
  }
  var obs = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (ent) {
      if (!ent.isIntersecting) return;
      ent.target.classList.add('is-visible');
      obs.unobserve(ent.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  animables.forEach(function (el) { obs.observe(el); });

}());
