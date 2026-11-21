# -*- coding: utf-8 -*-
"""
Vercel Serverless Entrypoint (WSGI & BaseHTTPRequestHandler)
Redirige instantanément vers l'application Streamlit Cloud en production.
"""
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        target = "https://power-data-pipeline-bqhbx2x3rta7odtqusg8bb.streamlit.app" + self.path
        self.send_response(302)
        self.send_header("Location", target)
        self.end_headers()
        self.wfile.write(b"Redirecting to Streamlit Cloud...")
        return

def app(environ, start_response):
    path = environ.get('PATH_INFO', '')
    target = f"https://power-data-pipeline-bqhbx2x3rta7odtqusg8bb.streamlit.app{path}"
    start_response('302 Found', [('Location', target), ('Content-Type', 'text/plain')])
    return [b"Redirecting to Streamlit Cloud..."]

application = app
