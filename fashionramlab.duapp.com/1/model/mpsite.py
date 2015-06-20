#! /usr/bin/env python
# -*- coding: utf-8 -*-

from orm import Base
from sqlalchemy import Text, Column, ForeignKey, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, backref

__author__ = 'chinfeng'


class MpSite(Base):
    __tablename__ = 'weicbd_mp_site'

    id = Column(Integer, primary_key=True)

    token = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    ghid = Column(String(255))
    appid = Column(String(255))
    secret = Column(String(255))
    validated = Column(Boolean)
    validate_time = Column(DateTime)
    enabled = Column(Boolean)

    user_id = Column(Integer)

    __table_args__ = (
        UniqueConstraint('token'),
    )

    def __init__(self, token, name, ghid=None, appid=None, secret=None, validated=False, validate_time=None, enabled=True, user_id=None):
        self.token = token
        self.name = name
        self.ghid = ghid
        self.appid = appid
        self.secret = secret
        self.validated = validated
        self.validate_time = validate_time
        self.enabled = enabled
        self.user_id = user_id


class MpSetting(Base):
    __tablename__ = 'weicbd_mp_setting'

    id = Column(Integer, primary_key=True)
    mpid = Column(Integer, ForeignKey('weicbd_mp_site.id'))
    key = Column(String(255), nullable=False)
    value = Column(Text)
    mpsite = relationship('MpSite', backref=backref('settings'))

    def __init__(self, key, value, mpid=None):
        self.key = key
        self.value = value
        self.mpid = mpid
