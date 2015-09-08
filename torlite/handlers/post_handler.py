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
import config
from torlite.core import tools
from torlite.core.base_handler import BaseHandler
from torlite.model.mpost import MPost
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from torlite.model.mpost_hist import MPostHist
from torlite.model.muser import MUser
from torlite.model.mpost2catalog import MPost2Catalog
from torlite.model.mreply import MReply
from torlite.model.mpost2reply import MPost2Reply
from torlite.model.mlabel_model import MPost2Label
from torlite.model.mlabel_model import MLabel
from torlite.model.m_rel_model import MRel


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
        self.mpost2reply = MPost2Reply()
        self.mapp2tag = MPost2Label()
        self.mrel = MRel()

        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get(self, url_str=''):


        if url_str == '':
            return
        url_arr = url_str.split('/')

        if len(url_arr) == 1 and url_str.endswith('.html'):

            self.wiki(url_str.split('.')[0])
        # 弃用, /search 代替
        # elif url_arr[0] == 'find':
        # self.find(url_arr[1])
        # elif url_str == 'find':
        #     self.to_find()
        elif url_str == 'add_document':
            self.to_add_document()
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

        if len(url_arr) == 1 and url_str.endswith('.html'):
            sig = url_str.split('.')[0]
            self.add_post()

        if url_arr[0] == 'modify':
            self.update(url_arr[1])
        elif url_str == 'find':
            self.post_find()
        elif url_str == 'add_document':
            self.user_add_post()
        elif url_arr[0] == 'add':
            self.add_post()
        else:
            self.redirect('/html/404.html')


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
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
        )

    def refresh(self):

        kwd = {
            'pager': '',
            'title': '最近文档',
        }
        self.render('tplite/post/refresh.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    view=self.mpost.query_dated(10),
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
            self.viewit(uid)
        else:

            self.to_add(uid)

    def to_add_document(self, ):
        kwd = {
            'pager': '',
            'cats': self.cats,
            'specs': self.specs,
            'uid': '',

        }
        self.render('tplite/post/addwiki.html', topmenu='',
                    kwd=kwd,
                    tag_infos=self.mcat.query_all(),
                    userinfo = self.userinfo,
        )


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

        is_update_time = True if post_data['is_update_time'][0] == '1' else False
        self.update_tag(uid)
        self.mpost.update(uid, post_data, update_time=is_update_time)
        self.update_catalog(uid)
        self.mpost_hist.insert_data(raw_data)

        self.redirect('/post/{0}.html'.format(uid))

    def update_tag(self, signature):
        if self.userinfo.privilege[4] == '1':
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        current_tag_infos = self.mapp2tag.get_by_id(signature)

        tags_arr = [x.strip() for x in post_data['tags'][0].split(',')]


        for tag_name in tags_arr:
            if tag_name == '':
                pass
            else:
                self.mapp2tag.add_record(signature, tag_name, 1)

        for cur_info in current_tag_infos:
            if cur_info.tag.name in tags_arr:
                pass
            else:
                self.mapp2tag.delete_by_id(cur_info.uid)

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
                    app2label_info=self.mapp2tag.get_by_id(id_rec),
                    app2tag_info=self.mpost2catalog.query_by_id(id_rec),
                    dbrec=a,
                    userinfo = self.userinfo,
        )

    # @tornado.web.authenticated
    # def to_modify_catalog(self, id_rec):
    # # 用户具有管理权限，
    # # 或
    # # 文章是用户自己发布的。
    # print(self.userinfo.privilege)
    # if self.userinfo.privilege[4] == '1':
    # pass
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

        last_post_id = self.get_cookie('last_post_uid')
        self.set_cookie('last_post_uid', post_id)

        if last_post_id:
            self.add_relation(last_post_id, post_id)

        cats = self.mpost2catalog.query_catalog(post_id)
        replys = self.mpost2reply.get_by_id(post_id)
        tag_info = self.mapp2tag.get_by_id(post_id)

        rec = self.mpost.get_by_uid(post_id)

        if rec == False:
            kwd = {
                'info': '您要找的云算应用不存在。',
            }
            self.render('html/404.html', kwd=kwd)
            return False

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
                    view=rec,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    tag_info=tag_info,
                    relations=self.mrel.get_app_relations(rec.uid),
                    replys=replys,

        )


    def add_relation(self, f_uid, t_uid):
        if False == self.mpost.get_by_uid(t_uid):
            return False
        if f_uid == t_uid:
            '''
            关联其本身
            '''
            return False
        self.mrel.add_relation(f_uid, t_uid)
        return True

    @tornado.web.authenticated
    def add_post(self):
        if self.userinfo.privilege[1] == '1':
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.get_current_user()
        id_post = post_data['uid'][0]
        cur_post_rec = self.mpost.get_by_id(id_post)
        if cur_post_rec is None:
            uid = self.mpost.insert_data(id_post, post_data)
            self.update_tag(uid)
            self.update_catalog(uid)
        self.redirect('/post/{0}.html'.format(id_post))

    @tornado.web.authenticated
    def user_add_post(self):
        if self.userinfo.privilege[1] == '1':
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uu5d()
        while self.mpost.get_by_id(cur_uid):
            cur_uid = tools.get_uu5d()

        uid = self.mpost.insert_data(cur_uid, post_data)
        self.update_tag(uid)
        self.update_catalog(uid)
        self.redirect('/post/{0}.html'.format(cur_uid))


