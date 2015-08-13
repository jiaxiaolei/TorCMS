# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import sys,os
import html2text
import tornado.escape
sys.path.append("../")

def html_strip(html):
    from HTMLParser import HTMLParser
    html = html.strip()
    html = html.strip("\n")
    result = []
    parse = HTMLParser()
    parse.handle_data = result.append
    parse.feed(html)
    parse.close()
    return "".join(result)

from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

from jieba.analyse import ChineseAnalyzer

sys.path.append('/opt/torlite/yunsuan')

from torlite.model.mpost import MPost
# from torapp.model.app_model import MApp

mpost = MPost()

recs = mpost.query_all()
# title, cnt_html


analyzer = ChineseAnalyzer()

schema = Schema(title=TEXT(stored=True, analyzer = analyzer), type=TEXT(stored=True), link=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
if not os.path.exists("lib/whoosh"):
    os.mkdir("lib/whoosh")

ix = create_in("lib/whoosh", schema) # for create new index
# ix = open_dir("tmp") # for read only
writer = ix.writer()

for rec in recs:
    # print(rec.title, rec.uid, rec.cnt_html)
    text2 =  html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
    print(text2)
    writer.add_document(
        title=rec.title,
        type='<span style="color:blue;">[文档]</span>',
        link='/post/{0}.html'.format(rec.uid),
        content= text2
    )


#  mapp = MApp()
#  app_recs = mapp.query_recent(2000)
#  for rec in app_recs:
#      # text2 =  html2text.html2text(rec.cnt_html)
#      text2 =  html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
#      print(text2)
#      writer.add_document(
#          title=rec.title,
#          type='<span style="color:red;">[计算]</span>',
#          link='/app/{0}'.format(rec.uid),
#          content= text2
#      )

writer.commit()
# searcher = ix.searcher()
