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

from torlite.model.core_tab import CabVoter2Reply
from torlite.model.core_tab import CabReply


class MReply2User():
    def __init__(self):
        try:
            CabVoter2Reply.create_table()
        except:
            pass


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
            entry = CabVoter2Reply.update(
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
            ).where(CabVoter2Reply.uid == uid)
        else:
            entry = CabVoter2Reply.update(
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
            ).where(CabVoter2Reply.uid == uid)
        entry.execute()


    def insert_data(self, user_id, reply_id):

        record = CabVoter2Reply.select().where(
            (CabVoter2Reply.reply_id == reply_id) & ( CabVoter2Reply.voter_id == user_id ))

        if record.count() > 0:
            pass
            return (False)
        else:
            entry = CabVoter2Reply.create(
                uid=tools.get_uuid(),
                reply_id=reply_id,
                voter_id=user_id,
                timestamp=time.time(),
            )
            cur_count = CabVoter2Reply.select().where(CabVoter2Reply.reply_id == reply_id).count()

            return cur_count


    def delete(self, del_id):

        try:
            del_count = CabReply.delete().where(CabReply.uid == del_id)
            del_count.execute()

            del_count2 = CabVoter2Reply.delete().where(CabVoter2Reply.reply_id == del_id)
            del_count2.execute()
            return True
        except:
            return False


    def query_old(self):
        return CabVoter2Reply.select().order_by('time_update').limit(10)


    def query_random(self, num=6):
        if config.dbtype == 1 or config.dbtype == 3:
            return CabVoter2Reply.select().order_by(peewee.fn.Random()).limit(num)
        elif config.dbtype == 2:
            return CabVoter2Reply.select().order_by(peewee.fn.Rand()).limit(num)


    def query_cat_random(self, cat_id, num=6):
        if cat_id == '':
            return self.query_random(num)
        if config.dbtype == 1 or config.dbtype == 3:
            return CabVoter2Reply.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(
                peewee.fn.Random()).limit(num)
        elif config.dbtype == 2:
            return CabVoter2Reply.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(
                peewee.fn.Rand()).limit(num)


    def get_by_id(self, in_uid):
        recs = CabVoter2Reply.select().where(CabVoter2Reply.post_id == in_uid).order_by(
            CabVoter2Reply.timestamp.desc())
        return recs


    def get_num_by_cat(self, cat_str):
        return CabVoter2Reply.select().where(CabVoter2Reply.id_cats.contains(',{0},'.format(cat_str))).count()


    def query_all(self):
        return CabVoter2Reply.select()


    def query_keywords_empty(self):
        return CabVoter2Reply.select().where(CabVoter2Reply.keywords == '')


    def query_recent(self, num=8):
        return CabVoter2Reply.select().order_by(CabVoter2Reply.time_update.desc()).limit(num)


    def query_dated(self, num=8):
        return CabVoter2Reply.select().order_by(CabVoter2Reply.time_update).limit(num)


    def query_cat_recent(self, cat_id, num=8):
        return CabVoter2Reply.select().join(CabPost2Catalog).where(CabPost2Catalog.catalog == cat_id).order_by(
            CabVoter2Reply.time_update.desc()).limit(num)


    def query_most(self, num=8):
        return CabVoter2Reply.select().order_by(CabVoter2Reply.view_count.desc()).limit(num)


    def query_recent_most(self, num=8, recent=30):
        time_that = int(time.time()) - recent * 24 * 3600
        return CabVoter2Reply.select().where(CabVoter2Reply.time_update > time_that).order_by(
            CabVoter2Reply.view_count.desc()).limit(num)


    def query_cat_by_pager(self, cat_str, cureent):
        tt = CabVoter2Reply.select().where(CabVoter2Reply.id_cats.contains(str(cat_str))).order_by(
            CabVoter2Reply.time_update.desc()).paginate(cureent, config.page_num)
        return tt


    def update_view_count(self, citiao):
        entry = CabVoter2Reply.update(view_count=CabVoter2Reply.view_count + 1).where(CabVoter2Reply.title == citiao)
        entry.execute()


    def update_view_count_by_uid(self, uid):
        entry = CabVoter2Reply.update(view_count=CabVoter2Reply.view_count + 1).where(CabVoter2Reply.uid == uid)
        entry.execute()


    def update_keywords(self, uid, inkeywords):
        entry = CabVoter2Reply.update(keywords=inkeywords).where(CabVoter2Reply.uid == uid)
        entry.execute()


    def get_by_wiki(self, citiao):
        tt = CabVoter2Reply.select().where(CabVoter2Reply.title == citiao).count()
        if tt == 0:
            return None
        else:
            self.update_view_count(citiao)
            return CabVoter2Reply.get(CabVoter2Reply.title == citiao)


    def get_next_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabVoter2Reply.select().where(CabVoter2Reply.time_update < current_rec.time_update).order_by(
            CabVoter2Reply.time_update.desc())
        if query.count() == 0:
            return None
        else:
            return query.get()


    def get_previous_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = CabVoter2Reply.select().where(CabVoter2Reply.time_update > current_rec.time_update).order_by(
            CabVoter2Reply.time_update)
        if query.count() == 0:
            return None
        else:
            return query.get()


    def query_by_spec(self, spec_id):
        tt = CabVoter2Reply.select().where(CabVoter2Reply.id_spec == spec_id).order_by(
            CabVoter2Reply.time_update.desc())
        return tt


    def get_by_keyword(self, par2):
        return CabVoter2Reply.select().where(CabVoter2Reply.title.contains(par2)).order_by(
            CabVoter2Reply.time_update.desc()).limit(20)

