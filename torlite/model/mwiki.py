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

# from torlite.model.core_tab import CabWiki2Catalog
from torlite.core import tools

from torlite.model.core_tab import CabWiki


class MWiki():
    def __init__(self):
        try:
            CabWiki.create_table()
        except:
            pass

    def update(self, uid, post_data):


        print(post_data['src_type'][0])
        if post_data['src_type'][0] == '1':
            cnt_html = tools.rst2html(post_data['cnt_md'][0])
        else:
            cnt_html = tools.markdown2html(post_data['cnt_md'][0])

        entry = CabWiki.update(
            title=post_data['title'][0],
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=time.time(),
            # id_spec=id_spec,
            # logo=post_data['logo'][0],
            src_type=post_data['src_type'][0]
        ).where(CabWiki.uid == uid)
        entry.execute()


    def insert_data(self, post_data):
        title = post_data['title'][0]
        uu = self.get_by_wiki(title)
        if uu is None:
            pass
        else:
            return (False)
        if 'id_spec' in post_data:
            id_spec = post_data['id_spec'][0]
        else:
            id_spec = 0
        if post_data['src_type'][0] == '1':
            cnt_html = tools.rst2html(post_data['cnt_md'][0])
        else:
            cnt_html = tools.markdown2html(post_data['cnt_md'][0])

        uid = tools.get_uuid()
        entry = CabWiki.create(
            title=post_data['title'][0],
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            uid=uid,
            time_create=time.time(),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=time.time(),
            view_count=1,
            src_type=post_data['src_type'][0]
        )
        return (uid)


    def query_old(self):
        return CabWiki.select().order_by('time_update').limit(10)

    def query_random(self, num=6):
        if config.dbtype == 1 or config.dbtype == 3:
            return CabWiki.select().order_by(peewee.fn.Random()).limit(num)
        elif config.dbtype == 2:
            return CabWiki.select().order_by(peewee.fn.Rand()).limit(num)



    def get_by_id(self, in_uid):
        tt = CabWiki.select().where(CabWiki.uid == in_uid).count()
        if tt == 0:
            return None
        else:
            return CabWiki.get(CabWiki.uid == in_uid)

    def get_num_by_cat(self, cat_str):
        return CabWiki.select().where(CabWiki.id_cats.contains(',{0},'.format(cat_str))).count()


    def query_recent(self, num=8):
        return CabWiki.select().order_by(CabWiki.time_update.desc()).limit(num)

    def query_dated(self, num=8):
        return CabWiki.select().order_by(CabWiki.time_update).limit(num)

    def query_most(self, num=8):
        return CabWiki.select().order_by(CabWiki.view_count.desc()).limit(num)

    def query_recent_most(self, num=8, recent=30):
        time_that = int(time.time()) - 30 * 24 * 3600
        return CabWiki.select().where(CabWiki.time_update > time_that).order_by(CabWiki.view_count.desc()).limit(num)

    def query_cat_by_pager(self, cat_str, cureent):
        tt = CabWiki.select().where(CabWiki.id_cats.contains(str(cat_str))).order_by(
            CabWiki.time_update.desc()).paginate(cureent, config.page_num)
        return tt

    def update_view_count(self, citiao):
        entry = CabWiki.update(view_count=CabWiki.view_count + 1).where(CabWiki.title == citiao)
        entry.execute()

    def update_view_count_by_uid(self, uid):
        entry = CabWiki.update(view_count=CabWiki.view_count + 1).where(CabWiki.uid == uid)
        entry.execute()

    def get_by_wiki(self, citiao):
        tt = CabWiki.select().where(CabWiki.title == citiao).count()
        if tt == 0:
            return None
        else:
            self.update_view_count(citiao)
            return CabWiki.get(CabWiki.title == citiao)


    def get_next_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabWiki.select().where(CabWiki.time_update < current_rec.time_update).order_by(
            CabWiki.time_update.desc())
        if query.count() == 0:
            return None
        else:
            return query.get()


    def get_previous_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabWiki.select().where(CabWiki.time_update > current_rec.time_update).order_by(CabWiki.time_update)
        if query.count() == 0:
            return None
        else:
            return query.get()


    def query_by_spec(self, spec_id):
        tt = CabWiki.select().where(CabWiki.id_spec == spec_id).order_by(CabWiki.time_update.desc())
        return tt

    def get_by_keyword(self, par2):
        return CabWiki.select().where(CabWiki.title.contains(par2)).order_by(CabWiki.time_update.desc()).limit(20)