#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '北极鱼'

import tornado.web, meta
from orm import getSession
import xml.etree.ElementTree as ET
from model.jopmodel import JopInfoHandler
from model.usermodel import FlowerUser
import time, datetime
from db import Mysqldb, log

class JopHandler(tornado.web.RedirectHandler):
    __metaclass__= meta.HandlerMetaClass
    route = r'/flower/jop/(.*)'

    # 修改招聘信息
    def put(self, jid):
        root = ET.fromstring(self.request.body)
        session = getSession()
        user = self.get_cookie('getuser')# 拿到cookie
        users = session.query(FlowerUser).filter(FlowerUser.user_name == str(user)).first() # 当前登录用户
        jop = session.query(JopInfoHandler).filter(JopInfoHandler.jop_id == int(jid)).first()
        if jop and users.user_name:
            jop.jop_position = root.find('position').text  # 职位
            jop.jop_desc = root.find('desc').text  # 描述
            jop.jop_reward = root.find('reward').text  # 报酬
            jop.jop_time = datetime.datetime.now()  # 发布时间  自动生成
            jop.jop_mobile = root.find('mobile').text  # 手机
            jop.jop_userid = root.get('uid')
            session.merge(jop)
            session.commit()
            self.write('<jopinfo id="%s"/>' %int(jop.jop_id))
        else:
            self.send_error(401)

    # 删除信息
    def delete(self, jid):
        id = int(jid)
        session = getSession()
        user = self.get_cookie('getuser')# 拿到cookie
        users = session.query(FlowerUser).filter(FlowerUser.user_name == str(user)).first()
        jop = session.query(JopInfoHandler).filter(JopInfoHandler.jop_id == id).first()
        if jop and users.user_name:
            session.delete(jop)
            session.commit()
            self.write('<jopinfo id="%s"/>'% int(jop.jop_id))
        else:
            self.send_error(401)


    # 查看单个招聘信息
    def get(self, jid):
        id = int(jid)
        root = ET.Element('jopinfos')
        session = getSession()
        jop = session.query(JopInfoHandler).filter(JopInfoHandler.jop_id == id).first()
        if jop:
            for val in jop:
                user = session.query(FlowerUser).filter(FlowerUser.user_id == int(val.user_id)).first()  # 根据ID找到发布人信息
                jp = ET.SubElement(root, 'jopinfo')
                jp.attrib['id'] = str(val.jop_id)       # 设置根节点属性
                ET.SubElement(jp, 'user').text = user.user_name                          # 发布人
                ET.SubElement(jp, 'position').text = val.jop_position  # 职位
                ET.SubElement(jp, 'desc').text = val.jop_desc  # 描述
                ET.SubElement(jp, 'reward').text = str(val.jop_reward)  # 报酬
                ET.SubElement(jp, 'time').text = val.jop_time  # 发布时间
                ET.SubElement(jp, 'mobile').text = val.jop_mobile # 联系方式

        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))


class JopInfoHandler(tornado.web.RequestHandler):
    __metaclass__= meta.HandlerMetaClass
    route = r'/flower/jop'

    # 发布招聘信息
    def post(self):
        root = ET.fromstring(self.request.body)
        position = root.find('position').text # 职位
        desc = root.find('desc').text  # 描述
        reward = root.find('reward').text  # 报酬
        mobile = root.find('mobile').text # 联系方式
        userid = root.get('uid')
        joptime = datetime.datetime.now() # 发布时间  自动生成
        session = getSession()
        # userid = session.query(FlowerUser).filter(FlowerUser.user_name == str(user)).first().user_id   # session.query(UserHandler).get(user).user_name
        user = self.get_cookie('getuser')# 拿到cookie
        users = session.query(FlowerUser).filter(FlowerUser.user_name == str(user)).first()
        jop = JopInfoHandler(position, desc, reward, joptime, mobile,userid )
        if jop and users.user_name:
            session.add(jop)
            session.commit()
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write('<jopinfo id="%d"/>' % jop.jop_id)
        else:
            self.send_error(401)


    def get(self):
        session = getSession()
        root = ET.Element('jopinfos')
        jop = session.query(JopInfoHandler).all()
        if jop:
            for val in jop:
                user = session.query(FlowerUser).filter(FlowerUser.user_id == int(val.user_id)).first()  # 根据ID找到发布人信息
                jp = ET.SubElement(root, 'jopinfo')
                jp.attrib['id'] = str(val.jop_id)       # 设置根节点属性
                ET.SubElement(jp, 'user').text = user.user_name                          # 发布人
                ET.SubElement(jp, 'position').text = val.jop_position   # 职位
                ET.SubElement(jp, 'desc').text = val.jop_desc  # 描述
                ET.SubElement(jp, 'reward').text = str(val.jop_reward)  # 报酬
                ET.SubElement(jp, 'time').text = val.jop_time  # 发布时间
                ET.SubElement(jp, 'mobile').text = val.jop_mobile # 联系方式

        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(root, encoding='UTF-8'))
