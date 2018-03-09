# coding:utf-8
# File Name: tasks.py
# Created Date: 2018-03-07 11:46:22
# Last modified: 2018-03-07 11:51:58
# Author: yeyong
from flask_celery import Celery
celery = Celery()
@celery.task()
def log(msg):
    return msg
