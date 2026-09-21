#!/usr/bin/env python3
"""Genera las paginas internas reusando la barra, la cabecera y el pie de
index.html, para que no se desincronicen. El contenido propio de cada pagina
vive en CONTENIDO.

Desde que la home paso a la maquetacion del shot de Dribbble, estas paginas
usan las mismas piezas que ella: css/estilo.css, js/home.js, la volanta, los
botones, las tarjetas, el acordeon y el filo de pincel. La home vieja quedo en
_plantilla-interna.html y ya no interviene.

Se corre despues de tocar la barra, la cabecera o el pie de index.html.
"""
import pathlib
import re
import urllib.parse as _up

base = pathlib.Path(__file__).parent
home = (base / 'index.html').read_text(encoding='utf-8')


def bloque(patron, que):
    m = re.search(patron, home, re.S)
    if not m:
        raise SystemExit('no encontré %s en index.html' % que)
    return m.group(1)


barra    = bloque(r'(<div class="barra">.*?\n</div>)', 'la barra de arriba')
cabecera = bloque(r'(<header class="cab".*?</header>)', 'la cabecera')
pie      = bloque(r'(<footer class="pie".*?</footer>)', 'el pie')
wpp      = bloque(r'(<a class="wpp".*?</a>)', 'el botón de WhatsApp')
sprite   = bloque(r'(<svg class="sprite-rasgado".*?</svg>)', 'el sprite del filo de pincel')
fuentes  = '\n'.join(re.findall(r'<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>', home))

# El menú de la home apunta a sus propias secciones. Desde una interna, cada
# entrada tiene que llevar a la página de verdad.
A_PAGINA = {
    '#': 'index.html',
    '#somos': 'somos.html',
    '#entrenamientos': 'entrenamientos.html',
    '#equipo': 'profes.html',
    '#gimnasio': 'gym.html',
    '#precios': 'precios.html',
    '#rutina': 'rutina.html',
    '#contacto': 'contacto.html',
}


def a_paginas(html, actual):
    """Reescribe los enlaces del chrome y marca en qué página estamos."""
    html = html.replace(' aria-current="page"', '')

    def cambiar(m):
        destino = A_PAGINA.get(m.group(1))
        return 'href="%s"' % destino if destino else m.group(0)

    html = re.sub(r'href="(#[a-z-]*)"', cambiar, html)
    # La entrada del menú que corresponde a esta página queda marcada
    html = html.replace('<a href="%s"' % actual, '<a href="%s" aria-current="page"' % actual, 1)
    return html


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
<link rel="stylesheet" href="css/estilo.css">
</head>
<body>

{barra}

{cabecera}

<main>
{contenido}
</main>

{pie}

{wpp}

{sprite}

<script src="js/home.js"></script>
</body>
</html>
"""

WA = "5493548592487"


def _wa(t):
    return "https://wa.me/%s?text=%s" % (WA, _up.quote(t))


# ── Piezas que se repiten ────────────────────────────────────────────────
# La tilde sigue en pie sólo para la lista de "qué buscamos" de somos.html,
# que todavía tiene su regla .lista-check svg en el CSS. La flecha del
# acordeón se dio de baja: ahora el <i> va vacío y el signo + / − lo pone
# el CSS, igual que en la home.
TILDE = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
         '<path d="m5 12 4.5 4.5L19 7"/></svg>')


def cabecera_pagina(volanta, titulo, bajada, foto, filo='b'):
    return f"""  <section class="cab-int">
    <div class="cab-int__foto" style="background-image:url('img/{foto}')"></div>
    <div class="cab-int__velo"></div>
    <div class="env cab-int__in">
      <span class="volanta volanta--plana" data-sube>{volanta}</span>
      <h1 data-sube>{titulo}</h1>
      <p class="cab-int__bajada" data-sube>{bajada}</p>
    </div>
    <svg class="filo filo--abajo" preserveAspectRatio="none" aria-hidden="true"><use href="#filo-{filo}"/></svg>
  </section>
"""


def cierre(titulo, texto, cta, href, externo=True, filo='a', encima='blanco'):
    """`encima` es el color de la sección de arriba: el filo se pinta de ese
    color, si no queda una costura entre el gris y el blanco del pincel."""
    tgt = ' target="_blank" rel="noopener"' if externo else ''
    tono = ' filo--gris' if encima == 'gris' else ''
    return f"""
  <section class="cierre">
    <svg class="filo filo--arriba{tono}" preserveAspectRatio="none" aria-hidden="true"><use href="#filo-{filo}"/></svg>
    <div class="env cierre__in" data-sube>
      <h2>{titulo}</h2>
      <p>{texto}</p>
      <a class="btn" href="{href}"{tgt}>{cta}</a>
    </div>
  </section>
