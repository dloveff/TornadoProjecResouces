#! /usr/bin/env python
# -*- coding: utf-8 -*-

from orm import Base
from sqlalchemy import String, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship, backref

__author__ = 'chinfeng'


class Tag(Base):
    __tablename__ = 'weicbd_mp_tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    mpid = Column(Integer, ForeignKey('weicbd_mp_site.id'))
    parent_id = Column(Integer, ForeignKey('weicbd_mp_tag.id'), nullable=True)

    # children = relationship('Tag', cascade='all', backref=backref("parent", remote_side='Tag.id'), collection_class=attribute_mapped_collection('name'))
    children = relationship('Tag', cascade='all', backref=backref("parent", remote_side='Tag.id'))
    mpsite = relationship('MpSite', backref=backref('tags'))

    __table_args__ = (
        UniqueConstraint('mpid', 'parent_id', 'name'),
    )

    def __init__(self, name, mpid, parent_id=None):
        self.name = name
        self.mpid = mpid
        self.parent_id = parent_id
