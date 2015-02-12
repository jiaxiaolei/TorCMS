# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

import hashlib
import peewee
from torlite.core.base_model import BaseModel
from torlite.model.core_tab import CabMember

class MUser(BaseModel):
    def __init__(self):
        try:
            CabMember.create_table()
        except:
            pass

    def get_by_uid(self, uid):
        try:
            return CabMember.get(CabMember.uid == uid)
        except:
            return False

    def get_by_id(self, uname):
        try:
            return CabMember.get(user_name=uname)
        except:
            return False

    def check_user(self,u_name,u_pass):
        tt = CabMember.select().where(CabMember.user_name == u_name).count()
        if tt == 0:
            return -1
        a = CabMember.get(user_name = u_name)
        if a.user_pass == hashlib.md5(u_pass.encode('utf-8')).hexdigest():
            return 1
        return 0

    def insert_data(self, post_data):

        uu = CabMember.select().aggregate(peewee.fn.Max(CabMember.uid))
        if uu:
            pass
        else:
            uu = 0

        try:
            entry = CabMember.create(
            uid = uu + 1,
            user_name = post_data['user_name'][0],
            user_pass =hashlib.md5(post_data['user_pass'][0].encode('utf-8')).hexdigest() ,
            user_email = post_data['user_email'][0]
            )
            return True
        except:
            return False
