# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

from torlite.handlers.post_handler import PostHandler
from torlite.handlers.user_handler import UserHandler
from torlite.handlers.cat_handler import CatHandler
from torlite.handlers.pic_handler import PicHandler
from torlite.handlers.spec_handler import SpecHandler
from torlite.handlers.index import IndexHandler
from torlite.handlers.page_handler import PageHandler
from torlite.handlers.static_handler import StaticHandler

urls = [
    (r"/pic/(.*)", PicHandler, dict()),
    (r"/category/(.*)", CatHandler, dict()),
    (r"/spec/(.*)", SpecHandler, dict()),
    (r"/user/(.*)", UserHandler, dict()),
    (r"/post/(.*)", PostHandler, dict()),
    (r"/page/(.*)", PageHandler, dict()),
    (r"/html/(.*)", StaticHandler, dict()),
    (r"/", IndexHandler, dict()),
]