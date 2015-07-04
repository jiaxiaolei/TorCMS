# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''


import uuid


from torlite.model.core_tab import  CabPostHist

class MPostHist():
    def __init__(self):
        try:
            CabPostHist.create_table()
        except:
            pass

    def insert_data(self, raw_data):
        print('============')
        print(raw_data.uid)
        print('--------------')
        uid = str(uuid.uuid1())
        entry = CabPostHist.create(
            uid=uid,
            title=raw_data.title,
            date=raw_data.date,
            post_id=raw_data.uid,
            time_create=raw_data.time_create,
            user_name=raw_data.user_name,
            cnt_md=raw_data.cnt_md,
            time_update=raw_data.time_update,
            id_spec=raw_data.id_spec,
            logo=raw_data.logo,
        )
        return (uid)

    def get_by_id(self, in_uid):
        tt = CabPostHist.get(CabPostHist.uid == in_uid)
        return tt


    def query_all(self):
        return CabPostHist.select().order_by('time_update')

