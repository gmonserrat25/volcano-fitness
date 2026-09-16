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

m_wipe = re.search(r'(<div class="wipe" id="wipe"></div>\s*<div class="wipe-logo".*?</div>)', home, re.S)
if not m_wipe: raise SystemExit('no encontré la cortina de entrada en index.html')
preloader = m_wipe.group(1)
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
<meta name="robots" content="noindex, nofollow">
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

# ── iPhone con el sitio real adentro (un iframe, no una captura) ──
def _iphone(pagina, etiqueta="Volcano Fitness"):
    return (
        '<div class="iphone">\n'
        '        <div class="iphone__marco">\n'
        '          <div class="iphone__isla"></div>\n'
        '          <iframe class="iphone__pantalla" src="{}" title="{} visto desde un celular"\n'
        '                  loading="lazy" scrolling="yes"></iframe>\n'
        '        </div>\n'
        '      </div>'
    ).format(pagina, etiqueta)



def _panel(titulo, bajada, foto, pos="center"):
    """Panel a pantalla completa, el mismo componente que usa la home."""
    return (
        '  <section class="panel panel--interior">\n'
        '    <div class="panel__media" style="background-image:url(\'img/{}\');background-position:{}"></div>\n'
        '    <div class="panel__scrim"></div>\n'
        '    <div class="panel__body">\n'
        '      <h1 class="panel__title" data-letras>{}</h1>\n'
        '      <p class="panel__lead" data-sube>{}</p>\n'
        '    </div>\n'
        '  </section>\n'
    ).format(foto, pos, titulo, bajada)



# ── Teléfono dibujado con CSS, con la rutina del día adentro ──
TELEFONO = """<div class="tel">
        <div class="tel__marco">
          <div class="tel__barra"><span></span></div>
          <div class="tel__cuerpo">
            <div class="tel__top">
              <span class="tel__lbl">Hoy &middot; D&iacute;a 2 de 4</span>
              <h3 class="tel__titulo">Tren inferior</h3>
            </div>
            <ul class="tel__lista">
              <li><span class="tel__ej">Sentadilla con barra</span><b>4 &times; 8</b><em>40 kg</em></li>
              <li><span class="tel__ej">Prensa 45&deg;</span><b>3 &times; 12</b><em>100 kg</em></li>
              <li><span class="tel__ej">Peso muerto rumano</span><b>3 &times; 10</b><em>35 kg</em></li>
              <li><span class="tel__ej">B&uacute;lgaras</span><b>3 &times; 10</b><em>10 kg</em></li>
              <li class="tel__mas"><span>y 3 ejercicios m&aacute;s</span></li>
            </ul>
            <div class="tel__pie">
              <span class="tel__check">&#10003;</span> Carg&aacute; tus kilos al terminar
            </div>
          </div>
        </div>
      </div>"""


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

    <aside class="vista-movil">
      <div class="vista-movil__txt">
        <span class="lbl">As&iacute; se ve en el celular</span>
        <h2 class="seccion__tit">La rutina, donde entren&aacute;s</h2>
        <p>No hace falta acordarse de nada: abr&iacute;s y lo primero que ves es el trabajo
        del d&iacute;a, con los kilos de la &uacute;ltima vez al lado de cada ejercicio.</p>
        <p class="vista-movil__nota">Es la pantalla de verdad, no una foto: tocala y
        prob&aacute;la.</p>
      </div>
      {_iphone("socios.html?demo=1")}
    </aside>

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
    ("gym.jpg",           "Las cintas, contra el ventanal", ""),
    ("hero-2.jpg",        "Barras y discos", ""),
    ("entrenamientos.jpg","Las máquinas de tren inferior", ""),
    ("contacto.jpg",      "La sala, bajo los arcos de luz", ""),
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

  <section class="ig">
    <div class="ig__txt">
      <span class="lbl">D&iacute;a a d&iacute;a</span>
      <h2 class="seccion__tit">Mir&aacute; c&oacute;mo es entrenar ac&aacute;</h2>
      <p>En Instagram subimos las clases, las rutinas y c&oacute;mo va quedando el lugar.
      Es la forma m&aacute;s honesta de ver el gimnasio antes de venir.</p>
      <a class="pill" href="https://instagram.com/volcano_fitnesslafalda"
         target="_blank" rel="noopener">
        <svg class="ig__ico" viewBox="0 0 24 24" aria-hidden="true">
          <rect x="2.5" y="2.5" width="19" height="19" rx="5.4"/>
          <circle cx="12" cy="12" r="4.6"/>
          <circle class="ig__pto" cx="17.6" cy="6.4" r="1.3"/>
        </svg>
        @volcano_fitnesslafalda
      </a>
    </div>
    <div class="ig__tira">
      <figure style="background-image:url('img/hero-2.jpg')"></figure>
      <figure style="background-image:url('img/entrenamientos.jpg')"></figure>
      <figure style="background-image:url('img/gym.jpg')"></figure>
      <figure style="background-image:url('img/profes.jpg')"></figure>
    </div>
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




