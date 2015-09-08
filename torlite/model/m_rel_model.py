# -*- coding:utf-8 -*-

from torlite.core import tools

from torlite.model.core_tab import *


class MRel(object):
    def __init__(self):
        # TabApp2tag.create_table()
        try:
            CabRelation.create_table()
        except:
            pass

    def add_relation(self, app_f, app_t):
        cur = CabRelation.select().where((CabRelation.app_f == app_f) & (CabRelation.app_t == app_t))
        if cur.count() > 1:
            for x in cur:
                self.delete_by_uid(x.uid)
        if cur.count() == 0:
            uid = tools.get_uuid()

            entry = CabRelation.create(
                uid=uid,
                app_f=app_f,
                app_t=app_t,
                count=1,
            )

            return entry.uid
        else:
            self.update_relation(app_f, app_t)

    def delete_by_uid(self, uid_base, uid_rel):
        entry = CabRelation.delete().where((CabRelation.app_f == uid_base)  & (CabRelation.app_t ==  uid_rel))
        entry.execute()

    def update_relation(self, app_f, app_t):
        try:
            uu = CabRelation.get((CabRelation.app_f == app_f) & (CabRelation.app_t == app_t))
        except:
            return False
        entry = CabRelation.update(
            count=uu.count + 1
        ).where((CabRelation.app_f == app_f) & (CabRelation.app_t == app_t))
        entry.execute()

    def get_app_relations(self, app_id):
        return CabRelation.select().join(CabPost).where(CabRelation.app_f == app_id).order_by(
            CabRelation.count.desc()).limit(20)
