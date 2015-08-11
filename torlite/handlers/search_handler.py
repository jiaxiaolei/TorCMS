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

from torlite.core.tools import whoosh_search


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
        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get(self, url_str=''):

        if url_str == '':
            return
        elif len(url_str) > 0:
            self.search(url_str)
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
    def search(self, keyword):
        results = whoosh_search(keyword, 20)
        # reswhoosh_search.keyworde limit=3limit=30)
        kwd = {'title':'查找结果'}
        self.render('tplite/search/search.html',
                    kwd=kwd,
                    srecs = results,
                    )