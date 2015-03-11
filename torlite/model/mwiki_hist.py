# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''
import uuid

from torlite.model.core_tab import  CabWikiHist

class MWikiHist():
    def __init__(self):
        try:
            CabWikiHist.create_table()
        except:
            pass

    def insert_data(self, raw_data):
        uid = str(uuid.uuid1())
        entry = CabWikiHist.create(
            uid=uid,
            title=raw_data.title,
            date=raw_data.date,
            wiki_id=raw_data.uid,
            time_create=raw_data.time_create,
            user_name=raw_data.user_name,
            cnt_md=raw_data.cnt_md,
            time_update=raw_data.time_update,
        )
        return (uid)

    def get_by_id(self, in_uid):
        tt = CabWikiHist.get(CabWikiHist.uid == in_uid)
        return tt


    def query_all(self):
        return CabWikiHist.select().order_by('time_update')

