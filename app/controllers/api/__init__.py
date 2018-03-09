# coding:utf-8
# File Name: __init__.py
# Created Date: 2018-02-26 11:02:31
# Last modified: 2018-03-07 10:19:06
# Author: yeyong
from .main import main
from .auth import auth
from .users import users
class ApiRouter:
    @staticmethod
    def init_app(app):
        app.register_blueprint(main)
        app.register_blueprint(auth)
        app.register_blueprint(users)
