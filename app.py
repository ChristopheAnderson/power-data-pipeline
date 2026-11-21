# -*- coding: utf-8 -*-
"""
Point d'entrée compatible Streamlit et Vercel
"""
def app(environ, start_response):
    path = environ.get('PATH_INFO', '')
    target = f"https://power-data-pipeline-bqhbx2x3rta7odtqusg8bb.streamlit.app{path}"
    start_response('302 Found', [('Location', target), ('Content-Type', 'text/plain')])
    return [b"Redirecting to Streamlit Cloud..."]

application = app
handler = app

if __name__ == "__main__":
    import os, sys
    os.system(f"{sys.executable} -m streamlit run streamlit_app.py")
