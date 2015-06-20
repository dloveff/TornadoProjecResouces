#! /usr/bin/env python -*- coding: utf-8 -*-
__author__ = '北极鱼'

from orm import Base
from sqlalchemy.schema import Table
from sqlalchemy import String, Column, ForeignKey, Integer, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from uuid import uuid4
from datetime import datetime

class Article(Base):
    __tablename__ = 'openerp_op_article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30))
    content = Column(Text)
    atime = Column(DateTime)
    priority = Column(Integer)
    tag = Column(String(50))

    def __init__(self, title, content, atime, priority, tag):

        self.title = title
        self.content = content
        self.atime = atime
        self.priority = priority
        self.tag = tag


class Comment(Base):
    __tablename__ = 'openerp_op_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id =Column(Integer, ForeignKey('openerp_op_article.id'))              #外键引用
    content = Column(Text)
    email = Column(String(35))

    article = relationship('Article', backref=backref('comments', uselist=True))    #一对多

    def __init__(self, article_id, content, email):
        self.article_id = article_id
        self.content = content
        self.email = email


class Password(Base):
      __tablename__='openerp_op_password'

      id = Column(Integer, primary_key=True, autoincrement=True)
      password=Column(String(30))

      def __init__(self, password):
          self.password = password
