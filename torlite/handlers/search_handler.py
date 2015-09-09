# -*- coding:utf-8 -*-

'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

import tornado.web
import tornado.escape

# from whoosh.index import create_in,open_dir
# from whoosh.fields import *
# from whoosh.qparser import QueryParser
# from jieba.analyse import ChineseAnalyzer


from torlite.core.base_handler import BaseHandler
from torlite.model.mpost import MPost
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from torlite.core import tools
from torlite.model.mpost_hist import MPostHist
from torlite.model.muser import MUser
from torlite.model.mpost2catalog import MPost2Catalog

from torlite.core.tool.whoosh_tool import yunsearch





class SearchHandler(BaseHandler):
    def initialize(self):
        # analyzer = ChineseAnalyzer()
        # schema = Schema(title=TEXT(stored=True, analyzer = analyzer), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
        # ix = config.ix
        # self.searcher = config.searcher
        # self.parser = config.parser
        # self.parser = QueryParser("content", schema=ix.schema)

        self.muser = MUser()
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.cats = self.mcat.query_all()
        self.mspec = SpesubModel()
        self.specs = self.mspec.get_all()
        self.mpost_hist = MPostHist()
        self.mpost2catalog = MPost2Catalog()
        self.ysearch = yunsearch()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get(self, url_str=''):
        if len(url_str) > 0:
            url_arr = url_str.split('/')
        if url_str == '':
            return
        elif len(url_arr) ==  1:
            self.search(url_str)
        elif len(url_arr)  == 2:
            self.search(url_arr[0], int(url_arr[1]))
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html', kwd=kwd)



    def post(self, url_str=''):
        keyword = self.get_argument('keyword')
        self.search(keyword)

    def to_find(self, ):
        kwd = {
            'pager': '',
        }
        self.render('tplite/post/find.html', topmenu='', kwd=kwd)

    def search(self, keyword, p_index = 1):

        res_all = self.ysearch.get_all_num(keyword)

        # res_all = get_all_num(keyword)
        # results = self.ysearch.search(keyword, 20)
        results = self.ysearch.search_pager(keyword, page_index=p_index, doc_per_page=20)
        print('-' * 40)
        page_num = int(res_all / 20)
        kwd = {'title':'查找结果',
               'pager': '',
               }
        self.render('tplite/search/search.html',
                    kwd=kwd,
                    srecs = results,
                    pager = tools.gen_pager_bootstrap_url('/search/{0}'.format(keyword), page_num, p_index),
                    )

