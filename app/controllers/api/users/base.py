# coding:utf-8
# File Name: base.py
# Created Date: 2018-03-06 10:16:17
# Last modified: 2018-03-09 09:30:35
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

    def show(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return  dict(msg="用户没有找到", code=404)
        else:
            return dict(user=user.to_json(), msg="ok", code=200)


    def owner(self):
        return dict(user=g.current_user.as_json(), msg="ok", code=200)