"""


def acordeon(items, claro=True):
    clase = 'acordeon acordeon--claro' if claro else 'acordeon'
    filas = []
    for i, (q, r) in enumerate(items):
        abierto = ' is-abierto' if i == 0 else ''
        expand = 'true' if i == 0 else 'false'
        filas.append(f"""        <div class="acor{abierto}">
          <button class="acor__cab" type="button" aria-expanded="{expand}">
            {q}
            <i aria-hidden="true"></i>
          </button>
          <div class="acor__cuerpo"><div><p>{r}</p></div></div>
        </div>""")
    return '      <div class="%s">\n%s\n      </div>' % (clase, '\n'.join(filas))


CONTENIDO = {}

DIRECCION = "Sarmiento 518"
CIUDAD = "La Falda, Córdoba"
MAPA_Q = "Sarmiento+518,+La+Falda,+C%C3%B3rdoba,+Argentina"

MAPA = f"""      <div class="mapa">
        <iframe title="Mapa: {DIRECCION}, {CIUDAD}" loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          src="https://maps.google.com/maps?q={MAPA_Q}&amp;z=16&amp;output=embed"></iframe>
      </div>"""


# ─────────────────────────────── Somos Volcano ───────────────────────────
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
    f"""        <article class="pilar">
          <span class="pilar__n">{i:02d}</span>
          <h3>{t}</h3>
          <p>{d}</p>
        </article>""" for i, (t, d) in enumerate(pilares, 1))

busca = [
    "Entrenadores que corrigen y explican",
    "Un plan armado para vos, no uno genérico",
    "Progreso medido, para que lo veas",
    "Equipamiento nuevo y sin esperas",
    "Un lugar donde nadie te mira raro",
]
busca_html = "\n".join(f'          <li>{TILDE}{x}</li>' for x in busca)

faq_somos = [
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

CONTENIDO['somos'] = (
    cabecera_pagina("Quiénes somos", "Somos Volcano",
                    "Un gimnasio donde se entrena en serio y se pasa bien. Música fuerte, "
                    "buenas vibras y entrenos que te hacen sudar pero también reír.",
                    "contacto.jpg")
    + f"""
  <section class="sec">
    <div class="env duo" data-sube>
      <div class="duo__txt">
        <span class="volanta">La historia</span>
        <h2 class="titulo-sec">Cómo empezó</h2>
        <p>[COMPLETAR: en qué año abrió Volcano, quién lo fundó y por qué. Dos o tres párrafos
        contando la historia real del gimnasio: de dónde salió la idea, cómo era el primer
        local y cómo se llegó al de ahora.]</p>
        <p>Hoy estamos en {DIRECCION}, en La Falda, con equipamiento nuevo y un equipo que
        conoce a cada uno de los que entrena acá.</p>
      </div>
      <div class="duo__foto"><img src="img/contacto.jpg" alt="El equipo de Volcano Fitness" loading="lazy"></div>
    </div>
  </section>

  <section class="sec sec--gris">
    <div class="env duo duo--invertido" data-sube>
      <div class="duo__txt">
        <span class="volanta">Qué buscamos</span>
        <h2 class="titulo-sec">Que entrenar te dure toda la vida</h2>
        <p>No creemos en los planes de tres semanas ni en los resultados de un verano. Nos
        interesa que aprendas a entrenar, que entiendas por qué hacés cada ejercicio y que
        sigas viniendo cuando se te pase el envión del principio.</p>
        <ul class="lista-check">
{busca_html}
        </ul>
      </div>
      <div class="duo__foto"><img src="img/profes.jpg" alt="Entrenamiento con seguimiento en Volcano" loading="lazy"></div>
    </div>
  </section>

  <section class="sec">
    <div class="env">
      <div class="sec__cab sec__cab--centro" data-sube>
        <span class="volanta">Cómo trabajamos</span>
        <h2 class="titulo-sec">Cuatro cosas que no negociamos</h2>
      </div>
      <div class="pilares" data-sube>
{pilares_html}
      </div>
    </div>
  </section>

  <section class="sec sec--gris">
    <div class="env">
      <div class="sec__cab sec__cab--centro" data-sube>
        <span class="volanta">Preguntas</span>
        <h2 class="titulo-sec">Lo que más nos preguntan</h2>
      </div>
      <div data-sube>
{acordeon(faq_somos)}
      </div>
    </div>
  </section>
