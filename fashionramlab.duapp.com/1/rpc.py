#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import meta
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

__author__ = '锦峰'


class XMLRPCDispatcher(SimpleXMLRPCDispatcher):
    def __init__(self, funcs):
        SimpleXMLRPCDispatcher.__init__(self, True, 'utf-8')
        self.funcs = funcs
        self.register_introspection_functions()


def test_rpc_method(s):
    from urllib import quote
    return {'result': quote(s)}

def make_rpc_server():
    return XMLRPCDispatcher({
        'add': lambda x, y: x + y,
        'sub': lambda x, y: x - y,
        'test': test_rpc_method
    })


class RpcHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/rpc'

    def post(self):
        from orm import getSession
        from model.test import XUser, XAddress
        session = getSession()
        u = XUser('a', 'b', 'c')
        adr = XAddress('a@tom.com')
        adr.user = u
        session.add(u)
        session.commit()
        # session.add(adr)


        dispatcher = make_rpc_server()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        response = dispatcher._marshaled_dispatch(self.request.body)
        self.write(response)




