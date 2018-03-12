# coding:utf-8
# File Name: accounts.py
# Created Date: 2018-03-12 10:23:16
# Last modified: 2018-03-12 12:16:09
# Author: yeyong
class AccountsView:
    def index(self):
        return dict(msg="This is account", code=200)

    def show(self, id):
        return dict(msg="This is account {}".format(id), code=200)

    def account(self):
        return dict(msg="acccccc", code=200)



