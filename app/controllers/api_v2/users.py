# coding:utf-8
# File Name: users.py
# Created Date: 2018-03-12 10:21:54
# Last modified: 2018-03-12 10:45:16
# Author: yeyong
class UsersView:
    def index(self):
        return dict(msg="ok", code=200)

    def show(self, id):
        return dict(msg="This is {}".format(id), code=200)
