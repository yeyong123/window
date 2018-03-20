# coding:utf-8
# File Name: api_routes.py
# Created Date: 2018-03-12 12:12:55
# Last modified: 2018-03-20 17:09:00
# Author: yeyong
from flask import g, request, Blueprint
from .base import route_api, view_api
from app.models.user import User
from app.models.order import Order
from app.controllers.api_v2.users import UsersView
from app.controllers.api_v2.accounts import AccountsView

users = route_api['users']
accounts = route_api["accounts"]
orders = route_api["orders"]
customers = route_api["customers"]
products = route_api["products"]

@accounts.before_request
@users.before_request
@orders.before_request
@customers.before_request
@products.before_request
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
    Order.set_account(user.account_id)
    Order.set_current_user(user)
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
add_route(route='users',path="/allocation_user_to_role", method="allocation_user_to_role", action="POST")
add_route(route='users',path="/set_price", method="set_raty", action="POST")
add_route(route='users',path="/toggle_account", method="remove_toggle_account", action="POST")
add_route(route='users',path="/remove_account", method="remove_toggle_account", action="POST")

## 结束用户的路由
##
##
## 账户有关的路由
add_route(route='accounts',path="/<int:id>", method="show")
add_route(route='accounts',path="", method="index")
add_route(route='accounts',path="", method="create", action="POST")
add_route(route='accounts',path="/salers", method="searach_role")
add_route(route='accounts',path="/<int:id>", method="update", action="POST")
add_route(route='accounts',path="/roles", method="roles")
add_route(route='accounts',path="/add_users", method="add_users", action="POST")
add_route(route='accounts',path="/find_users", method="find_user")
add_route(route='accounts',path="/permissions", method="permissions")
add_route(route='accounts',path="/company", method="company")
add_route(route='accounts',path="/regions", method="regions")
add_route(route='accounts',path="/materail", method="material")
add_route(route='accounts',path="/category", method="category")
add_route(route='accounts',path="/create_material", method="create_material", action="POST")
add_route(route='accounts',path="/create_company", method="create_company", action="POST")
add_route(route='accounts',path="/create_category", method="create_category", action="POST")
add_route(route='accounts',path="/create_permiession", method="create_permiession", action="POST")
add_route(route='accounts',path="/delete_user_from_account", method="delete_user_from_account", action="POST")


##########
#订单
###########
add_route(route="orders", path="", method="index")
add_route(route="orders", path="/<int:id>", method="show")
add_route(route="orders", path="/<int:id>", method="update", action="POST")
add_route(route="orders", path="", method="create_order", action="POST")
add_route(route="orders", path="/<int:id>/order_process", method="order_process", action="POST")
add_route(route="orders", path="/<int:id>/toggle_order", method="toggle_order", action="POST")
add_route(route="orders", path="/<int:id>/create_detail", method="create_detail", action="POST")
add_route(route="orders", path="/<int:id>/update_detail", method="update_detail", action="POST")

#######################################
#结束 订单
#######################################

##########################
## 客户
##########################
add_route(route="customers", path="", method="index")
add_route(route="customers", path="/<int:id>", method="show")
add_route(route="customers", path="/<int:id>", method="update", action="PUT")
add_route(route="customers", path="", method="create", action="POST")
add_route(route="customers", path="/<int:id>", method="destroy", action="DELETE")
add_route(route="customers", path="/<int:id>/create_comm", method="create_common", action="POST")

#########################################
#结束客户
########################################

###################################
## 产品库
####################################
add_route(route="products", path="", method="index")




