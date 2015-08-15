# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''

from whoosh.fields import *
from whoosh.index import create_in, open_dir
from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser

analyzer = ChineseAnalyzer()
ix = open_dir("database/whoosh")
parser = QueryParser("content", schema=ix.schema)


def search(keyword, limit=20):
    q = parser.parse(keyword)
    try:
        tt = ix.searcher().search(q, limit=limit)
        return (tt)
    finally:
        pass
        # Don't close the searcher.
        # searcher1.close()


def search_pager(keyword, page_index=1, doc_per_page=10):
    q = parser.parse(keyword)
    try:
        tt = ix.searcher().search(q, limit=page_index * doc_per_page)
        return (tt[(page_index - 1) * doc_per_page: page_index * doc_per_page])
    finally:
        pass
