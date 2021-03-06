# coding:utf-8
# File Name: auth.py
# Created Date: 2018-03-12 15:13:06
# Last modified: 2018-04-08 14:39:19
# Author: yeyong
from flask import Blueprint, request
from app.models.user import User
from app.models.send_code import SendCode
auth_route = Blueprint("auth_list", __name__, url_prefix="/api")

@auth_route.route("/login", methods=["POST"])
def login():
    if request.is_json:
        args = request.get_json()
        phone = args.get("phone")
        password = args.get("password")
        data = args.get("hash")
    else:
        phone = request.form.get("phone", None)
        password = request.form.get("password", None)
    if phone is None or password is None:
        return dict(msg="手机和密码不能为空", code=422)
    user = User.query.filter_by(phone=phone).first()
    if user and user.verify_password(password):
        user.reset_token()
        token = user.generate_token
        user.record_option(
                body="登录了账户",
                ip=request.remote_addr,
                event="login"
                )
        return dict(msg="ok", token=token, user=user.as_json(), code=200)
    else:
        return dict(msg="账户或密码错误", code=422)


@auth_route.route("/signup", methods=["POST"])
def signup():
    kwargs = request.form
    validate_form(**kwargs.to_dict())
    ok, user = User.user_create(**kwargs.to_dict())
    if not ok:
        return dict(msg=user, code=422)
    user.record_option(
            ip = request.remote_addr,
            body="注册了新账户",
            event="signup"
            )
    return dict(user=user.as_json(), code=200)
    
    

@auth_route.route("/send_code", methods=["POST"])
def send_code():
    phone = request.form.get("phone", None)
    ok, code = SendCode.code(phone)
    if not ok:
        return dict(msg=code, code=422)
    kwargs = dict(to=phone, vars = dict(code=code, time="3"))
    ok, msg = SendCode.send(**kwargs)
    if not ok:
        return dict(msg=msg, code=422)
    return dict(msg=msg, code=200)
    


@auth_route.route("/regiest", methods=["POST"])
def regiset_password():
    pass


def validate_form(**kwargs):
    phone = kwargs.get("phone", None)
    password = kwargs.get("passcord", None)
    confirm_password = kwargs.get("confirm_password", None)
    if phone is None:
        return dict(msg="手机号不能为空", code=422)
    if password is None or confirm_password is None:
        return dict(msg="密码不能为空", code=422)
    if password != confirm_password:
        return dict(msg="两次密码不一致", code=422)
    return True, ok





