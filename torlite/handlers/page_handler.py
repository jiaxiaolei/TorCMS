# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

import tornado.web
import tornado.escape
from torlite.core import tools
from torlite.model.muser import MUser
from torlite.core.base_handler import BaseHandler
from torlite.model.mpage import MPage
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel


class PageHandler(BaseHandler):
    def initialize(self):
        self.muser = MUser()
        self.mdb = MPage()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mspec = SpesubModel()
        self.specs = self.mspec.get_all()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get(self, input=''):
        if input == '':
            return
        ip_arr = input.split(r'/')
        if (ip_arr[0] == 'modify'):
            self.to_modify(ip_arr[1])
        elif len(ip_arr) == 1 and input.endswith('.html'):
            self.wiki(input.split('.')[0])
        else:
            self.render('/html/404.html')

    def post(self, input=''):
        if len(input) > 0:
            ip_arr = input.split(r'/')
        if input == '':
            pass

        elif ip_arr[0] == 'modify':
            self.update(ip_arr[1])
        else:
            uuid = self.wikinsert()

    def wiki(self, slug):
        dbdate = self.mdb.get_by_slug(slug)
        if dbdate:
            self.viewit(dbdate)
        else:
            self.to_add(slug)

    @tornado.web.authenticated
    def to_add(self, citiao):
        kwd = {
            'cats': self.cats,
            'specs': self.specs,
            'slug': citiao,
            'pager': '',
        }
        self.render('tplite/page/addwiki.html', kwd=kwd)

    @tornado.web.authenticated
    def update(self, slug):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        self.mdb.update(slug, post_data)
        self.redirect('/page/{0}.html'.format(post_data['slug'][0]))

    @tornado.web.authenticated
    def to_modify(self, slug):
        kwd = {
            'pager': '',

        }
        self.render('tplite/page/modify.html',
                    view=self.mdb.get_by_slug(slug),
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape, )

    def viewit(self, dbdata):
        kwd = {
            'pager': '',
            'editable': 1 if self.get_current_user() else 0,
        }
        self.render('tplite/page/page_view.html',
                    view=dbdata,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    format_date=tools.format_date,
                    userinfo = self.userinfo,
                    )

    @tornado.web.authenticated
    def wikinsert(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        tt = self.mdb.get_by_slug(post_data['slug'][0])
        if tt is None:
            uid = self.mdb.insert_data(post_data)

        self.redirect('/page/{0}.html'.format(post_data['slug'][0]))
