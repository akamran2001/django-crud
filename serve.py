import os
import socket
import subprocess
import http.server
import socketserver
from CRUD.settings import DEBUG

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080
DIRECTORY = "media/"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if(DEBUG):
    os.system("python manage.py runserver")
else:
    gu = subprocess.Popen("gunicorn -b 0.0.0.0 CRUD.wsgi", shell=True)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(F"http://{HOST}:{PORT}/")
        httpd.serve_forever()
    




