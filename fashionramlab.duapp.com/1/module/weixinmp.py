#! /usr/bin/env python
# -*- coding: utf-8 -*-

from . import ModuleBase
from model.weixinmp import WeixinMP
from model.module import ModuleDeployment
from service import ServiceHandlerBase
import xml.etree.ElementTree as ET
from orm import getSession
import auth


class WeixinModule(ModuleBase):
    __module_template__ = 'wxconsole.html'
    __module_name__ = '微信'
    __module_version__ = '0.0.1'
    

# 以下是该模块使用的 service
class WeixinMPService(ServiceHandlerBase):
    __route__ = r'/m/weixinmp/(.*)'
    
    @auth.authenticated
    def get(self, mid_str):
        # mid 为模块id
        root = ET.Element('weixinmp')
        mid = int(mid_str)
        session = getSession()
        mp = session.query(WeixinMP).filter(WeixinMP.deployment_id == mid).first()
        if mp:
            root.attrib['id'] = str(mp.id)
            root.attrib['deployment-id'] = str(mp.deployment.id)
            root.attrib['deployment-serial'] = mp.deployment.serial
            ET.SubElement(root, 'token').text = mp.token
            ET.SubElement(root, 'name').text = mp.name
            ET.SubElement(root, 'ghid').text = mp.ghid
            ET.SubElement(root, 'appid').text = mp.appid
            ET.SubElement(root, 'secret').text = mp.secret
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))
        
    @auth.authenticated
    def post(self, mid_str):
        root = ET.fromstring(self.request.body)
        mid = int(mid_str)
        
        session = getSession()
        mp = WeixinMP(
            root.findtext('token'),
            root.findtext('name'),
            root.findtext('ghid'),
            root.findtext('appid'),
            root.findtext('secret'),
            mid
        )
        session.merge(mp)
        session.commit()
        
        root = ET.Element('weixinmp')
        root.attrib['id'] = str(mp.id)
        root.attrib['deployment-id'] = mid_str
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))
