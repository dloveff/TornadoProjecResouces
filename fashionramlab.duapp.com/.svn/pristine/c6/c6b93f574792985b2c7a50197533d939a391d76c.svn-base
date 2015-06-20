#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import mktime, localtime
import xml.etree.ElementTree as ET
import meta, base64, zlib
from urllib import quote_plus
from db import log
import tornado.web

textTmpl =  u'''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>
'''

spec_tmpl =  u'''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[<a href="%s">活动专场，全民大轮盘，赶快进入！</a>]]></Content>
</xml>
'''


class BasePlugin(object):
     def response_message(self, request=None):
         pass

        
class WallPlugin(BasePlugin):
    __metaclass__ = meta.PluginMetaClass
    name = '微信墙插件'

    def response_message(self, request):
        prefix = '%s://%s' % (request.protocol, request.host)
        in_key = self.settings['in-key']
        out_key = self.settings['out-key']
        openid = self.parameters['FromUserName']
        spec_key = self.settings.get('spec-key', None)
        ghid = self.parameters['ToUserName']
        outside_setting = self.settings['outside-wall']
        enter_setting = self.settings['enter-wall']
        sended_setting = self.settings['sended-wall']
        exit_setting = self.settings['exit-wall']
        dao = WallDao()

        state = dao.get_current_state(ghid, openid)
        if spec_key and (self.parameters['MsgType'] == 'text') and (self.parameters['Content'] == spec_key):
            return spec_tmpl % (self.parameters['FromUserName'], self.parameters['ToUserName'], int(mktime(localtime())), self.redirect_url(prefix, r'/spec-fan.html', self.parameters['FromUserName'], self.parameters['ToUserName']))
        elif state == 'in-wall':
            if (self.parameters['MsgType'] == 'text') and (self.parameters['Content'] == out_key):
                dao.set_state(ghid, openid, 'out-wall')
                return self.reply(prefix, openid, ghid, exit_setting)
            else:
                dao.push_message(ghid, openid, request.body)
                return self.reply(prefix, openid, ghid, sended_setting)
        elif state == 'out-wall':
            if (self.parameters['MsgType'] == 'text') and (self.parameters['Content'] == in_key):
                dao.set_state(ghid, openid, 'in-wall')
                return self.reply(prefix, openid, ghid, enter_setting)
            else:
                return self.reply(prefix, openid, ghid, outside_setting)

    def redirect_url(self, prefix, url, openid, ghid):
        if url[0:1] == '/':
            return '%s/mpctx?redirect=%s&s=%s' % (prefix,
                quote_plus('%s#weixin.qq.com' % url),
                quote_plus(base64.b64encode(zlib.compress(('openid=%s&ghid=%s' % (openid, ghid)))))
            )
        else:
            return url

    def reply(self, prefix, openid, ghid, reply_setting):
        from common import text_reply, articles_reply
        if 'Content' in reply_setting:
            return text_reply(prefix, openid, ghid, reply_setting['Content'])
        if 'Articles' in reply_setting:
            return articles_reply(prefix, openid, ghid, reply_setting['Articles'])


class MPWallListAfterIdHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mpwall/(.*)/(.*)'

    def get(self, token, mid):
        dao = WallDao()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<messages>')
        for mid, name, xml in dao.get_all_wall_message_after_id(token, int(mid)):
            self.write('<message id="%s">' % mid)
            root = ET.fromstring(xml)
            msgtype = root.findtext('MsgType')
            self.write('<openid>%s</openid>' % name)
            if msgtype == 'text':
                self.write('<text>%s</text>' % root.findtext('Content'))
            elif msgtype == 'image':
                self.write('<picurl>%s</picurl>' % root.findtext('PicUrl'))
            self.write('</message>')
        self.write('</messages>')

class MPSpecWallFanHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mpspecfan'

    def get(self):
        try:
            openid = self.get_secure_cookie('openid')
            ghid = self.get_secure_cookie('ghid')
            dao = WallDao()
            dao.set_spec_fan_join(ghid, openid)
            self.set_header('Content-Type', 'text/plain; charset=utf-8')
            f = dao.get_spec_fan_state(ghid, openid)
            self.write(str(f))
        except:
            import traceback
            log(traceback.format_exc())

class MPSpecWallFanListHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mpspecfans/(.*)'

    def get(self, token):
        dao = WallDao()
        spec_list_all = dao.get_all_spec_fan(token)
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<list>')
        map(lambda x: self.write('<openid>%s</openid>' % x), spec_list_all)
        self.write('</list>')

    def delete(self, token):
        dao = WallDao()
        dao.clear_spec_fan(token)
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<clear/>')

class MPSpecWallHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mpspecwall/(.*)/(.*)'

    def get(self, token, count):
        c = int(count)
        dao = WallDao()
        from random import shuffle
        spec_list_all = dao.get_all_spec_fan(token)
        shuffle(spec_list_all)
        spec_list = spec_list_all[:c]
        dao.set_spec_wall_state(token, spec_list)
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<list>')
        map(lambda x: self.write('<openid>%s</openid>' % x), spec_list)
        self.write('</list>')


class WallDao(object):
    def __init__(self):
        from db import Mysqldb
        self.db = Mysqldb()
        self.__create_table(self.db)

    def __create_table(self, db):
        db.execute('''
            CREATE TABLE IF NOT EXISTS weicbd_mp_wall_state (
                id bigint NOT NULL AUTO_INCREMENT,
                ghid varchar(255) NOT NULL,
                openid varchar(255) NOT NULL,
                state varchar(20) NOT NULL,

                PRIMARY KEY (id),
                UNIQUE(ghid, openid)
            ) DEFAULT CHARACTER SET=utf8;
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS weicbd_mp_wall_message (
                id bigint NOT NULL AUTO_INCREMENT,
                ghid varchar(255) NOT NULL,
                openid varchar(255) NOT NULL,
                content text,

                PRIMARY KEY (id)
            ) DEFAULT CHARACTER SET=utf8;
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS weicbd_mp_spec_wall (
                id bigint NOT NULL AUTO_INCREMENT,
                ghid varchar(255) NOT NULL,
                openid varchar(255) NOT NULL,
                flag tinyint DEFAULT 0,
                tm TIMESTAMP DEFAULT 0,

                PRIMARY KEY (id),
                UNIQUE(ghid, openid)
            ) DEFAULT CHARACTER SET=utf8;
        ''')

        db.commit()

    def get_current_state(self, ghid, openid):
        state, = self.db.fetchone('SELECT STATE FROM weicbd_mp_wall_state WHERE ghid=%s AND openid=%s', (ghid, openid)) or ('out-wall',)
        return state

    def push_message(self, ghid, openid, body):
        self.db.execute('INSERT INTO weicbd_mp_wall_message(ghid, openid, content) VALUES(%s, %s, %s)', (ghid, openid, body))
        self.db.commit()

    def set_state(self, ghid, openid, state):
        self.db.execute('REPLACE INTO weicbd_mp_wall_state(ghid, openid, state) VALUES(%s, %s, %s)', (ghid, openid, state))
        self.db.commit()

    def get_all_wall_message(self, token):
        return self.db.fetchall('SELECT msg.id, msg.openid, msg.content FROM weicbd_mp_wall_message msg, weicbd_mp_site mp WHERE msg.ghid=mp.ghid AND mp.token=%s ORDER BY ID ASC', (token,)) or []

    def get_all_wall_message_after_id(self, token, mid):
        return self.db.fetchall('SELECT msg.id, msg.openid, msg.content FROM weicbd_mp_wall_message msg, weicbd_mp_site mp WHERE msg.ghid=mp.ghid AND mp.token=%s AND msg.id>%s ORDER BY ID ASC', (token, mid)) or []

    def set_spec_fan_join(self, ghid, openid):
        from datetime import datetime
        self.db.execute('INSERT IGNORE INTO weicbd_mp_spec_wall(ghid, openid, tm) VALUES(%s, %s, %s)', (ghid, openid, datetime.now()))
        self.db.commit()

    def get_spec_fan_state(self, ghid, openid):
        f, = self.db.fetchone('SELECT flag FROM weicbd_mp_spec_wall WHERE ghid=%s AND openid=%s', (ghid, openid)) or (0,)
        return f

    def get_all_spec_fan(self, token):
        return [x[0] for x in (self.db.fetchall('SELECT w.openid FROM weicbd_mp_spec_wall w, weicbd_mp_site m WHERE w.ghid=m.ghid AND m.token=%s ORDER BY w.id ASC', (token, )) or [])]
    def clear_spec_fan(self, token):
        ghid, = self.db.fetchone('SELECT ghid FROM weicbd_mp_site WHERE token=%s', (token,))
        self.db.execute('DELETE FROM weicbd_mp_spec_wall WHERE ghid=%s', (ghid,))
        self.db.commit()

    def set_spec_wall_state(self, token, spec_list):
        ghid, = self.db.fetchone('SELECT ghid FROM weicbd_mp_site WHERE token=%s', (token,))
        self.db.execute('UPDATE weicbd_mp_spec_wall SET flag=0 WHERE ghid=%s', (ghid,))
        self.db.executemany('UPDATE weicbd_mp_spec_wall SET flag=%s WHERE openid=%s', [(1, openid) for openid in spec_list])
        self.db.commit()