# coding:utf-8
# File Name: products.py
# Created Date: 2018-03-20 17:04:53
# Last modified: 2018-03-27 16:33:06
# Author: yeyong
from flask import g, request, jsonify
from app.models.product import Product
class ProductsView:
    def index(self):
        account = g.current_account
        products, page = Product.model_search(account_id=account.id)
        return dict(msg="ok", code=200, products=[p.to_json() for p in products], page=page)


    def create_product(self):
        args = request.form.to_dict()
        name = {}
        pictures = request.form.getlist("pictures[image]")
        args.update(account_id=g.current_account.id, pictures=pictures)

        ok, p = Product.create_product(**args)
        if ok:
            return dict(msg="ok", code=200, product=p.to_json())
        else:
            return dict(msg=p, code=422)

