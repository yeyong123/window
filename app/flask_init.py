# coding:utf-8
# File Name: flask_init.py
# Created Date: 2018-02-26 10:48:01
<<<<<<< HEAD
# Last modified: 2018-03-05 15:55:05
=======
# Last modified: 2018-03-07 10:26:28
>>>>>>> 0dce874eff429d191b6bd7acc9a49d1402d441ad
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

