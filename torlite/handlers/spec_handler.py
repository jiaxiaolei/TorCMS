# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''
import tornado.web
from torlite.model.muser import MUser
from torlite.model.mpost import MPost
from torlite.model.mpage import MPage
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from torlite.core.base_handler import BaseHandler


class SpecHandler(BaseHandler):
    def initialize(self):
        self.muser = MUser()
        self.mpage = MPage()
        self.mdb = MPost()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mspec = SpesubModel()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None


    def get(self, input=''):
        if len(input) > 0:
            ip_arr = input.split(r'/')
        if input == '':
            self.index()
        elif input == 'add':
            self.to_add()
        elif len(ip_arr) == 1:
            self.list(input)
        elif len(ip_arr) == 2 and ip_arr[1] == 'edit':
            self.to_edit(ip_arr[0])
        else:
            self.render('/html/404.html')

    def post(self, input=''):
        if len(input) > 0:
            ip_arr = input.split(r'/')
        if input == '':
            pass
        elif input == 'add':
            self.add()
        elif len(ip_arr) == 2 and ip_arr[1] == 'edit':
            self.edit(ip_arr[0])
        else:
            self.render('/html/404.html')
        self.redirect('/spec/')

    @tornado.web.authenticated
    def edit(self, uid):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        self.mspec.update(uid, post_data)

    @tornado.web.authenticated
    def add(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        self.mspec.addata(post_data)

    @tornado.web.authenticated
    def to_edit(self, uid):
        spec_rec = self.mspec.get_by_id(uid)
        self.render('tplite/spec/edit.html', spec_rec=spec_rec)

    @tornado.web.authenticated
    def to_add(self):
        # spec_rec = self.mspec.get_by_id(uid)
        # uuu = self.mcat.query_all()
        print('to_add')
        self.render('tplite/spec/add.html')

    def list(self, spec_slug):
        '''
        列出专题信息，按某一分类
        '''
        page_rec = self.mspec.get_by_slug(spec_slug)
        # content = self.mpage.get_by_wiki(page_rec.name)

        # if content is None:
        # re_url = '/page/{0}'.format(tornado.escape.url_escape(page_rec.name))
        #     self.redirect(re_url)



        kwd = {
            # 'spec': content,
            # 'view': recs,

            'editable': self.editable()
        }
        self.render('tplite/spec/list.html',
                    kwd=kwd,
                    spec=page_rec,
                    unescape=tornado.escape.xhtml_unescape,
                    spec_recs=self.mdb.query_by_spec(page_rec.uid),
        )


    def index(self):
        kwd = {
            # 'spec': content,
            # 'view': recs,
            'editable': self.editable()
        }
        spec_recs = self.mspec.get_all()
        self.render('tplite/spec/index.html', spec_recs=spec_recs, kwd=kwd)



