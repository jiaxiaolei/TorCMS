from whoosh.fields import *
from whoosh.index import create_in, open_dir
from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser

analyzer = ChineseAnalyzer()
# schema = Schema(title=TEXT(stored=True, analyzer=analyzer), path=ID(stored=True),
#                 content=TEXT(stored=True, analyzer=analyzer))
# ix = config.ix
# self.searcher = ix.searcher()
ix = open_dir("lib/whoosh")
print('=' * 30)

print(ix.schema)
print('=' * 30)
parser = QueryParser("content", schema=ix.schema)


def search(keyword, limit=20):
    q = parser.parse(keyword)
    try:
        searcher1 = ix.searcher()
        tt = searcher1.search(q, limit=limit)
        return (tt)
    finally:
        pass
        # searcher1.close()


def search_pager(keyword, page_index=1, doc_per_page=10):
    q = parser.parse(keyword)
    try:
        searcher1 = ix.searcher()
        tt = searcher1.search(q, limit=page_index * doc_per_page)
        return (tt[(page_index - 1) * doc_per_page: page_index * doc_per_page])
    finally:
        pass
        # searcher1.close()
