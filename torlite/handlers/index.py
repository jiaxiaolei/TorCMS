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
            self.render('/html/404.html')

    def index(self):
        # dbdata = self.mpost.query_by_cat(',6,')
        recent = self.mpost.query_recent(8)
        self.render('tplite/index/index.html',
                    # view=dbdata,
                    recent=recent,
                    unescape=tornado.escape.xhtml_unescape,
                    format_yr=tools.format_yr)




