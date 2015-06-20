#! /usr/bin/env python
# -*- coding: utf-8 -*-

from orm import getSession
from model.location import MpLocation
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

    def output_locations(self, mpid):
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<locations mpid="%d">' % mpid)
        locs = self.get_session().query(MpLocation).filter(MpLocation.mpid == mpid)
        for loc in locs:
            self.write('<location priority="%d">' % loc.priority)
            self.write('<name>%s</name>' % loc.name)
            self.write('<address>%s</address>' % loc.address)
            self.write('<lon>%f</lon>' % loc.lon)
            self.write('<lat>%f</lat>' % loc.lat)
            self.write('<thumb>%s</thumb>' % loc.thumb)
            self.write('</location>')
        self.write('</locations>')


class MpLocationConsoleHandler(BaseTagHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mploc/(.*)'

    def get(self, mpid_str):
        self.output_locations(int(mpid_str))

    def post(self, mpid_str):
        mpid = int(mpid_str)
        session = self.get_session()
        mpsite = session.query(MpSite).filter(MpSite.id == mpid).one()
        mpsite.locations[:] = []


        root = ET.fromstring(self.request.body)
        for loc_elm in root.iter('location'):
            priority = loc_elm.attrib['priority']
            name = loc_elm.findtext('name').encode('utf-8')
            address = loc_elm.findtext('address').encode('utf-8')
            lon = float(loc_elm.findtext('lon'))
            lat = float(loc_elm.findtext('lat'))
            thumb = loc_elm.findtext('thumb').encode('utf-8')
            mploc = MpLocation(name, address, priority, lon, lat, thumb)
            mploc.mpsite = mpsite
            session.add(mploc)
        session.commit()
        session.close()

        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<locations mpid="%d"/>' % mpid)


class MpLocationListHandler(BaseTagHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mploc'

    def get(self):
        ghid = self.get_secure_cookie('ghid')
        try:
            mp = self.get_session().query(MpSite).filter(MpSite.ghid == ghid).one()
            self.output_locations(mp.id)
            self.get_session().close()
        except NoResultFound:
            self.send_error('500')
