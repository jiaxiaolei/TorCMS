# -*- coding:utf-8 -*-

import tornado.web
from torlite.core import tools
from torlite.model.mpost import MPost
from torlite.model.mcatalog import MCatalog


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.mpost = MPost()
        self.mcat = MCatalog()

    def get(self, input=''):
        if input == '':
            self.index()
        else:
            self.render('html/404.html')

    def index(self):
        # dbdata = self.mpost.query_cat_recent(5, 16)
        # recent = self.mpost.query_recent(10,8)
        # recent = self.mpost.query_cat_recent(10,8)
        cstr = tools.get_uuid()
        self.set_cookie('user_pass', cstr)
        kwd = {
            'cookie_str': cstr
        }
        self.render('tplite/index/index.html',
                    kwd = kwd,
                    # view=dbdata,
                    # recent=recent,
                    )




