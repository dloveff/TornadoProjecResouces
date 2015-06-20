#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '北极鱼'

from orm import Base
from sqlalchemy import Column, Integer, DateTime, Text
from datetime import datetime

class Logging(Base):
    __tablename__ = 'sohobiz_logging'

    id = Column(Integer, primary_key=True)
    tm = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)

    __table_args__ = {
        'extend_existing': True
    }

    def __init__(self, content, tm=datetime.now()):
        self.content = content
        self.tm = tm
