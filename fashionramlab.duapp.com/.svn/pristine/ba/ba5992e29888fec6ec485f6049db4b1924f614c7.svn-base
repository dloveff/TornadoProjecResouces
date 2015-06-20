#! /usr/bin/env python -*- coding: utf-8 -*-

__author__ = '锦峰'

from orm import Base
from sqlalchemy.schema import Table
from sqlalchemy import String, Column, ForeignKey, Integer, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from uuid import uuid4
from datetime import datetime

circle_passport_rel = Table('weicbd_circle_passport_rel', Base.metadata,
                            Column('passport_id', Integer, ForeignKey('weicbd_passport.id')),
                            Column('circle_id', Integer, ForeignKey('weicbd_circle.id')))


class Circle(Base):
    __tablename__ = 'weicbd_circle'

    id = Column(Integer, primary_key=True)
    serial = Column(String(128))
    name = Column(String(255))
    description = Column(Text)
    create_time = Column(DateTime)

    owner_id = Column(Integer, ForeignKey('weicbd_passport.id'))

    owner = relationship('Passport', backref=backref('own_circles'))

    members = relationship('Passport', secondary=circle_passport_rel, backref='joined_circles')

    __table_args__ = (
        UniqueConstraint('serial'),
    )

    def __init__(self, name, description, owner_id=None):
        self.serial = uuid4().hex
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.create_time = datetime.now()
