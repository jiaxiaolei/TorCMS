# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

from torlite.core.base_handler import BaseHandler
from torlite.model.muser import MUser
import os

class StaticHandler(BaseHandler):

    def get(self, url_str):
        kwd = {
            'pager': '',
        }
        testfile = 'templates/static/{0}'.format(url_str)
        if os.path.exists(testfile) and os.path.isfile(testfile):
            kwd['pager'] = ''
            self.render('static/{0}'.format(url_str), kwd=kwd)
        else:
            kwd['info'] = '您要找的文件不存在！'
            self.render('static/404.html', kwd=kwd)




