# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

import uuid
import os
import tornado.web
import tornado.ioloop
from torlite.model.pic_model import MPic


class PicHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.mpic = MPic()

    def get(self, input=''):
        if input == '':
            return
        url_arr = input.split(r'/')
        if input == 'add':
            self.to_add()
        elif (input == 'list' or input == ''):
            self.list()
        elif len(input) > 36:
            self.view(input)
        else:
            self.render('/html/404.html')

    def post(self, input=''):
        if input == '':
            return
        ip_arr = input.split(r'/')
        if input == 'add' or input == '':
            self.add_pic()
        else:
            self.render('/html/404.html')

    def list(self):
        recs = self.mpic.getall()
        kwd = {
            'pager': '',
        }
        self.render('tplite/pic/list.html', imgs=recs, kwd=kwd)

    def to_add(self):
        kwd = {
            'pager': '',
        }
        self.render('tplite/pic/addpic.html', kwd=kwd)

    def add_pic(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        file_dict_list = self.request.files['file']
        for file_dict in file_dict_list:
            filename = file_dict["filename"]

            (qian, hou) = os.path.splitext(filename)
            signature = str(uuid.uuid1())
            outfilename = '{0}{1}'.format(signature, hou)
            outpath = 'static/upload/{0}'.format(signature[:2])
            if os.path.exists(outpath):
                pass
            else:
                os.mkdir(outpath)
            with open(os.path.join(outpath, outfilename), "wb") as f:
                f.write(file_dict["body"])
            path_save = os.path.join(signature[:2], outfilename)
            self.mpic.insert_data(signature, path_save)
        self.redirect('/pic/{0}'.format(path_save))

    def view(self, outfilename):
        kwd = {
            'pager': '',
            # 'imgpath':
        }
        self.render('tplite/pic/showpic.html', filename=outfilename, kwd=kwd)