"""
    + cierre("La primera clase es de prueba y no tiene costo",
             "Venís, entrenás y ves si te gusta. No pagás nada ni dejás datos de tarjeta.",
             "Probá una clase", _wa('Hola! Quiero probar una clase en Volcano.'), encima='gris'))


# ─────────────────────────── Entrenamientos ──────────────────────────────
anclas = ["musculacion", "funcional", "personalizado", "acondicionamiento"]

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

discs = "\n".join(
    f"""      <article class="disc" id="{anclas[i]}" data-sube>
        <div class="disc__foto"><img src="img/{img}" alt="{nom} en Volcano Fitness" loading="lazy"></div>
        <div class="disc__txt">
          <span class="volanta">0{i + 1}</span>
          <h2>{nom}</h2>
          <p>{desc}</p>
          <ul class="tags">{''.join(f'<li>{t}</li>' for t in tags)}</ul>
          <a class="btn" href="{href}" target="_blank" rel="noopener">{cta}</a>
        </div>
      </article>""" for i, (nom, img, desc, tags, cta, href) in enumerate(disciplinas))

CONTENIDO['entrenamientos'] = (
    cabecera_pagina("Qué hacemos", "Entrenamientos",
                    "Vengas de donde vengas, hay una forma de entrenar para vos. "
                    "Todas incluyen el seguimiento de un entrenador.",
                    "entrenamientos.jpg", filo='c')
    + f"""
  <section class="sec">
    <div class="env discs">
{discs}
    </div>
  </section>

  <section class="sec sec--gris">
    <div class="env duo" data-sube>
      <div class="duo__txt">
        <span class="volanta">Incluido en todos los planes</span>
        <h2 class="titulo-sec">Tu rutina, siempre a mano</h2>
        <p>Entrás con tu usuario y ahí está el trabajo del día: los ejercicios, las series y
        los kilos que levantaste la última vez. Tu entrenador la actualiza y te llega al toque.</p>
        <a class="btn" href="rutina.html">Ver cómo funciona</a>
      </div>
      <div class="duo__foto"><img src="img/mockup-celular.jpg" alt="El área de socios de Volcano en el celular" loading="lazy"></div>
    </div>
  </section>
"""
    + cierre("¿No sabés por dónde empezar?",
             "Contanos cómo venís entrenando y lo vemos juntos. Sin compromiso.",
             "Escribinos", _wa('Hola! No sé por dónde empezar, me orientan?'), filo='b', encima='gris'))


# ──────────────────────────────── Los profes ─────────────────────────────
def profe(nombre, rol, foto=None):
    if foto:
        marco = f'<div class="profe__foto"><img src="img/{foto}" alt="{nombre}" loading="lazy"></div>'
    else:
        marco = ('<div class="profe__foto profe__foto--vacia">'
                 '<img src="img/logo.png" alt="" width="520" height="396"></div>')
    return f"""        <article class="profe">
          {marco}
          <h3>{nombre}</h3>
          <span>{rol}</span>
        </article>"""


equipo_html = "\n".join([
    profe("Ludmi Porrino", "Entrenadora", "profe-ludmi.jpg"),
    profe("[COMPLETAR: nombre]", "[COMPLETAR: especialidad]"),
    profe("[COMPLETAR: nombre]", "[COMPLETAR: especialidad]"),
    profe("[COMPLETAR: nombre]", "[COMPLETAR: especialidad]"),
])

CONTENIDO['profes'] = (
    cabecera_pagina("Nuestro equipo", "Entrenadores",
                    "No te dejan solo frente a la máquina: corrigen tu técnica, ajustan "
                    "las cargas y te acompañan en cada etapa.",
                    "profes.jpg")
    + f"""
  <section class="sec">
    <div class="env">
      <div class="equipo__grid" data-sube>
{equipo_html}
      </div>
    </div>
  </section>
