# -*- coding:utf-8 -*-

import tornado
from wtforms.fields import StringField

from wtforms.validators import Required
from wtforms_tornado import Form

from torlite.core.base_handler import BaseHandler

from torlite.model.muser import MUser


class SumForm(Form):
    user_name = StringField(validators=[Required()])
    user_pass = StringField(validators=[Required()])
    user_email = StringField(validators=[Required()])


class UserHandler(BaseHandler):
    def initialize(self):
        self.muser = MUser()
        self.user_name = self.get_current_user()

    def get(self, url_str):
        url_arr = url_str.split('/')
        if url_str == 'regist':
            if self.get_current_user():
                self.redirect('/')
            else:
                self.__to_register__()
        elif url_str == 'login':
            self.to_login()
        elif url_str == 'info':
            self.show_info()
        elif url_str == 'logout':
            self.logout()
        elif url_str == 'changepass':
            self.changepass()
        elif url_str == 'changeinfo':
            self.change_info()
        elif url_arr[0] == 'changeprivilege':
            self.change_privilege(url_arr[1])
        elif url_str == 'find':
            self.to_find()
        elif url_arr[0] == 'find':
            self.find(url_arr[1])
        elif url_arr[0] == 'delete_user':
            self.delete(url_arr[1])

    def post(self, url_str):
        url_arr = url_str.split('/')
        if url_str == 'regist':
            self.register()
        elif url_str == 'login':
            self.login()
        elif url_str == 'changepass':
            self.changepassword()
        elif url_str == 'changeinfo':
            self.changeinfo()
        elif url_str == 'find':
            self.post_find()
        elif url_arr[0] == 'changeprivilege':
            self.changeprivilege(url_arr[1])

    @tornado.web.authenticated
    def changepassword(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        uu = self.muser.check_user(self.user_name, post_data['rawpass'][0])
        print(uu)
        if uu == 1:
            self.muser.update_pass(self.user_name, post_data['user_pass'][0])
            self.redirect(('/user/info'))
        else:
            return False

    @tornado.web.authenticated
    def changeinfo(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        uu = self.muser.check_user(self.user_name, post_data['rawpass'][0])
        print(uu)
        if uu == 1:
            self.muser.update_info(self.user_name, post_data['user_email'][0])
            self.redirect(('/user/info'))
        else:
            return False

    @tornado.web.authenticated
    def changeprivilege(self, xg_username):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

            self.muser.update_privilege(xg_username, post_data['privilege'][0])
            self.redirect(('/user/info'))

    @tornado.web.authenticated
    def logout(self):
        self.clear_all_cookies()
        self.redirect('/')

    @tornado.web.authenticated
    def changepass(self):
        self.render('tplite/user/changepass.html',
                    user_info=self.muser.get_by_id(self.user_name))

    @tornado.web.authenticated
    def change_info(self):
        self.render('tplite/user/changeinfo.html',
                    user_info=self.muser.get_by_id(self.user_name))

    @tornado.web.authenticated
    def change_privilege(self, xg_username):
        self.render('tplite/user/changeprivilege.html',

                    user_info=self.muser.get_by_id(xg_username))

    @tornado.web.authenticated
    def show_info(self):
        self.render('tplite/user/info.html',
                    user_info=self.muser.get_by_id(self.user_name))

    def to_login(self):
        if self.get_current_user():
            self.redirect('/')
        else:
            kwd = {
                'pager': '',
            }
            self.render('tplite/user/login.html', kwd=kwd)

    def register(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        form = SumForm(self.request.arguments)

        if form.validate():
            if self.muser.insert_data(post_data) == True:
                self.redirect('/user/login')
            else:
                self.render('html/404.html')
                self.set_status(400)

    def __to_register__(self):
        kwd = {
            'pager': '',
        }
        self.render('tplite/user/regist.html', kwd=kwd)

    def login(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        if 'next' in post_data:
            next_url = post_data['next'][0]
        else:
            next_url = '/'
        u_name = post_data['user_name'][0]
        u_pass = post_data['user_pass'][0]

        kwd = {
            'pager': '',
        }
        result = self.muser.check_user(u_name, u_pass)
        if result == 1:
            self.set_secure_cookie("user", u_name)
            self.redirect("{0}".format(next_url))
        elif result == -1:
            kwd = {
                'info': '没有这个用户'
            }
            self.render('html/404.html', kwd=kwd)
        else:
            self.redirect("{0}".format(next_url))

    def to_find(self, ):
        kwd = {
            'pager': '',
        }
        self.render('tplite/user/find.html', topmenu='', kwd=kwd)

    def find(self, keyword):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '查找结果',
        }
        self.render('tplite/user/find_list.html'.format(input),
                    kwd=kwd,
                    view=self.muser.get_by_keyword(keyword),
                    )

    def delete(self, del_id):
        is_deleted = self.muser.delete(del_id)

        self.redirect('/user/find')



    def post_find(self):
        keyword = self.get_argument('keyword')
        self.find(keyword)
