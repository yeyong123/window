# coding:utf-8
# File Name: customers.py
# Created Date: 2018-03-12 14:17:27
# Last modified: 2018-04-08 14:58:43
# Author: yeyong
from flask import g, request
from app.models.customer import Customer

class CustomersView:
    def index(self):
        args = dict(
                account_id=g.current_account.id,
                user=g.current_user,
                customer_type=request.args.get("type", 1),
                name=request.args.get("name"),
                phone=request.args.get("phone"),
                city=request.args.get("city"),
                server_id=request.args.get("server_id"),
                start_time= request.args.get("start_time"),
                end_time = request.args.get("end_time")
                )
        customers, page = Customer.filter_customer(**args)
        return dict(msg="ok", code=200, customers=[c.to_json() for c in customers], page=page)



    def show(self, id):
        cust = self.find_customer(id)
        if not cust:
            return dict(msg="无效的 ID", code=422)
        return dict(msg="ok", code=200, customer=cust.as_json())

    def update(self, id):
        cust = self.find_customer(id)
        if not cust:
            return dict(msg="无效的 ID", code=422)
        ok, c = cust.update(**request.form.to_dict())
        if not ok:
            return dict(msg=c, code=422)
        cust.record_option(
                body="修改了客户的信息",
                ip = request.remote_addr,
                name = g.current_user.name,
                event = "update"
                )
        return dict(msg="ok", code=200, customer=c.as_json())

    def destroy(self, id):
        cust = self.find_customer(id)
        if not cust:
            return dict(msg="无效的 ID", code=422)
        cust.delete_customer()
        return dict(msg="ok", code=200)
        

        
    def create(self):
        """
        创建客户
        """
        account_id = g.current_account.id
        kwargs = request.form.to_dict()
        kwargs.update(account_id=account_id)
        ok, cust = Order.create_customer(**kwargs)
        if not ok:
            return dict(msg=cust, code=422)
        cust.record_option(
                body="添加了新的客户",
                event="create",
                ip = request.remote_addr,
                name = g.current_user.name
                )
        return dict(msg="ok", code=200, customer=cust.as_json())
        

    def create_common(self, id):
        kwargs = request.form.to_dict()
        kwargs.update(account_id=g.current_account.id, user_id=g.current_user.id)
        cust = self.find_customer(id)
        if not cust:
            return dict(msg="无效的 ID", code=422)
        ok, comm = cust.create_commoncation(**kwargs)
        if not ok:
            return dict(msg=comm, code=422)
        cust.record_option(
                body="发布了新的交流信息",
                event="communicate",
                ip = request.remote_addr,
                name = g.current_user.name
                )
        return dict(msg="ok", code=200, comm=comm.to_json())
        


    def find_customer(self, id):
        return Customer.query.filter_by(id=id).first()
