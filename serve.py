#!/usr/bin/env python
#
# Runs a Tornado web server with a django project
# Make sure to edit the DJANGO_SETTINGS_MODULE to point to your settings.py
#

import tornado.httpserver
from tornado.options import parse_command_line
import tornado.ioloop
import tornado.web
import CRUD.asgi

PORT = 8080
GLOBAL_CHARSET = "utf-8"


class AsgiHandler(tornado.web.RequestHandler):
    '''
        Credit to @plter on GitHub for the ASGI Handler
        https://github.com/plter/tornado_asgi_handler
    '''

    def initialize(self, asgi_app) -> None:
        super().initialize()
        self._asgi_app = asgi_app

    async def handle_request(self):
        headers = []
        for k in self.request.headers:
            for v in self.request.headers.get_list(k):
                headers.append(
                    (k.encode(GLOBAL_CHARSET).lower(), v.encode(GLOBAL_CHARSET))
                )

        scope = {
            "type": self.request.protocol,
            "http_version": self.request.version,
            "path": self.request.path,
            "method": self.request.method,
            "query_string": self.request.query.encode(GLOBAL_CHARSET),
            "headers": headers,
            "client": (self.request.remote_ip, 0)
        }

        async def receive():
            return {'body': self.request.body, "type": "http.request", "more_body": False}

        async def send(data):
            if data['type'] == 'http.response.start':
                self.set_status(data['status'])
                self.clear_header("content-type")
                self.clear_header("server")
                self.clear_header("date")
                for h in data['headers']:
                    if len(h) == 2:
                        self.add_header(
                            h[0].decode(GLOBAL_CHARSET),
                            h[1].decode(GLOBAL_CHARSET)
                        )
            elif data['type'] == 'http.response.body':
                self.write(data['body'])
            else:
                raise RuntimeError(
                    f"Unsupported response type \"{data['type']}\" for asgi app")

        await self._asgi_app(scope, receive, send)

    async def get(self):
        await self.handle_request()

    async def post(self):
        await self.handle_request()

    async def delete(self):
        await self.handle_request()


def main():
    asgi_app = CRUD.asgi.application
    parse_command_line()
    tornado_app = tornado.web.Application(
        [
            ("/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'}),  # Serve Static Files
            ("/media/(.*)", tornado.web.StaticFileHandler, {'path': 'media'}),  # Serve Media Files
            ('.*', AsgiHandler, dict(asgi_app=asgi_app)),  # Serve Django Application
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    print(F"Application running on http://localhost:{PORT}/")
    main()
