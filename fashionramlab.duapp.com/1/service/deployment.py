#! /usr/bin/env python
# -*- coding: utf-8 -*-

import meta, auth
from model.aaa import Passport
from model.circle import Circle
from model.module import ModuleDeployment
from orm import getSession
from uuid import uuid4
import xml.etree.ElementTree as ET
from . import ServiceHandlerBase


class DeploymentHandler(ServiceHandlerBase):
    __route__ = r'/deployment/(.*)'

    def get(self, did_str):
        did = int(did_str)
        root = ET.Element('deployment')

        session = getSession()
        d = session.query(ModuleDeployment).filter(ModuleDeployment.id == did).first()

        if d:
            root.attrib['id'] = str(d.id)
            ET.SubElement(root, 'name').text = d.name
            ET.SubElement(root, 'class').text = d.cls
            ET.SubElement(root, 'serial').text = d.serial
            ET.SubElement(root, 'version').text = d.version
            circle_elm = ET.SubElement(root, 'circle')
            circle_elm.attrib['id'] = str(d.circle_id)
            ET.SubElement(circle_elm, 'name').text = d.circle.name

        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))