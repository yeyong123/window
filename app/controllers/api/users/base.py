# coding:utf-8
# File Name: base.py
# Created Date: 2018-03-06 10:16:17
# Last modified: 2018-03-07 12:47:03
# Author: yeyong
from flask import request,g
from app.models.user import User

class UsersView:
    def index(self):
        args = dict(
                page = request.args.get("page", 1)
                )
        users, page = User.model_search(**args)
        return dict(users=[user.to_json() for user in users], page=page, msg="ok", code=200, user=g.current_user.to_json())

