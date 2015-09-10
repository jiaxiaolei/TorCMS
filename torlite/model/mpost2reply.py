# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

import time
import tornado.escape
import config
import peewee
import datetime

from torlite.model.core_tab import CabPost2Catalog
from torlite.core import tools

from torlite.model.core_tab import CabReply
from torlite.model.core_tab import CabVoter2Reply
from torlite.model.core_tab import CabPost2Reply


class MPost2Reply():
    def __init__(self):
        self.tab = CabPost2Reply
        try:
            CabPost2Reply.create_table()
        except:
            pass
    def insert_data2(self, id_post, id_reply):
        uid = tools.get_uuid()
        try:
            entry = self.tab.create(
                uid=uid,
                post_id=id_post,
                reply_id= id_reply,
                timestamp=time.time(),
            )
            return (uid)
        except:
            return False

    def get_by_id(self, in_uid):
        recs = self.tab.select().join(CabReply).where(self.tab.post_id == in_uid).order_by(self.tab.timestamp.desc())
        return recs






