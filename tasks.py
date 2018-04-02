# coding:utf-8
# File Name: tasks.py
# Created Date: 2018-03-07 11:46:22
# Last modified: 2018-03-30 15:24:57
# Author: yeyong

from app.models.user import User
from flask_celery import Celery
celery = Celery()
@celery.task()
def log(msg):
    return msg


@celery.task()
def check_users(name=None):
    users = User.query.filter_by(name=name).all()
    return [u.to_json() for u in users]

