#!/usr/bin/env python3
"""Sirve el sitio en http://localhost:8899 sin caché.

http.server normal deja que el navegador cachee, y entonces se ven versiones
viejas del HTML y del CSS despues de editarlos. Esto manda no-store en todo.
"""
import http.server, functools, sys

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 8899

class SinCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

http.server.HTTPServer(('', PUERTO), SinCache).serve_forever()
