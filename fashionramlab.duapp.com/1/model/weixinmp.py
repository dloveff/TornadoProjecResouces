#! /usr/bin/env python
# -*- coding: utf-8 -*-

from orm import Base
from sqlalchemy import Text, Column, ForeignKey, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, backref

__author__ = 'chinfeng'


class WeixinMP(Base):
    __tablename__ = 'weicbd_weixin_mp'
    
    id = Column(Integer, autoincrement=True)

    token = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    ghid = Column(String(255))
    appid = Column(String(255))
    secret = Column(String(255))
    validated = Column(Boolean)
    validate_time = Column(DateTime)
    enabled = Column(Boolean)

    deployment_id = Column(Integer, ForeignKey('weicbd_module_deployment.id'), primary_key=True)
    deployment = relationship('ModuleDeployment', backref=backref('weixinmp', uselist=False))

    __table_args__ = (
        UniqueConstraint('deployment_id'),
    )

    def __init__(self, token, name, ghid=None, appid=None, secret=None, deployment_id=None):
        self.token = token
        self.name = name
        self.ghid = ghid
        self.appid = appid
        self.secret = secret
        self.validated = False
        self.validate_time = None
        self.enabled = True
        self.deployment_id = deployment_id

