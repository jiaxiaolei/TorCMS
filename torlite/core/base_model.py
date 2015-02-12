# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

import config
import peewee




# create a base model class that our application's models will extend. From django
class BaseModel(peewee.Model):
    class Meta:
        database = config.dbconnect