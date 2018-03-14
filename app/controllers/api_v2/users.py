# coding:utf-8
# File Name: users.py
# Created Date: 2018-03-12 10:21:54
# Last modified: 2018-03-14 14:38:08
# Author: yeyong
class UsersView:
    def index(self):
        return dict(msg="ok", code=200)

    def show(self, id):
        return dict(msg="This is {}".format(id), code=200)


    #用户的事件以及用户的操作
    
    ## 用户加入公司
    ## 用户退出公司
    ## 列出我加入的公司

