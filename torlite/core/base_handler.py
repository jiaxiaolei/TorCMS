# -*- coding:utf-8 -*-
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def init_cond(self):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("user")
    def editable(self):
        if self.get_current_user():
            return 1
        else:
            return 0
