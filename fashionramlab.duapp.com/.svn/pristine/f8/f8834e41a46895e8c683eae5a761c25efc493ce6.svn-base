#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '锦峰'

import tornado.web, meta, auth
import xml.etree.ElementTree as ET
from orm import getSession
from model.aaa import Account
from model.circle import Circle


#class CreateCircleHandler(tornado.web.RequestHandler):
    #__metaclass__ = meta.HandlerMetaClass
    #route = r'/circle'

    #def get_current_user(self):
        #return self.get_secure_cookie('username')

    #@auth.authenticated
    #def post(self):
        #root = ET.fromstring(self.request.body)
        #session = getSession()
        #a = session.query(Account).filter(Account.username == self.get_secure_cookie('username')).one()
        #c = Circle(
            #root.findtext('name').encode('utf-8'),
            #root.findtext('description').encode('utf-8'),
            #a.id
        #)
        #session.add(c)
        #session.commit()

        #self.set_header('Content-Type', 'text/xml; charset=utf-8')
        #self.write('<circle id="%d"/>' % c.id)
        #session.close()


#class CircleListHandler(tornado.web.RequestHandler):
    #__metaclass__ = meta.HandlerMetaClass
    #route = r'/circles'

    #def get_current_user(self):
        #return self.get_secure_cookie('username')

    #@auth.authenticated
    #def get(self):
        #session = getSession()
        #a = session.query(Account).join(Circle).filter(Account.username == self.get_current_user()).one()
        #root = ET.Element('circles')
        #for circle in a.own_circles + a.joined_circles:
            #circle_elm = ET.SubElement(root, 'circle', {'id': str(circle.id), 'serial': circle.serial})
            #self.__append_element(circle_elm, 'name', circle.name)
            #self.__append_element(circle_elm, 'description', circle.description)
            #self.__append_element(circle_elm, 'create-time', str(circle.create_time))
        #self.set_header('Content-Type', 'text/xml; charset=utf-8')
        #self.write(ET.tostring(root, encoding='UTF-8'))
        #session.close()

    #@staticmethod
    #def __append_element(parent, tag, value):
        #e = ET.Element(tag)
        #if value:
            #e.text = value
        #parent.append(e)