# ─────────────────────────── Entrenamientos ──────────────────────────────
import urllib.parse as _up
WA = "5493548592487"
def _wa(t): return f"https://wa.me/{WA}?text={_up.quote(t)}"

anclas = ["musculacion","funcional","personalizado","acondicionamiento"]

disciplinas = [
    ("Musculación", "hero-2.jpg",
     "Sala completa con jaula, multipower, bancos, mancuernas y peso libre. Entrenás con "
     "tu rutina, corregida y actualizada por tu entrenador.",
     ["Todos los niveles", "Rutina propia", "Sin turno"],
     "Quiero saber más de musculación", _wa("Hola! Quiero saber más sobre musculación en Volcano.")),

    ("Funcional", "contacto.jpg",
     "Clases en grupo, circuitos que cambian todas las semanas y trabajo de fuerza, "
     "resistencia y movilidad. La clase que más se llena.",
     ["En grupo", "Con reserva", "45 minutos"],
     "Consultar horarios de funcional", _wa("Hola! Quiero consultar los horarios de funcional.")),

    ("Entrenamiento personalizado", "profes.jpg",
     "Uno a uno con tu entrenador. Para arrancar de cero, volver después de una lesión "
     "o romper un techo que no se mueve hace meses.",
     ["Uno a uno", "Con turno", "Plan a medida"],
     "Pedir una evaluación", _wa("Hola! Quiero pedir una evaluación para entrenamiento personalizado.")),

    ("Acondicionamiento", "gym.jpg",
     "Cintas y bicicletas frente a los ventanales. Plan de cardio que se ajusta a tu "
     "estado actual y va subiendo con vos.",
     ["Por tu cuenta", "Sin turno", "Con seguimiento"],
     "Consultar por acondicionamiento", _wa("Hola! Quiero consultar por acondicionamiento en Volcano.")),
]

tarjetas = "\n".join(
    f"""      <article class="disc" id="{anclas[i]}">
        <div class="disc__foto"><img src="img/{img}" alt="{nom}" loading="lazy"></div>
        <div class="disc__txt">
          <h2 class="disc__nom">{nom}</h2>
          <p class="disc__desc">{desc}</p>
          <ul class="disc__tags">{''.join(f'<li>{t}</li>' for t in tags)}</ul>
          <a class="pill pill--sm" href="{href}" target="_blank" rel="noopener">{cta}</a>
        </div>
      </article>""" for i,(nom, img, desc, tags, cta, href) in enumerate(disciplinas))

CONTENIDO['entrenamientos'] = f"""  <header class="cabecera">
    <span class="lbl">Qué hacemos</span>
    <h1 class="cabecera__titulo">Entrenamientos</h1>
    <p class="cabecera__bajada">Vengas de donde vengas, hay una forma de entrenar para vos.
    Todas incluyen el seguimiento de un entrenador.</p>
  </header>

  <section class="discs">
{tarjetas}
  </section>

  <section class="destacado">
    <div class="destacado__txt">
      <span class="lbl">Incluido en todos los planes</span>
      <h2 class="seccion__tit">Tu rutina, siempre a mano</h2>
      <p>Entrás con tu usuario y ahí está el trabajo del día: los ejercicios, las series y
      los kilos que levantaste la última vez. Tu entrenador la actualiza y te llega al toque.</p>
      <a class="pill" href="rutina.html">Ver cómo funciona</a>
    </div>
    <div class="destacado__tel">{TELEFONO}</div>
  </section>

  <section class="cierre">
    <p class="cierre__aviso">¿No sabés por dónde empezar? Escribinos y lo vemos juntos.</p>
    <a class="pill pill--ghost" href="{_wa('Hola! No sé por dónde empezar, me orientan?')}"
       target="_blank" rel="noopener">Escribinos</a>
  </section>
"""


