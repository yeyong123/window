# coding:utf-8
# File Name: report.py
# Created Date: 2018-03-23 14:34:56
# Last modified: 2018-03-23 15:15:02
# Author: yeyong
from flask import g, request
from app.models.order import Order
class ReportView:
    def orders(self):
        page  = request.args.get("page", 1)
        orders, page = Order.complete_orders(page)
        return dict(
                msg="ok",
                code=200,
                orders=[o.to_json() for o in orders],
                page=page
                )

    def expense(self):
        params = request.args.get("type", None)
        if params == "ship":
            orders = Order.group_service_orders(kind="ship")
        elif params == "deduct":
            orders = Order.group_service_orders(kind="intro")
        else:
            orders = Order.group_service_orders()

        return dict(
                msg="ok",
                code=200,
                orders=orders
                )
        

    def income_increase(self):
        orders = Order.group_income_orders()
        return dict(
                msg="ok",
                code=200,
                orders=orders
                )

    def order_increase(self):
        orders = Order.group_income_orders(kind="orders")
        return dict(
                msg="ok",
                code=200,
                orders=orders
                )

    def report_orders(self):
        return dict(
                msg="ok", 
                code=200,
                total_amount=Order.total_income_amount(),
                total_count = Order.total_orders_count(),
                total_amount_month=Order.total_income_amount(current=True),
                total_count_month=Order.total_orders_count(current=True),
                expense = Order.expense_total_amount(),
                profit=Order.expense_total_amount(profit=True),
                sale=Order.total_income_amount(kind="intro"),
                install=Order.total_income_amount(kind="install"),
                ship = Order.total_income_amount(kind="ship"),
                measure=Order.total_income_amount(kind="measure")
                )