class LabelHandler(BaseHandler):
    def initialize(self):
        self.muser = MUser()
        self.mequa = MPost()
        self.mtag = MLabel()
        self.mapp2tag = MPost2Label()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get(self, input=''):
        if len(input) > 0:
            url_arr = input.split(r'/')

        if len(url_arr) == 1:
            self.list(input)
        elif len(url_arr) == 2:
            self.list(url_arr[0], url_arr[1])

    def post(self, url_str=''):
        if len(url_str) > 0:
            url_arr = url_str.split('/')
        if url_arr[0] == 'edit':
            self.edit(url_arr[1])

    def list(self, tag_slug, cur_p=''):
        '''
        根据 cat_handler.py 中的 def view_cat_new(self, cat_slug, cur_p = '')
        :param tag_slug:
        :return:
        '''
        if cur_p == '':
            current_page_number = 1
        else:
            current_page_number = int(cur_p)
        # taginfo = self.mtag.get_by_slug(tag_slug)
        # num_of_tag = self.mapp2tag.catalog_record_number(taginfo.uid)
        # page_num = int(num_of_tag / config.page_num ) + 1
        # tag_name = taginfo.name

        tag_name = 'fd'
        kwd = {
            'tag_name': tag_name,
            'tag_slug': tag_slug,
            'title': tag_name,
        }

        page_num = 5

        # infos = self.mapp2tag.query_by_slug(tag_slug)
        self.render('tplite/label/list.html',
                    infos=self.mapp2tag.query_pager_by_slug(tag_slug),
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    pager='',
                    userinfo=self.userinfo,
                    # self.gen_pager(tag_slug, page_num, current_page_number),
        )

    def gen_pager(self, cat_slug, page_num, current):
        # cat_slug 分类
        # page_num 页面总数
        # current 当前页面
        if page_num == 1:
            return ''

        pager_shouye = '''
        <li class="pure-menu-item first {0}">
        <a class="pure-menu-link" href="/tag/{1}">&lt;&lt; 首页</a>
                    </li>'''.format('hidden' if current <= 1 else '', cat_slug)

        pager_pre = '''
                    <li class="pure-menu-item previous {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">&lt; 前页</a>
                    </li>
                    '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
        pager_mid = ''
        for ind in range(0, page_num):
            tmp_mid = '''
                    <li class="pure-menu-item page {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">{2}</a></li>
                    '''.format('selected' if ind + 1 == current else '', cat_slug, ind + 1)
            pager_mid += tmp_mid
        pager_next = '''
                    <li class="pure-menu-item next {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">后页 &gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
        pager_last = '''
                    <li class="pure-menu-item last {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">末页
                        &gt;&gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
        pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
        return (pager)