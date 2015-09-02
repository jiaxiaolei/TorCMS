# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''
import tornado.web
import tornado.escape

import json
from torlite.core import tools
from torlite.core.base_handler import BaseHandler
from torlite.model.mwiki import MWiki
from torlite.model.mcatalog import MCatalog
from torlite.model.mspec import SpesubModel
from torlite.model.mwiki_hist import MWikiHist
from torlite.model.muser import MUser

from torlite.model.mreply import MReply
from torlite.model.mreply2user import MReply2User
from torlite.model.core_tab import CabReply
from torlite.model.core_tab import CabVoter2Reply
from torlite.model.mreply import MReply
from torlite.model.mpost2reply import MPost2Reply




class Post2ReplyHandler(BaseHandler):
    def initialize(self):
        self.muser = MUser()
        self.mreply = MReply()
        self.mreply2user = MReply2User()
        self.mpost2reply = MPost2Reply()

        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None

    def get(self, url_str=''):
        if url_str == '':
            return
        url_arr = url_str.split(r'/')

        if url_arr[0] == 'delete_reply':
            self.delete_by_id(url_arr[1])
        elif url_arr[0] == 'get':
            self.get_by_id(url_arr[1])
        elif url_arr[0] == 'zan':
            self.zan(url_arr[1])
    def post(self, url_str = ''):
        if url_str == '':
            return
        url_arr = url_str.split(r'/')

        if url_arr[0] == 'add':

            self.add_comment(url_arr[1])


    @tornado.web.authenticated
    def add_comment(self, id_post):

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_id'] = self.userinfo.uid
        post_data['user_name'] = self.userinfo.user_name


        comment_uid = self.mreply.insert_data(post_data)

        if comment_uid:
            comment2 = self.mpost2reply.insert_data2(id_post, comment_uid)
            output = {
                'pinglun': comment_uid,
            }
        else:
            output = {
                'pinglun': 0,
            }

        return json.dump(output, self)

    @tornado.web.authenticated
    def zan(self, id_reply):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_id'] = self.userinfo.uid

        cur_count = self.mreply2user.insert_data(self.userinfo.uid, id_reply)

        if cur_count:
            self.mreply.update_vote(id_reply, cur_count)
            output = {
                'text_zan': cur_count,
            }
        else:
            output = {
                'text_zan': 0,
            }

        return json.dump(output, self)

    def delete_by_id(self, del_id):


        is_deleted = self.mreply2user.delete(del_id)

        if is_deleted:

            output = {
                'del_zan': 1
            }
        else:
            output = {
                'del_zan': 0,
            }

        return json.dump(output, self)



