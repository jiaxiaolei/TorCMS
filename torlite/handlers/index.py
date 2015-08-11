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
try:
    import torapp
except:
    pass


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


class AppIndexHandler(tornado.web.RequestHandler):
    '''
    For site with Additional Application. Use Redis to speed up the site
    '''
    def initialize(self):
        self.mpost = MPost()
        self.mapp = torapp.model.app_model.MApp()

        self.mcat = MCatalog()
        self.muser = MUser()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get_current_user(self):
        return self.get_secure_cookie("user")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, input=''):
        if input == '':
            self.index()
        else:
            self.render('html/404.html')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def index(self):
        cstr = tools.get_uuid()
        self.set_cookie('user_pass', cstr)
        kwd = {
            'cookie_str': cstr
        }

        out_str = self.gen_info()

        pipe = c.pipeline()
        pipe.set('fooa', out_str)
        pipe.expire('fooa', 60 * 60 * 25)

        res_hset, res_expire = yield tornado.gen.Task(pipe.execute)
        foo2 = yield tornado.gen.Task(c.get, 'fooa')

        self.render('tplite/index/index.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    catalog_info = self.mcat.query_all(by_order=True),
                    foo=foo2,
                    unescape=tornado.escape.xhtml_unescape,
                    )

    def gen_info(self):
        tmpl1 = '''
        <div class="pure-u-1-2 pure-u-md-1-2">
                <div class="panel-cat">
                    <h3><a href="http://www.yunsuan.org/tag/{0}">{1} App</a></h3>
                    <ul>
                    {2}
                    </ul>
                </div>
            </div>
            '''

        tmpl2 = '''
        <li ><a href="/app/{0}" title="{1}">{1}</a></li>
            '''
        out_str = ''

        catalog_info = self.mcat.query_all(by_order=True)
        for cat_info in catalog_info:
            li_str = ''
            all_cats = self.mapp.query_most_by_cat(10, cat_info.uid)
            for rec in all_cats:
                str2 = tmpl2.format(rec.uid, rec.title)
                li_str += str2
            str1 = tmpl1.format(cat_info.slug, cat_info.name, li_str)
            out_str += str1
        return out_str
