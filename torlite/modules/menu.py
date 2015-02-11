# -*- coding:utf-8 -*-
__author__ = 'bukun'

import tornado.web
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from config import menu_arr
class ModuleCatMenu(tornado.web.UIModule):
    def render(self):
        self.mcat = MCatalog()
        all_cats = self.mcat.query_all()
        kwd = {
            'cats': all_cats,
        }
        # yyinfos = self.mrefresh.get_by_id(info_id)
        return self.render_string('tplite/modules/menu.html', kwd=kwd)

class ModuleSpecMenu(tornado.web.UIModule):
    def render(self):
        self.mcat = SpesubModel()
        all_cats = self.mcat.get_all()
        kwd = {
            'cats': all_cats,
        }
        # yyinfos = self.mrefresh.get_by_id(info_id)
        return self.render_string('tplite/modules/spec_menu.html', kwd=kwd)

class TopMenu(tornado.web.UIModule):
    def render(self):
        outstr = ''
        for x in menu_arr:
            tmp_str = '''<li><a href="{0}">{1}</a></li>'''.format(x[1], x[0])
            outstr += tmp_str

        # yyinfos = self.mrefresh.get_by_id(info_id)
        return outstr