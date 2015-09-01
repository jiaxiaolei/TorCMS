# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

import tornado.web
import tornado.escape

import  config
from torlite.core import tools
from torlite.core.base_handler import BaseHandler
from torlite.model.mpost import MPost
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from torlite.model.mpost2catalog import MPost2Catalog
from torlite.model.muser import MUser


class CatHandler(BaseHandler):
    def initialize(self):
        self.muser = MUser()
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mspec = SpesubModel()
        self.specs = self.mspec.get_all()
        self.mpost2catalog = MPost2Catalog()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get(self, input=''):
        if len(input) > 0:
            ip_arr = input.split(r'/')
        if input == '':
            pass
        elif len(ip_arr) == 1 :
            self.list_catalog(input)
        elif len(ip_arr) == 2:
            self.list_catalog(ip_arr[0], ip_arr[1])
        else:
            self.render('/html/404.html')

    def list_catalog(self, cat_slug, cur_p = ''):
        if cur_p == '':
            current_page_num = 1
        else:
            current_page_num = int(cur_p)

        cat_rec = self.mcat.get_by_slug(cat_slug)
        num_of_cat = self.mpost2catalog.catalog_record_number(cat_rec.uid)
        page_num = int(num_of_cat / config.page_num ) + 1
        cat_name = cat_rec.name
        kwd = {
             'cat_name': cat_name,
             'cat_slug': cat_slug,
             'unescape':  tornado.escape.xhtml_unescape,
             'title': cat_name,
        }

        self.render('tplite/catalog/list.html',
                    infos=self.mpost2catalog.query_pager_by_slug(cat_slug,current_page_num),
                    pager = tools.gen_pager(cat_slug, page_num, current_page_num),
                    userinfo = self.userinfo,
                    kwd=kwd)

    # def view_cat_old(self, cat_slug, cur_p=''):
    #     if cur_p == '':
    #         current = 1
    #     else:
    #         current = int(cur_p)
    #
    #     cat_rec = self.mcat.get_by_slug(cat_slug)
    #     num_of_cat = self.mpost.get_num_by_cat(cat_rec.id_cat)
    #     page_num = int(num_of_cat / config.page_num ) + 1
    #
    #     cat_name = cat_rec.name
    #     kwd = {
    #         'cat_name': cat_name,
    #         'cat_slug': cat_slug,
    #         'unescape':  tornado.escape.xhtml_unescape,
    #         'pager': tools.gen_pager(cat_slug, page_num, current),
    #         'title': cat_name,
    #     }
    #     for x in self.cats:
    #         if x.slug == cat_slug:
    #             search_str = ',{0},'.format(x.id_cat)
    #     dbdata = self.mpost.query_cat_by_pager(search_str, current)
    #     self.render('tplite/post/all.html',
    #                 kwd = kwd,
    #                 view=dbdata,
    #                 rand_recs = self.get_random(),
    #                 format_date = tools.format_date)



    def get_random(self):
        return self.mpost.query_random()