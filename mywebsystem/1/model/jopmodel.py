#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '北极鱼'

from orm import Base
from sqlalchemy.schema import Table
from sqlalchemy import String, Column, ForeignKey, Integer, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from uuid import uuid4
from datetime import datetime

class JopInfoHandler(Base):
    __tablename__ = 'flower_jop_table'

    jop_id = Column(Integer, primary_key=True, autoincrement=True)  # 招聘编号
    jop_position = Column(String(50))   # 招聘职位名称
    jop_desc = Column(Text) # 招聘职位
    jop_reward =Column(Integer)  #报酬    可为空
    jop_time = Column(DateTime,default=datetime.now) # 发布时间
    jop_mobile = Column(String(100)) # 联系方式
    jop_userid = Column(Integer, ForeignKey('flower_user_table.user_id'), nullable=False)   # 用户外键

    def __init__(self, jop_position, jop_desc, jop_reward, jop_time, jop_mobile, jop_userid):
        self.jop_position = jop_position
        self.jop_desc = jop_desc
        self.jop_reward = jop_reward
        self.jop_time = jop_time
        self.jop_userid = jop_userid
        self.jop_mobile = jop_mobile