#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '北极鱼'

from orm import Base
from sqlalchemy import String, Column, ForeignKey, Integer, Text


class FlowerTypeHandler(Base):  # 类别
    __tablename__ = 'flower_type_table '

    ftype_id = Column(Integer, primary_key=True, autoincrement=True)  # 编号
    ftype_name = Column(String(50))  # 类别名称

    def __init__(self, ftype_name):
        self.ftype_name = ftype_name

class FlowerHandler(Base):  # 花卉
    __tablename__ = 'flower_table'

    flower_id = Column(Integer, primary_key=True, autoincrement=True)  # 编号
    flower_name = Column(String(50))   # 花卉名称
    flower_desc = Column(Text)  # 花卉描述
    ftype_id = Column(Integer, ForeignKey('flower_type_table.ftype_id'), nullable=False)   # 类别外键
    tags_id = Column(Integer, ForeignKey('flower_tags_table.tags_id'), nullable=False)   # 标签外键

    def __init__(self, flower_name, flower_desc, ftype_id, tags_id):
        self.flower_name = flower_name
        self.flower_desc = flower_desc
        self.ftype_id = ftype_id
        self.tags_id = tags_id

class FlowerTagsHandler(Base):  # 标签
    __tablename__ = 'flower_tags_table'

    tags_id = Column(Integer, primary_key=True, autoincrement=True)   # 编号
    tags_name = Column(String(50))  # 标签名
    flower_id = Column(Integer, ForeignKey('flower_table.flower_id'), nullable=False)   # 外键 花卉



