# ─────────────────────────── Somos Volcano ───────────────────────────────
pilares = [
    ("Tu rutina", "Nadie entrena a ciegas. Tu entrenador te arma el plan según de dónde "
     "venís y a dónde querés llegar, y lo va corrigiendo. Lo tenés siempre a mano, con los "
     "kilos de la última vez al lado de cada ejercicio."),
    ("El acompañamiento", "No te dejamos solo frente a la máquina. Te miramos la técnica, "
     "ajustamos las cargas y te damos una mano el día que no tenés ganas. Esa es la parte "
     "que hace la diferencia entre entrenar y sólo ir al gimnasio."),
    ("El lugar", "Equipamiento nuevo y espacio suficiente para entrenar sin esperar turno. "
     "Paredes oscuras, luz cálida y música: un lugar al que dan ganas de volver."),
    ("El ritmo", "La constancia le gana a la intensidad. Preferimos que vengas tres veces "
     "por semana durante un año antes que cinco veces durante un mes. Por eso medimos el "
     "progreso: para que lo veas y no aflojes."),
]
pilares_html = "\n".join(
    f"""      <article class="pilar">
        <span class="pilar__n">{i:02d}</span>
        <h3 class="pilar__tit">{t}</h3>
        <p>{d}</p>
      </article>""" for i,(t,d) in enumerate(pilares, 1))

faq = [
    ("¿Sirve si nunca entrené?",
     "Sí, y es el caso más común. Se arranca con una evaluación para ver de dónde partís, "
     "y el plan se arma desde ahí. Nadie te va a tirar a la sala a ver cómo te las arreglás."),
    ("¿Hace falta reservar?",
     "Para la sala no: venís en el horario que te quede bien. Para las clases de funcional y "
     "para los turnos uno a uno sí, porque los cupos son limitados."),
    ("¿Qué llevo la primera vez?",
     "Ropa cómoda, calzado deportivo, una toalla y agua. Nada más."),
    ("¿Puedo probar antes de asociarme?",
     "Sí. La primera clase es de prueba y no tiene costo. Escribinos por WhatsApp y "
     "arreglamos el día."),
    ("¿Dónde están y en qué horarios?",
     "En Sarmiento 518, La Falda. Lunes a viernes de 7 a 12 y de 14 a 22, sábados de 9 a 12."),
]
faq_html = "\n".join(
    f"""      <details class="faq">
        <summary>{q}</summary>
        <p>{r}</p>
      </details>""" for q,r in faq)

CONTENIDO['somos'] = f"""""" + _panel("Somos Volcano", "Un gimnasio donde se entrena en serio y se pasa bien. Música fuerte, buenas vibras y entrenos que te hacen sudar pero también reír.", "contacto.jpg") + """
  <section class="intro-dos">
    <div class="intro-dos__txt">
      <h2 class="seccion__tit">Cómo empezó</h2>
      <p>[COMPLETAR: en qué año abrió Volcano, quién lo fundó y por qué. Dos o tres párrafos
      contando la historia real del gimnasio: de dónde salió la idea, cómo era el primer
      local y cómo se llegó al de ahora.]</p>
      <p>Hoy estamos en Sarmiento 518, en La Falda, con equipamiento nuevo y un equipo que
      conoce a cada uno de los que entrena acá.</p>
    </div>
    <figure class="intro-dos__foto">
      <img src="img/contacto.jpg" alt="El equipo de Volcano Fitness" loading="lazy">
    </figure>
  </section>

  <section class="mision">
    <div class="mision__txt">
      <span class="lbl">Qué buscamos</span>
      <h2 class="seccion__tit">Que entrenar te dure toda la vida</h2>
      <p>No creemos en los planes de tres semanas ni en los resultados de un verano. Nos
      interesa que aprendas a entrenar, que entiendas por qué hacés cada ejercicio y que
      sigas viniendo cuando se te pase el envión del principio.</p>
    </div>
    <ul class="mision__lista">
      <li>Entrenadores que corrigen y explican</li>
      <li>Un plan armado para vos, no uno genérico</li>
      <li>Progreso medido, para que lo veas</li>
      <li>Equipamiento nuevo y sin esperas</li>
      <li>Un lugar donde nadie te mira raro</li>
    </ul>
  </section>

  <section class="pilares-sec">
    <div class="cabecera-sec">
      <span class="lbl">Cómo trabajamos</span>
      <h2 class="seccion__tit">Cuatro cosas que no negociamos</h2>
    </div>
    <div class="pilares">
{pilares_html}
    </div>
  </section>

  <section class="faqs">
    <div class="cabecera-sec">
      <span class="lbl">Preguntas</span>
      <h2 class="seccion__tit">Lo que más nos preguntan</h2>
    </div>
    <div class="faqs__lista">
{faq_html}
    </div>
  </section>

  <section class="cierre">
    <p class="cierre__aviso">La primera clase es de prueba y no tiene costo.</p>
    <a class="pill" href="{_wa('Hola! Quiero probar una clase en Volcano.')}"
       target="_blank" rel="noopener">Probá una clase</a>
  </section>
"""


