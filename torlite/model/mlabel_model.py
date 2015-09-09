# -*- coding:utf-8 -*-
'''
App对应的Tag
'''

import uuid

import peewee

from torlite.core import tools
import config
from torlite.model.core_tab import *


# from model.tag_model import MTag
from torlite.model.core_tab import CabCatalog
from torlite.model.core_tab import CabLabel
from torlite.model.core_tab import CabPost2Label
from torlite.model.core_tab import CabPost
# from torlite.tag_model import CabCatalog

# from torlite.model.mpost2catalog import CatPost2Catalog

class MLabel():
    def __init__(self):
        self.tab = CabLabel
        try:
            CabLabel.create_table()
        except:
            pass
    def get_id_by_name(self, tag_name):
        uu = self.tab.select().where(self.tab.name == tag_name)
        if uu.count() > 0:
            return uu.get().uid
        else:
            return self.create_tag(tag_name)

    def create_tag(self, tag_name):
        uid = tools.get_uu8d()
        while self.tab.select().where(self.tab.uid == uid).count() > 0:
            uid = tools.get_uu8d()

        entry = self.tab.create(
                uid= uid,
                name = tag_name,
                count = 0
            )
        return uid

class MPost2Label():
    def __init__(self):
        self.tab = CabPost2Label
        self.tab_label = CabLabel
        self.tab_post = CabPost
        self.mtag = MLabel()
        try:
            CabPost2Label.create_table()
        except:
            pass

    def generate_catalog_list(self, signature):
        # self.mapp2tag = model.app2tag_model.MApp2Tag()
        tag_infos = self.get_by_id(signature)
        out_str = ''
        for tag_info in tag_infos:
            tmp_str = '<li><a href="/tag/{0}" >{1}</a></li>'.format(tag_info.tag , tag_info.catalog_name)
            out_str += tmp_str
        # print(out_str)
        return out_str

    def query_all(self):
        recs = self.tab.select().order_by(self.tab.order)
        return (recs)

    # def query_count(self):
    #     recs = self.tab.select(self.tab.catalog, peewee.fn.COUNT(self.tab.catalog).alias('num')).group_by(self.tab.catalog)
    #     return (recs)


    # def query_by_slug(self, slug):
    #     return self.tab.select().join(CabCatalog).where(CabCatalog.slug == slug).order_by(peewee.fn.Rand())

    def get_by_id(self, idd):
        return self.tab.select().join(self.tab_label).where(self.tab.app ==  idd)

    def get_by_info(self, post_id, catalog_id):
        tmp_recs = self.tab.select().where((self.tab.app == post_id) & (self.tab.tag == catalog_id))
        print(tmp_recs.count())
        if tmp_recs.count() > 1:
            ''' 如果多于1个，则全部删除
            '''
            for tmp_rec in tmp_recs:
                self.delete_by_id(tmp_rec.uid)
            return False

        elif tmp_recs.count() == 1:
            return tmp_recs.get()
        else:
            return False

    def add_record(self, post_id, tag_name, order=1):
        print('=' * 100)
        print(post_id)
        print(tag_name)

        tag_id = self.mtag.get_id_by_name(tag_name)
        print(tag_id)
        tt = self.get_by_info(post_id, tag_id)
        print(tt)
        if tt == False:
            entry = self.tab.create(
                    uid=str(uuid.uuid1()),
                    app=post_id,
                    tag=tag_id,
                    order=order,
            )

        else:
            entry = self.tab.update(
                order=order,
            ).where(self.tab.uid == tt.uid)
            entry.execute()

    def delete_by_id(self, uid):
        entry = self.tab.delete().where(self.tab.uid == uid)
        entry.execute()
    def catalog_record_number(self, tag_id):
        return self.tab.select().where(self.tab.catalog == tag_id).count()

    def query_pager_by_slug(self, slug, current_page_num=1):
        return self.tab_post.select().join(self.tab).where(self.tab.tag == slug). paginate(current_page_num, config.page_num)