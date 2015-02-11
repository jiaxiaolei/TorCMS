# -*- coding:utf-8 -*-
__author__ = 'bukun'

import tornado.web
from torlite.model.mcatalog import MCatalog
from torlite.model.mpost import MPost
from torlite.model.mpost2catalog import MPost2Catalog
from torlite.model.mspec import SpesubModel
from torlite.core import tools
import bs4


class get_footer(tornado.web.UIModule):
    def render(self):
        self.mcat = MCatalog()
        all_cats = self.mcat.query_all()
        kwd = {
            'cats': all_cats,
        }
        # yyinfos = self.mrefresh.get_by_id(info_id)
        return self.render_string('tplite/modules/menu.html', kwd=kwd)


class previous_post_link(tornado.web.UIModule):
    def render(self, current_id):
        self.mpost = MPost()
        prev_record = self.mpost.get_previous_record(current_id)
        # print(prev_record)
        if prev_record is None:
            outstr = '已经是最后一篇了'
        else:
            outstr = '''<a href="/post/{0}.html">上一篇</a>'''.format(prev_record.uid, prev_record.title)
        return outstr

class post_most_view(tornado.web.UIModule):
    def render(self, num):
        self.mpost = MPost()
        recs = self.mpost.query_most(num)
        kwd = {
            'date': False,
        }
        return self.render_string('tplite/modules/post_list.html', recs = recs, kwd=kwd)
class post_random(tornado.web.UIModule):
    def render(self, num):
        self.mpost = MPost()
        recs = self.mpost.query_random(num)
        kwd = {
            'date': False,
        }
        return self.render_string('tplite/modules/post_list.html', recs = recs, kwd=kwd)

class post_cat_random(tornado.web.UIModule):
    def render(self, cat_id, num):
        print(cat_id)
        print(num)
        self.mpost = MPost()
        recs = self.mpost.query_cat_random(cat_id, num)
        kwd = {
            'date': False,
        }
        return self.render_string('tplite/modules/post_list.html', recs = recs, kwd=kwd)

class post_recent_most_view(tornado.web.UIModule):
    def render(self, num, recent):
        self.mpost = MPost()
        recs = self.mpost.query_recent_most(num, recent)
        kwd = {
            'date': False,
        }
        return self.render_string('tplite/modules/post_list.html', recs = recs, kwd = kwd)
class post_recent(tornado.web.UIModule):
    def render(self, num, date = False):
        self.mpost = MPost()
        recs = self.mpost.query_recent(num)
        kwd = {
            'date': date,
        }
        return self.render_string('tplite/modules/post_list.html',
                                  recs = recs, kwd=kwd,
                                  format_yr=tools.format_yr)

class post_category_recent(tornado.web.UIModule):
    def render(self, cat_id, num):
        self.mpost = MPost()
        self.mpost2cat = MPost2Catalog()
        recs = self.mpost2cat.query_by_catid(1)
        kwd = {
            'date': False,
        }
        return self.render_string('tplite/modules/post_cat.html',
                                  recs = recs, kwd=kwd,    )

class next_post_link(tornado.web.UIModule):
    def render(self, current_id):
        self.mpost = MPost()
        next_record = self.mpost.get_next_record(current_id)
        if next_record is None:
            outstr = '已经是最新一篇了'
        else:
            outstr = '''<a href="/post/{0}.html">下一篇</a>'''.format(next_record.uid)
        return outstr


class the_category(tornado.web.UIModule):
    def render(self, post_id):
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.mpost2cat = MPost2Catalog()
        current_record = self.mpost2cat.query_catalog(post_id)
        # current_record = self.mpost.get_by_id(post_id)

        # cat_arr = current_record.id_cats.split(',')
        # print(cat_arr)
        outstr = ''
        for uu in current_record:
            tmp_str = '''<a href="/category/{0}">{1}</a>'''.format( uu.catalog.slug, uu.catalog.name)
            outstr += tmp_str
        return outstr

class list_categories(tornado.web.UIModule):
    def render(self, cat_id, list_num):
        self.mpost = MPost()
        recs = self.mpost.query_by_cat(cat_id, list_num)
        out_str = ''
        for rec in recs:
            tmp_str = '''<li><a href="/{0}">{1}</a></li>'''.format(rec.title, rec.title)
            out_str += tmp_str
        return out_str

class generate_abstract(tornado.web.UIModule):
    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup( tornado.escape.xhtml_unescape(html_str))
        return tmp_str.get_text()[:130] + '....'

        # 

class category_menu(tornado.web.UIModule):
    def render(self):
        self.mcat = MCatalog()
        recs = self.mcat.query_all()
        kwd = {
            'date': False,
        }
        out_str = ''
        for rec in recs:
            tmp_str = '''<li><a href="/category/{0}" title="{1}">{1}</a></li>'''.format(rec.slug, rec.name)
            out_str += tmp_str
        return out_str

class post_catalogs(tornado.web.UIModule):
    def render(self, signature):
        self.mapp2tag = MPost2Catalog()
        tag_infos = self.mapp2tag.query_by_id(signature)
        # tag_infos = self.mapp2tag.query_all()
        out_str = ''
        ii = 1
        for tag_info in tag_infos:
            # print(tag_info.owner.name)
            tmp_str = '<a href="/category/{0}" class="tag{1}">{2}</a>'.format( tag_info.catalog.slug, ii, tag_info.catalog.name)
            out_str += tmp_str
            print(ii)
            ii += 1

        # print(out_str)
        return out_str