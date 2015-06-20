#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '北极鱼'

import tornado.web, meta
from orm import getSession
import xml.etree.ElementTree as ET
from model.flowermodel import FlowerHandler, FlowerTypeHandler, FlowerTagsHandler

class FlowersInfoHandler(tornado.web.RequestHandler):
    __metaclass__= meta.HandlerMetaClass
    route = r'/flower/info'

    # 添加产品
    def post(self):
        root = ET.fromstring(self.request.body)
        session = getSession()
        fname = root.find('name').text  # 花卉名称
        fdesc = root.find('desc').text  # 花卉描述
        type = root.find('tyid').text   # 类别编号
        tags = root.find('tgid').text   # 标签编号
        flower = FlowerHandler(fname, fdesc, type, tags)
        if flower:
            session.add(flower)
            session.commit()
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write('<flower id="%d"/>' % flower.flower_id)
        else:
            self.send_error(401)

    #  查看全部产品
    def get(self):
        session = getSession()
        root = ET.Element('flowers')
        flower = session.query(FlowerHandler).all()
        if flower:
            for val in flower:
                fl = ET.SubElement(root, 'flower')
                fl.attrib['id'] = str(val.flower_id)       # 设置根节点属性
                fl.attrib['tid'] = str(val.ftype_id)   # 类型编号
                fl.attrib['tgid'] = str(val.tags_id)    # 标签编号
                ET.SubElement(fl, 'name').text = val.flower_name   # 名称
                ET.SubElement(fl, 'desc').text = val.flower_desc   # 描述
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))




class FlowerTypeInfoHandler(tornado.web.RequestHandler):
    __metaclass__= meta.HandlerMetaClass
    route = r'/flower/type'

    # 增加花卉类型
    def post(self):
        root = ET.fromstring(self.request.body)
        session = getSession()
        tname = str(root.find('tname').text)  # 类别名称
        ftype = FlowerTypeHandler(tname)
        if ftype:
            session.add(ftype)
            session.commit()
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write('<flowertype id="%d"/>' % ftype.ftype_id)
        else:
            self.send_error(401)

    # 查看全部类型
    def get(self):
        session = getSession()
        root = ET.Element('flowertypes')
        ftype = session.query(FlowerTypeHandler).all()
        if ftype:
            for val in ftype:
                # user = session.query(FlowerTypeHandler).filter(FlowerTypeHandler.ftype_id == int(val.user_id)).first()  # 根据ID找到发布人信息
                ft = ET.SubElement(root, 'flowertype')
                ft.attrib['id'] = str(val.ftype_id)       # 设置根节点属性
                ET.SubElement(ft, 'name').text = val.ftype_name   # 类型
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))

class FlowerTypesHandler(tornado.web.RequestHandler):
    __metaclass__= meta.HandlerMetaClass
    route = r'/flower/type/(.*)'

    # 修改类型
    def put(self, tid):
        id = int(tid)
        session = getSession()
        root = ET.fromstring(self.request.body)
        ftype = session.query(FlowerTypeHandler).filter(FlowerTypeHandler.ftype_id == id).first()
        if ftype:
            ftype.ftype_name = root.find('tname').text  # 类型
            ftype.flower_id = root.get('fid')
            session.merge(ftype)
            session.commit()
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write('<flowertype id="%d"/>' % ftype.ftype_id)
        else:
            self.send_error(401)

class FlowerTagsInfoHandler(tornado.web.RequestHandler):
    __metaclass__= meta.HandlerMetaClass
    route = r'/flower/tags'

    # 新增标签
    def post(self):
        root = ET.fromstring(self.request.body)
        tagname = root.find('tagname').text
        fid = int(root.get('fid'))
        session = getSession()
        tags = FlowerTagsHandler(tagname, fid)
        if tags:
            session.add(tags)
            session.commit()
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write('<flowertags id="%d"/>' % tags.tags_id)
        else:
            self.send_error(401)

    # 查看所有标签
    def get(self):
        session = getSession()
        root = ET.Element('flowertags')
        ftype = session.query(FlowerTypeHandler).all()
        if ftype:
            for val in ftype:
                #user = session.query(FlowerTypeHandler).filter(FlowerTypeHandler.ftype_id == int(val.user_id)).first()  # 根据ID找到发布人信息
                ft = ET.SubElement(root, 'flowertag')
                ft.attrib['id'] = str(val.tag_id)       # 设置根节点属性
                ft.attrib['fid'] = str(val.flower_id)   # 花卉编号
                ET.SubElement(ft, 'name').text = val.tags_name   # 类型
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))


