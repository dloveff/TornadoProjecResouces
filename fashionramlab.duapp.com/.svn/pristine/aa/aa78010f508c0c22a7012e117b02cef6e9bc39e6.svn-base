#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '锦峰'

from orm import Base
from sqlalchemy import Column, Integer, DateTime, Text
from datetime import datetime

__author__ = 'chinfeng'


class Logging(Base):
    __tablename__ = 'cloud_logging'

    id = Column(Integer, primary_key=True)
    tm = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)

    def __init__(self, content, tm=datetime.now()):
        self.content = content
        self.tm = tm