# ────────────────────────────── Precios ──────────────────────────────────
planes = [
    ("Libre", "Para quien ya sabe lo que hace y quiere entrenar por su cuenta.",
     ["Sala y cardio sin límite", "Tu rutina en el área de socios", "Seguimiento del entrenador"], False),
    ("Full", "El más elegido: sumás las clases en grupo y el seguimiento completo.",
     ["Todo lo del plan Libre", "Clases de funcional", "Evaluación cada 3 meses", "Reserva de clases"], True),
    ("Personalizado", "Uno a uno con tu entrenador, con turnos reservados para vos.",
     ["Todo lo del plan Full", "Turnos uno a uno", "Plan ajustado semana a semana"], False),
]
planes_html = "\n".join(
    '      <article class="plan{}">\n{}        <h3 class="plan__nom">{}</h3>\n'
    '        <p class="plan__desc">{}</p>\n'
    '        <p class="plan__precio"><span class="plan__signo">$</span><em>[—]</em><small>/mes</small></p>\n'
    '        <ul class="plan__lista">{}</ul>\n'
    '        <a class="pill{}" href="{}" target="_blank" rel="noopener">Consultar</a>\n'
    '      </article>'.format(
        ' plan--destacado' if dest else '',
        '        <span class="plan__tag">El más elegido</span>\n' if dest else '',
        n, d, ''.join('<li>{}</li>'.format(x) for x in items),
        '' if dest else ' pill--ghost',
        _wa('Hola! Quiero consultar el plan ' + n + '.'))
    for n, d, items, dest in planes)

CONTENIDO['precios'] = (
    '  <header class="cabecera">\n'
    '    <span class="lbl">Planes</span>\n'
    '    <h1 class="cabecera__titulo">Precios</h1>\n'
    '    <p class="cabecera__bajada">Sin matr&iacute;cula y sin permanencia. La primera clase es\n'
    '    de prueba y no tiene costo.</p>\n'
    '  </header>\n\n'
    '  <section class="planes">\n' + planes_html + '\n  </section>\n\n'
    '  <p class="planes__nota"><strong>Los valores est&aacute;n por confirmar.</strong> '
    'Escribinos y te pasamos el precio actualizado.</p>\n\n'
    '  <section class="faqs">\n'
    '    <div class="cabecera-sec"><span class="lbl">Sobre los planes</span>\n'
    '      <h2 class="seccion__tit">Antes de decidir</h2></div>\n'
    '    <div class="faqs__lista">\n'
    '      <details class="faq"><summary>&iquest;Hay que firmar permanencia?</summary>\n'
    '        <p>No. Los planes son mes a mes y pod&eacute;s cambiar o dar de baja cuando quieras.</p></details>\n'
    '      <details class="faq"><summary>&iquest;C&oacute;mo se paga?</summary>\n'
    '        <p>[COMPLETAR: efectivo, transferencia, d&eacute;bito o tarjeta. Aclarar si hay\n'
    '        descuento por pago adelantado.]</p></details>\n'
    '      <details class="faq"><summary>&iquest;Tienen plan para estudiantes o familias?</summary>\n'
    '        <p>[COMPLETAR si existe. Si no, se saca esta pregunta.]</p></details>\n'
    '      <details class="faq"><summary>&iquest;Puedo congelar el plan si viajo?</summary>\n'
    '        <p>[COMPLETAR las condiciones.]</p></details>\n'
    '    </div>\n  </section>\n\n'
    '  <section class="cierre">\n'
    '    <p class="cierre__aviso">&iquest;No sab&eacute;s qu&eacute; plan te conviene? Contanos c&oacute;mo\n'
    '    entren&aacute;s y lo vemos.</p>\n'
    '    <a class="pill" href="' + _wa('Hola! Quiero que me ayuden a elegir un plan.') + '"\n'
    '       target="_blank" rel="noopener">Escribinos</a>\n'
    '  </section>\n')

