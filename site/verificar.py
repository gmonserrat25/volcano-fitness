"""Chequeo de las paginas generadas: chrome completo, hojas nuevas y nada del estilo viejo."""
import pathlib
import re

base = pathlib.Path(__file__).parent
paginas = ['somos', 'entrenamientos', 'profes', 'gym', 'precios', 'contacto', 'rutina']

# Clases que eran del estilo viejo y no deberian sobrevivir
VIEJAS = ['panel', 'cabecera__titulo', 'pill', 'seccion__tit', 'lbl', 'iphone',
          'wipe', 'menu__list', 'vista-movil', 'disc__nom', 'plan__nom', 'via--info']

problemas = 0
for p in paginas:
    h = (base / (p + '.html')).read_text(encoding='utf-8')
    hojas = re.findall(r'<link rel="stylesheet" href="([^"]+)"', h)
    guiones = re.findall(r'<script src="([^"]+)"', h)
    falta = [c for c in ['class="barra"', 'class="cab"', 'class="pie"', 'class="wpp"', 'sprite-rasgado']
             if c not in h]
    viejas = sorted({c for c in VIEJAS if re.search(r'class="[^"]*\b%s\b' % re.escape(c), h)})
    filos = len(re.findall(r'<use href="#filo-', h))
    imgs = re.findall(r'src="(img/[^"]+)"', h)
    faltan_img = sorted({i for i in imgs if not (base / i).exists()})
    enlaces = sorted({l for l in re.findall(r'href="([a-z-]+\.html)"', h)
                      if not (base / l).exists()})

    estado = []
    if hojas != ['css/estilo.css']:
        estado.append('HOJA=%s' % hojas)
    if guiones != ['js/home.js']:
        estado.append('JS=%s' % guiones)
    if falta:
        estado.append('FALTA_CHROME=%s' % falta)
    if viejas:
        estado.append('CLASES_VIEJAS=%s' % viejas)
    if faltan_img:
        estado.append('IMG_ROTA=%s' % faltan_img)
    if enlaces:
        estado.append('ENLACE_ROTO=%s' % enlaces)
    # gym cierra con el mapa y no con franja de CTA, asi que le alcanza con uno
    if filos < 1:
        estado.append('SIN_FILO')

    problemas += len(estado)
    print('%-16s %s' % (p, ' | '.join(estado) if estado else 'ok (filos: %d)' % filos))

print('\nproblemas:', problemas)
