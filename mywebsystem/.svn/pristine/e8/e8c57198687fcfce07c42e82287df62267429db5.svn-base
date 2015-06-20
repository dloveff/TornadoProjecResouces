#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '北极鱼'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from db import getLogger

import sys

Base = declarative_base()

if 'bae' in sys.modules:
    from bae.core import const
    engine = create_engine(
        'mysql://%s:%s@%s:%s/NtwLDxlnbZIsMEPsgrFH?charset=utf8' % (
        const.MYSQL_USER, const.MYSQL_PASS, const.MYSQL_HOST, const.MYSQL_PORT),
        echo=False, encoding='utf-8', poolclass=NullPool)
elif 'sae' in sys.modules:
    from sae import const
    engine = create_engine(       # 配置云平台引擎
        'mysql://%s:%s@%s:%s/%s?charset=utf8' % (
        const.MYSQL_USER, const.MYSQL_PASS, const.MYSQL_HOST, const.MYSQL_PORT, const.MYSQL_DB),
        echo=False, encoding='utf-8', poolclass=NullPool)
else:
    import sqlalchemy.engine.url
    import sqlite3
    url = sqlalchemy.engine.url.URL('sqlite', database=r'd:\weicbd_db.sqlite3')
    engine = create_engine(sqlalchemy.engine.url.make_url(url), connect_args={'detect_types': sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES, 'isolation_level': 'DEFERRED'},
                native_datetime=True, encoding='utf-8', poolclass=sqlalchemy.pool.NullPool)
    # engine.raw_connection().connection.text_factory = str

import model

def getSession():
    Session = sessionmaker(bind=engine) # 从绘画工厂里面拿到 sqlalchemy引擎
    return Session()


