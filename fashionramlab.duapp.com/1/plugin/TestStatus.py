#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import mktime, localtime
import xml.etree.ElementTree as ET
import meta, base64, zlib
from urllib import quote_plus
from db import log

# 请求状态
textTmpl = u'''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[<a href="http://fashionramlab.duapp.com/xf.html">%s</a>]]></Content>
</xml>
'''

all_mp_menu = u'''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>
'''


top_menu =  u'''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>
'''


bottom_menu =  u'''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>
'''


class BasePlugin(object):
    def response_message(self, request = None):
        pass

class TestingReplyPlugin(BasePlugin):
    __metaclass__ = meta.PluginMetaClass
    name = '内部测试雷'

    def response_message(self,request):
        try: 
            in_key = self.settings['in-key']
            out_key = self.settings['out-key']
            openid = self.parameters['FromUserName']
            ghid = self.parameters['ToUserName']
            content = self.parameters['Content'] 
            dao = MenuDao()
            state = dao.query_current_status(ghid,openid)  #   或得当前用户状态
            # 判断用户第一次输入
            if content == '菜单':   # 一级菜单                
                dao.create_status(ghid,openid,'菜单a')    # 新建菜单,设置状态            
                result = dao.query_all_menu()         # 菜单列表    
                if result is not None:
                    return all_mp_menu %(openid,ghid,int(mktime(localtime())),self.response(result))          
            elif (content=='1') or (content=='2'): # 二级菜单
                statea = dao.query_current_status(ghid,openid) 
                if statea == '菜单a':
                    dao.create_status(ghid,openid,'菜单b') # 改变状态
                    result = dao.query_bottom_menu(content)  #进入二级菜单   
                    if result is not None:
                        return bottom_menu %(self.parameters['FromUserName'],self.parameters['ToUserName'],int(mktime(localtime())),self.response(result))                               
            elif content=='3': # 返回一级菜单
                stateb = dao.query_current_status(ghid,openid) 
                if stateb == '菜单b':
                    dao.create_status(ghid,openid,'菜单a')
                    result = dao.query_all_menu()
                    if result is not None:
                        return all_mp_menu %(self.parameters['FromUserName'],self.parameters['ToUserName'],int(mktime(localtime())),self.response(result)) 
            else:
                return textTmpl %(self.parameters['FromUserName'],self.parameters['ToUserName'],int(mktime(localtime())),u'您的输入有误!')  
        except:
            import traceback
            log(traceback.format_exc())
            
    def response(self,result):
        return '\n'.join(['%s: %s' % (r1, r2) for r1, r2 in result])
   
            
class MenuDao(object):
    
    def __init__(self):
        from db import Mysqldb
        self.db = Mysqldb()
        self.__create_table(self.db)
            
    def __create_table(self,db):
        db.execute('''
            create table if not exists weicbd_mp_teststatus(
                id bigint AUTO_INCREMENT,
                ghid varchar(255) NOT NULL,
                openid varchar(255) NOT NULL,
                state varchar(50) not null,
                       
                PRIMARY KEY (id)
            )
        ''')
        db.execute('''
            create table if not exists weicbd_mp_menu(
                id bigint AUTO_INCREMENT,
                menu varchar(255) not null,
                menuid varchar(255) not null,
                content text null,    
                PRIMARY KEY (id)
            )
        ''')
        db.commit()
        
    #   创建/修改状态             
    def create_status(self, ghid, openid, state):
        result = self.db.fetchone('select * from weicbd_mp_teststatus where ghid=%s and openid=%s',(ghid,openid))
        if result is not None:
            rt = self.db.execute('update weicbd_mp_teststatus set state=%s where ghid=%s and openid=%s',(state,ghid,openid))
            self.db.commit()
            return rt
        else:
            rt = self.db.execute('REPLACE INTO weicbd_mp_teststatus (ghid,openid,state) values(%s,%s,%s)',(ghid,openid,state))
            self.db.commit()
            return rt
    #   查看当前状态
    def query_current_status(self,ghid,openid):
        state, = self.db.fetchone('select state from weicbd_mp_teststatus where ghid=%s and openid=%s',(ghid,openid)) or('out_wall',)    
        return state
        
    #   返回当前用户信息
    def query_current_userinfo(self, ghid):
        return self.db.fetchone('select ghid,openid,state weicbd_mp_teststatus wehere ghid=%s',(ghid,))
        
    #   创建目录    
    def create_menu(self, menu, menuid, content):
        rt = self.db.execute('insert into weicbd_mp_menu (menu,menuid,content) values(%s,%s,%s)',(menu,menuid,content))
        self.db.commit()
        return rt
        
    #   查一级菜单列表    
    def query_all_menu(self):
        return self.db.fetchall('select menu,content from weicbd_mp_menu where menuid=0')
   
    #   查二级菜单
    def query_bottom_menu(self,menu):
        return self.db.fetchall('select menuid,content from weicbd_mp_menu where menu=%s and menuid>0',(menu,))

    