# coding:utf-8
# File Name: task.py
# Created Date: 2018-03-07 11:39:56
# Last modified: 2018-03-07 11:51:33
# Author: yeyong
import os
from app.flask_init import create_app
from celery import Celery
from tasks import log

def make_celery(app):
    celery = Celery(app.import_name,broker=app.config.get("CELERY_BROKER_URL"), backend=app.config.get("CELERY_BACKEND"))
    celery.conf.update(app.config)
    TaskBase = celery.Task
    
    class ContextTask(TaskBase):
        abstract = True
        
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

flask_app = create_app()
celery = make_celery(flask_app)