"""
    + cierre("Entrenás acompañado desde el primer día",
             "Contanos tu objetivo y te decimos con qué entrenador conviene que arranques.",
             "Hablar con un entrenador", _wa('Hola! Quiero que me orienten con un entrenador.'),
             filo='c'))


# ──────────────────────────────── El gym ─────────────────────────────────
fotos = [
    ("hero-1.jpg", "Los racks, con la luz cálida detrás", "shot--ancha"),
    ("gym.jpg", "Las cintas, contra el ventanal", ""),
    ("hero-2.jpg", "Barras y discos", ""),
    ("entrenamientos.jpg", "Las máquinas de tren inferior", ""),
    ("contacto.jpg", "La sala, bajo los arcos de luz", ""),
]
galeria = '\n'.join(
    f'        <figure class="shot {c}"><img src="img/{f}" alt="{a}" loading="lazy">'
    f'<figcaption>{a}</figcaption></figure>' for f, a, c in fotos)

equipamiento = [
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
equipos_html = '\n'.join(
    '        <div class="equipo-grupo">\n'
    f'          <h3>{t}</h3>\n          <ul>\n'
    + '\n'.join(f'            <li>{x}</li>' for x in items)
    + '\n          </ul>\n        </div>' for t, items in equipamiento)

CONTENIDO['gym'] = (
    cabecera_pagina("Las instalaciones", "El gimnasio",
                    "Paredes negras, luz cálida detrás de los racks y ventanales a la "
                    "calle. Equipamiento nuevo y espacio suficiente para entrenar sin "
                    "esperar turno.",
                    "gym.jpg")
    + f"""
  <section class="sec">
    <div class="env">
      <div class="shots" data-sube>
{galeria}
      </div>
    </div>
  </section>

  <section class="sec sec--gris">
    <div class="env">
      <div class="sec__cab sec__cab--centro" data-sube>
        <span class="volanta">Equipamiento</span>
        <h2 class="titulo-sec">Qué vas a encontrar</h2>
        <p>Si buscás algo puntual y no lo ves en la lista, preguntanos: el equipamiento
        se sigue sumando.</p>
      </div>
      <div class="equipos" data-sube>
{equipos_html}
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="env">
      <div class="sec__cab" data-sube>
        <span class="volanta">Día a día</span>
        <h2 class="titulo-sec">Mirá cómo es entrenar acá</h2>
        <p>En Instagram subimos las clases, las rutinas y cómo va quedando el lugar. Es la
        forma más honesta de ver el gimnasio antes de venir.</p>
        <a class="btn" href="https://instagram.com/volcano_fitnesslafalda" target="_blank" rel="noopener">@volcano_fitnesslafalda</a>
      </div>
      <div class="ig-tira" data-sube>
        <figure style="background-image:url('img/hero-2.jpg')"></figure>
        <figure style="background-image:url('img/entrenamientos.jpg')"></figure>
        <figure style="background-image:url('img/gym.jpg')"></figure>
        <figure style="background-image:url('img/profes.jpg')"></figure>
      </div>
    </div>
  </section>

  <section class="sec sec--gris">
    <div class="env donde" data-sube>
      <div>
        <span class="volanta">Dónde estamos</span>
        <p class="donde__dir">{DIRECCION}<span>{CIUDAD}</span></p>
        <dl class="donde__dl">
          <div><dt>Horarios</dt><dd>Lunes a viernes, 7 a 12 y 14 a 22 h<br>Sábados, 9 a 12 h</dd></div>
          <div><dt>Teléfono</dt><dd><a href="tel:+543548592487">3548 59-2487</a> · <a href="{_wa('Hola! Quiero probar una clase en Volcano.')}" target="_blank" rel="noopener">WhatsApp</a></dd></div>
        </dl>
        <div class="donde__acciones">
          <a class="btn" href="https://www.google.com/maps/dir/?api=1&amp;destination={MAPA_Q}" target="_blank" rel="noopener">Cómo llegar</a>
          <a class="btn btn--linea" href="contacto.html">Probá una clase</a>
        </div>
      </div>
{MAPA}
    </div>
  </section>
