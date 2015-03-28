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

    def get(self, input):
        if input == 'regist':
            self.__to_register__()
        elif input == 'login':
            self.to_login()
        elif input == 'info':
            self.show_info()
        elif input == 'logout':
            self.logout()

    @tornado.web.authenticated
    def logout(self):
        self.clear_all_cookies()
        self.redirect('/')

    @tornado.web.authenticated
    def show_info(self):
        self.render('tplite/user/info.html',
                    user_info = self.muser.get_by_id(self.user_name))

    def post(self, input):
        if input == 'regist':
            self.register()
        elif input == 'login':
            self.login()

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
            next_url = ''
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
            self.render('html/404.html', kwd = kwd)
        else:
            self.redirect("{0}".format(next_url))