# coding:utf-8
# File Name: routes.py
# Created Date: 2018-02-26 14:30:16
# Last modified: 2018-02-26 16:06:04
# Author: yeyong
from .base import AuthRoute
from . import auth

auth_route = AuthRoute()

auth.add_url_rule("/login", view_func=auth_route.login, methods=["POST"])
auth.add_url_rule("/signup/<int:id>", view_func=auth_route.signup, methods=["POST"])
