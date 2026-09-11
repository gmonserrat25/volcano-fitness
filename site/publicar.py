#!/usr/bin/env python3
"""Convierte index.html al formato que pide Artifact y lo deja en artifact.html.

Artifact envuelve el archivo en su propio <!doctype>/<head>/<body>, asi que hay que
entregarle solo el contenido. Se corre despues de tocar el sitio, antes de republicar.
"""
import io, re, sys, pathlib

base = pathlib.Path(__file__).parent
src  = (base / 'index.html').read_text(encoding='utf-8')

cuerpo = re.search(r'<body[^>]*>(.*)</body>', src, re.S)
if not cuerpo:
    sys.exit('no encontré el <body> en index.html')
cuerpo = cuerpo.group(1).strip()

# del <head> nos llevamos solo las fuentes; charset y viewport los pone Artifact
fuentes = re.findall(r'<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>', src)

partes = [
    '<title>Volcano Fitness</title>',
    *fuentes,
    '<link rel="stylesheet" href="css/style.css">',
    '',
    cuerpo,
]
(base / 'artifact.html').write_text('\n'.join(partes) + '\n', encoding='utf-8')
print('artifact.html generado:', len('\n'.join(partes)), 'bytes')
