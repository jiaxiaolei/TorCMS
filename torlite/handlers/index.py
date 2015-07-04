# -*- coding:utf-8 -*-

import tornado.web
from torlite.core import tools
from torlite.model.mpost import MPost
from torlite.model.mcatalog import MCatalog
from torlite.model.muser import MUser

class IndexHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.muser = MUser()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self, input=''):
        if input == '':
            self.index()
        else:
            self.render('html/404.html')

    def index(self):
        cstr = tools.get_uuid()
        self.set_cookie('user_pass', cstr)
        kwd = {
            'cookie_str': cstr
        }
        self.render('tplite/index/index.html',
                    kwd = kwd,
                    userinfo=self.userinfo,
                    catalog_info  = self.mcat.query_all( by_order=True)
                    )
