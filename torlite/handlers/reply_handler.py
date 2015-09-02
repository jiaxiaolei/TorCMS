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




class ReplyHandler(BaseHandler):
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

        if url_arr[0] == 'get':
            self.get_by_id(url_arr[1])


    def get_by_id(self, reply_id):
        reply = self.mreply.get_reply_by_uid(reply_id)

        self.render( 'tplite/reply/show_reply.html',
                     cnt = reply.cnt_html,
                     username=reply.user_name,
                     date=reply.date,
                     vote=reply.vote,
                     uid=reply.uid,
                     userinfo=self.userinfo,
                     unescape=tornado.escape.xhtml_unescape,
                     )

    def get_zan(self, f_zan):
        zan = self.mreply.get_by_zan(f_zan)
        if zan:
            output = {
                'zan': zan.zan,
            }
        else:
            output = {
                ''
            }

