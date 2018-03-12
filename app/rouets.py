# coding:utf-8
# File Name: rouets.py
# Created Date: 2018-03-12 10:29:27
# Last modified: 2018-03-12 12:03:14
# Author: yeyong
from app.controllers.api_v2.base import temp_record

class ApiV2:
    @staticmethod
    def init_app(app):
        for k, v in temp_record.__dict__.items():
            app.register_blueprint(v)
