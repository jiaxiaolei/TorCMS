# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun#osgeo.cn
CopyRight: http://www.yunsuan.org
Bu Kun's Homepage: http://bukun.net
'''

from torlite.model.core_tab import *

try:
    CabReply.create_table()
except:
    pass

try:
    CabPost2Reply.create_table()
except:
    pass