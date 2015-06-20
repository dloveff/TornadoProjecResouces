#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '锦峰'

from orm import Base
from sqlalchemy import String, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship, backref


class Passport(Base):
    __tablename__ = 'weicbd_passport'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True)
    mobile = Column(String(100), unique=True)
    password = Column(String(255))

    def __init__(self, email, mobile, password):
        self.email = email
        self.mobile = mobile
        self.password = password


class MemberInformation(Base):
    __tablename__ = 'weicbd_member_information'

    id = Column(Integer, primary_key=True, autoincrement=True)
    passport_id = Column(Integer, ForeignKey('weicbd_passport.id'))
    nickname = Column(String(255))

    passport = relationship('Passport', backref=backref('information', uselist=False))

    def __init__(self):
        pass


class Account(Base):
    __tablename__ = 'weicbd_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    password = Column(String(255))
    fullname = Column(String(255))
    mobile = Column(String(100))
    email = Column(String(255))

    role_id = Column(Integer, ForeignKey('weicbd_role.id'))
    role = relationship('Role', backref=backref('users'))

    __table_args__ = (
        UniqueConstraint('fullname'),
    )

    def __init__(self, username, password, fullname, mobile, email, role_id=None):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.mobile = mobile
        self.email = email
        self.role_id = role_id


class Role(Base):
    __tablename__ = 'weicbd_role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(255))
    name = Column(String(255))

    __table_args__ = (
        UniqueConstraint('role'),
    )

    def __init__(self, role, name):
        self.role = role
        self.name = name