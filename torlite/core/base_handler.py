# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def init_cond(self):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("user")



    def editable(self):
        # Deprecated.
        if self.get_current_user():
            return 1
        else:
            return 0
