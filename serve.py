#!/usr/bin/env python
#
# Runs a Tornado web server with a django project
# Make sure to edit the DJANGO_SETTINGS_MODULE to point to your settings.py
#


import os
from tornado.options import options, define, parse_command_line
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado_asgi_handler
import CRUD.asgi

PORT = 8080


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'CRUD.settings'
    parse_command_line()
    asgi_app = CRUD.asgi.application

    tornado_app = tornado.web.Application(
        [
            ("/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'}),  # Serve Static Files
            ("/media/(.*)", tornado.web.StaticFileHandler, {'path': 'media'}),  # Serve Media Files
            ('.*', tornado_asgi_handler.AsgiHandler, dict(asgi_app=asgi_app)),  # Serve Django Application
        ])

    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(PORT)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    print(F"Application running on http://localhost:{PORT}/")
    main()
