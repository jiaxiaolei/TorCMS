# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''


from torlite.model.core_tab import CabCatalog

class MCatalog():
    def __init__(self):
        try:
            CabCatalog.create_table()
        except:
            pass

    def query_all(self):
        recs = CabCatalog.select().order_by(CabCatalog.name)
        return (recs)

    def query_field_count(self, limit_num):
        recs = CabCatalog.select().order_by(CabCatalog.app_count.desc()).limit(limit_num)
        return (recs)

    def get_by_slug(self, slug):
        return CabCatalog.get(slug=slug)

    def get_by_id(self, idd):
        return CabCatalog.get(id_cat=idd)
    def update_app_catalog_num(self, cat_id, num):
        entry = CabCatalog.update(
            app_count = num,
        ).where(CabCatalog.uid == cat_id )
        entry.execute()
    def update_post_catalog_num(self, cat_id, num):
        entry = CabCatalog.update(
            post_count = num,
        ).where(CabCatalog.uid == cat_id )
        entry.execute()
    def update_post_catalog_num(self, cat_id, num):
        entry = CabCatalog.update(
            post_count = num,
        ).where(CabCatalog.uid == cat_id )
        entry.execute()
    def initial_db(self, post_data):
        '''
        初始化数据库
        :param post_data:
        :return:
        '''
        entry = CabCatalog.create(
            name=post_data['name'],
            id_cat=post_data['id_cat'],
            slug=post_data['slug'],
            order=post_data['order'],
        )