# -*- coding: utf-8 -*-
"""
Created on Feb 23, 2018

@author: guxiwen
"""
from functools import wraps
from flask import g, abort,current_app
from flask_login import current_user, user_logged_in


class RequireRole(object):
    roles = {
        "user": 0,
        "vip": 1,
        "admin": 2
    }

    def __init__(self, role):
        self.role = role

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.role is None:
                return func(*args, **kwargs)
            elif not hasattr(current_user, "type"):
                return abort(403)
            elif current_user.type < self.roles[self.role]:
                return abort(403)
            return func(*args, **kwargs)
        return wrapper


require_login = RequireRole("user")
require_vip = RequireRole("vip")
require_admin = RequireRole("admin")


def track_login(sender, user, **extra):
    print "%s login on %s..." % (user.username, user.last_login_ip)
    #user_logged_in.connect(record, app)

