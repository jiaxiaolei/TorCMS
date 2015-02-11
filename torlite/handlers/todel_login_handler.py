# -*- coding:utf-8 -*-

from torlite.core.base_handler import BaseHandler
from torlite.model.muser import MUser


class LoginHandler(BaseHandler):
    def initialize(self):
        self.mdb = MUser()




