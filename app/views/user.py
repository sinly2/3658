# -*- coding: utf-8 -*-
"""
Created on Feb 23, 2018

@author: guxiwen
"""

from flask import request
from . import main
from app import db
from ..models.user import User
from ..forms.user import RegisterForm
from flask_login import login_user,logout_user,current_user
from ..utils.user import require_login, require_vip


@main.route('/test')
def test():
    username = request.args.get("username")
    password = request.args.get("pwd")
    #print db.sessoin.query(user)
    #print db.session.query(User).first()
    user = User.query.filter_by(username=username).first()
    print user.last_login_ip
    if user and user.check_password(password):
        return "hahaha"
    return "ok"

@main.route("/test2")
@require_login
def test2():
    return "xici.net"


@main.route("/register",methods=['POST'])
def register():
    #recommend_id = request.args.get("recommend_id")
    form = RegisterForm(request.form)
    try:
        #form.validate_username()
        if not form.validate():
            print form.errors
        form.save()
    except ValueError:
        return u"用户名已注册..."
    except Exception as e:
        print e
    return "ok"


@main.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user,remember=False)
        print current_user.id
        return "hahaha"
    return "ok"

@main.route("/logout")
@require_login
def logout():
    logout_user()
    return "ok"