#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chinfeng'


class MessagePatternDao(object):
    def __init__(self):
        from db import Mysqldb
        self.db = Mysqldb()
        self.__create_table(self.db)

    def __create_table(self, db):
        # 事件规则使用表：weicbd_mp_message_patterns(id, site_id, pattern, class, settings)
        # 根据获得的xml文本，匹配处理插件
        # pattern 为一个xpath 表达式，如：/xml[MsgType="event" and Event="CLICK"]
        # 当表达式找到元素，则匹配这个class
        db.execute('''
            CREATE TABLE IF NOT EXISTS weicbd_mp_message_patterns (
                id bigint NOT NULL AUTO_INCREMENT,
                site_id bigint NOT NULL,
                pattern varchar(255) NOT NULL,
                class varchar(255) NOT NULL,
                settings text, 

                PRIMARY KEY (id),
                FOREIGN KEY (site_id) REFERENCES weicbd_mp_site(id)
            ) DEFAULT CHARACTER SET=utf8;
        ''')
        db.commit()

    def get_mp_plugins_by_token(self, token):
        return self.db.fetchall('SELECT p.pattern, p.class, p.settings FROM weicbd_mp_message_patterns p, weicbd_mp_site s WHERE p.site_id = s.id AND s.token=%s', (token,))
        
    def get_mp_plugins_by_id(self, id):
        return self.db.fetchall('SELECT id, pattern, class, settings FROM weicbd_mp_message_patterns WHERE site_id=%s', (id,))
        
    def add_plugin(self, site_id, pattern, cn, settings):
        rt = self.db.execute('INSERT IGNORE INTO weicbd_mp_message_patterns(site_id, pattern, class, settings) VALUES(%s, %s, %s, %s)',
            (site_id, pattern, cn, settings))
        self.db.commit()
        return rt
        
    def remove_plugin(self, id):
        self.db.execute('DELETE FROM weicbd_mp_message_patterns WHERE id=%s', (id,))
        self.db.commit()