# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''

import tornado.web
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from config import menu_arr

class ModuleCatMenu(tornado.web.UIModule):
    def render(self, with_count=True):
        self.mcat = MCatalog()
        all_cats = self.mcat.query_all(with_count=True)
        kwd = {
            'cats': all_cats,
            'with_count': with_count,
        }
        return self.render_string('tplite/modules/menu_post.html', kwd=kwd)


class ModuleSpecMenu(tornado.web.UIModule):
    def render(self):
        self.mcat = SpesubModel()
        all_cats = self.mcat.get_all()
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('tplite/modules/spec_menu.html', kwd=kwd)


class TopMenu(tornado.web.UIModule):
    def render(self):
        outstr = ''
        for x in menu_arr:
            tmp_str = '''<li><a href="{0}">{1}</a></li>'''.format(x[1], x[0])
            outstr += tmp_str

        return outstr