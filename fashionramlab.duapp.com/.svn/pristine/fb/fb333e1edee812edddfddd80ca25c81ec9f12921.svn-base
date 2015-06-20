#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web, meta, auth
import xml.etree.ElementTree as ET
from db import Mysqldb, log

class MessagePatternHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mpreply/(.*)'

    def get_current_user(self):
        return self.get_secure_cookie('username') 
    def get_current_role(self):    
        return self.get_secure_cookie('role') 

    def get(self,mpid):
#       try:
        dao = MessageDaoHandler()
        root = ET.Element('message-pattern')   #设置根节点
        
        if dao.validmp(self.get_current_user(), mpid) or (self.get_current_role()=='admin'):
            #查出当前用户下信息 
            for result in dao.query_user_message_pattern(mpid) or []:
                id,pattern,claz,settings =result
                mess = ET.SubElement(root,'message', {'id':str(id), 'site-id':str(mpid)}) #设置子节点 属性值
                self.__append_element(mess, 'pattern', pattern)  #设置孙节点
                self.__append_element(mess, 'class', claz)
                self.__append_element(mess, 'settings', settings)         
            self.set_header('Content-Type', 'text/xml; charset=utf-8')    
            self.write(ET.tostring(root, encoding='UTF-8')) 
        else:
            self.send_error(401)    

    def __append_element(self, parent, tag, value):
        e = ET.Element(tag)
        if value:
            e.text = value
        parent.append(e)   
       
#    def put(self,rid):
#        dao =MessageDaoHandler()
#        root = ET.fromstring(self.request.body)
#        pattern =root.find('pattern').text    
#        clasz =root.find('class').text
#        settings =root.find('settings').text  
#      
#        if dao.validptn(self.get_current_user(), rid) or (self.get_current_role()=='admin'):
#            dao.put_message_pattern(int(rid),pattern,clasz,settings)
#            self.set_header('Content-Type', 'text/xml; charset=utf-8')
#            self.write('<message id = "%s"/>' % int(rid))        
#        else:
#            self.send_error(401)

                  
    def delete(self,rid):  
        dao =MessageDaoHandler()
        if dao.validptn(self.get_current_user(), rid) or (self.get_current_role()=='admin'):   
            dao.remove_message_pattern(int(rid)) 
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write('<message id="%s">' %int(rid))
        else:
            self.send_error(401)

class CreateMessageHandler(tornado.web.RequestHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = r'/mpreply'

    def get_current_user(self):
        return self.get_secure_cookie('username') 
    def get_current_role(self):    
        return self.get_secure_cookie('role') 
                   
    def post(self):
        dao = MessageDaoHandler()
        root = ET.fromstring(self.request.body)
        siteid =root.get('site-id')
        pattern =root.find('pattern').text
        claz =root.find('class').text
        settings =root.find('settings').text
            
        if dao.validmp(self.get_current_user(), siteid) or (self.get_current_role()=='admin'):
            res =dao.create_message_pattern(siteid,pattern,claz,settings)
            self.set_header('Content-Type', 'text/xml; charset=utf-8')
            self.write('<message id = "%s"/>' %int(res))
        else:
            self.send_error(401) 
     
            
class MessageDaoHandler(object):
     def __init__(self):
        self.db = Mysqldb()
        self.__create_table(self.db)
           
     def __create_table(self,db):  
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
        
        
     # 查找所有            
     def query_message_pattern(self,tid):
        return self.db.fetchall('select id,site_id,pattern,class,settings from weicbd_mp_message_patterns where site_id=%s',(tid,))   
     
     # 查找当前用户的所有信息
     def query_user_message_pattern(self,tid):
        return self.db.fetchall('select id,pattern,class,settings from weicbd_mp_message_patterns where site_id= %s ',(tid,))
     
     # 查当前用户  siteid
#     def query_username(self,siteid):
#        return self.db.fetchone('select a.username from weicbd_account as a,weicbd_mp_site as s where a.id=s.user_id and s.id=%s',(siteid,))
     
     # 查当前用户 rid
#     def query_rid_username(self,rid):
#        siteid = self.db.fetchone('select m.site_id from  weicbd_mp_message_patterns as  m,weicbd_mp_site as s where m.site_id=s.id and m.id=%s',(rid,))
#        return self.db.fetchone('select a.username from weicbd_account as a,weicbd_mp_site as s where a.id=s.user_id and s.id=%s',(siteid[0],))
     
     
     #  新建
     def create_message_pattern(self,userid,pattern,claz,settings):
        rt = self.db.execute('insert into weicbd_mp_message_patterns (site_id,pattern,class,settings) values(%s,%s,%s,%s)',(userid,pattern,claz,settings))
        self.db.commit()
        return rt
         
     #    编辑
     def put_message_pattern(self,rid,pattern,claz,setting):
        rt = self.db.execute("update weicbd_mp_message_patterns set pattern=%s,class=%s,settings=%s where id=%s",(pattern,claz,setting,rid))      
        self.db.commit()
        return rt   
        
     #   删除
     def remove_message_pattern(self,rid):
         rt =  self.db.execute('delete from weicbd_mp_message_patterns where id = %s',(rid,))
         self.db.commit()
         return rt   
         
     def validmp(self, username, mpid):
         n, = self.db.fetchone('SELECT COUNT(a.ID) FROM weicbd_account a, weicbd_mp_site m WHERE m.user_id=a.id AND a.username=%s AND m.id=%s',(username, mpid))
         return n == 1
     def validptn(self, username, rid):
         n, = self.db.fetchone('SELECT COUNT(a.ID) FROM weicbd_account a, weicbd_mp_site m, weicbd_mp_message_patterns p WHERE p.site_id=m.id AND m.user_id=a.id AND a.username=%s AND p.id=%s',(username, rid))
         return n == 1