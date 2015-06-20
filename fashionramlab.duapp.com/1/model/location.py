#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chinfeng'

from orm import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Integer, UniqueConstraint
from sqlalchemy.orm import relationship, backref


class MpLocation(Base):
    __tablename__ = 'weicbd_mp_location'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    priority = Column(Integer)
    lon = Column(Float)
    lat = Column(Float)
    thumb = Column(String(500))

    mpid = Column(Integer, ForeignKey('weicbd_mp_site.id'))
    mpsite = relationship('MpSite', backref=backref('locations'))

    __table_args__ = (
        UniqueConstraint('mpid', 'priority'),
    )

    def __init__(self, name, address, priority, lon, lat, thumb, mpid=None):
        self.name = name
        self.address = address
        self.priority = priority
        self.lon = lon
        self.lat = lat
        self.thumb = thumb
        self.mpid = mpid
