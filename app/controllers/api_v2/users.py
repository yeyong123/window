# coding:utf-8
# File Name: users.py
# Created Date: 2018-03-12 10:21:54
# Last modified: 2018-03-16 13:19:20
# Author: yeyong
from flask import request, g
from app.models.user import User
class UsersView:

    def index(self):
        args = dict(
                name=request.args.get("name", None),
                phone=request.args.get("phone", None),
                role=request.args.get("role", None),
                start_time=request.args.get("start_time", None),
                end_time=request.args.get("end_time", None)
                )
        users, page = User.model_search(**args)
        return dict(msg="ok", code=200, users=[u.to_json() for u in users], page = page)

    def show(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return dict(msg="该用户不在此星球", code=404)
        return dict(user=user.as_json(), msg="ok", code=200)

    
    def owner(self):
        if not hasattr(g, "current_user"):
            return dict(msg="未登录用户", code=419)
        user = g.current_user.as_json()
        return dict(user = user, msg="ok", code=200)

    def update(self, id):
        """修改密码"""
        password = request.form.get("password", None)
        user = g.current_user
        if not password is None and len(password) > 1:
            old_pass = request.form.get("old_password", None)
            confirm_pass = request.form.get("confirm_password", None)
            if old_pass is None or len(old_pass) < 1:
                return dict(msg="原密码不能为空", code=422)
            if not user.verify_password(old_pass):
                return dict(msg="原密码不正确", code=422)
            if password != confirm_pass:
                return dict(msg="两次密码不一致")
            user.password = password
        kwargs = request.form.to_dict()
        ok, user = user.update(**kwargs)
        if not ok:
            return dict(msg=user, code=422)
        return dict(msg="ok", user=user.as_json(), code=200)
        

    def owner_accounts(self):
        """列出我加入的公司"""
        user= g.current_user
        accounts, page = user.accounts_list(request.args.get("page", 1))
        return dict(msg="ok", code=200, accounts=[a.to_json() for a in accounts], page=page)

    def add_account(self):
        """加入公司"""
        acc_id = request.form.get("account_id", None)
        if not acc_id:
            return dict(msg="所选企业无效, 不能为空", code=422)
        ok, u = g.current_user.add_account(acc_id)
        if not ok:
            return dict(msg=u, code=422)
        return dict(msg="ok", code=200, u=u.as_json())

    def remove_toggle_account(self):
        """退出公司"""
        acc_id = request.form.get("account_id", None)
        kind = request.form.get("kind", "toggle")
        ok, u = g.current_user.toggle_and_remove_account(account_id=acc_id, kind=kind)
        if not ok:
            return dict(msg=u, code=422)
        return dict(msg="ok", code=200, u=u.as_json())

    def allocation_user_to_role(self):
        """为用户分配/修改权限"""
        ids = request.form.getlist("role_id[]", None)
        if type(ids) != list  or len(ids) < 1:
            return dict(msg="角色还未指定", code=422)
        ok, user = g.current_user.allocation_role(ids)
        if not ok:
            return dict(msg=user, code=422)
        return dict(msg="ok", code=200, user=user.as_json())

        
    def set_raty(self):
        """设置用户的提成"""
        raty = request.form.get("raty", 0.0)
        ok, raty = g.current_user.set_current_account_raty(raty=raty)
        if not ok:
            return dict(msg=raty, code=422)
        return dict(msg="ok", code=200, raty=raty.to_json())
        
        



