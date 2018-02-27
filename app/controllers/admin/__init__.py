# coding:utf-8
# File Name: __init__.py
# Created Date: 2018-02-26 11:03:40
# Last modified: 2018-02-26 11:04:02
# Author: yeyong
class AdminRouter:
    @staticmethod
    def init_app(app):
        app.register_blueprint(main)
