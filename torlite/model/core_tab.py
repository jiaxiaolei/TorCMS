# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

import peewee

from torlite.core.base_model import BaseModel


class CabCatalog(BaseModel):
    uid = peewee.IntegerField(null=False, index=True, unique=True, primary_key=True, help_text='', )
    slug = peewee.CharField(null=False, index=True, unique=True, max_length=35, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()
    post_count = peewee.IntegerField(default=0)
    app_count = peewee.IntegerField(default=0)


class CabPage(BaseModel):
    title = peewee.CharField(null=False, max_length=255, )
    slug = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=35, help_text='', )
    date = peewee.DateTimeField()
    cnt_html = peewee.TextField()
    time_create = peewee.IntegerField()
    id_user = peewee.CharField()
    cnt_md = peewee.CharField()
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()


class CabPost(BaseModel):
    uid = peewee.CharField(null=False, index=False, unique=True, primary_key=True, default='00000',
                           max_length=5, help_text='', )
    title = peewee.CharField(null=False,  help_text='Title')
    date = peewee.DateTimeField()
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, max_length=35, help_text='UserName', )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    id_spec = peewee.CharField()
    logo = peewee.CharField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    src_type = peewee.IntegerField( default= 0) # 0 for markdown, 1 for rst



# Todo: 是否添加单独的首页滚动图片字段 ??
class CabPostHist(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, help_text='', primary_key=True, max_length=36)
    title = peewee.CharField(null=False, max_length=255, help_text='', )
    date = peewee.DateTimeField()
    post_id = peewee.CharField(null=False, max_length=5, help_text='', )
    time_create = peewee.IntegerField()
    user_name = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()
    id_spec = peewee.CharField()
    logo = peewee.CharField()


class CabSpec(BaseModel):
    uid = peewee.CharField()
    name = peewee.CharField()
    slug = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=35, help_text='', )
    order = peewee.IntegerField()
    img = peewee.CharField()
    abstract = peewee.CharField()
    desc = peewee.CharField()


class CabMember(BaseModel):
    # user_id = peewee.CharField()
    '''
    privilege:
    11111
    read,add,edit,delete,manage
    '''
    uid = peewee.IntegerField(null=False, index=True, unique=True, primary_key=True, help_text='', )
    user_name = peewee.CharField(null=False, index=True, unique=True, max_length=16, help_text='', )
    privilege = peewee.CharField(null=False, default='10000', help_text='用户权限', )
    user_pass = peewee.CharField(null=False, max_length=255, )
    user_email = peewee.CharField(null=False, max_length=255, )


class CabPic(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, )
    imgpath = peewee.CharField(null=False, unique=True, max_length=255, help_text='', )
    create_timestamp = peewee.IntegerField()


class CabPost2Catalog(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=35, help_text='', )
    catalog = peewee.ForeignKeyField(CabCatalog, related_name='cat_id')
    post = peewee.ForeignKeyField(CabPost, related_name='post_id')
    order = peewee.IntegerField()
