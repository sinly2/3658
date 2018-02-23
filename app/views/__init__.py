# -*- coding: utf-8 -*-
"""
Created on Feb 23, 2018

@author: guxiwen
"""

from flask import Blueprint
main = Blueprint('user', __name__)
from . import  user