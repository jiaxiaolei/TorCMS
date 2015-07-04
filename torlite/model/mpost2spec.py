# # -*- coding:utf-8 -*-
# '''
# Author: Bu Kun
# E-mail: bukun@osgeo.cn
# CopyRight: http://www.yunsuan.org
# '''
# import peewee
# import uuid
#
# from torlite.model.core_tab import CabPost2Spec
# from torlite.model.core_tab import CabSpec
# from torlite.model.core_tab import CabPost
# import config
#
#
# class MPost2Spec():
#     def __init__(self):
#         try:
#             CabPost2Spec.create_table()
#         except:
#             pass
#
#     def query_all(self):
#         recs = CabPost2Spec.select().order_by(CabPost2Spec.order)
#         return (recs)
#
#
#     def query_by_catid(self, catid):
#         return CabPost2Spec.select().where(CabPost2Spec.catalog == catid)
#
#     def query_by_id(self, idd):
#         return CabPost2Spec.select().join(CabSpec).where(CabPost2Spec.post == idd)
#
#     def get_by_info(self, post_id, catalog_id):
#         recs = CabPost2Spec.select().where(
#             (CabPost2Spec.post == post_id) & (CabPost2Spec.catalog == catalog_id))
#         if recs.count() > 1:
#             for rec in recs:
#                 self.delete_by_id(rec.uid)
#             return False
#         elif recs.count() == 1:
#             return CabPost2Spec.get((CabPost2Spec.post == post_id) & (CabPost2Spec.catalog == catalog_id))
#         else:
#             return False
#
#     def query_count(self):
#         recs = CabPost2Spec.select(CabPost2Spec.catalog,
#                                       peewee.fn.COUNT(CabPost2Spec.catalog).alias('num')).group_by(
#             CabPost2Spec.catalog)
#         return (recs)
#
#     def add_record(self, post_id, spec_id, order=1):
#
#         tt = self.get_by_info(post_id, spec_id)
#         if tt == False:
#             print('a')
#             entry = CabPost2Spec.create(
#                 uid=str(uuid.uuid1()),
#                 post=post_id,
#                 catalog=spec_id,
#                 order=order,
#             )
#         else:
#             entry = CabPost2Spec.update(
#                 order=order,
#             ).where(CabPost2Spec.uid == tt.uid)
#             entry.execute()
#
#     def delete_by_id(self, uid):
#         entry = CabPost2Spec.delete().where(CabPost2Spec.uid == uid)
#         entry.execute()
#
#     def catalog_record_number(self, cat_id):
#         return CabPost2Spec.select().where(CabPost2Spec.catalog == cat_id).count()
#
#     def query_catalog(self, post_id):
#         return CabPost2Spec.select().where(CabPost2Spec.post == post_id)
#
#     def query_pager_by_slug(self, slug, current_page_num=1):
#         return CabPost.select().join(CabPost2Spec).join(CabSpec).where(CabSpec.slug == slug).order_by(
#             CabPost.time_update.desc()).paginate(current_page_num, config.page_num)
