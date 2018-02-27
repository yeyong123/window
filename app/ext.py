# coding:utf-8
# File Name: ext.py
# Created Date: 2018-02-26 10:50:58
# Last modified: 2018-02-26 16:17:23
# Author: yeyong
from .json_response import MyFlask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
db = SQLAlchemy()
app = MyFlask(__name__)
redis = FlaskRedis()
