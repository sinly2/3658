# -*- coding: utf-8 -*-
"""
Created on Feb 23, 2018

@author: guxiwen
"""

from app import *
from flask_login import UserMixin


class User(UserMixin,db.Model):
    __table__name = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True)
    status = db.Column(db.Integer)
    type = db.Column(db.Integer)
    password = db.Column(db.String(100))
    retry_times = db.Column(db.Integer)
    recommend_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    last_login_time = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(20))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.username

    def __repr__(self):
        return '<Account: %s>' % self.username

    def check_password(self, raw):
        return self.password == raw

    def check_status(self):
        return self.status == 1

    def get_id(self):
        return unicode(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
