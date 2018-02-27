# coding:utf-8
# File Name: __init__.py
# Created Date: 2018-02-26 11:02:31
# Last modified: 2018-02-26 14:50:10
# Author: yeyong
from .main import main
from .auth import auth
class ApiRouter:
    @staticmethod
    def init_app(app):
        app.register_blueprint(main)
        app.register_blueprint(auth)
