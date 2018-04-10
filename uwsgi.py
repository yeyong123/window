# coding:utf-8
# File Name: uwsgi.py
# Created Date: 2018-04-10 15:02:41
# Last modified: 2018-04-10 15:18:51
# Author: yeyong

from app.flask_init import create_app

app = create_app('pro')
