"""Arma en _preview/ una version de una sola pagina de la home, para publicarla.

El sitio tiene varias paginas; el preview es solo la home, asi que los enlaces
a las otras se redirigen a la seccion equivalente de la misma home y no quedan
rotos. Sirve para pasarle la home a alguien por link sin depender del deploy.
"""
import os
import re
import shutil

h = open('index.html').read()

mapa = {
    'somos.html': '#somos',
    'contacto.html': '#contacto',
    'socios.html': '#rutina',
    'profes.html': '#equipo',
    'gym.html': '#gimnasio',
    'precios.html': '#precios',
    'entrenamientos.html': '#entrenamientos',
}
for viejo, nuevo in mapa.items():
    # primero las que traen ancla propia (entrenamientos.html#funcional)
    h = h.replace('href="%s#' % viejo, 'href="%s@' % nuevo)
    h = h.replace('href="%s"' % viejo, 'href="%s"' % nuevo)
h = re.sub(r'href="(#[a-z]+)@[a-z]+"', r'href="\1"', h)

# La seccion del area de socios no tenia id: en el sitio completo es una pagina
h = h.replace('<section class="meta">', '<section class="meta" id="rutina">')

sueltos = re.findall(r'href="[a-z-]+\.html[^"]*"', h)
assert not sueltos, sueltos[:3]
faltan = sorted({a for a in re.findall(r'href="#([a-z-]+)"', h)
                 if 'id="%s"' % a not in h and not a.startswith('filo')})
assert not faltan, faltan

if os.path.isdir('_preview'):
    shutil.rmtree('_preview')
os.makedirs('_preview/css')
os.makedirs('_preview/js')
open('_preview/index.html', 'w').write(h)
shutil.copy('css/estilo.css', '_preview/css/estilo.css')
shutil.copy('js/home.js', '_preview/js/home.js')
shutil.copytree('img', '_preview/img')
shutil.copytree('video', '_preview/video')
print('preview armado en _preview/')
