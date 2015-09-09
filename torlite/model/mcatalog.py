# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

from torlite.model.core_tab import CabCatalog


class MCatalog():
    def __init__(self):
        self.tab = CabCatalog
        try:
            CabCatalog.create_table()
        except:
            pass

    def query_all(self, with_count=False, by_order=False):
        if with_count == True:
            recs = self.tab.select().order_by(self.tab.post_count.desc())
        elif by_order == True:
            recs = self.tab.select().order_by(self.tab.order)
        else:
            recs = self.tab.select().order_by(self.tab.name)
        return (recs)

    def query_field_count(self, limit_num):
        recs = self.tab.select().order_by(self.tab.app_count.desc()).limit(limit_num)
        return (recs)

    def get_by_slug(self, slug):
        return self.tab.get(slug=slug)

    def get_by_id(self, idd):
        return self.tab.get(id_cat=idd)

    def update_app_catalog_num(self, cat_id, num):
        entry = self.tab.update(
            app_count=num,
        ).where(self.tab.uid == cat_id)
        entry.execute()

    def update_post_catalog_num(self, cat_id, num):
        entry = self.tab.update(
            post_count=num,
        ).where(self.tab.uid == cat_id)
        entry.execute()

    def initial_db(self, post_data):
        entry = self.tab.create(
            name=post_data['name'],
            id_cat=post_data['id_cat'],
            slug=post_data['slug'],
            order=post_data['order'],
        )

