# coding:utf-8
# File Name: intercept.py
# Created Date: 2018-03-12 14:49:42
# Last modified: 2018-03-27 16:19:16
# Author: yeyong

from  flask import Blueprint, request
from app.ext import app
from app.models.photo import Photo
main_route = Blueprint("main_list", __name__)


@main_route.route("/")
def main():
    return dict(msg="创管家欢迎您", code=200)

@main_route.route("/upload", methods=["POST"])
def upload_file():
    f = request.files.get("image")
    name = f.filename
    if not f:
        return dict(msg="图片文件不能为空", code=422)
    f.save("/tmp/file")
    ok, photo = Photo.upload("/tmp/file", name)
    if not ok:
        return dict(msg=photo, code=422)
    return dict(photo=photo.to_json(), msg="ok", code=200)



@main_route.app_errorhandler(404)
def page_not_found(e):
    return {'msg': "此路径无效, 访问的路径不存在", 'code': 404}, 200

@main_route.app_errorhandler(400)
def no_method(e):
    print("参数请求失败{}".format(e))
    return {'msg': "参数请求失败", 'code': 400}, 200

@main_route.app_errorhandler(500)
def internal_server(e):
    print("服务器内部错误{}".format(e))
    return {"msg": "服务器内部错误", "code": 500}, 200


@main_route.before_app_request
def log_request_info():
    try:
        app.logger.warn("headers: {}".format(request.headers))
        if request.method == "GET":
            app.logger.warn("Body:  {}".format(request.args.to_dict()))
        else:
            if request.content_type == "application/x-www-form-urlencoded":
                app.logger.warn("Form => Body: %s",request.form.to_dict())
            else:
                app.logger.warn("Data => Body: %s", request.get_json())
    except Exception as e:
        return None
