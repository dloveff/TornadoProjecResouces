#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '锦峰'

import tornado.web, meta, auth
import xml.etree.ElementTree as ET
from db import Mysqldb, log
from uuid import uuid4
from model.aaa import Passport, Account, Role
from orm import getSession


#class LoginHandler(tornado.web.RequestHandler):
    #__metaclass__ = meta.HandlerMetaClass
    #route = r'/login'

    #def post(self):
        #dao = AAADao()
        #root = ET.fromstring(self.request.body)
        #username = root.findtext('username') or ''
        #password = root.findtext('password') or ''
        #if dao.valid(username, password):
            #atk = uuid4().hex
            #self.set_header('Content-Type', 'text/xml; charset=utf-8')
            #self.write('<login><access-token>%s</access-token></login>' % atk)
            #self.set_secure_cookie('username', username)
            #self.set_secure_cookie('role', dao.get_role(username).role)
            #self.set_secure_cookie('access-token', atk)
        #else:
            #self.send_error(401)


#class LogoutHandler(tornado.web.RequestHandler):
    #__metaclass__ = meta.HandlerMetaClass
    #route = r'/logout'

    #def post(self):
        #self.clear_cookie('username')
        #self.clear_cookie('role')
        #self.clear_cookie('access-token')
        #self.set_header('Content-Type', 'text/xml; charset=utf-8')
        #self.write('<logout/>')


class PutUserHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/user'

    def get_current_user(self):
        return self.get_secure_cookie('username')

    @auth.authenticated
    def put(self):
        dao = AAADao()
        root = ET.fromstring(self.request.body)
        fullname = root.findtext('fullname')
        mobile = root.findtext('mobile')
        email = root.findtext('email')
        user_id = dao.update_user(self.get_current_user(), fullname, mobile, email)
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<user id="%s"/>' % user_id)


class GetCurrentUserHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/currentuser'

    def get_current_user(self):
        return self.get_secure_cookie('username')

    @auth.authenticated
    def get(self):
        dao = AAADao()
        username = self.get_current_user()
        u = dao.get_user(username)
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<user id="%s">' % u.id)
        self.write('<username>%s</username>' % username)
        self.write('<fullname>%s</fullname>' % u.fullname)
        self.write('<mobile>%s</mobile>' % u.mobile)
        self.write('<email>%s</email>' % u.email)
        self.write('<role>%s</role>' % u.role.role)
        self.write('<role-name>%s</role-name>' % u.role.name)
        self.write('</user>')


# class RegisterHandler(tornado.web.RequestHandler):
#     __metaclass__ = meta.HandlerMetaClass
#     route = r'/register'
#
#     def post(self):
#         root = ET.fromstring(self.request.body)
#         session = getSession()
#         a = Account(
#             root.findtext('username'),
#             root.findtext('password'),
#             root.findtext('fullname'),
#             root.findtext('mobile'),
#             root.findtext('email')
#         )
#         user_role = session.query(Role).filter(Role.role == 'user').one()
#         a.role = user_role
#         session.add(a)
#         session.commit()
#
#         self.set_secure_cookie('username', a.username)
#         self.set_secure_cookie('role', 'user')
#         self.set_secure_cookie('access-token', uuid4().hex)
#         self.set_header('Content-Type', 'text/xml; charset=utf-8')
#         self.write('<register><user id="%s"/></register>' % a.id)
#         session.close()


class UserListHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/users'

    def get_current_user(self):
        return self.get_secure_cookie('username') if self.get_secure_cookie('role') == 'admin' else None

    @auth.authenticated
    def get(self):
        dao = AAADao()
        ul = dao.get_user_list()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<users>')
        for u in ul:
            self.write('<user id="%d">' % u.id)
            self.write('<username>%s</username>' % u.username)
            self.write('<fullname>%s</fullname>' % u.fullname)
            self.write('<mobile>%s</mobile>' % u.mobile)
            self.write('<email>%s</email>' % u.email)
            self.write('<role>%s</role>' % u.role.role)
            self.write('<role-name>%s</role-name>' % u.role.name)
            self.write('</user>')
        self.write('</users>')


class ResetPasswordHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/resetpwd/(.*)'

    def get_current_user(self):
        return self.get_secure_cookie('username')

    @auth.authenticated
    def put(self, user_id):
        dao = AAADao()
        u = dao.get_user(self.get_current_user())
        # 当前用户或管理员可改变
        if (u[4] == 'admin') or (u[0] == int(user_id)):
            root = ET.fromstring(self.request.body)
            password = root.findtext('password')
            dao.reset_password_by_id(user_id, password)
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write('<user id="%s"/>' % user_id)
        else:
            self.send_error(401)


