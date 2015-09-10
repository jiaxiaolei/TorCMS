# -*- coding:utf-8 -*-

try:
    import tornadoredis
    c = tornadoredis.Client()
    c.connect()

except:
    pass
import tornado.web
import tornado.escape
from torlite.core import tools
from torlite.model.mpost import MPost
from torlite.model.mcatalog import MCatalog
from torlite.model.muser import MUser
# try:
#     import tormap
# except:
#     pass


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
