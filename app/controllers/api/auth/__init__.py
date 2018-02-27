# coding:utf-8
# File Name: __init__.py
# Created Date: 2018-02-26 14:29:10
# Last modified: 2018-02-26 14:51:02
# Author: yeyong
from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api")

from . import routes
