
# -*- coding:utf-8 -*-
# import tornpg
import peewee

from torlite.core.base_model import BaseModel


class CabCatalog(BaseModel):
    uid = peewee.IntegerField(null=False, index = True, unique=True, primary_key=True,help_text='',)
    slug = peewee.CharField( null=False, index = True, unique=True, max_length = 35, help_text='', )
    name = peewee.CharField(null=False, max_length = 255, help_text='',)
    order = peewee.IntegerField()
    post_count = peewee.IntegerField(default=0)
    app_count = peewee.IntegerField(default=0)

class CabPage(BaseModel):
    title = peewee.CharField(null=False, max_length=255,)
    slug = peewee.CharField( null=False, index = True, unique=True, primary_key=True, max_length = 35, help_text='',)
    date = peewee.DateTimeField()
    cnt_html = peewee.TextField()
    time_create = peewee.IntegerField()
    id_user = peewee.CharField()
    cnt_md = peewee.CharField()
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()

class CabPost(BaseModel):
    uid = peewee.CharField(null=False, index=False, unique=True, primary_key=True, default='00000', max_length=5,
                               help_text='', )
    title = peewee.CharField(null=False, unique=True, help_text='标题')
    date = peewee.DateTimeField()
    # tags = peewee.CharField()
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, max_length = 35, help_text='创建的用户名',)
    time_update = peewee.IntegerField()
    # id_cats = peewee.CharField()
    view_count = peewee.IntegerField()
    id_spec = peewee.CharField()
    logo = peewee.CharField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()

# Todo: 是否添加单独的首页滚动图片字段 ??
class CabPostHist(BaseModel):
    uid = peewee.CharField( null=False, index = True, unique=True, help_text='', primary_key=True, max_length=36)
    title = peewee.CharField(null=False, max_length = 255, help_text='',)
    date = peewee.DateTimeField()
    # cnt_html = peewee.TextField()
    # tags = peewee.CharField()
    post_id = peewee.CharField(null=False, max_length = 5, help_text='',)
    time_create = peewee.IntegerField()
    user_name= peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()
    # id_cats = peewee.CharField()
    id_spec = peewee.CharField()
    logo = peewee.CharField()

class CabSpec(BaseModel):
    uid = peewee.CharField()
    name = peewee.CharField()
    slug = peewee.CharField(null=False, index = True, unique=True, primary_key=True, max_length = 35, help_text='',)
    order = peewee.IntegerField()
    img = peewee.CharField()
    abstract = peewee.CharField()
    desc = peewee.CharField()

class CabMember(BaseModel):
    # user_id = peewee.CharField()
    '''
    privilege:
    11111
    读、写、改、删、管
    默认具有读的权限
    '''
    uid = peewee.IntegerField(null=False, index = True, unique=True, primary_key=True, help_text='',)
    user_name = peewee.CharField(null=False, index = True, unique=True, max_length = 16, help_text='',)
    privilege = peewee.CharField(null = False, default = '10000', help_text='用户权限',)
    user_pass = peewee.CharField(null = False, max_length=255,)
    user_email = peewee.CharField(null = False, max_length=255,)
class CabPic(BaseModel):
    # user_id = peewee.CharField()
    uid = peewee.CharField(null = False, index=True, unique=True, primary_key=True, max_length=36, )
    imgpath = peewee.CharField(null=False, unique=True,  max_length = 255, help_text='',)
    create_timestamp = peewee.IntegerField()
class CabPost2Catalog(BaseModel):
    uid = peewee.CharField(null=False, index = True, unique=True, primary_key=True, max_length = 35, help_text='', )
    catalog = peewee.ForeignKeyField(CabCatalog, related_name='cat_id')
    post = peewee.ForeignKeyField(CabPost,  related_name='post_id')
    order = peewee.IntegerField()
