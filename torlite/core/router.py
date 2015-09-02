# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

from torlite.handlers.post_handler import PostHandler
from torlite.handlers.user_handler import UserHandler
from torlite.handlers.cat_handler import CatHandler
from torlite.handlers.pic_handler import PicHandler
from torlite.handlers.spec_handler import SpecHandler
from torlite.handlers.index import IndexHandler
from torlite.handlers.page_handler import PageHandler
from torlite.handlers.wiki_handler import WikiHandler
from torlite.handlers.static_handler import StaticHandler
from torlite.handlers.search_handler import SearchHandler
from torlite.handlers.reply_handler import ReplyHandler
from torlite.handlers.post2reply_handler import Post2ReplyHandler

urls = [
    ("/pic/(.*)", PicHandler, dict()),
    ("/category/(.*)", CatHandler, dict()),
    ("/spec/(.*)", SpecHandler, dict()),
    ("/user/(.*)", UserHandler, dict()),
    ("/post/toreply/(.*)", Post2ReplyHandler, dict()),
    ("/post/(.*)", PostHandler, dict()),
    ("/page/(.*)", PageHandler, dict()),
    ("/wiki/(.*)", WikiHandler, dict()),
    ("/html/(.*)", StaticHandler, dict()),
    ("/search/(.*)", SearchHandler, dict()),
    ("/reply/(.*)", ReplyHandler, dict()),

    ("/", IndexHandler, dict()),
]
