#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web, meta, auth
from weicbd.mp import MPSiteDao
from weicbd.pattern import MessagePatternDao
import xml.etree.ElementTree as ET

class MPListHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mplist'

    def get_current_user(self):
        tk = self.get_secure_cookie('token')
        return tk if (tk is not None) or (tk == 'administrator') else None
    
    @auth.authenticated
    def get(self):
        dao = MPSiteDao()
        root = ET.Element('mp-list')
        for s in dao.get_all_sites():
            id, token, name, wxid, appid, secret, validated, validateTime, enabled = s
            mp = ET.SubElement(root, 'mp', id=str(id))
            self.__append_element(mp, 'token', token)
            self.__append_element(mp, 'name', name)
            self.__append_element(mp, 'wxid', wxid)
            self.__append_element(mp, 'appid', appid)
            self.__append_element(mp, 'secret', secret)
            self.__append_element(mp, 'validated', validated)
            self.__append_element(mp, 'validateTime', validateTime)
            self.__append_element(mp, 'enabled', enabled)
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))
                
    def __append_element(self, parent, tag, value):
        e = ET.Element(tag)
        if value is not None:
            e.text = str(value)
        parent.append(e)
        
class MPUpdateHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mpupdate'
    
    def get_current_user(self):
        tk = self.get_secure_cookie('token')
        return tk if (tk is not None) or (tk == 'administrator') else None
    
    @auth.authenticated
    def put(self):
        root = ET.fromstring(self.request.body)
        dao = MPSiteDao()
        dao.update_sites(
            int(root.attrib['id']),
            root.findtext('name'),
            root.findtext('wxid'),
            root.findtext('appid'),
            root.findtext('secret'),
            int(root.findtext('enabled'))
        )
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<update/>')

class MPPluginHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mpplugin/(.*)'
    
    def get_current_user(self):
        tk = self.get_secure_cookie('token')
        return tk if (tk is not None) or (tk == 'administrator') else None
    
    @auth.authenticated
    def get(self, mp_id):
        dao = MessagePatternDao()
        root = ET.Element('plugins', mp_id=mp_id)
        
        for s in dao.get_mp_plugins_by_id(int(mp_id)):
            id, pattern, pclass, settings = s
            elm = ET.SubElement(root, 'plugin', id=str(id))
            self.__append_element(elm, 'pattern', pattern)
            self.__append_element(elm, 'class', pclass)
            self.__append_element(elm, 'settings', settings)
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))
        
    @auth.authenticated
    def put(self, site_id):
        root = ET.fromstring(self.request.body)
        dao = MessagePatternDao()
        pid = dao.add_plugin(
            int(root.attrib['site_id']),
            root.findtext('pattern'),
            root.findtext('class'),
            root.findtext('settings')
        )
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<plugin id="%d"/>' % pid)
        
    @auth.authenticated
    def delete(self, plugin_id):
        dao = MessagePatternDao()
        dao.remove_plugin(plugin_id)
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<plugin id="%s"/>' % plugin_id)


    def __append_element(self, parent, tag, value):
        e = ET.Element(tag)
        if value is not None:
            e.text = str(value)
        parent.append(e)
    