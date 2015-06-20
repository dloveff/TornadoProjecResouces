#! /usr/bin/env python
# -*- coding: utf-8 -*-

from orm import getSession
from model.tag import Tag
import meta
import tornado.web
from sqlalchemy.orm.exc import NoResultFound
import xml.etree.ElementTree as ET
from model.mpsite import MpSite
from weicbd.mpconsole import MPSiteDao
from db import log

__author__ = 'chinfeng'


class BaseTagHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = None
        self.mpdao = None
    
    def get_session(self):
        if not self.session:
            self.session = getSession()
        return self.session

    def get_mpdao(self):
        if not self.mpdao:
            self.mpdao = MPSiteDao()
        return self.mpdao

    def output_tags_by_mpid(self, mpid, r):
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<tags mpid="%d">' % mpid)
        tags = self.get_session().query(Tag).filter(Tag.mpid == mpid, Tag.parent_id == None)
        for tag in tags:
            self.write_tag(tag, r)
        self.write('</tags>')

    def write_tag(self, tag, r):
        self.write('<tag id="%d" name="%s">' % (tag.id, tag.name))
        if int(r) != 0:
            for t in tag.children:
                self.write_tag(t, r)
        self.write('</tag>')


class TagListHandler(BaseTagHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mptags'

    def get(self):
        ghid = self.get_secure_cookie('ghid')
        try:
            r = self.get_argument('r', 1)
            mp = self.get_session().query(MpSite).filter(MpSite.ghid == ghid).one()
            self.output_tags_by_mpid(mp.id, r)
            self.get_session().close()
        except NoResultFound:
            self.send_error('500')


class ConsoleTagListHandler(BaseTagHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mptags/(.*)'

    def get(self, mpid_str):
        mpid = int(mpid_str)
        r = self.get_argument('r', 1)
        self.output_tags_by_mpid(int(mpid), r)
        self.get_session().close()

class ConsoleTagHandler(BaseTagHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/tag/(.*)'

    def delete(self, tag_id):
        session = getSession()
        t = session.query(Tag).filter(Tag.id == int(tag_id)).one()
        if not self.get_mpdao().own(self.get_secure_cookie('username'), t.mpid):
            raise tornado.web.HTTPError(401)
        name = t.name
        session.delete(t)
        session.commit()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<tag id="%s" name="%s"/>' % (tag_id, name))

    def put(self, tag_id):
        session = getSession()
        root = ET.fromstring(self.request.body)
        name = root.attrib['name']
        t = session.query(Tag).filter(Tag.id == int(tag_id)).one()
        if not self.get_mpdao().own(self.get_secure_cookie('username'), t.mpid):
            raise tornado.web.HTTPError(401)
        t.name = name.encode('utf-8')
        session.commit()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<tag id="%s" name="%s"/>' % (tag_id, name))

    def post(self, tag_id):
        session = getSession()
        root = ET.fromstring(self.request.body)
        name = root.attrib['name']
        pt = session.query(Tag).filter(Tag.id == int(tag_id)).one()
        if not self.get_mpdao().own(self.get_secure_cookie('username'), pt.mpid):
            raise tornado.web.HTTPError(401)

        t = Tag(name.encode('utf-8'), pt.mpid)
        t.parent = pt
        session.add(t)
        session.commit()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<tag id="%s" name="%s"/>' % (tag_id, name))

    def get(self, tag_id):
        r = self.get_argument('r', 1)
        tag = self.get_session().query(Tag).filter(Tag.id == int(tag_id)).one()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write_tag(tag, r)
        self.get_session().close()

class ConsoleRootTagHandler(BaseTagHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mptag/(.*)'

    def post(self, mpid_str):
        mpid = int(mpid_str)
        if not self.get_mpdao().own(self.get_secure_cookie('username'), mpid):
            raise tornado.web.HTTPError(401)

        root = ET.fromstring(self.request.body)
        name = root.attrib['name']
        session = getSession()
        t = Tag(name.encode('utf-8'), mpid)
        session.add(t)
        session.commit()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<tag id="%d" name="%s"/>' % (t.id, name))

#     def post(self, mpid_str):
#         session = getSession()
#         self.set_header('Content-Type', 'text/xml; charset=utf-8')
#         mpid = int(mpid_str)
#         tag = session.query(Tag).filter_by(mpid=mpid_str).first()
#         import json
#         x = add_value_to_tag(json.loads(self.request.body))
#         if not tag:
#            tag = Tag(mpid, json.dumps(x, ensure_ascii=False).encode('utf8'))
#         else:
#            tag.setting = json.dumps(x, ensure_ascii=False).encode('utf8')
#         session.add(tag)
#         session.commit()
#         self.write(tag.setting)
#
#
# def add_value_to_tag(tag_json, parent='/'):
#     for k, v in tag_json.items():
#         v['value'] = '%s%s/' % (parent, k)
#         if 'children' in v:
#             add_value_to_tag(v['children'], v['value'])
#     return tag_json
#
