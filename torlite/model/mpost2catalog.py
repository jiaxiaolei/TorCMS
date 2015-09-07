# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''
import peewee
import uuid
from torlite.core.base_model import BaseModel

from torlite.model.core_tab import CabPost2Catalog
from torlite.model.core_tab import CabCatalog
from torlite.model.core_tab import CabPost
import config


class MPost2Catalog():
    def __init__(self):

        try:
            CabPost2Catalog.create_table()
        except:
            pass

    def query_all(self):
        recs = CabPost2Catalog.select().order_by(CabPost2Catalog.order)
        return (recs)


    def query_by_catid(self, catid):
        return CabPost2Catalog.select().where(CabPost2Catalog.catalog == catid)

    def query_by_id(self, idd):
        return CabPost2Catalog.select().join(CabCatalog).where(CabPost2Catalog.post == idd)

    def get_by_info(self, post_id, catalog_id):
        recs = CabPost2Catalog.select().where(
            (CabPost2Catalog.post == post_id) & (CabPost2Catalog.catalog == catalog_id))
        if recs.count() > 1:
            for rec in recs:
                self.delete_by_id(rec.uid)
            return False
        elif recs.count() == 1:
            return CabPost2Catalog.get((CabPost2Catalog.post == post_id) & (CabPost2Catalog.catalog == catalog_id))
        else:
            return False

    def query_count(self):
        recs = CabPost2Catalog.select(CabPost2Catalog.catalog,
                                      peewee.fn.COUNT(CabPost2Catalog.catalog).alias('num')).group_by(
            CabPost2Catalog.catalog)
        return (recs)

    def add_record(self, post_id, catalog_id, order=1):

        tt = self.get_by_info(post_id, catalog_id)
        if tt == False:
            print('a')
            entry = CabPost2Catalog.create(
                uid=str(uuid.uuid1()),
                post=post_id,
                catalog=catalog_id,
                order=order,
            )
        else:
            entry = CabPost2Catalog.update(
                order=order,
            ).where(CabPost2Catalog.uid == tt.uid)
            entry.execute()

    def delete_by_id(self, uid):
        entry = CabPost2Catalog.delete().where(CabPost2Catalog.uid == uid)
        entry.execute()

    def catalog_record_number(self, cat_id):
        return CabPost2Catalog.select().where(CabPost2Catalog.catalog == cat_id).count()

    def query_catalog(self, post_id):
        return CabPost2Catalog.select().where(CabPost2Catalog.post == post_id)

    def query_pager_by_slug(self, slug, current_page_num=1):
        return CabPost.select().join(CabPost2Catalog).join(CabCatalog).where(CabCatalog.slug == slug).order_by(
            CabPost.time_update.desc()).paginate(current_page_num, config.page_num)
    
    def query_by_app_uid(self, idd):
        return CabPost2Catalog.select().join(CabCatalog).where(CabPost2Catalog.post ==  idd).order_by(CabPost2Catalog.order)