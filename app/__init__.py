# -*- coding: utf-8 -*-
"""
Created on Feb 23, 2018

@author: guxiwen
"""
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, user_logged_in
from flask_bootstrap import Bootstrap
from utils.user import track_login
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'


def create_app():
    app = Flask(__name__)
    from .views import main as main__blueprint
    app.config['SECRET_KEY'] = 'hehe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.register_blueprint(main__blueprint)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    user_logged_in.connect(track_login, app)

    # @user_logged_in.connect_via(app)
    # def record(sender, **extra):
    #     print "====================================="
    return app
