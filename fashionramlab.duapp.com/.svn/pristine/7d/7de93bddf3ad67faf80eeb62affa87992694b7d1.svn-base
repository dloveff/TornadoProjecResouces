#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import meta
from weicbd.mp import MPSiteDao
from db import log, Mysqldb
from weicbd.pattern import MessagePatternDao
from urlparse import parse_qs


def decode_s_parameter(s):
    from zlib import decompress
    from base64 import b64decode
    return decompress(b64decode(s))


def encode_s_parameters(s):
    from zlib import compress
    from base64 import b64encode
    return b64encode(compress(s))


class WXHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/wx/(.*)'

    def get(self, token):
        try:
            from hashlib import sha1

            signature = sha1((''.join(
                sorted([token, self.get_argument('timestamp'), self.get_argument('nonce')])
            ))).hexdigest()
            #log(signature)
            #log(params['signature'][0])
            if signature == self.get_argument('signature'):
                # 验证成功
                dao = MPSiteDao()
                if dao.access(token):
                    self.write(self.get_argument('echostr'))
                else:
                    self.send_error(500)
        except:
            import traceback
            log(traceback.format_exc())

    def post(self, token):
        try:
            # log('\n'.join(['%s: %s' % (k, v) for k, v in self.request.headers.iteritems()]))
            # log('\n'.join(['%s: %s' % (k, v) for k, v in self.request.arguments.iteritems()]))
            plg = create_plugin_by_message(token, self.request)
            self.write(plg.response_message(self.request) if plg is not None else '')
        except:
            import traceback
            log(traceback.format_exc())


def create_plugin_by_message(token, request):
    plugin_class = None
    plugin_settings = None

    from lxml import etree

    root = etree.fromstring(request.body)
    dao = MessagePatternDao()
    for pt, pc, ps in dao.get_mp_plugins_by_token(token):
        if len(root.xpath(pt)) > 0:
            plugin_class = pc
            plugin_settings = ps
            break
    return None if plugin_class is None else create_plugin(plugin_class, root, plugin_settings, request)


def create_plugin(pc, et, settings_json, request):
    from json import loads

    settings = None
    try:
        settings = loads(settings_json)
    except:
        pass

    params = {}
    for elm in et.iter():
        params[elm.tag] = elm.text
    plg = load_class(pc)()
    plg.parameters = params
    plg.settings = settings
    plg.request = request
    return plg


def load_class(pc):
    component = pc.split('.')
    mod_name = '.'.join(component[:-1])
    cls_name = component[-1]
    mod = __import__(mod_name, fromlist=[cls_name])
    return getattr(mod, cls_name)


class weicbd_mp_context_redirect_app(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mpctx'

    def get(self):
        owp = parse_qs(decode_s_parameter(self.get_arguments('s')[0]))

        openid = owp['openid'][0]
        ghid = owp['ghid'][0]
        destUrl = self.get_argument('redirect')

        self.weicbd_register(ghid, openid)
        self.set_secure_cookie('openid', openid)
        self.set_secure_cookie('ghid', ghid)

        url = '%s://%s%s' % (self.request.protocol, self.request.host, destUrl)
        self.add_header('Content-Type', 'text/html; charset=utf-8')
        self.write('<!DOCTYPE html>')
        self.write('<html>')
        self.write('<head>')
        self.write('<meta charset="utf-8">')
        self.write('<script>')
        # 微信浏览器的BUG ？阻止浏览器刷新的重定向，可避免空白页出现
        self.write('window.history.replaceState({},"","%s");' % url)
        self.write('window.location.replace("%s");' % url)
        self.write('</script>')
        self.write('</html>')

        # 会出现空白页BUG的中转
        # self.redirect('http://fashionramlab.duapp.com%s' % destUrl)



    def weicbd_register(self,ghid,openid):
        db = Mysqldb()
        db.execute('''
            CREATE TABLE IF NOT EXISTS weicbd_mp_member_rel (
            id bigint NOT NULL AUTO_INCREMENT,
            ghid varchar(255) NULL,
            openid varchar(255) NULL,
            memberid bigint NULL,
            FOREIGN KEY (memberid) REFERENCES weicbd_member(id),
            PRIMARY KEY (id))''')
        result = db.fetchone('select id, ghid, openid from weicbd_mp_member_rel where ghid = %s and openid = %s', (ghid, openid)) or (None, )
        if result is None:
            db.execute('insert into weicbd_mp_member_rel (ghid,openid) values(%s,%s)', (ghid, openid))
            db.commit()


class weicbd_mp_current_member(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/curmember'

    def get(self):
        self.add_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<member>')
        self.write('<ghid>%s</ghid>' % self.get_secure_cookie('ghid') or 'None')
        self.write('<openid>%s</openid>' % self.get_secure_cookie('openid') or 'None')
        self.write('</member>')








