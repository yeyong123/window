# coding:utf-8
# File Name: flask_init.py
# Created Date: 2018-02-26 10:48:01
# Last modified: 2018-04-10 15:08:26
# Author: yeyong
from config import config
from .ext import  db, app, redis
from app.controllers.admin import AdminRouter
from app.rouets import Api


def create_app(env):
    app.config.from_object(config[env])
    config[env].init_app(app)
    db.init_app(app)
    redis.init_app(app)
    Api.init_app(app)
    return app

