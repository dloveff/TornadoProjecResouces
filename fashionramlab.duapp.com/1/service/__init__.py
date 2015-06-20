#! /usr/bin/env python
# -*- coding: utf-8 -*-

from db import getLogger
import os
import meta
import json
import tornado.web

class ServiceHandlerBase(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    
    def get_current_user(self):
        pp = self.get_secure_cookie('passport')
        return json.loads(pp) if pp else None
    
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    try:
        __import__(module[:-3], locals(), globals())
    except ImportError as e:
        getLogger().info('[%s] %s: %s' % (module, e.__class__.__name__, e.message))
del module
