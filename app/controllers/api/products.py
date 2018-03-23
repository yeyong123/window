# coding:utf-8
# File Name: products.py
# Created Date: 2018-03-20 17:04:53
# Last modified: 2018-03-20 17:09:21
# Author: yeyong
from flask import g, request
from app.models.product import Product
class ProductsView:
    def index(self):
        account = g.current_account
        products = Product.query
        return dict(msg="ok", code=200, products=[p.to_json() for p in products])
