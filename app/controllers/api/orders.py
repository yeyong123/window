# coding:utf-8
# File Name: orders.py
# Created Date: 2018-03-12 14:17:34
# Last modified: 2018-04-08 15:02:39
# Author: yeyong

from flask import g, request
from app.models.order import Order

class OrdersView:
    def index(self):
        p = request.args
        args = dict(
                category_id=p.get("category_id"),
                customer_name = p.get("customer_name"),
                serial_no = p.get("serial_no"),
                status=p.get("status"),
                order_type=p.get("order_type"),
                sub=p.get("sub"),
                event=p.get("type"),
                user=g.current_user,
                start_time=p.get("start_time"),
                end_time = p.get("end_time")
                )
        orders, page = Order.filter_orders(**args)
        return dict(msg="ok", code=200, orders=[o.to_json() for o in orders], page=page)

    def create_order(self):
        kwargs = request.form.to_dict()
        kwargs = {k: v for k, v in kwargs.items() if k in self.params() and v}
        kwargs.update(account_id=g.current_account.id, user_id=g.current_user.id, ip=request.remote_addr, u_name = g.current_user.name)
        ok, order = Order.create_order(**kwargs)
        if not ok:
            return dict(msg=order, code=422)
        order.record_options(event="create", body="创建了订单")
        return dict(msg="ok", code=200, order=order.show_json())

    def show(self, id):
        order = self.find_order(id)
        if not order:
            return dict(msg="无效的 ID", code=422)
        return dict(msg="ok", code=200, order=order.show_json())



    def find_order(self, id=None):
        account = g.current_account
        return Order.query.filter_by(account_id=account.id,id=id).first()


    def update(self, id):
        kwargs = request.form.to_dict()
        kwargs = {k: v for k, v in kwargs.items() if k in self.params() and v}
        order = self.find_order(id)
        if not order:
            return dict(msg="无效的 ID",code=422)
        ok, temp = order.update(**kwargs)
        if not ok:
            return dict(msg=temp, code=422)
        order.record_option(
                body="操作修改了订单",
                ip=request.remote_addr,
                name=g.current_user.name,
                event="update"
                )
        return dict(msg="ok", code=200, order=temp.show_json())


    def order_process(self, id):
        """处理订单事件"""
        user = g.current_user
        key = request.form.get("event")
        content = request.form.get("content")
        order = self.find_order(id)
        ok, result = order.handle_order_event(key=key, user=user, content=content, ip=request.remote_addr)
        if not ok:
            return dict(msg=result, code=422)
        return dict(msg="ok", code=200, order=result.show_json())


    def toggle_order(self, id):
        order = self.find_order(id)
        if not order:
            return dict(msg="无效的 ID", code=422)
        order.toggle_order()
        return dict(msg="ok", code=200, order=order.to_json())

    def create_detail(self, id):
        order = self.find_order(id)
        kwargs = request.form.to_dict()
        ok, result = order.create_detail(**kwargs)
        if not ok:
            return dict(msg=result, code=422)
        return dict(msg="ok", code=200, order_detail=result.to_json())

    def update_detail(self, id):
        order = self.find_order(id)
        kwargs = request.form.to_dict()
        ok, temp = order.update_detail(**kwargs)
        if not ok:
            return dict(msg=temp, code=422)
        return dict(msg="ok", code=200, detail=temp.to_json())
        

    def params(self):
        """订单模型中允许传入的字段"""
        args = set(Order.__table__.columns.keys())
        columns = {"id", "account_id", "user_id", "total_amount"}
        for p in columns:
            args.remove(p)
        return args

