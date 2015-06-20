#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web, json
import meta
from model.aaa import Passport
from orm import getSession
import xml.etree.ElementTree as ET
import auth
from . import ServiceHandlerBase


class AuthBaseHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass

    def get_current_user(self):
        pp = self.get_secure_cookie('passport')
        return json.loads(pp) if pp else None


class RegisterHandler(ServiceHandlerBase):
    __route__ = r'/register'

    def post(self):
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        mobile = self.get_argument('mobile', '')
        try:
            session = getSession()
            pp = Passport(email, mobile, password)
            session.add(pp)
            session.commit()
            self.set_secure_cookie('passport', json.dumps(dict(id=pp.id, email=pp.email, mobile=pp.mobile)))
            self.redirect(r'/')
        except:
            self.set_status(500)
            self.render('error.html', status=500, message='注册失败，请重新输入')


class LoginHandler(AuthBaseHandler):
    route = r'/login'
        
    def get(self):
        try:
            prompt = self.get_argument('prompt')
        except:
            prompt = ''
        self.render('login.html', prompt=prompt)

    def post(self):
        session = getSession()
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')        
        pp = session.query(Passport).filter(Passport.email == email, Passport.password == password).first()
        from urlparse import urlparse
        next_url = urlparse(self.get_argument('next', self.request.headers.get('Referer', r'/')))
        next = ''.join([
            ('%s' % next_url.path) if next_url.path else '/',
            (';%s' % next_url.params) if next_url.params else '',
            ('?%s' % next_url.query) if next_url.params else '',
            ('#%s' % next_url.fragment) if next_url.fragment else ''
        ])
        if pp:
            self.set_secure_cookie('passport', json.dumps(dict(id=pp.id, email=pp.email, mobile=pp.mobile)))
            self.redirect(next)
        else:
            prompt_msg = u'?prompt=%s&next=%s' % (tornado.escape.url_escape(u'用户名或密码错误'), tornado.escape.url_escape(next))
            self.redirect(u"/login%s" % prompt_msg)
        session.close()

class LogoutHandler(ServiceHandlerBase):
    __route__ = r'/logout'

    @auth.authenticated
    def post(self):
        self.clear_cookie('passport')
        # self.redirect(self.get_argument('next', self.request.headers.get('Referer', r'/')))
        self.redirect(r'/')


class LoginServiceHandler(ServiceHandlerBase):
    route = r'/r/login'

    @auth.authenticated
    def get(self):
        pp = self.get_current_user()
        out_elm = ET.Element('passport')
        out_elm.attrib['id'] = str(pp['id'])
        ET.SubElement(out_elm, 'email').text = pp['email']
        ET.SubElement(out_elm, 'mobile').text = pp['mobile']
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(ET.tostring(out_elm, encoding='UTF-8'))

    def post(self):
        in_elm = ET.fromstring(self.request.body)
        session = getSession()
        email = in_elm.findtext('email')
        password = in_elm.findtext('password')
        pp = session.query(Passport).filter(Passport.email == email, Passport.password == password).first()
        if pp:
            out_elm = ET.Element('passport')
            out_elm.attrib['id'] = str(pp.id)
            ET.SubElement(out_elm, 'email').text = pp.email
            ET.SubElement(out_elm, 'mobile').text = pp.mobile
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write(self.write(ET.tostring(out_elm, encoding='UTF-8')))
        else:
            self.send_error(401)


class PassportHandler(AuthBaseHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/passport'

    def get(self):
        pp = self.get_current_user()
        
        if pp:
            root = ET.Element('passport', id=str(pp.get('id')))
            ET.SubElement(root, 'email').text = pp.get('email')
            ET.SubElement(root, 'mobile').text = pp.get('mobile')
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write(ET.tostring(root, encoding='UTF-8'))
        else:
            self.send_error(401)
            
    def post(self):
        root = ET.fromstring(self.request.body)
        
        session = getSession()
        
        pp = Passport(
            root.findtext('email'),
            root.findtext('mobile'),
            root.findtext('password')
        )
        session.add(pp)
        session.commit()
        
        self.set_secure_cookie('passport', json.dumps(dict(id=pp.id, email=pp.email, mobile=pp.mobile)))
        
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<passport id ="%d"/>' % pp.id)
        
    def put(self):
        root = ET.fromstring(self.request.body)
        email = root.findtext('email')
        mobile = root.findtext('mobile')
        
        from sqlalchemy import or_
        
        session = getSession()
        pp = session.query(Passport).filter(or_(Passport.email == email, Passport.mobile == mobile)).first()
        cpp = self.get_current_user()
        if pp and (pp.id == cpp['id']):
            pp.email = email
            pp.mobile = mobile
            pp.password = root.findtext('password')
            
            session.merge(pp)
            session.commit()
            
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write('<passport id ="%d"/>' % pp.id)
        else:
            self.send_error(403)

