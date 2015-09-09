# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

import time
import datetime
import tornado
from torlite.core import tools
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
            cnt_html= tools.markdown2html(post_data['cnt_md'][0]),
            id_user='',
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=time.time(),
        ).where(CabPage.slug == slug)
        entry.execute()

    def insert_data(self, post_data):
        slug = post_data['slug'][0]
        uu = self.get_by_slug(slug)
        if uu is None:
            pass
        else:
            return (False)
        if 'id_spec' in post_data:
            id_spec = int(post_data['id_spec'][0])
        else:
            id_spec = 0

        try:
            entry = CabPage.create(
                title=post_data['title'][0],
                date=datetime.datetime.now(),
                slug=slug,
                cnt_html= tools.markdown2html(post_data['cnt_md'][0]),
                time_create=time.time(),
                id_user='',
                cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
                time_update=time.time(),
                view_count=1,
            )
        except:
            return ''
        return slug

    # def md2html(self, text):
    #     html = markdown2.markdown(text, extras=["wiki-tables"])
    #     return tornado.escape.xhtml_escape(html)
    #
    # def get_by_id(self, input):
    #     return CabPage.get(uid=input)


    def query_all(self):
        return CabPage.select().order_by('time_update')

    # def get_by_id(self, in_uid):
    #    return CabPage.get(id_post=in_uid)



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


    # def get_by_id(self, in_uid):
    #     tt = CabPage.get(CabPage.id_post == in_uid)
    #     return tt
    #
    #
