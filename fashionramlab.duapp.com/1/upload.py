#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '锦峰'

import tornado.web
import meta
import os
import base64
from db import log


class UploadFileHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/u'

    def post(self):
        path_prefix = '/uploadimg/nobody/'
        if self.get_secure_cookie('username'):
            from weicbd.aaa import AAADao
            dao = AAADao()
            path_prefix = '/uploadimg/%d/' % dao.get_user(self.get_secure_cookie('username'))[0]

            file_metas = self.request.files['file']
            for meta in file_metas:
                filename = meta['filename'].decode('utf-8')
                body = meta['body']
                self.save_to_bcs(path_prefix + filename, body)


        self.add_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<upload><path>%s</path></upload>' % (path_prefix + filename))

    def save_to_bcs(self, path, body):
        from bae.core import const
        from bae.api import bcs
        baebcs = bcs.BaeBCS(const.BCS_ADDR, const.ACCESS_KEY, const.SECRET_KEY)
        baebcs.put_object(u'fashionramlab', path, base64.b64encode(body))


class UploadFileHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/uploadimg_z/(.*)'

    def get(self, sub_path):
        path = os.path.join(os.sep + 'uploadimg', sub_path)
        self.write(self.get_from_bcs(path))

    def get_from_bcs(self, path):
        from bae.core import const
        from bae.api import bcs
        baebcs = bcs.BaeBCS(const.BCS_ADDR, const.ACCESS_KEY, const.SECRET_KEY)
        e, response = baebcs.get_object(u'fashionramlab', path)
        return base64.b64decode(response)