from orm import getSession
from model.aaa import Account, Role


class AAADao(object):
    # def __init__(self):
    #     self.db = Mysqldb()
    #     self.__create_table(self.db)

    # def __create_table(self, db):
    #     db.execute('''
    #         CREATE TABLE IF NOT EXISTS weicbd_role (
    #             id bigint NOT NULL AUTO_INCREMENT,
    #             role varchar(255) NOT NULL,
    #             name varchar(255) NOT NULL,
    #
    #             PRIMARY KEY(id),
    #             UNIQUE KEY(role)
    #         ) DEFAULT CHARACTER SET=utf8;
    #     ''')
    #
    #     db.execute('''
    #         CREATE TABLE IF NOT EXISTS weicbd_account (
    #             id bigint NOT NULL AUTO_INCREMENT,
    #             role_id bigint NOT NULL,
    #             username varchar(255) NOT NULL,
    #             password varchar(255) NOT NULL,
    #             fullname varchar(255) NOT NULL,
    #             mobile varchar(12) NOT NULL,
    #             email varchar(255) DEFAULT NULL,
    #
    #             PRIMARY KEY(id),
    #             FOREIGN KEY(role_id) REFERENCES weicbd_role(id),
    #             UNIQUE KEY(username),
    #             unique(mobile)
    #         ) DEFAULT CHARACTER SET=utf8;
    #     ''')
    #
    #     rid = db.execute('INSERT IGNORE INTO weicbd_role(role, name) VALUES(%s, %s)', ('admin','管理员'))
    #     db.execute('INSERT IGNORE INTO weicbd_role(role, name) VALUES(%s, %s)', ('user','用户'))
    #     db.execute('INSERT IGNORE INTO weicbd_account(role_id, username, password, fullname, mobile) VALUES(%s, %s, %s, %s, %s)', (rid, 'admin', 'admin','超级管理员', '13392260602'))
    #     db.commit()

    def valid(self, username, password):
        session = getSession()
        n = session.query(Account).filter(Account.username == username, Account.password == password).count()
        return n == 1
        # n, = self.db.fetchone('SELECT COUNT(id) FROM weicbd_account WHERE username=%s AND password=%s', (username, password))
        # return n == 1

    def get_user(self, username):
        session = getSession()
        return session.query(Account).filter(Account.username == username).first()
        # return self.db.fetchone('SELECT u.id, u.fullname, u.mobile, u.email, r.role, r.name FROM weicbd_account u, weicbd_role r WHERE u.role_id = r.id AND u.username=%s', (username, ))

    def insert_user(self, username, password, fullname, mobile, email):
        session = getSession()
        a = Account(username, password, fullname, mobile, email)
        session.add(a)
        session.commit()
        return a.id
        # rt = self.db.execute('INSERT INTO weicbd_account(username, password, fullname, mobile, email, role_id) SELECT %s, %s, %s, %s, %s, id FROM weicbd_role WHERE role=%s', (username, password, fullname, mobile, email, 'user'))
        # self.db.commit()
        # return rt

    def get_role(self, username):
        session = getSession()
        a = session.query(Account).filter(Account.username == username).first()
        return a.role
        # role, = self.db.fetchone('SELECT r.role FROM weicbd_account u, weicbd_role r WHERE u.role_id = r.id AND u.username=%s', (username, ))
        # return role

    def get_user_list(self):
        session = getSession()
        return session.query(Account).all()
        # return self.db.fetchall('SELECT u.id, u.username, u.fullname, u.mobile, u.email, r.role, r.name FROM weicbd_account u, weicbd_role r WHERE u.role_id = r.id')

    def reset_password_by_id(self, user_id, password):
        session = getSession()
        a = session.query(Account).filter(Account.id == user_id).first()
        a.password = password
        session.merge(a)
        session.commit()
        # self.db.execute('UPDATE weicbd_account SET password=%s WHERE id=%s', (password, user_id))
        # self.db.commit()

    def update_user(self, username, fullname, mobile, email):
        session = getSession()
        a = session.query(Account).filter(Account.username == username).first()
        a.fullname = fullname
        a.mobile = mobile
        a.email = email
        session.merge(a)
        session.commit()
        return a.id
        # rt = self.db.execute('UPDATE weicbd_account SET fullname=%s, mobile=%s, email=%s WHERE username=%s',
        #                 (fullname, mobile, email, username))
        # self.db.commit()
        # return rt
