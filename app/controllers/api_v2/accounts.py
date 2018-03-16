# coding:utf-8
# File Name: accounts.py
# Created Date: 2018-03-12 10:23:16
# Last modified: 2018-03-16 14:33:28
# Author: yeyong
from flask import request, g
from app.models.user import User, Account

class AccountsView:

    def index(self):
        args = dict(
                name=request.args.get("name", None),
                phone=request.args.get("phone", None),
                role=request.args.get("role", None),
                start_time=request.args.get("start_time"),
                end_time= request.args.get("end_time"),
                account_id=g.current_user.account_id
                )
        users, page = User.model_search(**args)
        return dict(msg="ok", code=200, users=[user.to_json() for user in users], page=page)


    def show(self, id):
        """ 获取账户详细"""
        account = Account.query.filter_by(id=id).first()
        if not account:
            return dict(msg="无效的账户", code=404)
        return dict(msg="ok", account=account.to_json(), code=200)

    def create(self):
        kwargs = request.form.to_dict()
        ok, account = Account.create_account(user=g.current_user, **kwargs)
        if not ok:
            return dict(msg=account, code=422)
        return dict(msg="ok", account=account.to_json(), code=200)



