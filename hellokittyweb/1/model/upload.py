#! /usr/bin/env python -*- coding: utf-8 -*-
__author__ = '北极鱼'

from orm import Base
from sqlalchemy.schema import Table
from sqlalchemy import String, Column, ForeignKey, Integer, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from uuid import uuid4
from datetime import datetime


class Images(Base):
    __tablename__ = 'openerp_op_upload'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255))
    filepath =Column(String(300))

    def __init__(self, filename, felepath):
        self.filename = filename
        self.filepath = felepath
