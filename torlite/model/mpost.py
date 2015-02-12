# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

import time
import tornado.escape
import config
import peewee
import datetime

from torlite.model.core_tab import CabPost2Catalog
from torlite.core import tools


from torlite.model.core_tab import  CabPost

class MPost():
    def __init__(self):
        try:
            CabPost.create_table()
        except:
            pass

    def update(self, uid, post_data):
        if 'id_spec' in post_data:
            id_spec = post_data['id_spec'][0]
        else:
            id_spec = 0

        entry = CabPost.update(
            title=post_data['title'][0],
            date=datetime.datetime.now(),
            cnt_html= tools.markdown2html(post_data['cnt_md'][0]),

            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=time.time(),
            id_spec=id_spec,
            logo=post_data['logo'][0],

        ).where(CabPost.uid == uid)
        entry.execute()


    def insert_data(self, id_post, post_data):
        uu = self.get_by_id(id_post)
        if uu is None:
            pass
        else:
            return (False)
        if 'id_spec' in post_data:
            id_spec = post_data['id_spec'][0]
        else:
            id_spec = 0
        entry = CabPost.create(
            title=post_data['title'][0],
            date=datetime.datetime.now(),
            cnt_html=  tools.markdown2html(post_data['cnt_md'][0]),
            uid=id_post,
            time_create=time.time(),
            user_name= post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=time.time(),
            view_count=1,
            id_spec=id_spec,
            logo=post_data['logo'][0],
        )
        return (id_post)




    def query_old(self):
        return CabPost.select().order_by('time_update').limit(10)

    def query_random(self, num=6):
        if config.dbtype == 1 or config.dbtype == 3:
            return CabPost.select().order_by(peewee.fn.Random()).limit(num)
        elif config.dbtype == 2:
            return CabPost.select().order_by(peewee.fn.Rand()).limit(num)

    def query_cat_random(self, cat_id, num=6):
        if cat_id == '':
            return self.query_random(num)
        if config.dbtype == 1 or config.dbtype == 3:
            return CabPost.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(peewee.fn.Random()).limit(num)
        elif config.dbtype == 2:
            return CabPost.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(peewee.fn.Rand()).limit(num)

    def get_by_id(self, in_uid):
        tt = CabPost.select().where(CabPost.uid == in_uid).count()
        if tt == 0:
            return None
        else:
            return CabPost.get(CabPost.uid == in_uid)

    def get_num_by_cat(self, cat_str):
        return CabPost.select().where(CabPost.id_cats.contains(',{0},'.format(cat_str))).count()



    def query_recent(self, num=8):
        return CabPost.select().order_by(CabPost.time_update.desc()).limit(num)

    def query_dated(self, num=8):
        return CabPost.select().order_by(CabPost.time_update).limit(num)

    def query_cat_recent(self, cat_id, num=8):
        # return CabPost.select().where(CabPost.id_cats.contains(',{0},'.format(cat_id))).order_by(
        #     CabPost.time_update.desc()).limit(num)
        return CabPost.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(CabPost.time_update.desc()).limit(num)

    def query_most(self, num=8):
        return CabPost.select().order_by(CabPost.view_count.desc()).limit(num)

    def query_recent_most(self, num=8, recent=30):
        time_that = int(time.time()) - 30 * 24 * 3600
        return CabPost.select().where(CabPost.time_update > time_that).order_by(CabPost.view_count.desc()).limit(num)

    def query_cat_by_pager(self, cat_str, cureent):
        tt = CabPost.select().where(CabPost.id_cats.contains(str(cat_str))).order_by(
            CabPost.time_update.desc()).paginate(cureent, config.page_num)
        return tt

    def update_view_count(self, citiao):
        entry = CabPost.update(view_count=CabPost.view_count + 1).where(CabPost.title == citiao)
        entry.execute()

    def update_view_count_by_uid(self, uid):
        entry = CabPost.update(view_count=CabPost.view_count + 1).where(CabPost.uid == uid)
        entry.execute()

    def get_by_wiki(self, citiao):
        tt = CabPost.select().where(CabPost.title == citiao).count()
        if tt == 0:
            return None
        else:
            self.update_view_count(citiao)
            return CabPost.get(CabPost.title == citiao)

    def get_next_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabPost.select().where(CabPost.time_update < current_rec.time_update).order_by(
            CabPost.time_update.desc())
        if query.count() == 0:
            return None
        else:
            return query.get()

    def get_previous_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabPost.select().where(CabPost.time_update > current_rec.time_update).order_by(CabPost.time_update)
        if query.count() == 0:
            return None
        else:
            return query.get()


    def query_by_spec(self, spec_id):
        tt = CabPost.select().where(CabPost.id_spec == spec_id).order_by(CabPost.time_update.desc())
        return tt

    def get_by_keyword(self, par2):
        # return CabPost.select().where(CabPost.title ** '*{0}*'.format(par2)).order_by(CabPost.time_update.desc()).limit(20)
        return CabPost.select().where(CabPost.title.contains(par2)).order_by(CabPost.time_update.desc()).limit(20)