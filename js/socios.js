/* Área de socios — demostración.
   No hay servidor: todo lo que se carga queda en localStorage de este navegador. */
(function () {
  'use strict';

  var CLAVE = 'volcano.socio';

  /* ── Datos de ejemplo ── */
  var EJERCICIOS = [
    { nom: 'Sentadilla con barra',    series: '4 × 8',        ult: 40  },
    { nom: 'Prensa 45°',              series: '3 × 12',       ult: 100 },
    { nom: 'Peso muerto rumano',      series: '3 × 10',       ult: 35  },
    { nom: 'Búlgaras con mancuernas', series: '3 × 10 x pierna', ult: 10 },
    { nom: 'Extensión de cuádriceps', series: '3 × 15',       ult: 30  },
    { nom: 'Camilla femoral',         series: '3 × 12',       ult: 25  },
    { nom: 'Elevación de gemelos',    series: '4 × 20',       ult: 50  }
  ];

  var PROGRESO = [
    { sem: 'S1', kg: 32 }, { sem: 'S2', kg: 34 }, { sem: 'S3', kg: 36 },
    { sem: 'S4', kg: 38 }, { sem: 'S5', kg: 38 }, { sem: 'S6', kg: 40 }
  ];

  var CLASES = [
    { dia: '17', mes: 'Sep', nom: 'Funcional',   meta: 'Miércoles, 19:00 · quedan 4 lugares' },
    { dia: '19', mes: 'Sep', nom: 'Funcional',   meta: 'Viernes, 19:00 · quedan 7 lugares' },
    { dia: '20', mes: 'Sep', nom: 'Turno con tu entrenador', meta: 'Sábado, 10:00 · uno a uno' }
  ];

  /* ── Estado guardado ── */
  function leer() {
    try { return JSON.parse(localStorage.getItem(CLAVE)) || {}; }
    catch (e) { return {}; }
  }
  function guardar(est) {
    try { localStorage.setItem(CLAVE, JSON.stringify(est)); } catch (e) {}
  }
  var estado = leer();
  estado.hechos = estado.hechos || {};
  estado.kilos = estado.kilos || {};
  estado.reservas = estado.reservas || {};

  /* ── Acceso ── */
  var acceso = document.getElementById('acceso');
  var panel = document.getElementById('panel');
  var input = document.getElementById('nombre');

  function mostrarPanel(nombre) {
    document.getElementById('saludo').textContent = nombre;
    acceso.hidden = true;
    panel.hidden = false;
    document.querySelector('.soc-header').focus?.();
  }

  document.getElementById('entrar').addEventListener('click', function () {
    var nombre = (input.value || '').trim() || 'socio';
    estado.nombre = nombre;
    guardar(estado);
    mostrarPanel(nombre);
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') document.getElementById('entrar').click();
  });

  document.getElementById('salir').addEventListener('click', function () {
    panel.hidden = true;
    acceso.hidden = false;
    input.value = '';
    input.focus();
  });

  /* ── Rutina del día ── */
  var lista = document.getElementById('ejs');

  function pintarEjercicios() {
    lista.innerHTML = '';
    EJERCICIOS.forEach(function (ej, i) {
      var hecho = !!estado.hechos[i];
      var kg = estado.kilos[i] != null ? estado.kilos[i] : ej.ult;

      var li = document.createElement('li');
      li.className = 'ej' + (hecho ? ' is-ok' : '');

      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'ej__check';
      btn.textContent = '✓';
      btn.setAttribute('aria-pressed', String(hecho));
      btn.setAttribute('aria-label', (hecho ? 'Desmarcar ' : 'Marcar como hecho ') + ej.nom);
      btn.addEventListener('click', function () {
        estado.hechos[i] = !estado.hechos[i];
        guardar(estado);
        pintarEjercicios();
      });

      var txt = document.createElement('div');
      var nom = document.createElement('span');
      nom.className = 'ej__nom';
      nom.textContent = ej.nom;
      var meta = document.createElement('span');
      meta.className = 'ej__meta';
      meta.textContent = ej.series + ' · la última vez ' + ej.ult + ' kg';
      txt.appendChild(nom); txt.appendChild(meta);

      var kgBox = document.createElement('div');
      kgBox.className = 'ej__kg';
      var inp = document.createElement('input');
      inp.type = 'number'; inp.min = '0'; inp.step = '2.5'; inp.value = kg;
      inp.id = 'kg-' + i;
      inp.setAttribute('aria-label', 'Kilos en ' + ej.nom);
      inp.addEventListener('change', function () {
        estado.kilos[i] = inp.value;
        guardar(estado);
      });
      var u = document.createElement('span');
      u.textContent = 'kg';
      kgBox.appendChild(inp); kgBox.appendChild(u);

      li.appendChild(btn); li.appendChild(txt); li.appendChild(kgBox);
      lista.appendChild(li);
    });

    var n = EJERCICIOS.filter(function (_, i) { return estado.hechos[i]; }).length;
    document.getElementById('listos').textContent = n;
    document.getElementById('hechos').textContent = n === EJERCICIOS.length ? 3 : 2;
  }

  document.getElementById('terminar').addEventListener('click', function () {
    EJERCICIOS.forEach(function (_, i) { estado.hechos[i] = true; });
    guardar(estado);
    pintarEjercicios();
  });
  document.getElementById('reiniciar').addEventListener('click', function () {
    estado.hechos = {};
    guardar(estado);
    pintarEjercicios();
  });

  /* ── Progreso: barras ancladas a la base, valor sólo en la última y al pasar el mouse ── */
  function pintarGrafico() {
    var graf = document.getElementById('graf');
    var tope = Math.max.apply(null, PROGRESO.map(function (p) { return p.kg; }));
    var piso = Math.min.apply(null, PROGRESO.map(function (p) { return p.kg; }));
    var base = Math.max(0, piso - 6);                       // deja aire abajo sin mentir la escala

    graf.innerHTML = '';
    PROGRESO.forEach(function (p, i) {
      var alto = ((p.kg - base) / (tope - base)) * 100;
      var col = document.createElement('div');
      col.className = 'barra' + (i === PROGRESO.length - 1 ? ' is-ultima' : '');
      col.title = p.sem + ': ' + p.kg + ' kg';

      var val = document.createElement('span');
      val.className = 'barra__val';
      val.textContent = p.kg;

      var fill = document.createElement('div');
      fill.className = 'barra__fill';
      fill.style.height = Math.max(8, alto) + '%';

      var sem = document.createElement('span');
      sem.className = 'barra__sem';
      sem.textContent = p.sem;

      col.appendChild(val); col.appendChild(fill); col.appendChild(sem);
      graf.appendChild(col);
    });

    var tb = document.getElementById('tablaProg');
    tb.innerHTML = PROGRESO.map(function (p) {
      return '<tr><td>' + p.sem + '</td><td class="rt__peso">' + p.kg + ' kg</td></tr>';
    }).join('');
  }

  /* ── Clases ── */
  function pintarClases() {
    var ul = document.getElementById('clases');
    ul.innerHTML = '';
    CLASES.forEach(function (c, i) {
      var res = !!estado.reservas[i];
      var li = document.createElement('li');
      li.className = 'clase' + (res ? ' is-res' : '');
      li.innerHTML =
        '<div class="clase__dia"><b>' + c.dia + '</b><span>' + c.mes + '</span></div>' +
        '<div><span class="clase__nom">' + c.nom + '</span>' +
        '<span class="clase__meta">' + c.meta + '</span></div>';
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'clase__btn';
      b.textContent = res ? '✓ Reservada' : 'Reservar';
      b.addEventListener('click', function () {
        estado.reservas[i] = !estado.reservas[i];
        guardar(estado);
        pintarClases();
      });
      li.appendChild(b);
      ul.appendChild(li);
    });
  }

  pintarEjercicios();
  pintarGrafico();
  pintarClases();
  if (estado.nombre) { input.value = estado.nombre; }

  /* Con ?demo=1 entra derecho al panel: lo usa el iPhone de la página "Tu rutina" */
  if (/[?&]demo=1/.test(location.search)) {
    mostrarPanel(estado.nombre || 'Guada');
  }
})();
