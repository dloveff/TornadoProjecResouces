#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '北极鱼'


from index import application
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop

if __name__ == '__main__':
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()