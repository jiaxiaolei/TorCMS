# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''

import tornado.web
import os
from urls import urls
from torlite.core.core_cfg import core_modules as modules

# 添加扩展的模块。
# from modules.extends import *

SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    'debug': True,
    "cookie_secret": "61oETzsdafKasdsdfXQA",
    "login_url": "/user/login",
    'ui_modules': modules,
}

application = tornado.web.Application(
    handlers=urls,
    **SETTINGS
)

if __name__ == '__main__':
    pass
