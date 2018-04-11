# coding:utf-8
# File Name: celery_runner.py
# Created Date: 2018-04-11 11:04:57
# Last modified: 2018-04-11 11:24:24
# Author: yeyong

import os
from app.flask_init import create_app
from celery import Celery


def make_celery(app):
    """
    工厂化 Celery服务, 集成到 Flask 中
    """
    celery = Celery(app.import_name, 
            broker=app.config.get("CELERY_BROKER_URL"), 
            backend=app.config.get("CELERY_BACKEND"))
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        """
        定义上下文执行环境
        抽象类
        """
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

fpp = create_app("pro")
celery = make_celery(fpp)



