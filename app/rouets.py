# coding:utf-8
# File Name: rouets.py
# Created Date: 2018-03-12 10:29:27
# Last modified: 2018-03-23 14:34:47
# Author: yeyong
from app.controllers.api.base import temp_record
from app.controllers.api.intercept import main_route
from app.controllers.api.auth import auth_route

class Api:
    @staticmethod
    def init_app(app):
        app.register_blueprint(main_route)
        app.register_blueprint(auth_route)
        for k, v in temp_record.__dict__.items():
            app.register_blueprint(v)
