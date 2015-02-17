# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

import time
import uuid
import datetime
import tornado
import markdown2
from torlite.model.core_tab import CabPage


class MPage():
    def __init__(self):
        try:

            CabPage.create_table()
        except:
            pass

    def update(self, slug, post_data):
        entry = CabPage.update(
            title=post_data['title'][0],
            date=datetime.datetime.now(),
            cnt_html=self.md2html(post_data['cnt_md'][0]),
            id_user='',
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=time.time(),
        ).where(CabPage.slug == slug)
        entry.execute()

    def insert_data(self, post_data):
        uu = self.get_by_slug(post_data['slug'][0])
        if uu is None:
            pass
        else:
            return (False)
        if 'id_spec' in post_data:
            id_spec = int(post_data['id_spec'][0])
        else:
            id_spec = 0

        entry = CabPage.create(
            title=post_data['title'][0],
            date=datetime.datetime.now(),
            slug=post_data['slug'][0],
            cnt_html=self.md2html(post_data['cnt_md'][0]),
            # id_post=id_post,
            time_create=time.time(),
            id_user='',
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=time.time(),
            view_count=1,
        )
        return (id_post)

    def md2html(self, text):
        html = markdown2.markdown(text, extras=["wiki-tables"])
        return tornado.escape.xhtml_escape(html)

    def get_by_id(self, input):
        return CabPage.get(uid=input)


    def query_all(self):
        return CabPage.select().order_by('time_update')

    def get_by_id(self, in_uid):
        return CabPage.get(id_post=in_uid)


    def query_by_cat(self, cat_str):
        tt = CabPage.select().where((CabPage.id_cats.contains(str(cat_str))) & ((CabPage.type == 1))).order_by(
            'time_update')
        return tt

    def query_recent(self):
        tt = CabPage.select().where(CabPage.type == 1).order_by(CabPage.time_update.desc()).limit(10)
        return tt


    def get_by_slug(self, slug):

        entry = CabPage.update(
            view_count=CabPage.view_count + 1,  # 版权声明
        ).where(CabPage.slug == slug)
        entry.execute()

        tt = CabPage.select().where(CabPage.slug == slug).count()
        if tt == 0:
            return None
        else:
            return CabPage.get(CabPage.slug == slug)


    def get_by_id(self, in_uid):
        tt = CabPage.get(CabPage.id_post == in_uid)
        return tt


