"""Arma en _preview/ una version de una sola pagina de site/v2/, para publicarla.

El sitio real tiene varias paginas; el preview es solo la home nueva, asi que los
enlaces a las otras paginas se redirigen a la seccion equivalente de esta misma
home y no quedan rotos.
"""
import os
import re
import shutil

h = open('v2/index.html').read()

# El preview cuelga de la raiz, no de v2/
h = h.replace('../img/', 'img/').replace('../video/', 'video/')
h = h.replace('href="css/estilo.css"', 'href="v2/css/estilo.css"')
h = h.replace('src="js/main.js"', 'src="v2/js/main.js"')

mapa = {
    '../somos.html': '#somos',
    '../contacto.html': '#contacto',
    '../socios.html': '#rutina',
    '../profes.html': '#equipo',
    '../gym.html': '#gimnasio',
    '../precios.html': '#precios',
    '../entrenamientos.html': '#entrenamientos',
}
for viejo, nuevo in mapa.items():
    # primero las que traen ancla propia (entrenamientos.html#funcional)
    h = h.replace('href="%s#' % viejo, 'href="%s@' % nuevo)
    h = h.replace('href="%s"' % viejo, 'href="%s"' % nuevo)
h = re.sub(r'href="(#[a-z]+)@[a-z]+"', r'href="\1"', h)

# Dos secciones que en el sitio completo son paginas y aca son ancla
h = h.replace('<section class="meta">', '<section class="meta" id="rutina">')
h = h.replace('<footer class="pie">', '<footer class="pie" id="contacto">')

sueltos = [l for l in h.split('\n') if '../' in l]
assert not sueltos, sueltos[:3]

os.makedirs('_preview/v2/css', exist_ok=True)
os.makedirs('_preview/v2/js', exist_ok=True)
open('_preview/index.html', 'w').write(h)
shutil.copy('v2/css/estilo.css', '_preview/v2/css/estilo.css')
shutil.copy('v2/js/main.js', '_preview/v2/js/main.js')
shutil.copytree('img', '_preview/img', dirs_exist_ok=True)
shutil.copytree('video', '_preview/video', dirs_exist_ok=True)
print('preview armado')
