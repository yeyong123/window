# coding:utf-8
# File Name: base.py
# Created Date: 2018-02-26 14:30:39
# Last modified: 2018-03-06 10:46:53
# Author: yeyong
from flask import request
from app.models.user import User

class AuthRoute:
    def login(self):
        phone = request.form.get("phone", None)
        password = request.form.get("password", None)
        user = User.query.filter_by(phone=phone).first()
        if user and user.verify_password(password):
            user.reset_token()
            token = user.generate_token
            return dict(msg="ok", token=token, user=user.as_json(), code=200)
        else:
            return dict(msg="账户或密码错误", code=422)


    def signup(self):
        pass

    def send_code(self):
        phone = request.form.get("phone", None)
        if phone is None:
            return dict(msg="手机号不能为空", code=404)
        


