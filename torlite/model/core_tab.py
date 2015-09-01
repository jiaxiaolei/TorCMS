# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

import peewee

from torlite.core.base_model import BaseModel


class CabCatalog(BaseModel):
    uid = peewee.IntegerField(null=False, index=True, unique=True, primary_key=True, help_text='', )
    slug = peewee.CharField(null=False, index=True, unique=True, max_length=36, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()
    post_count = peewee.IntegerField(default=0)
    app_count = peewee.IntegerField(default=0)


class CabPage(BaseModel):
    title = peewee.CharField(null=False, max_length=255, )
    slug = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    date = peewee.DateTimeField()
    cnt_html = peewee.TextField()
    time_create = peewee.IntegerField()
    id_user = peewee.CharField()
    cnt_md = peewee.CharField()
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()


class CabPost(BaseModel):
    uid = peewee.CharField(null=False, index=False, unique=True, primary_key=True, default='00000',
                           max_length=8, help_text='', )
    title = peewee.CharField(null=False,  help_text='Title')
    keywords = peewee.CharField(null=False,  help_text='Keywords')
    date = peewee.DateTimeField()
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, max_length=36, help_text='UserName', )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    id_spec = peewee.CharField()
    logo = peewee.CharField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    src_type = peewee.IntegerField( default= 0) # 0 for markdown, 1 for rst

class CabWiki(BaseModel):
    uid = peewee.CharField(null=False, index=False,
                           unique=True,
                           primary_key=True,
                           default='00000',
                           max_length=8, help_text='', )
    title = peewee.CharField(null=False, unique=True, help_text='Title')
    date = peewee.DateTimeField()
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, max_length=36, help_text='UserName', )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    src_type = peewee.IntegerField( default= 0) # 0 for markdown, 1 for rst


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

class CabWikiHist(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, help_text='', primary_key=True, max_length=36)
    title = peewee.CharField(null=False, max_length=255, help_text='', )
    date = peewee.DateTimeField()
    wiki_id = peewee.CharField(null=False, max_length=8, help_text='', )
    time_create = peewee.IntegerField()
    user_name = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()



class CabSpec(BaseModel):
    uid = peewee.CharField()
    name = peewee.CharField()
    slug = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    order = peewee.IntegerField()
    img = peewee.CharField()
    abstract = peewee.CharField()
    desc = peewee.CharField()
    date = peewee.DateTimeField()


class CabMember(BaseModel):
    # user_id = peewee.CharField()
    '''
    privilege:
    11111
    read,add,edit,delete,manage
    '''
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    user_name = peewee.CharField(null=False, index=True, unique=True, max_length=16, help_text='', )
    privilege = peewee.CharField(null=False, default='10000', help_text='Member Privilege', )
    user_pass = peewee.CharField(null=False, max_length=255, )
    user_email = peewee.CharField(null=False, max_length=255, )


class CabPic(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, )
    imgpath = peewee.CharField(null=False, unique=True, max_length=255, help_text='', )
    create_timestamp = peewee.IntegerField()


class CabPost2Catalog(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    catalog = peewee.ForeignKeyField(CabCatalog, related_name='cat_id')
    post = peewee.ForeignKeyField(CabPost, related_name='post_id')
    order = peewee.IntegerField()

class CabReply(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    #post_id = peewee.ForeignKeyField(CabPost, related_name='reply_post_id')
    create_user_id = peewee.ForeignKeyField(CabMember, related_name='reply_member_id')
    user_name = peewee.TextField()
    timestamp = peewee.IntegerField()
    date = peewee.DateTimeField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    vote = peewee.IntegerField()

class CabPost2Reply(BaseModel):
    uid =peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    post_id = peewee.ForeignKeyField( CabPost , related_name='post_reply_id')
    reply_id = peewee.ForeignKeyField(CabReply, related_name='reply_post_id')
    timestamp = peewee.IntegerField()

class CabVoter2Reply(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    reply_id = peewee.ForeignKeyField(CabReply, related_name='reply_voter_id')
    voter_id = peewee.ForeignKeyField(CabMember, related_name='voter_reply_id')
    timestamp = peewee.IntegerField()

# class CabPost2Spec(BaseModel):
#     uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
#     spec_id = peewee.ForeignKeyField(CabSpec, related_name='spec_post_id')
#     post_id = peewee.ForeignKeyField(CabPost, related_name='post_spec_id')
#     # order = peewee.IntegerField()