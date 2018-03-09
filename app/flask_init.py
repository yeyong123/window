# coding:utf-8
# File Name: flask_init.py
# Created Date: 2018-02-26 10:48:01
# Last modified: 2018-03-05 15:55:05
# Author: yeyong
from config import Config
from .ext import  db, app, redis
from app.controllers.api import ApiRouter
from app.controllers.admin import AdminRouter


def create_app():
    app.config.from_object(Config)
    Config.init_app(app)
    db.init_app(app)
    redis.init_app(app)
    ApiRouter.init_app(app)

    return app

