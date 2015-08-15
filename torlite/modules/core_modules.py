# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''

import bs4
import tornado.web
from torlite.model.mcatalog import MCatalog
from torlite.model.mpost import MPost
from torlite.model.mpost2catalog import MPost2Catalog
import config


class get_footer(tornado.web.UIModule):
    def render(self):
        self.mcat = MCatalog()
        all_cats = self.mcat.query_all()
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('tplite/modules/menu.html', kwd=kwd)


class previous_post_link(tornado.web.UIModule):
    def render(self, current_id):
        self.mpost = MPost()
        prev_record = self.mpost.get_previous_record(current_id)
        if prev_record is None:
            outstr = '已经是最后一篇了'
        else:
            outstr = '''<a href="/post/{0}.html">上一篇</a>'''.format(prev_record.uid, prev_record.title)
        return outstr


class post_most_view(tornado.web.UIModule):
    def render(self, num, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_most(num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('tplite/modules/post_list.html', recs=recs, kwd=kwd)


class post_random(tornado.web.UIModule):
    def render(self, num, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_random(num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('tplite/modules/post_list.html', recs=recs, kwd=kwd)


class post_cat_random(tornado.web.UIModule):
    def render(self, cat_id, num, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_cat_random(cat_id, num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('tplite/modules/post_list.html', recs=recs, kwd=kwd)


class post_recent_most_view(tornado.web.UIModule):
    def render(self, num, recent, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_recent_most(num, recent)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('tplite/modules/post_list.html', recs=recs, kwd=kwd)


class post_recent(tornado.web.UIModule):
    def render(self, num=10, with_catalog=True, with_date=True):
        self.mpost = MPost()
        recs = self.mpost.query_recent(num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('tplite/modules/post_list.html',
                                  recs=recs,
                                  kwd=kwd, )


class post_category_recent(tornado.web.UIModule):
    def render(self, cat_id, num=10, with_catalog=True, with_date=True):
        self.mpost = MPost()
        self.mpost2cat = MPost2Catalog()
        # recs = self.mpost2cat.query_by_catid(cat_id)
        recs = self.mpost.query_cat_recent(cat_id, num)
        kwd = {
            'with_catalog': with_catalog,
            'with_date': with_date,
        }
        return self.render_string('tplite/modules/post_list.html',
                                  recs=recs,
                                  kwd=kwd, )


class showout_recent(tornado.web.UIModule):
    def render(self, cat_id, num=10, with_catalog=True, with_date=True, width=160, height=120):
        self.mpost = MPost()
        self.mpost2cat = MPost2Catalog()
        # recs = self.mpost2cat.query_by_catid(cat_id)
        recs = self.mpost.query_cat_recent(cat_id, num)

        kwd = {
            'with_catalog': with_catalog,
            'with_date': with_date,
            'width': width,
            'height': height,
        }

        return self.render_string('tplite/modules/showout_list.html',
                                  recs=recs,
                                  kwd=kwd, )


class site_url(tornado.web.UIModule):
    def render(self):
        return config.site_url


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
        self.mpost2cat = MPost2Catalog()
        current_record = self.mpost2cat.query_catalog(post_id)
        outstr = ''
        for uu in current_record:
            tmp_str = '''<a href="/category/{0}">{1}</a>'''.format(uu.catalog.slug, uu.catalog.name)
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
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:130] + '....'


class generate_description(tornado.web.UIModule):
    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:100]


class category_menu(tornado.web.UIModule):
    def render(self):
        self.mcat = MCatalog()
        recs = self.mcat.query_all()
        out_str = ''
        for rec in recs:
            tmp_str = '''<li><a href="/category/{0}" title="{1}">{1}</a></li>'''.format(rec.slug, rec.name)
            out_str += tmp_str
        return out_str


class post_catalogs(tornado.web.UIModule):
    def render(self, signature):
        self.mapp2tag = MPost2Catalog()
        tag_infos = self.mapp2tag.query_by_id(signature)
        out_str = ''
        ii = 1
        for tag_info in tag_infos:
            tmp_str = '''<a href="/category/{0}" class="tag{1}">{2}</a>
            '''.format(tag_info.catalog.slug, ii, tag_info.catalog.name)
            out_str += tmp_str
            ii += 1

        return out_str
