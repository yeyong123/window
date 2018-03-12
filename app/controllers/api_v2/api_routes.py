# coding:utf-8
# File Name: api_routes.py
# Created Date: 2018-03-12 12:12:55
# Last modified: 2018-03-12 14:48:08
# Author: yeyong
from .base import route_api, view_api


users = route_api['users']

@users.before_request
def check_login():
    return dict(msg="need login", code=420)


def add_route(route=None, view=None, path="", method="index"):
    view = view_api[view] if view else view_api["{}_view".format(route)]
    route_api.get(route).add_url_rule(path, view_func=getattr(view, method))


add_route(route='users')
add_route(route='users',path="/<int:id>", method="show")
add_route(route='accounts',path="/<int:id>", method="show")
add_route(route='accounts',path="", method="index")
add_route(route='accounts',path="/account", method="account")








