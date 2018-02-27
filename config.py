# coding:utf-8
# File Name: config.py
# Created Date: 2018-02-26 10:38:12
# Last modified: 2018-02-26 16:20:28
# Author: yeyong
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True
    DEBUG=True
    REDIS_URL="redis://:5mutian_chuang@106.14.16.196:6379/5"
    QINIU_AK = "D2HoWxWkb2MHhZVO5J5902DyeGNA05csQJOomlg0"
    QINIU_SK = "TmrvwiSTzBO9snZ2dg8JOYuCQA19IetyN-gZpZT8"
    BUCKET_NAME = "keeper"
    QINIU_URL = "https://images.salesgj.com/"

    @staticmethod
    def init_app(app):
        pass
