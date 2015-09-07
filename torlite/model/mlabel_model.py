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
        try:
            CabLabel.create_table()
        except:
            pass
    def get_id_by_name(self, tag_name):
        uu = CabLabel.select().where(CabLabel.name == tag_name)
        if uu.count() > 0:
            return uu.get().uid
        else:
            return self.create_tag(tag_name)

    def create_tag(self, tag_name):
        uid = tools.get_uu8d()
        while CabLabel.select().where(CabLabel.uid == uid).count() > 0:
            uid = tools.get_uu8d()
        entry = CabLabel.create(
                uid= uid,
                name = tag_name,
                count = 0
            )
        return uid

class MPost2Label():
    def __init__(self):
        try:
            CabPost2Label.create_table()
        except:
            pass
        # self.mCabCatalog = MTag()
        self.mtag = MLabel()
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
        recs = CabPost2Label.select().order_by(CabPost2Label.order)
        return (recs)

    def query_count(self):
        recs = CabPost2Label.select(CabPost2Label.catalog, peewee.fn.COUNT(CabPost2Label.catalog).alias('num')).group_by(CabPost2Label.catalog)
        return (recs)


    def query_by_slug(self, slug):
        return CabPost2Label.select().join(CabCatalog).where(CabCatalog.slug == slug).order_by(peewee.fn.Rand())

    def get_by_id(self, idd):
        return CabPost2Label.select().join(CabLabel).where(CabPost2Label.app ==  idd)

    def get_by_info(self, post_id, catalog_id):
        tmp_recs = CabPost2Label.select().where((CabPost2Label.app == post_id) & (CabPost2Label.tag == catalog_id))
        if tmp_recs.count() > 1:
            ''' 如果多于1个，则全部删除
            '''
            for tmp_rec in tmp_recs:
                self.delete_by_id(tmp_rec.uid)
            return False
        if tmp_recs.count() == 1:
            return tmp_recs.get()
        else:
            return False

    def add_record(self, post_id, tag_name, order=1):


        tag_id = self.mtag.get_id_by_name(tag_name)
        tt = self.get_by_info(post_id, tag_id)
        if tt == False:

            entry = CabPost2Label.create(
                    uid=str(uuid.uuid1()),
                    app=post_id,
                    tag=tag_id,
                    order=order,
            )

        else:
            entry = CabPost2Label.update(
                order=order,
            ).where(CabPost2Label.uid == tt.uid)
            entry.execute()

    def delete_by_id(self, uid):
        entry = CabPost2Label.delete().where(CabPost2Label.uid == uid)
        entry.execute()
    def catalog_record_number(self, tag_id):
        return CabPost2Label.select().where(CabPost2Label.catalog == tag_id).count()

    def query_pager_by_slug(self, slug, current_page_num=1):
        return CabPost.select().join(CabPost2Label).where(CabPost2Label.tag == slug). paginate(current_page_num, config.page_num)