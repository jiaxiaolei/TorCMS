# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

import time
import tornado.escape
import config
import peewee
import datetime

from torlite.model.core_tab import CabPost2Catalog
from torlite.core import tools

from torlite.model.core_tab import CabReply
from torlite.model.core_tab import CabVoter2Reply
from torlite.model.core_tab import CabPost2Reply



class MReply():
    def __init__(self):
        try:
            CabReply.create_table()
        except:
            pass

    def add_one(self):


        pass

    def update_vote(self, reply_id, count):

        entry = CabReply.update(
            vote=count
        ).where(CabReply.uid == reply_id)

        entry.execute()


    def update(self, uid, post_data, update_time=False):

        if 'id_spec' in post_data:
            id_spec = post_data['id_spec'][0]
        else:
            id_spec = 0

        if 'src_type' in post_data and post_data['src_type'][0] == '1':
            cnt_html = tools.rst2html(post_data['cnt_md'][0])
        else:
            cnt_html = tools.markdown2html(post_data['cnt_md'][0])

        if update_time == True:
            entry = CabReply.update(
                title=post_data['title'][0],
                date=datetime.datetime.now(),
                cnt_html=cnt_html,
                user_name=post_data['user_name'],
                cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
                time_update=time.time(),
                id_spec=id_spec,
                logo=post_data['logo'][0],
                keywords=post_data['keywords'][0],
                src_type=post_data['src_type'][0] if ('src_type' in post_data) else 0
            ).where(CabReply.uid == uid)
        else:
            entry = CabReply.update(
                title=post_data['title'][0],
                # date=datetime.datetime.now(),
                cnt_html=cnt_html,
                user_name=post_data['user_name'],
                cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
                # time_update=time.time(),
                id_spec=id_spec,
                logo=post_data['logo'][0],
                keywords=post_data['keywords'][0],
                src_type=post_data['src_type'][0] if ('src_type' in post_data) else 0
            ).where(CabReply.uid == uid)
        entry.execute()


    def insert_data(self, post_data):

        uid = tools.get_uuid()

        entry = CabReply.create(
                uid=uid,
                #post_id=id_post,
                user_name=post_data['user_name'],
                create_user_id=post_data['user_id'],
                timestamp=time.time(),
                date=datetime.datetime.now(),
                cnt_md=post_data['cnt_md'][0],
                cnt_html=tools.markdown2html(post_data['cnt_md'][0]),
                vote=0,
            )

        return (uid)




    def query_old(self):
        return CabReply.select().order_by('time_update').limit(10)

    def query_random(self, num=6):
        if config.dbtype == 1 or config.dbtype == 3:
            return CabReply.select().order_by(peewee.fn.Random()).limit(num)
        elif config.dbtype == 2:
            return CabReply.select().order_by(peewee.fn.Rand()).limit(num)

    def query_cat_random(self, cat_id, num=6):
        if cat_id == '':
            return self.query_random(num)
        if config.dbtype == 1 or config.dbtype == 3:
            return CabReply.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(
                peewee.fn.Random()).limit(num)
        elif config.dbtype == 2:
            return CabReply.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(
                peewee.fn.Rand()).limit(num)



    def get_reply_by_uid(self, reply_id):
        rec = CabReply.get(CabReply.uid == reply_id)
        return rec
    def get_num_by_cat(self, cat_str):
        return CabReply.select().where(CabReply.id_cats.contains(',{0},'.format(cat_str))).count()

    def query_all(self):
        return CabReply.select()

    def query_keywords_empty(self):
        return CabReply.select().where(CabReply.keywords == '')

    def query_recent(self, num=8):
        return CabReply.select().order_by(CabReply.time_update.desc()).limit(num)

    def query_dated(self, num=8):
        return CabReply.select().order_by(CabReply.time_update).limit(num)

    def query_cat_recent(self, cat_id, num=8):
        return CabReply.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(
            CabReply.time_update.desc()).limit(num)

    def query_most(self, num=8):
        return CabReply.select().order_by(CabReply.view_count.desc()).limit(num)

    def query_recent_most(self, num=8, recent=30):
        time_that = int(time.time()) - recent * 24 * 3600
        return CabReply.select().where(CabReply.time_update > time_that).order_by(CabReply.view_count.desc()).limit(num)

    def query_cat_by_pager(self, cat_str, cureent):
        tt = CabReply.select().where(CabReply.id_cats.contains(str(cat_str))).order_by(
            CabReply.time_update.desc()).paginate(cureent, config.page_num)
        return tt

    def update_view_count(self, citiao):
        entry = CabReply.update(view_count=CabReply.view_count + 1).where(CabReply.title == citiao)
        entry.execute()

    def update_view_count_by_uid(self, uid):
        entry = CabReply.update(view_count=CabReply.view_count + 1).where(CabReply.uid == uid)
        entry.execute()

    def update_keywords(self, uid, inkeywords):
        entry = CabReply.update(keywords=inkeywords).where(CabReply.uid == uid)
        entry.execute()

    def get_by_wiki(self, citiao):
        tt = CabReply.select().where(CabReply.title == citiao).count()
        if tt == 0:
            return None
        else:
            self.update_view_count(citiao)
            return CabReply.get(CabReply.title == citiao)


    def get_next_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabReply.select().where(CabReply.time_update < current_rec.time_update).order_by(
            CabReply.time_update.desc())
        if query.count() == 0:
            return None
        else:
            return query.get()


    def get_previous_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabReply.select().where(CabReply.time_update > current_rec.time_update).order_by(CabReply.time_update)
        if query.count() == 0:
            return None
        else:
            return query.get()

    def query_by_spec(self, spec_id):
        tt = CabReply.select().where(CabReply.id_spec == spec_id).order_by(CabReply.time_update.desc())
        return tt

    def get_by_keyword(self, par2):
        return CabReply.select().where(CabReply.title.contains(par2)).order_by(CabReply.time_update.desc()).limit(20)

    def get_by_zan(self, reply_id):
        return CabVoter2Reply.select().where(CabVoter2Reply.reply_id == reply_id).count()




