# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''
import tornado.web
import tornado.escape


from torlite.core.base_handler import BaseHandler
from torlite.model.mwiki import MWiki
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from torlite.core import tools
from torlite.model.mwiki_hist import MWikiHist
from torlite.model.muser import MUser


class WikiHandler(BaseHandler):
    def initialize(self):
        self.muser = MUser()
        self.mwiki = MWiki()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mspec = SpesubModel()
        self.specs = self.mspec.get_all()
        self.mwiki_hist = MWikiHist()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get(self, url_str=''):
        if url_str == '':
            return
        url_arr = url_str.split(r'/')

        if url_str == 'find':
            self.to_find()
        # elif url_arr[0] == 'find':
        #     self.find(url_arr[1])
        elif url_str == 'recent':
            self.recent()
        elif url_str == 'refresh':
            self.refresh()
        elif (url_arr[0] == 'modify'):
            self.to_modify(url_arr[1])
        elif len(url_arr) == 1:
            self.wiki(url_str)
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html', kwd=kwd)

    def post(self, input=''):
        if input == '':
            return
        url_arr = input.split(r'/')
        if url_arr[0] == 'modify':
            self.update(url_arr[1])
        # elif input == 'find':
        #     self.post_find()
        elif url_arr[0] == 'add':
            self.wikinsert()
        else:
            self.redirect('html/404.html')


    def to_find(self, ):
        kwd = {
            'pager': '',
        }
        self.render('tplite/post/find.html', topmenu='', kwd=kwd)


    def recent(self):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '最近文档',
        }
        self.render('tplite/wiki/all.html'.format(input),
                    kwd=kwd,
                    view=self.mwiki.query_recent(),
                    # rand_recs=self.get_random(),
                    format_date=tools.format_date, )

    def refresh(self):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '最近文档',
        }
        self.render('tplite/wiki/all.html'.format(input),
                    kwd=kwd,
                    view=self.mwiki.query_dated(16),
                    format_date=tools.format_date, )

    # def post_find(self):
    #     keyword = self.get_argument('keyword')
    #     self.find(keyword)

    # def find(self, keyword):
    #     kwd = {
    #         'pager': '',
    #         'unescape': tornado.escape.xhtml_unescape,
    #         'title': '查找结果',
    #     }
    #     self.render('tplite/wiki/find_list.html'.format(input),
    #                 kwd=kwd,
    #                 view=self.mwiki.get_by_keyword(keyword),
    #     )


    def get_random(self):
        return self.mwiki.query_random()




    def wiki(self, title):
        dbdate = self.mwiki.get_by_wiki(title)
        if dbdate:
            self.mwiki.update_view_count_by_uid(dbdate.uid)
            self.viewit(dbdate)
        else:
            self.to_add(title)


    @tornado.web.authenticated
    def to_add(self, title):
        kwd = {
            'cats': self.cats,
            'specs': self.specs,
            'title': title,
            'pager': '',
        }
        self.render('tplite/wiki/addwiki.html', kwd=kwd, )

    @tornado.web.authenticated
    def update(self, uid):
        raw_data = self.mwiki.get_by_id(uid)
        if self.userinfo.privilege[2] == '1' or raw_data.user_name == self.get_current_user():
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_name'] = self.get_current_user()
        self.mwiki.update(uid, post_data)
        self.mwiki_hist.insert_data(raw_data)
        self.redirect('/wiki/{0}'.format(post_data['title'][0]))

    @tornado.web.authenticated
    def to_modify(self, id_rec):
        a = self.mwiki.get_by_id(id_rec)
        # 用户具有管理权限，
        # 或
        # 文章是用户自己发布的。
        if self.userinfo.privilege[2] == '1' or a.user_name == self.get_current_user():
            pass
        else:
            return False

        kwd = {
            'pager': '',
            'cats': self.cats,
            'specs': self.specs,
        }
        self.render('tplite/wiki/modify.html',
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    tag_infos=self.mcat.query_all(),
                    dbrec =  a,
        )



    def viewit(self, view):
        # cats = self.mpost2catalog.query_catalog(post_id)
        kwd = {
            'pager': '',
            'editable': self.editable(),
        }

        self.render('tplite/wiki/viewiki.html',
                    view=view,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo, )


    @tornado.web.authenticated
    def wikinsert(self):
        if self.userinfo.privilege[1] == '1':
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.get_current_user()
        tt = self.mwiki.get_by_wiki(post_data['title'][0])
        if tt is None:
            uid = self.mwiki.insert_data( post_data)

        self.redirect('/wiki/{0}'.format(post_data['title'][0]))
