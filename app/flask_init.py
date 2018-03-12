# coding:utf-8
# File Name: flask_init.py
# Created Date: 2018-02-26 10:48:01
# Last modified: 2018-03-12 15:11:27
# Author: yeyong
from config import Config
from .ext import  db, app, redis
#from app.controllers.api import ApiRouter
from app.controllers.admin import AdminRouter
from app.rouets import ApiV2


def create_app():
    app.config.from_object(Config)
    Config.init_app(app)
    db.init_app(app)
    redis.init_app(app)
    #ApiRouter.init_app(app)
    ApiV2.init_app(app)
    return app

