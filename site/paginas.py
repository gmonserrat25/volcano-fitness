#!/usr/bin/env python3
"""Genera las paginas internas (rutina.html, profes.html) reusando el
preloader, el header, el menu y el footer de index.html, para que no se
desincronicen. El contenido propio de cada pagina vive en CONTENIDO.

Se corre despues de tocar el header/menu/footer de index.html.
"""
import re, pathlib

base = pathlib.Path(__file__).parent
home = (base / 'index.html').read_text(encoding='utf-8')

def bloque(marca, cierre):
    m = re.search(r'(<%s\b.*?</%s>)' % (marca, cierre), home, re.S)
    if not m: raise SystemExit('no encontré <%s> en index.html' % marca)
    return m.group(1)

preloader = re.search(r'(<div class="preloader".*?</div>\s*</div>)', home, re.S).group(1)
header    = bloque('header', 'header')
menu      = bloque('nav', 'nav')          # el primero es el menu overlay
footer    = bloque('footer', 'footer')
fuentes   = '\n'.join(re.findall(r'<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>', home))

# en las paginas internas, los anclas de la home tienen que volver a la home
def a_la_home(html):
    return re.sub(r'href="#([a-z-]+)"', r'href="index.html#\1"', html)

menu_i   = a_la_home(menu)
header_i = a_la_home(header)
footer_i = a_la_home(footer)

PLANTILLA = """<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fuentes}
<link rel="stylesheet" href="css/style.css">
</head>
<body class="interior">

{preloader}

{header}

{menu}

<main class="pagina">
{contenido}
</main>

{footer}

<script src="js/main.js"></script>
</body>
</html>
"""

CONTENIDO = {}

# ─────────────────────────────── Tu rutina ───────────────────────────────
ejercicios = [
    ("Sentadilla con barra",        "4", "8",        "90 s", "40 kg"),
    ("Prensa 45°",                  "3", "12",       "75 s", "100 kg"),
    ("Peso muerto rumano",          "3", "10",       "90 s", "35 kg"),
    ("Búlgaras con mancuernas",     "3", "10 x pierna", "60 s", "10 kg"),
    ("Extensión de cuádriceps",     "3", "15",       "45 s", "30 kg"),
    ("Camilla femoral",             "3", "12",       "45 s", "25 kg"),
    ("Elevación de gemelos",        "4", "20",       "40 s", "50 kg"),
]
filas = '\n'.join(
    f"""        <tr>
          <td class="rt__n">{i}</td>
          <td class="rt__ej">{n}</td>
          <td class="rt__num">{s}</td>
          <td class="rt__num">{r}</td>
          <td class="rt__num rt__desc">{d}</td>
          <td class="rt__num rt__peso">{p}</td>
        </tr>""" for i,(n,s,r,d,p) in enumerate(ejercicios, 1))

CONTENIDO['rutina'] = f"""  <header class="cabecera">
    <span class="lbl">Tu rutina · Día 2 de 4</span>
    <h1 class="cabecera__titulo">Tren inferior completo</h1>
    <p class="cabecera__bajada">Mirá el trabajo del día y empezá. Los kilos que ves
    al final son los de la última vez que lo hiciste.</p>
  </header>

  <section class="rutina">
    <div class="tabla-scroll">
      <table class="rt">
        <caption class="visualmente-oculto">Ejercicios del día, con series, repeticiones, descanso y el peso de la última sesión</caption>
        <thead>
          <tr>
            <th scope="col"><span class="visualmente-oculto">Orden</span></th>
            <th scope="col">Ejercicio</th>
            <th scope="col">Series</th>
            <th scope="col">Reps</th>
            <th scope="col">Descanso</th>
            <th scope="col">La última vez</th>
          </tr>
        </thead>
        <tbody>
{filas}
        </tbody>
      </table>
    </div>

    <aside class="nota">
      <h2>Antes de empezar</h2>
      <p>Diez minutos de bici o cinta suave y movilidad de cadera. Si algo te molesta,
      pará y avisale a tu entrenador: se cambia el ejercicio, no se soporta.</p>
    </aside>

    <div class="cierre">
      <p class="cierre__aviso">Esta es una rutina de ejemplo, para mostrar cómo se ve.
      La tuya la arma tu entrenador.</p>
      <a class="pill" href="index.html#contacto">Pedí la tuya</a>
    </div>
  </section>
"""

# ──────────────────────────────── Los profes ─────────────────────────────
silueta = """<svg class="silueta" viewBox="0 0 64 64" aria-hidden="true">
            <circle cx="32" cy="23" r="12"/>
            <path d="M8 60c0-13.3 10.7-22 24-22s24 8.7 24 22"/>
          </svg>"""

CONTENIDO['profes'] = f"""  <header class="cabecera">
    <span class="lbl">Nuestro equipo</span>
    <h1 class="cabecera__titulo">Entrenadores</h1>
    <p class="cabecera__bajada">No te dejan solo frente a la máquina: corrigen tu técnica, ajustan las cargas
    y te acompañan en cada etapa.</p>
  </header>

  <section class="equipo">
    <article class="profe">
      <div class="profe__foto">
        <img src="img/profe-ludmi.jpg" alt="Ludmi Porrino" width="900" height="1200" loading="lazy">
      </div>
      <div class="profe__datos">
        <h2 class="profe__nombre">Ludmi Porrino</h2>
      </div>
    </article>

    <article class="profe profe--vacio">
      <div class="profe__foto">
        <div class="profe__ph">
          {silueta}
        </div>
      </div>
      <div class="profe__datos">
        <h2 class="profe__nombre">&nbsp;</h2>
      </div>
    </article>

    <article class="profe profe--vacio">
      <div class="profe__foto">
        <div class="profe__ph">
          {silueta}
        </div>
      </div>
      <div class="profe__datos">
        <h2 class="profe__nombre">&nbsp;</h2>
      </div>
    </article>
  </section>
"""


