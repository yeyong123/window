# coding:utf-8
# File Name: __init__.py
# Created Date: 2018-02-26 11:12:12
# Last modified: 2018-02-26 14:54:54
# Author: yeyong
from flask import Blueprint
main = Blueprint('main', __name__, url_prefix = '/api')
from . import routes, intercept
