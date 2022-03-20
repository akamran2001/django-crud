#!/usr/bin/env python
#
# Runs a Tornado web server with a django project
# Make sure to edit the DJANGO_SETTINGS_MODULE to point to your settings.py
#

import os
import tornado.httpserver
from tornado.options import parse_command_line
import tornado.ioloop
import web
import CRUD.asgi

PORT = 8080


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'CRUD.settings'
    asgi_app = CRUD.asgi.application
    parse_command_line()
    tornado_app = web.Application(
        [
            ("/static/(.*)", web.StaticFileHandler, {'path': 'static'}),  # Serve Static Files
            ("/media/(.*)", web.StaticFileHandler, {'path': 'media'}),  # Serve Media Files
            ('.*', web.AsgiHandler, dict(asgi_app=asgi_app)),  # Serve Django Application
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    print(F"Application running on http://localhost:{PORT}/")
    main()
