#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '锦峰'

from orm import Base
from sqlalchemy import String, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship, backref


class ModuleDeployment(Base):
    __tablename__ = 'weicbd_module_deployment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cls = Column(String(255))
    name = Column(String(255))
    version = Column(String(255))
    serial = Column(String(33))
    
    circle_id = Column(Integer, ForeignKey('weicbd_circle.id'))
    circle = relationship('Circle', backref=backref('module_deployments'))

    def __init__(self, cls, name, version, serial, circle_id=None):
        self.cls = cls
        self.name = name
        self.version = version
        self.serial = serial
        self.circle_id = circle_id

