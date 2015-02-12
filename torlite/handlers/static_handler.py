# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

from torlite.core.base_handler import BaseHandler
from torlite.model.muser import MUser


class StaticHandler(BaseHandler):

    def get(self, url):
        kwd = {
            'pager': '',
        }
        self.render('static/{0}'.format(url), kwd=kwd)


