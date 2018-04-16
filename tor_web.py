# coding:utf-8
# File Name: tirnado.py
# Created Date: 2018-04-16 11:10:26
# Last modified: 2018-04-16 11:19:05
# Author: yeyong
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from tornado.httpserver import HTTPServer
from uwsgi import app

class MainHandler(RequestHandler):
    def get(self):
        self.write(dict(msg="好久不见甚是想念", code=200))


flask_route = WSGIContainer(app)
application = Application([
    (r"/", MainHandler),
    (r".*", FallbackHandler, dict(fallback=flask_route))
    ])

if __name__ == "__main__":
    application.listen("9001", address="0.0.0.0")
    IOLoop.instance().start()
