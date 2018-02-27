# coding:utf-8
# File Name: intercept.py
# Created Date: 2018-02-26 14:54:07
# Last modified: 2018-02-26 15:15:46
# Author: yeyong
from . import main
from app.extra import app

@main.app_errorhandler(404)
def page_not_found(e):
    return {'msg': " 访问的路径不存在", 'code': 404}, 200

@main.app_errorhandler(400)
def no_method(e):
    print("参数请求失败{}".format(e))
    return {'msg': "参数请求失败", 'code': 400}, 200

@main.app_errorhandler(500)
def internal_server(e):
    print("服务器内部错误{}".format(e))
    return {"msg": "服务器内部错误", "code": 500}, 200


@main.before_app_request
def log_request_info():
    try:
        app.logger.info("headers: {}".format(request.headers))
        if request.method == "GET":
            app.logger.info("Body:  {}".format(request.args.to_dict()))
        else: 
            print(">>>>>>>>>>>>>>", request.form.to_dict(), '\n')
            if request.content_type == "application/x-www-form-urlencoded":
                app.logger.info("Form => Body: %s",request.form.to_dict())
            else:
                app.logger.info("Data => Body: %s", request.get_json())
    except Exception as e:
        return None

