# coding:utf-8
# File Name: api_routes.py
# Created Date: 2018-03-12 12:12:55
# Last modified: 2018-03-16 14:33:17
# Author: yeyong
from flask import g, request, Blueprint
from .base import route_api, view_api
from app.models.user import User
from app.controllers.api_v2.users import UsersView
from app.controllers.api_v2.accounts import AccountsView

users = route_api['users']
accounts = route_api["accounts"]

@users.before_request
@accounts.before_request
def check_login():
    """
    获取用户请求头中的 Headers 中的 Authorization的值
    根据这个的值找出数据库中的用户的解析, 并且返回用户
    如果没有找到就返回错误
    """
    token = request.headers.get("Authorization", None)
    if not token:
        return dict(msg="需要授权登录才能访问", code=419)
    user = User.conver_token(token)
    if not user:
        return dict(msg="登录验证失效",code=419)
    User.set_account(user.account_id)
    g.current_user = user
    g.current_account = user.current_account


def add_route(route=None, view=None, path="", method="index", action="GET"):
    view = view_api[view] if view else view_api["{}_view".format(route)]
    route_api.get(route).add_url_rule(path, view_func=getattr(view, method), methods=[action])

##用户的路由

add_route(route='users')
add_route(route='users',path="/<int:id>", method="show")
add_route(route='users',path="/owner", method="owner")
add_route(route='users',path="/<int:id>", method="update", action="POST")
add_route(route='users',path="/account_list", method="owner_accounts")
add_route(route='users',path="/add_account", method="add_account", action="POST")
add_route(route='users',path="/allocation_role", method="allocation_user_to_role", action="POST")
add_route(route='users',path="/set_raty", method="set_raty", action="POST")
add_route(route='users',path="/toggle_account", method="remove_toggle_account", action="POST")
add_route(route='users',path="/remove_account", method="remove_toggle_account", action="POST")

## 结束用户的路由
##
##
## 账户有关的路由
add_route(route='accounts',path="/<int:id>", method="show")
add_route(route='accounts',path="", method="index")
add_route(route='accounts',path="", method="create", action="POST")








