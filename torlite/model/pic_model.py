# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''
import time
import cgi
import  uuid

from torlite.model.core_tab import CabPic


class MPic():
    def __init__(self):
        try:
            CabPic.create_table()
        except:
            pass
    def getall(self):

        sql_cmd = 'select * from pics order by timestamp DESC'
        db_data = self.db.query(sql_cmd)
        return (db_data)

    def get_by_id(self, input):
        field_dic = ['id_post', 'title', 'cnt_html', 'id_cats']
        uuid = input
        # self.write(input)
        tmp_arr = []
        for fkey in field_dic:
            tmp_arr.append(fkey)
        tmp_str = ','.join(tmp_arr)
        a = self.db.get("select {0} from bblog where id_post='{1}'".format(tmp_str, uuid))
        return (a)

    def get_by_cat(self, cat_str):
        field_dic = ['id_post', 'title', 'cnt_html', 'id_cats']
        uuid = cat_str
        # self.write(input)
        tmp_arr = []
        for fkey in field_dic:
            tmp_arr.append(fkey)
        tmp_str = ','.join(tmp_arr)
        sql_cmd = "select %s from bblog where id_cats like '%%%s%%'" % (tmp_str, uuid)
        print(sql_cmd)
        a = self.db.query(sql_cmd)
        return (a)

    def get_md_by_id(self, input):
        field_dic = ['id_post', 'title', 'cnt_md', 'id_cats']
        uuid = input
        tmp_arr = []
        for fkey in field_dic:
            tmp_arr.append(fkey)
        tmp_str = ','.join(tmp_arr)
        a = self.db.get("select %s from bblog where id_post='%s'" % (tmp_str, uuid))
        return (a)

    def get_by_wiki(self, citiao):
        field_dic = ['id_post', 'title', 'cnt_html']

        tmp_arr = []
        for fkey in field_dic:
            tmp_arr.append(fkey)
        tmp_str = ','.join(tmp_arr)

        # db = tornpg.Connection('localhost', 'geodb', user='wen1', password='123456')
        sql_cmd = "select %s from bblog where title='%s'" % (tmp_str, citiao)

        a = self.db.get(sql_cmd)
        return (a)


    def insert_data(self, signature, impath):

        uu  = CabPic.create(
            uid = str(uuid.uuid1()),
            imgpath = impath,
            create_timestamp = time.time()
        )

    def update(self, uid, post_data):
        field_dic = ['title', 'cnt_html', 'time_create', 'cnt_md', 'id_cats']

        tmp_arr = []

        for fkey in field_dic:
            tmp_arr.append(fkey)
            if fkey == 'id_post':
                tmp_arr.append(uid)
            elif fkey == 'time_create':
                tmp_arr.append(int(time.time()))
            elif fkey == 'cnt_md':
                tmp_arr.append(cgi.escape(post_data[fkey][0]))
            elif fkey == 'cnt_html':
                tmp_arr.append(self.md2html(post_data['cnt_md'][0]))
            elif fkey == 'id_cats':
                if fkey in post_data:
                    tmp_str = ',%s,' % (','.join(post_data[fkey]))
                else:
                    tmp_str = ',,'

                tmp_arr.append(tmp_str)
            else:
                tmp_arr.append(post_data[fkey][0])
        tmp_arr.append(uid)
        print(tmp_arr)
        fd_tup = tuple(tmp_arr)

        sql_cmd = "update bblog set %s='%s',%s ='%s',%s=%s,%s='%s', %s='%s' where id_post = '%s' " % fd_tup

        a = self.db.execute(sql_cmd)
        return (uid)