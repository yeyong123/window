# coding:utf-8
# File Name: routes.py
# Created Date: 2018-03-06 10:23:59
# Last modified: 2018-03-06 10:56:54
# Author: yeyong
from .base import UsersView
from . import users
from flask import request, g
from app.models.user import User
users_view = UsersView()
users.add_url_rule("", view_func=users_view.index)

@users.before_request
def check_login():
    token = request.headers.get("Authorization", None)
    if not token:
        return dict(msg="需要授权才能访问", code=419), 200
    user = User.conver_token(token)
    if not user:
        return dict(msg="无效的验证,请重新登录", code=419), 200
    User.set_account(user.account_id)
    g.current_user = user


