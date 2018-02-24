# -*- coding: utf-8 -*-
"""
Created on Feb 23, 2018

@author: guxiwen
"""
from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Email, Length, Regexp
from wtforms.validators import Optional, URL
from ..models.user import User
from ..utils.common import stack_info


class RegisterForm(Form):
    username = StringField("username", validators=[Length(min=4, max=25)])
    password = StringField("password", validators=[Length(min=4, max=25)])

    @stack_info
    def validate_username(self,field):
        if User.query.filter_by(username=field.data.lower()).count():
            raise ValueError('This username has been registered.')

    def save(self):
        if self.validate():
            print self.data
            user = User(**self.data)
            user.save()
            return user
