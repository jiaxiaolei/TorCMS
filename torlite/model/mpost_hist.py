# -*- coding:utf-8 -*-

import time
import tornado.escape
import markdown2
import config
import uuid
import peewee
import datetime
from torlite.core.base_model import BaseModel

from torlite.model.core_tab import  CabPostHist

class MPostHist():
    def __init__(self):
        try:
            CabPostHist.create_table()
        except:
            pass

    def insert_data(self, raw_data):
        uid = str(uuid.uuid1())
        entry = CabPostHist.create(
            uid=uid,
            title=raw_data.title,
            date=raw_data.date,
            # tags=raw_data.tags,
            post_id=raw_data.uid,
            time_create=raw_data.time_create,
            user_name=raw_data.user_name,
            cnt_md=raw_data.cnt_md,
            time_update=raw_data.time_update,
            # id_cats=raw_data.id_cats,
            id_spec=raw_data.id_spec,
            logo=raw_data.logo,
        )
        return (uid)




    def get_by_id(self, in_uid):
        tt = CabPostHist.get(CabPostHist.uid == in_uid)
        return tt


    def query_all(self):
        return CabPostHist.select().order_by('time_update')

