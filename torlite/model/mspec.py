# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''


import uuid



from torlite.model.core_tab import  CabSpec


class SpesubModel():
    def __init__(self):
        try:
            CabSpec.create_table()
        except:
            pass


    def addata(self, post_data):
        entry = CabSpec.create(
            uid=str(uuid.uuid1()),
            name=post_data['title'][0],
            slug=post_data['slug'][0],
            order=post_data['order'][0],
            img=post_data['img'][0],
            desc=post_data['desc'][0],
            abstract = post_data['abstract'][0],
        )


    def get_by_id(self, uid):
        return CabSpec.get(uid=uid)

    def get_by_slug(self, input):
        user = CabSpec.get(slug=input)
        return (user)

    def update(self, uid, post_data):

        entry = CabSpec.update(
            name=post_data['title'][0],
            slug=post_data['slug'][0],
            order=post_data['order'][0],
            img=post_data['img'][0],
            desc=post_data['desc'][0],
            abstract = post_data['abstract'][0],
        ).where(CabSpec.uid == uid)
        entry.execute()

    def get_all(self):
        recs = CabSpec.select().order_by(CabSpec.order)
        return (recs)


    def initial_db(self, post_data):
        entry = CabSpec.create(
            name=post_data['name'],
            id_cat=post_data['id_cat'],
            slug=post_data['slug'],
            order=post_data['order'],
        )