# ────────────────────────────── Contacto ─────────────────────────────────
def _via(href, lbl, dato, pie, ext=True):
    if href:
        tgt = ' target="_blank" rel="noopener"' if ext else ''
        ini = '      <a class="via" href="{}"{}>'.format(href, tgt); fin = '      </a>'
    else:
        ini = '      <div class="via via--info">'; fin = '      </div>'
    return (ini + '\n        <span class="via__lbl">{}</span>\n'
            '        <span class="via__dato">{}</span>\n'
            '        <span class="via__pie">{}</span>\n'.format(lbl, dato, pie) + fin)

_vias = "\n".join([
    _via(_wa('Hola! Quiero hacer una consulta.'), 'WhatsApp', '3548 59-2487', 'Lo m&aacute;s r&aacute;pido'),
    _via('tel:+543548592487', 'Tel&eacute;fono', '3548 59-2487', 'En horario de atenci&oacute;n', False),
    _via('https://instagram.com/volcano_fitnesslafalda', 'Instagram', '@volcano_fitnesslafalda', 'Ah&iacute; subimos el d&iacute;a a d&iacute;a'),
    _via(None, 'D&oacute;nde estamos', 'Sarmiento 518', 'La Falda, C&oacute;rdoba'),
    _via(None, 'Horarios', '7 a 12 y 14 a 22', 'Lunes a viernes &middot; S&aacute;bados 9 a 12'),
])

CONTENIDO['contacto'] = (
    '  <header class="cabecera">\n'
    '    <span class="lbl">Hablemos</span>\n'
    '    <h1 class="cabecera__titulo">Contacto</h1>\n'
    '    <p class="cabecera__bajada">La forma m&aacute;s r&aacute;pida es WhatsApp: contestamos en el\n'
    '    d&iacute;a. Tambi&eacute;n pod&eacute;s pasar por el gimnasio.</p>\n'
    '  </header>\n\n'
    '  <section class="contacto-grid">\n'
    '    <div class="contacto-vias">\n' + _vias + '\n    </div>\n'
    '    <div class="donde__mapa">\n'
    '      <iframe title="Mapa: Sarmiento 518, La Falda" loading="lazy"\n'
    '        referrerpolicy="no-referrer-when-downgrade"\n'
    '        src="https://maps.google.com/maps?q=Sarmiento+518,+La+Falda,+C%C3%B3rdoba,+Argentina&amp;z=16&amp;output=embed"></iframe>\n'
    '    </div>\n  </section>\n\n'
    '  <section class="cierre">\n'
    '    <p class="cierre__aviso">&iquest;Quer&eacute;s probar una clase? Decinos qu&eacute; d&iacute;a te queda bien.</p>\n'
    '    <a class="pill" href="' + _wa('Hola! Quiero probar una clase. Que dias tienen lugar?') + '"\n'
    '       target="_blank" rel="noopener">Coordinar una clase</a>\n'
    '  </section>\n')


PAGINAS = {
  'somos.html': ('Somos Volcano — Volcano Fitness',
                  'Quiénes somos, cómo trabajamos y qué podés esperar de Volcano Fitness, el gimnasio de La Falda.',
                  CONTENIDO['somos']),
  'precios.html': ('Precios — Volcano Fitness',
                  'Planes y precios de Volcano Fitness, el gimnasio de La Falda.',
                  CONTENIDO['precios']),
  'contacto.html': ('Contacto — Volcano Fitness',
                  'Cómo contactarnos y dónde estamos: Sarmiento 518, La Falda, Córdoba.',
                  CONTENIDO['contacto']),
  'entrenamientos.html': ('Entrenamientos — Volcano Fitness',
                  'Musculación, funcional, entrenamiento personalizado y acondicionamiento en Volcano Fitness, La Falda.',
                  CONTENIDO['entrenamientos']),
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