# ──────────────────────────────── El gym ─────────────────────────────────
fotos = [
    ("hero-1.jpg",        "Los racks, con la luz cálida detrás", "ancha"),
    ("hero-3.jpg",        "La sala principal", "alta"),
    ("hero-2.jpg",        "Barras y discos", "alta"),
    ("gym.jpg",           "Las cintas, contra el ventanal", ""),
    ("entrenamientos.jpg","Las máquinas de tren inferior", ""),
    ("hero-4.jpg",        "La jaula y el cruce de poleas", ""),
    ("historias.jpg",     "Las poleas, contra la pared negra", ""),
]
galeria = '\n'.join(
    f'      <figure class="shot {c}"><img src="img/{f}" alt="{a}" loading="lazy">'
    f'<figcaption>{a}</figcaption></figure>' for f,a,c in fotos)

equipo = [
    ("Fuerza", [
        "Jaula de sentadillas con barra olímpica y discos",
        "Multipower (barra guiada)",
        "Bancos planos y regulables",
        "Mancuernas con su rack",
        "Barra de dominadas",
    ]),
    ("Máquinas", [
        "Cruce de poleas y multiestación",
        "Extensión de cuádriceps",
        "Camilla femoral",
    ]),
    ("Cardio", [
        "Cintas de correr con pantalla",
        "Bicicletas fijas",
    ]),
    ("La sala", [
        "Espejos de pared entera",
        "Pantallas y equipo de música",
        "Ventanales a la calle, con luz natural",
    ]),
]
listas = '\n'.join(
    '      <div class="equipo__grupo">\n'
    f'        <h3 class="equipo__tit">{t}</h3>\n        <ul>\n'
    + '\n'.join(f'          <li>{x}</li>' for x in items)
    + '\n        </ul>\n      </div>' for t, items in equipo)

DIRECCION = "Sarmiento 518"
CIUDAD = "La Falda, Córdoba"
MAPA_Q = "Sarmiento+518,+La+Falda,+C%C3%B3rdoba,+Argentina"

CONTENIDO['gym'] = f"""  <header class="cabecera">
    <span class="lbl">Las instalaciones</span>
    <h1 class="cabecera__titulo">El gimnasio</h1>
    <p class="cabecera__bajada">Paredes negras, luz cálida detrás de los racks y ventanales
    a la calle. Equipamiento nuevo y espacio suficiente para entrenar sin esperar turno.</p>
  </header>

  <section class="galeria">
{galeria}
  </section>

  <section class="equipo-lista">
    <h2 class="seccion__tit">Qué vas a encontrar</h2>
    <div class="equipo__grid">
{listas}
    </div>
    <p class="equipo__nota">Si buscás algo puntual y no lo ves en la lista, preguntanos:
    el equipamiento se sigue sumando.</p>
  </section>

  <section class="donde">
    <div class="donde__datos">
      <h2 class="seccion__tit">Dónde estamos</h2>
      <p class="donde__dir">{DIRECCION}<br><span>{CIUDAD}</span></p>
      <dl class="donde__dl">
        <dt>Horarios</dt><dd>Lunes a viernes, 7 a 12 y 14 a 22 h<br>Sábados, 9 a 12 h</dd>
        <dt>Teléfono</dt><dd><a href="tel:+543548592487">3548 59-2487</a> · <a href="https://wa.me/5493548592487?text=Hola%21%20Quiero%20probar%20una%20clase%20en%20Volcano." target="_blank" rel="noopener">WhatsApp</a></dd>
      </dl>
      <div class="donde__acciones">
        <a class="pill" href="https://www.google.com/maps/dir/?api=1&amp;destination={MAPA_Q}"
           target="_blank" rel="noopener">Cómo llegar</a>
        <a class="pill pill--ghost" href="index.html#contacto">Probá una clase</a>
      </div>
    </div>
    <div class="donde__mapa">
      <iframe title="Mapa: {DIRECCION}, {CIUDAD}" loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        src="https://maps.google.com/maps?q={MAPA_Q}&amp;z=16&amp;output=embed"></iframe>
    </div>
  </section>
"""

PAGINAS = {
  'gym.html':    ('El gimnasio — Volcano Fitness',
                  'El gimnasio de Volcano Fitness en Sarmiento 518, La Falda: equipamiento, fotos y cómo llegar.',
                  CONTENIDO['gym']),
  'rutina.html': ('Tu rutina — Volcano Fitness',
                  'La rutina del día para los socios de Volcano Fitness: ejercicios, series, repeticiones y los kilos de la última vez.',
                  CONTENIDO['rutina']),
  'profes.html': ('Entrenadores — Volcano Fitness',
                  'El equipo de entrenadores de Volcano Fitness, el gimnasio de La Falda.',
                  CONTENIDO['profes']),
}

for archivo, (titulo, desc, contenido) in PAGINAS.items():
    (base / archivo).write_text(PLANTILLA.format(
        titulo=titulo, desc=desc, fuentes=fuentes,
        preloader=preloader, header=header_i, menu=menu_i,
        footer=footer_i, contenido=contenido), encoding='utf-8')
    print('generada', archivo)
