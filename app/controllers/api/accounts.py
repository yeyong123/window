# coding:utf-8
# File Name: accounts.py
# Created Date: 2018-03-12 10:23:16
# Last modified: 2018-03-20 17:05:58
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
        """添加公司"""
        kwargs = request.form.to_dict()
        ok, account = Account.create_account(user=g.current_user, **kwargs)
        if not ok:
            return dict(msg=account, code=422)
        return dict(msg="ok", account=account.to_json(), code=200)


    def searach_role(self):
        """搜索销售, 司机, 技工"""
        title = request.args.get("title", "销售")
        page = request.args.get("page", 1)
        users, page = g.current_account.searach_role(title=title, page=page)
        return dict(msg="ok", code=200, users=[u.to_json() for u in users], page=page)


    def update(self, id):
        """更新修改"""
        account = g.current_account
        kwargs = request.form.to_dict()
        ok, account = account.update(**kwargs)
        if not ok:
            return dict(msg=account, code=422)
        return dict(msg="ok", code=200, account=account.to_json())


       

    def add_users(self):
        """将用户添加角色并添加价格"""
        account = g.current_account
        phone = request.form.get("phone", None)
        roles = request.form.getlist("roles[]", None)
        raty = request.form.get("raty", 0.0)
        ok, account = account.add_user_and_allcate_roles(phon=phone, roles=roles, raty_price=raty)
        if not ok:
            return dict(msg=account, code=422)
        return dict(msg="ok", code=200, account=account.to_json())

    def permissions(self):
        data, page = self.temp_data(key="permissions")
        return dict(msg="ok", code=200, page=page, permissions=[p.to_json() for p in data])

    def company(self):
        data, page = self.temp_data(key="companies")
        return dict(msg="ok", code=200, page=page, companies=[p.to_json() for p in data])

    def material(self):
        data, page = self.temp_data(key="permissions")
        return dict(msg="ok", code=200, page=page, materials=[p.to_json() for p in data])

    def regions(self):
        data, page = self.temp_data(key="regions")
        return dict(msg="ok", code=200, page=page, regions=[p.to_json() for p in data])

    def category(self):
        data, page = self.temp_data(key="categories")
        return dict(msg="ok", code=200, page=page, categories=[cate.to_json() for cate in data])

    def roles(self):
        """获取本公司下的角色"""
        roles, page = self.temp_data(key="roles")
        return dict(msg="ok", code=200, roles=[role.to_json() for role in roles], page=page)

    
    def find_user(self):
        """搜索本公司的用户"""
        account = g.current_account
        key = request.args.get("key", None)
        page = request.args.get("page", 1)
        users, page = account.searach_role_users(key=key, page=1)
        return dict(msg="ok", code=200, users=[user.to_json() for user in users], page=page)

    def create_company(self):
        return self.temp_create_date(key="company")
        
    def create_material(self):
        return self.temp_create_date(key="material")
    
    def create_category(self):
        return self.temp_create_date(key="category")

    def create_role(self):
        return self.temp_create_date(key="role")

    def create_permiession(self):
        return self.temp_create_date(key="permissions")

    
    def delete_user_from_account(self):
        """从企业中移除用户"""
        user = request.form.get("user_id", None)
        if not user:
            return dict(msg="无效的用户", code=422)
        ok, account = g.current_account.delete_user(user)
        if not ok:
            return dict(msg=account, code=422)
        return dict(msg="ok", code=200, account=account.to_json())


    def temp_create_date(self, key=None):
        kwargs = request.form.to_dict()
        ok, data = g.current_account.base_create_data(key=key, **kwargs)
        if not ok:
            return dict(msg=data, code=422)
        return dict(msg="ok", code=200, data=data.to_json())



    def temp_data(self, key=None):
        """找出有关这个账户的数据如, 品牌, 渠道, 角色"""
        page = request.args.get("page", 1)
        return g.current_account.fetch_data_from_account(key=key, page=page)

        





