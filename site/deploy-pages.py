#!/usr/bin/env python3
"""Publica el sitio en la rama gh-pages.

No usamos el workflow de Actions porque el token de `gh` de esta maquina no
tiene el scope `workflow` y GitHub rechaza cualquier push que traiga
.github/workflows/. Esto hace lo mismo desde aca: arma el sitio y lo empuja
como rama huerfana, que al no llevar el workflow adentro si pasa.

Es el mismo truco que scripts/deploy-pages.mjs de paolini-automotores.

Se publica solo lo que el visitante necesita: quedan afuera los guiones, el
LEEME, las fotos originales y _plantilla-interna.html (la home vieja, que se
dio de baja y no tiene por que llegar al sitio publicado).
"""
import os
import pathlib
import shutil
import subprocess
import tempfile

base = pathlib.Path(__file__).parent

# Se regeneran las internas antes de publicar, como hacia el workflow
subprocess.run(['python3', 'paginas.py'], cwd=base, check=True)

CARPETAS = ('css', 'js', 'img', 'video')
FUERA = {'_plantilla-interna.html', 'mockup.html'}


def correr(*args, cwd):
    subprocess.run(args, cwd=cwd, check=True)


remoto = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=base,
                        capture_output=True, text=True, check=True).stdout.strip()

etapa = pathlib.Path(tempfile.mkdtemp(prefix='volcano-pages-'))
try:
    for html in base.glob('*.html'):
        if html.name not in FUERA:
            shutil.copy(html, etapa / html.name)
    for carpeta in CARPETAS:
        shutil.copytree(base / carpeta, etapa / carpeta)

    # Sin esto, Pages corre Jekyll y se saltea los directorios que empiezan con _
    (etapa / '.nojekyll').write_text('')

    correr('git', 'init', '-q', '-b', 'gh-pages', cwd=etapa)
    correr('git', 'add', '-A', cwd=etapa)
    correr('git', '-c', 'user.name=deploy', '-c', 'user.email=deploy@local',
           'commit', '-q', '-m', 'Publicar sitio', cwd=etapa)
    correr('git', 'push', '-f', remoto, 'gh-pages', cwd=etapa)
    archivos = sum(1 for _ in etapa.rglob('*') if _.is_file())
    print('\nPublicado en gh-pages (%d archivos).' % archivos)
finally:
    shutil.rmtree(etapa, ignore_errors=True)
