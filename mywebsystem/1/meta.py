#! /usr/bin/env python
# -*- coding: utf-8 -*-

from db import log
import tornado.web
import json


class HandlerMetaClass(type):
    handlers = []

    def __new__(cls, clsname, bases, attrs):
        newclass = super(cls, HandlerMetaClass).__new__(cls, clsname, bases, attrs)
        if '__route__' in dir(newclass):
            HandlerMetaClass.handlers.append((newclass.__route__, newclass))        
        elif 'route' in dir(newclass):
            HandlerMetaClass.handlers.append((newclass.route, newclass))
        return newclass


class RequestHandlerBase(tornado.web.RequestHandler):
    __metaclass__ = HandlerMetaClass
    
    def get_current_user(self):
        pp = self.get_secure_cookie('passport')
        return json.loads(pp) if pp else None


class PluginMetaClass(type):
    plugins = {}

    def __new__(cls, clsname, bases, attrs):
        newclass = super(cls, PluginMetaClass).__new__(cls, clsname, bases, attrs)
        if type(bases[0]) != type(object):
            PluginMetaClass.plugins['%s.%s' % (newclass.__module__, clsname)] = newclass
        return newclass


class ModuleMetaClass(type):
    modules = {}

    def __new__(cls, clsname, bases, attrs):
        newclass = super(cls, ModuleMetaClass).__new__(cls, clsname, bases, attrs)
        if type(bases[0]) != type(object):
            ModuleMetaClass.modules['%s.%s' % (newclass.__module__, clsname)] = newclass
        return newclass

