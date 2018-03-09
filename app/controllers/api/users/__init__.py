# coding:utf-8
# File Name: __init__.py
# Created Date: 2018-03-06 10:14:18
# Last modified: 2018-03-06 10:49:09
# Author: yeyong

from flask import Blueprint
users = Blueprint("users", __name__, url_prefix="/api/users")
from . import routes



