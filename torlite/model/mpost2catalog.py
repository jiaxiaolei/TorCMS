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
        self.tab_post2catalog = CabPost2Catalog
        self.tab_catalog = CabCatalog
        self.tab_post = CabPost
        try:
            CabPost2Catalog.create_table()
        except:
            pass

    def query_all(self):
        recs = self.tab_post2catalog.select().order_by(self.tab_post2catalog.order)
        return (recs)


    def query_by_catid(self, catid):
        return self.tab_post2catalog.select().where(self.tab_post2catalog.catalog == catid)

    def query_by_id(self, idd):
        return self.tab_post2catalog.select().join(self.tab_catalog).where(self.tab_post2catalog.post == idd)

    def get_by_info(self, post_id, catalog_id):
        recs = self.tab_post2catalog.select().where(
            (self.tab_post2catalog.post == post_id) & (self.tab_post2catalog.catalog == catalog_id))
        if recs.count() > 1:
            for rec in recs:
                self.delete_by_id(rec.uid)
            return False
        elif recs.count() == 1:
            return self.tab_post2catalog.get((self.tab_post2catalog.post == post_id) & (self.tab_post2catalog.catalog == catalog_id))
        else:
            return False

    def query_count(self):
        recs = self.tab_post2catalog.select(self.tab_post2catalog.catalog,
                                      peewee.fn.COUNT(self.tab_post2catalog.catalog).alias('num')).group_by(
            self.tab_post2catalog.catalog)
        return (recs)

    def add_record(self, post_id, catalog_id, order=1):

        tt = self.get_by_info(post_id, catalog_id)
        if tt == False:
            print('a')
            entry = self.tab_post2catalog.create(
                uid=str(uuid.uuid1()),
                post=post_id,
                catalog=catalog_id,
                order=order,
            )
        else:
            entry = self.tab_post2catalog.update(
                order=order,
            ).where(self.tab_post2catalog.uid == tt.uid)
            entry.execute()

    def delete_by_id(self, uid):
        entry = self.tab_post2catalog.delete().where(self.tab_post2catalog.uid == uid)
        entry.execute()

    def catalog_record_number(self, cat_id):
        return self.tab_post2catalog.select().where(self.tab_post2catalog.catalog == cat_id).count()

    def query_catalog(self, post_id):
        return self.tab_post2catalog.select().where(self.tab_post2catalog.post == post_id)

    def query_pager_by_slug(self, slug, current_page_num=1):
        return self.tab_post.select().join(self.tab_post2catalog).join(self.tab_catalog).where(self.tab_catalog.slug == slug).order_by(
            self.tab_post.time_update.desc()).paginate(current_page_num, config.page_num)
    
    def query_by_app_uid(self, idd):
        return self.tab_post2catalog.select().join(self.tab_catalog).where(self.tab_post2catalog.post ==  idd).order_by(self.tab_post2catalog.order)

    def get_app_catalog(self, app_uid):
        # print(app_uid)
        uu = self.tab_post2catalog.select(). where((self.tab_post2catalog.post ==  app_uid) & (self.tab_post2catalog.order == 1))
        if uu.count() > 0:
            return uu.get()
        else:
            return False