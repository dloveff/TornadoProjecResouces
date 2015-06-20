#! /usr/bin/env python
# -*- coding: utf-8 -*-

from orm import getSession
from model.tag import Tag
import meta
import tornado.web
from db import log
from sqlalchemy.orm.exc import NoResultFound
import xml.etree.ElementTree as ET
# from model.mpsite import MpSite, MpSetting
# from model.shop import Product, ProductSnap, Cart, Order

__author__ = '锦峰'
#
# class BaseShopHandler(tornado.web.RequestHandler):
#     def initialize(self):
#         self.session = getSession()
#
# class ProductsListHandler(BaseShopHandler):
#     __metaclass__ = meta.HandlerMetaClass
#     route = '...'