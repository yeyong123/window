# coding:utf-8
# File Name: auth.py
# Created Date: 2018-03-12 15:13:06
# Last modified: 2018-03-12 15:27:47
# Author: yeyong
from flask import Blueprint, request
from app.models.user import User
auth_route = Blueprint("auth_list", __name__)

@auth_route.route("/login", methods=["POST"])
def login():
    phone = request.form.get("phone", None)
    password = requets.form.get("password", None)
    user = User.query..filter_by(phone=phone).first()
    if user and user.verify_password(password):
        user.reset_token()
        token = user.generate_token
        return dict(msg="ok", token=token, user=user.as_json(), code=200)
    else:
        return dict(msg="账户或密码错误", code=422)


@auth_route.route("/signup", methods=["POST"])
def signup():
    pass


@auth_route.route("/send_code", methods=["POST"])
def send_code():
    pass


@auth_route.route("/regiest", methods=["POST"])
def regiset_password():
    pass