""")


# ────────────────────────────── Precios ──────────────────────────────────
# Cada plan traía su icono en un cuadrado azul que sobresalía arriba a la
# izquierda, y cada ítem de la lista su tilde dibujada. Se dieron de baja
# junto con el resto de los iconos, y la lista la ordena la viñeta cuadrada
# que pone el CSS en .plan li::before.

planes = [
    ("Libre", "Para quien ya sabe lo que hace y quiere entrenar por su cuenta.",
     ["Sala y cardio sin límite", "Tu rutina en el área de socios", "Seguimiento del entrenador"], False),
    ("Full", "El más elegido: sumás las clases en grupo y el seguimiento completo.",
     ["Todo lo del plan Libre", "Clases de funcional", "Evaluación cada 3 meses", "Reserva de clases"], True),
    ("Personalizado", "Uno a uno con tu entrenador, con turnos reservados para vos.",
     ["Todo lo del plan Full", "Turnos uno a uno", "Plan ajustado semana a semana"], False),
]

planes_html = "\n".join(
    """        <article class="plan{dest}">
          <h3>{nom}{tag}</h3>
          <!-- Cuando estén los valores: <span class="sig">$</span><span class="num">18000</span><span class="per">/mes</span> -->
          <p class="plan__precio plan__precio--pendiente"><span class="num">A confirmar</span></p>
          <p class="plan__nota">{desc}</p>
          <ul>{items}</ul>
          <a class="btn" href="{href}" target="_blank" rel="noopener">Consultar</a>
        </article>""".format(
        dest=' plan--destacado' if dest else '',
        nom=nom,
        tag=' <span class="volanta" style="margin-left:8px;vertical-align:middle">El más elegido</span>' if dest else '',
        desc=desc,
        items=''.join('<li>%s</li>' % x for x in items),
        href=_wa('Hola! Quiero consultar el plan ' + nom + '.'))
    for nom, desc, items, dest in planes)

faq_precios = [
    ("¿Hay que firmar permanencia?",
     "No. Los planes son mes a mes y podés cambiar o dar de baja cuando quieras. Tampoco "
     "cobramos matrícula."),
    ("¿Cómo se paga?",
     "[COMPLETAR: efectivo, transferencia, débito o tarjeta. Aclarar si hay descuento por "
     "pago adelantado.]"),
    ("¿Tienen plan para estudiantes o familias?",
     "[COMPLETAR si existe. Si no, se saca esta pregunta.]"),
    ("¿Puedo congelar el plan si viajo?",
     "[COMPLETAR las condiciones.]"),
]

CONTENIDO['precios'] = (
    cabecera_pagina("Planes", "Precios",
                    "Sin matrícula y sin permanencia. La primera clase es de prueba y no "
                    "tiene costo.",
                    "hero-1.jpg", filo='a')
    + f"""
  <section class="sec">
    <div class="env">
      <div class="precios__grid" data-sube>
{planes_html}
      </div>
      <p class="precios__pie"><strong>Los valores están por confirmar.</strong>
      Escribinos y te pasamos el precio actualizado.</p>
    </div>
  </section>

  <section class="sec sec--gris">
    <div class="env">
      <div class="sec__cab sec__cab--centro" data-sube>
        <span class="volanta">Sobre los planes</span>
        <h2 class="titulo-sec">Antes de decidir</h2>
      </div>
      <div data-sube>
{acordeon(faq_precios)}
      </div>
    </div>
  </section>
"""
    + cierre("¿No sabés qué plan te conviene?",
             "Contanos cómo entrenás y cuántos días por semana podés venir, y lo vemos.",
             "Escribinos", _wa('Hola! Quiero que me ayuden a elegir un plan.'), filo='c', encima='gris'))


# ────────────────────────────── Contacto ─────────────────────────────────
ICO_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21a9 9 0 1 0-7.8-4.5L3 21l4.5-1.2A9 9 0 0 0 12 21z"/></svg>'
ICO_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/></svg>'
ICO_IG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.4"/>'
          '<circle cx="12" cy="12" r="4.6"/><circle cx="17.6" cy="6.4" r="1.1"/></svg>')
ICO_PIN = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-5.3 7-11a7 7 0 1 0-14 0c0 5.7 7 11 7 11z"/>'
           '<circle cx="12" cy="10" r="2.6"/></svg>')
ICO_RELOJ = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/></svg>'


def via(ico, lbl, dato, pie, href=None, externo=True):
    cuerpo = (f'<span class="via__ico">{ico}</span>\n'
              f'        <span class="via__lbl">{lbl}</span>\n'
              f'        <span class="via__dato">{dato}</span>\n'
              f'        <span class="via__pie">{pie}</span>')
    if href:
        tgt = ' target="_blank" rel="noopener"' if externo else ''
        return f'        <a class="via" href="{href}"{tgt}>\n        {cuerpo}\n        </a>'
    return f'        <div class="via">\n        {cuerpo}\n        </div>'


vias_html = "\n".join([
    via(ICO_WA, 'WhatsApp', '3548 59-2487', 'Lo más rápido: contestamos en el día',
        _wa('Hola! Quiero hacer una consulta.')),
    via(ICO_TEL, 'Teléfono', '3548 59-2487', 'En horario de atención',
        'tel:+543548592487', externo=False),
    via(ICO_IG, 'Instagram', '@volcano_fitnesslafalda', 'Ahí subimos el día a día',
        'https://instagram.com/volcano_fitnesslafalda'),
    via(ICO_PIN, 'Dónde estamos', DIRECCION, CIUDAD),
    via(ICO_RELOJ, 'Horarios', '7 a 12 y 14 a 22', 'Lunes a viernes · Sábados 9 a 12'),
])

CONTENIDO['contacto'] = (
    cabecera_pagina("Hablemos", "Contacto",
                    "La forma más rápida es WhatsApp: contestamos en el día. También "
                    "podés pasar por el gimnasio.",
                    "contacto.jpg", filo='c')
    + f"""
  <section class="sec">
    <div class="env">
      <div class="vias" data-sube>
{vias_html}
      </div>
    </div>
  </section>

  <section class="sec sec--junta">
    <div class="env" data-sube>
{MAPA}
    </div>
  </section>
