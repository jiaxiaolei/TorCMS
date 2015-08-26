# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''

import tornado.web
import tornado.escape
import json
from torlite.core import tools
from torlite.core.base_handler import BaseHandler
from torlite.model.mpost import MPost
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from torlite.model.mpost_hist import MPostHist
from torlite.model.muser import MUser
from torlite.model.mpost2catalog import MPost2Catalog
from torlite.model.mreply import MReply


class PostHandler(BaseHandler):
    def initialize(self):
        self.muser = MUser()
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mspec = SpesubModel()
        self.specs = self.mspec.get_all()
        self.mpost_hist = MPostHist()
        self.mpost2catalog = MPost2Catalog()
        self.mreply = MReply()

        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get(self, url_str=''):


        if url_str == '':
            return
        url_arr = url_str.split('/')
        print(url_arr)
        if len(url_arr) == 1 and url_str.endswith('.html'):
            self.wiki(url_str.split('.')[0])
        elif url_str == 'find':
            self.to_find()
        elif url_arr[0] == 'find':
            self.find(url_arr[1])
        elif url_str == 'recent':
            self.recent()
        elif url_str == 'refresh':
            self.refresh()
        elif (url_arr[0] == 'modify'):
            self.to_modify(url_arr[1])

        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html', kwd=kwd)

    def post(self, url_str=''):
        if url_str == '':
            return
        url_arr = url_str.split('/')
        if url_arr[0] == 'modify':
            self.update(url_arr[1])
        elif url_str == 'find':
            self.post_find()
        elif url_arr[0] == 'add':
            self.add_post(url_arr[1])
        elif url_arr[0] == 'comment_add':
            self.add_comment(url_arr[1])

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
        self.render('tplite/post/all.html'.format(input),
                    kwd=kwd,
                    view=self.mpost.query_recent(),
                    # rand_recs=self.get_random(),
                    format_date=tools.format_date, )

    def refresh(self):
        kwd = {
            'pager': '',

            'title': '最近文档',
        }
        self.render('tplite/post/all.html'.format(input),
                    kwd=kwd,
                    view=self.mpost.query_dated(60),
                    format_date=tools.format_date,
                    unescape=tornado.escape.xhtml_unescape, )

    def post_find(self):
        keyword = self.get_argument('keyword')
        self.find(keyword)

    def find(self, keyword):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '查找结果',
        }
        self.render('tplite/post/find_list.html'.format(input),
                    kwd=kwd,
                    view=self.mpost.get_by_keyword(keyword),
        )


    def get_random(self):
        return self.mpost.query_random()

    def view_cat(self, cat_slug):
        for x in self.cats:
            if x.slug == cat_slug:
                search_str = ',{0},'.format(x.id_cat)
        dbdata = self.mpost.query_by_cat(search_str)
        self.render('tplite/post/all.html', view=dbdata, unescape=tornado.escape.xhtml_unescape)

    def wiki(self, uid):
        dbdate = self.mpost.get_by_id(uid)
        if dbdate:
            self.mpost.update_view_count_by_uid(dbdate.uid)
            self.viewit(dbdate)
        else:
            self.to_add(uid)

    @tornado.web.authenticated
    def to_add(self, uid):
        kwd = {
            'cats': self.cats,
            'specs': self.specs,
            'uid': uid,
            'pager': '',
        }
        self.render('tplite/post/addwiki.html', kwd=kwd, tag_infos=self.mcat.query_all(), )

    @tornado.web.authenticated
    def update(self, uid):
        raw_data = self.mpost.get_by_id(uid)
        if self.userinfo.privilege[2] == '1' or raw_data.user_name == self.get_current_user():
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_name'] = self.get_current_user()

        # if update the time
        is_update_time = True if post_data['is_update_time'][0] == '1' else False

        self.mpost.update(uid, post_data, update_time=is_update_time)
        self.update_catalog(uid)
        self.mpost_hist.insert_data(raw_data)
        self.redirect('/post/{0}.html'.format(uid))

    @tornado.web.authenticated
    def update_catalog(self, uid):
        raw_data = self.mpost.get_by_id(uid)
        if self.userinfo.privilege[2] == '1' or raw_data.user_name == self.get_current_user():
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        current_infos = self.mpost2catalog.query_by_id(uid)
        new_tag_arr = []
        for key in ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']:
            if post_data[key][0] == '':
                pass
            else:
                new_tag_arr.append(int(post_data[key][0]))
                self.mpost2catalog.add_record(uid, post_data[key][0], int(key[-1]))

        for cur_info in current_infos:
            if cur_info.catalog.uid not in new_tag_arr:
                self.mpost2catalog.delete_by_id(cur_info.uid)

                # self.redirect('/post/{0}.html'.format(uid))

    @tornado.web.authenticated
    def to_modify(self, id_rec):
        a = self.mpost.get_by_id(id_rec)
        # 用户具有管理权限，
        # 或
        # 文章是用户自己发布的。
        if self.userinfo.privilege[2] == '1' or a.user_name == self.get_current_user():
            pass
        else:
            return False

        id_spec = a.id_spec
        kwd = {
            'pager': '',
            'cats': self.cats,
            'specs': self.specs,
            'id_spec': id_spec,
        }
        self.render('tplite/post/modify.html',
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    tag_infos=self.mcat.query_all(),
                    app2tag_info=self.mpost2catalog.query_by_id(id_rec),
                    dbrec=a,
        )

    # @tornado.web.authenticated
    # def to_modify_catalog(self, id_rec):
    # # 用户具有管理权限，
    #     # 或
    #     # 文章是用户自己发布的。
    #     print(self.userinfo.privilege)
    #     if self.userinfo.privilege[4] == '1':
    #         pass
    #     else:
    #         print('Error')
    #         return False
    #     a = self.mpost.get_by_id(id_rec)
    #
    #     id_spec = a.id_spec
    #     kwd = {
    #         'pager': '',
    #         'cats': self.cats,
    #         'specs': self.specs,
    #         'view': a,
    #         'id_spec': id_spec,
    #     }
    #     self.render('tplite/post/edit_catalog.html', kwd=kwd, unescape=tornado.escape.xhtml_unescape,
    #                 tag_infos=self.mcat.query_all(),
    #                 app2tag_info=self.mpost2catalog.query_by_id(id_rec),
    #                 )

    def get_cat_str(self, cats):
        cat_arr = cats.split(',')
        out_str = ''
        for xx in self.cats:
            if str(xx.uid) in cat_arr:
                tmp_str = '''<li><a href="/category/{0}" style="margin:10px auto;"> {1} </a></li>
                '''.format(xx.slug, tornado.escape.xhtml_escape(xx.name))
                out_str += tmp_str

        return (out_str)

    def get_cat_name(self, id_cat):
        for x in self.cats:
            if x['id_cat'] == id_cat:
                return (x['name'])

    def viewit(self, post_id):
        cats = self.mpost2catalog.query_catalog(post_id)

        replys = self.mreply.get_by_id(post_id)

        for reply in replys:
            print(reply.vote)

        if cats.count() == 0:
            cat_id = ''
        else:
            cat_id = cats.get().catalog
        kwd = {
            'pager': '',
            'editable': self.editable(),
            'cat_id': cat_id
        }

        self.render('tplite/post/viewiki.html',
                    view=post_id,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    replys=replys,

        )

    @tornado.web.authenticated
    def add_post(self, id_post):
        if self.userinfo.privilege[1] == '1':
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.get_current_user()
        cur_post_rec = self.mpost.get_by_id(id_post)
        if cur_post_rec is None:
            uid = self.mpost.insert_data(id_post, post_data)
            self.update_catalog(uid)
        self.redirect('/post/{0}.html'.format(id_post))


    @tornado.web.authenticated
    def add_comment(self, id_post):
        if self.userinfo.privilege[0] == '1':
            pass
        else:
            return False

        post_data = {}

        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        print(post_data)
        post_data['user_id'] = self.userinfo.uid
        post_data['user_name'] = self.userinfo.user_name

        pl = self.mreply.insert_data(id_post, post_data)
        if pl:

            output = {
                'pinglun': pl,
            }
        else:
            output = {
                'pinglun': 0,
            }

        return json.dump(output, self)

        #self.redirect('/post/{0}.html'.format(id_post))


    def get_zan(self, f_zan):
        zan = self.mreply.get_by_zan(f_zan)
        if zan:
            output = {
                'zan': zan.zan,
            }
        else:
            output = {
                ''
            }




