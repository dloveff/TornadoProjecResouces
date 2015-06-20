#! /usr/bin/env python
# -*- coding: utf-8 -*-

from orm import getSession
from model.tag import Tag
import meta
import tornado.web
from db import log
from sqlalchemy.orm.exc import NoResultFound
import xml.etree.ElementTree as ET
from model.cms import Article
from model.mpsite import MpSite
from weicbd.mpconsole import MPSiteDao

__author__ = 'chinfeng'


class BaseArticleListHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = getSession()

    def output_article_list_by_ghid(self, ghid, taglist, start, count):
        articles = self.session.query(Article).join(MpSite).filter(MpSite.ghid == ghid, Article.id > start)
        self.output_article_list(articles, taglist, count)

    def output_article_list_by_mpid(self, mpid, taglist, start, count):
        articles = self.session.query(Article).join(MpSite).filter(MpSite.id == mpid, Article.id > start)
        self.output_article_list(articles, taglist, count)

    def output_article_list(self, articles, taglist, count):
        if taglist:
            articles = articles.filter(Article.tags.any(Tag.id.in_(taglist))).limit(count)

        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<articles>')
        for article in articles:
            self.write('<article id="%d" mpid="%d">' % (article.id, article.mpsite.id))
            self.write('<title>%s</title>' % article.title)
            self.write('<dt>%s</dt>' % article.dt)
            self.write('<priority>%d</priority>' % article.priority)
            self.write('<summary>%s</summary>' % article.summary)
            self.write('<thumb>%s</thumb>' % article.thumb)
            self.write('<enabled>%d</enabled>' % article.enabled)
            self.write('<tags>')
            for t in article.tags:
                self.write('<tag id="%d" name="%s"/>' % (t.id, t.name))
            self.write('</tags>')
            self.write('</article>')
        self.write('</articles>')


class ConsoleArticleListHandler(BaseArticleListHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = '/mod/cms/mparticles/(.*)'

    def get(self, mpid_str):
        mpid = int(mpid_str)
        taglist = self.get_arguments('tag', [])
        start = int(self.get_argument('start', 0))
        count = int(self.get_argument('count', 50))
        self.output_article_list_by_mpid(mpid, taglist, start, count)


class MpArticleListHandler(BaseArticleListHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = '/mod/cms/mparticles'

    def get(self):
        ghid = self.get_secure_cookie('ghid')
        taglist = self.get_arguments('tag', [])
        start = int(self.get_argument('start', 0))
        count = int(self.get_argument('count', 50))
        self.output_article_list_by_ghid(ghid, taglist, start, count)

class PostMpArticleHandler(BaseArticleListHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = '/mod/cms/mparticle/(.*)'

    def post(self, mpid_str):
        mpid = int(mpid_str)
        root = ET.fromstring(self.request.body)
        title = root.findtext('title').encode('utf-8')
        from datetime import datetime
        dt = datetime.now()
        summary = root.findtext('summary').encode('utf-8')
        content = root.findtext('content').encode('utf-8')
        priority = root.findtext('priority')
        taglist = []
        map(lambda t: taglist.append(t.attrib['id']), root.find('tags').iter('tag'))
        thumb = root.findtext('thumb').encode('utf-8')
        images = ET.tostring(root.find('images'), encoding='utf-8')
        enabled = root.findtext('enabled')

        session = getSession()
        mpsite = session.query(MpSite).filter(MpSite.id == mpid).one()
        tags = session.query(Tag).filter(Tag.id.in_(taglist)).all()
        a = Article(title, dt, summary, content, priority, thumb, images, enabled)
        map(lambda t: a.tags.append(t), tags)
        a.mpsite = mpsite
        session.add(a)
        session.commit()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<article id="%d"/>' % a.id)

class MpArticleHandler(BaseArticleListHandler):
    __metaclass__ = meta.HandlerMetaClass
    route = '/mod/cms/article/(.*)'

    def get(self, aid_str):
        aid = int(aid_str)
        session = getSession()
        article = session.query(Article).filter(Article.id == aid).one()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<article id="%d">' % article.id)
        self.write('<title>%s</title>' % article.title)
        self.write('<dt>%s</dt>' % article.dt)
        self.write('<priority>%d</priority>' % article.priority)
        self.write('<summary>%s</summary>' % article.summary)
        self.write('<content><![CDATA[%s]]></content>' % article.content)
        self.write('<thumb>%s</thumb>' % article.thumb)
        self.write('<enabled>%d</enabled>' % article.enabled)
        self.write(article.images)
        self.write('<tags>')
        for t in article.tags:
            self.write('<tag id="%d" name="%s"/>' % (t.id, t.name))
        self.write('</tags>')
        self.write('</article>')

    def put(self, aid_str):
        aid = int(aid_str)
        session = getSession()
        article = session.query(Article).filter(Article.id == aid).one()
        root = ET.fromstring(self.request.body)
        article.title = root.findtext('title').encode('utf-8')
        from datetime import datetime
        article.dt = datetime.now()
        article.summary = root.findtext('summary').encode('utf-8')
        article.content = root.findtext('content').encode('utf-8')
        article.priority = root.findtext('priority')
        taglist = []
        map(lambda t: taglist.append(t.attrib['id']), root.find('tags').iter('tag'))
        tags = session.query(Tag).filter(Tag.id.in_(taglist)).all()
        article.tags[:] = tags
        article.thumb = root.findtext('thumb').encode('utf-8')
        article.images = ET.tostring(root.find('images'), encoding='utf-8')
        article.enabled = root.findtext('enabled')

        session.add(article)
        session.commit()
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write('<article id="%d"/>' % article.id)
