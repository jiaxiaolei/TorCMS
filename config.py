# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

import peewee
import socket

def hostname():
    return (socket.gethostname())

menu_arr = [['首页', '/'],
            ['文档', '/category/geography'],
            ['云算', '/calc/find'],
            ['专题', '/spec/'],
]

page_num = 10

site_url = 'http://lab.osgeo.cn'

# if hostname() == 'v':
#     dbconnect = peewee.MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = 'fdfsrwt', database = 'yunsuan', )
# else:
#     dbconnect = peewee.MySQLDatabase(host = '127.0.0.1', user = 'yunsuan', passwd = 'yunsuan_pass', database = 'yunsuan', )

# 使用DataBase的不同形式，以应对Peewe针对数据库的不同语法
# 1 for SQLite
# 2 for MySQL
# 3 for PostgreSQL
dbtype = 1

dbconnect = peewee.SqliteDatabase('./db/torcms.db')


