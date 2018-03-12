# coding:utf-8
# File Name: __init__.py
# Created Date: 2018-03-12 10:16:44
# Last modified: 2018-03-12 10:19:33
# Author: yeyong
from flak import Blueprint
accounts = Blueprint("accounts", __name__, url_prefix="/api/accounts")
