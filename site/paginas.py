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
    <p class="cabecera__bajada">Entrás, mirás qué te toca hoy y arrancás. Los kilos que ves
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
      pará y avisale a tu profe: se cambia el ejercicio, no se aguanta.</p>
    </aside>

    <div class="cierre">
      <p class="cierre__aviso">Esta es una rutina de ejemplo, para mostrar cómo se ve.
      La tuya te la arma tu profe.</p>
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
    <span class="lbl">El equipo</span>
    <h1 class="cabecera__titulo">Los profes</h1>
    <p class="cabecera__bajada">No te dejan solo con la máquina: te miran, te corrigen y te
    bancan el día que no tenés ganas.</p>
  </header>

  <section class="equipo">
    <article class="profe">
      <div class="profe__foto">
        <img src="img/profe-ludmi.jpg" alt="Ludmi Porrino" width="900" height="1200" loading="lazy">
      </div>
      <div class="profe__datos">
        <h2 class="profe__nombre">Profe Ludmi Porrino</h2>
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

PAGINAS = {
  'rutina.html': ('Tu rutina — Volcano Fitness',
                  'La rutina del día para los socios de Volcano Fitness: ejercicios, series, repeticiones y los kilos de la última vez.',
                  CONTENIDO['rutina']),
  'profes.html': ('Los profes — Volcano Fitness',
                  'El equipo de profes de Volcano Fitness, el gimnasio de La Falda.',
                  CONTENIDO['profes']),
}

for archivo, (titulo, desc, contenido) in PAGINAS.items():
    (base / archivo).write_text(PLANTILLA.format(
        titulo=titulo, desc=desc, fuentes=fuentes,
        preloader=preloader, header=header_i, menu=menu_i,
        footer=footer_i, contenido=contenido), encoding='utf-8')
    print('generada', archivo)