"""
    + cierre("¿Querés probar una clase?",
             "Decinos qué día te queda bien y te esperamos. La primera es sin costo.",
             "Coordinar una clase",
             _wa('Hola! Quiero probar una clase. Que dias tienen lugar?')))


# ─────────────────────────────── Tu rutina ───────────────────────────────
ejercicios = [
    ("Sentadilla con barra", "4", "8", "90 s", "40 kg"),
    ("Prensa 45°", "3", "12", "75 s", "100 kg"),
    ("Peso muerto rumano", "3", "10", "90 s", "35 kg"),
    ("Búlgaras con mancuernas", "3", "10 x pierna", "60 s", "10 kg"),
    ("Extensión de cuádriceps", "3", "15", "45 s", "30 kg"),
    ("Camilla femoral", "3", "12", "45 s", "25 kg"),
    ("Elevación de gemelos", "4", "20", "40 s", "50 kg"),
]
filas = '\n'.join(
    f"""            <tr>
              <td class="rt__n">{i}</td>
              <td class="rt__ej">{n}</td>
              <td class="rt__num">{s}</td>
              <td class="rt__num">{r}</td>
              <td class="rt__num">{d}</td>
              <td class="rt__num rt__peso">{p}</td>
            </tr>""" for i, (n, s, r, d, p) in enumerate(ejercicios, 1))

CONTENIDO['rutina'] = (
    cabecera_pagina("Tu rutina · Día 2 de 4", "Tren inferior completo",
                    "Mirá el trabajo del día y empezá. Los kilos que ves al final son los "
                    "de la última vez que lo hiciste.",
                    "entrenamientos.jpg", filo='a')
    + f"""
  <section class="sec">
    <div class="env" data-sube>
      <div class="tabla-scroll">
        <table class="rt">
          <caption class="sr">Ejercicios del día, con series, repeticiones, descanso y el peso de la última sesión</caption>
          <thead>
            <tr>
              <th scope="col"><span class="sr">Orden</span></th>
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
    </div>
  </section>

  <section class="sec sec--junta">
    <div class="env" data-sube>
      <div class="aviso">
        <h2>Antes de empezar</h2>
        <p>Diez minutos de bici o cinta suave y movilidad de cadera. Si algo te molesta,
        pará y avisale a tu entrenador: se cambia el ejercicio, no se soporta.</p>
      </div>
    </div>
  </section>

  <section class="sec sec--gris">
    <div class="env duo" data-sube>
      <div class="duo__txt">
        <span class="volanta">Así se ve en el celular</span>
        <h2 class="titulo-sec">La rutina, donde entrenás</h2>
        <p>No hace falta acordarse de nada: abrís y lo primero que ves es el trabajo del
        día, con los kilos de la última vez al lado de cada ejercicio.</p>
        <p>Es la pantalla de verdad, no una foto: tocala y probala.</p>
      </div>
      <div class="fono">
        <iframe src="socios.html?demo=1" title="El área de socios vista desde un celular" loading="lazy"></iframe>
      </div>
    </div>
  </section>
"""
    + cierre("Esta es una rutina de ejemplo",
             "Sirve para mostrar cómo se ve. La tuya la arma tu entrenador, según de dónde venís.",
             "Pedí la tuya", _wa('Hola! Quiero que me armen una rutina.'), filo='b', encima='gris'))


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
    'gym.html': ('El gimnasio — Volcano Fitness',
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
        barra=barra,
        cabecera=a_paginas(cabecera, archivo),
        pie=a_paginas(pie, archivo),
        wpp=wpp, sprite=sprite,
        contenido=contenido), encoding='utf-8')
    print('generada', archivo)
