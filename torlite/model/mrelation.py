# -*- coding:utf-8 -*-

from torlite.core import tools

from torlite.model.core_tab import *



class MRelation(object):
    def __init__(self):
        self.tab =CabRelation
        self.deftab = CabPost
        try:
            CabRelation.create_table()
        except:
            pass

    def add_relation(self, app_f, app_t):
        cur = self.tab.select().where((self.tab.app_f == app_f) & (self.tab.app_t == app_t))
        if cur.count() > 1:
            for x in cur:
                self.delete_by_uid(x.uid)
        if cur.count() == 0:
            uid = tools.get_uuid()

            entry = self.tab.create(
                uid=uid,
                app_f=app_f,
                app_t=app_t,
                count=1,
            )
            return entry.uid
        else:
            self.update_relation(app_f, app_t)

    def delete_by_uid(self, uid_base, uid_rel):
        entry = self.tab.delete().where((self.tab.app_f == uid_base)  & (self.tab.app_t ==  uid_rel))
        entry.execute()

    def update_relation(self, app_f, app_t):
        try:
            uu = self.tab.get((self.tab.app_f == app_f) & (self.tab.app_t == app_t))
        except:
            return False
        entry = self.tab.update(
            count=uu.count + 1
        ).where((self.tab.app_f == app_f) & (self.tab.app_t == app_t))
        entry.execute()

    def get_app_relations(self, app_id):
        return self.tab.select().join(self.deftab ).where(self.tab.app_f == app_id).order_by(
            self.tab.count.desc()).limit(20)
