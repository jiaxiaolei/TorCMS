# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

import tornado.autoreload
import tornado.ioloop
import tornado.locale

import sys


from application import application

PORT = '8088'

if __name__ == "__main__":
    tornado.locale.load_gettext_translations('locale', 'yunsuan')
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    application.listen(PORT)
    print ('Development server is running at http://127.0.0.1:{0}/'.format(PORT))
    print ('Quit the server with CONTROL-C')
    tornado.ioloop.IOLoop.instance().start()
