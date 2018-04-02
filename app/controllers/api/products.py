# coding:utf-8
# File Name: products.py
# Created Date: 2018-03-20 17:04:53
# Last modified: 2018-03-30 10:18:54
# Author: yeyong
from flask import g, request, jsonify
from app.models.product import Product
class ProductsView:
    def index(self):
        account = g.current_account
        products, page = Product.model_search(account_id=account.id, hide=False)
        return dict(msg="ok", code=200, products=[p.to_json() for p in products], page=page)


    def create_product(self):
        if request.is_json:
            args = request.get_json()
        else:
            args = request.form.to_dict()
        args.update(account_id=g.current_account.id)
        ok, p = Product.create_product(**args)
        if ok:
            return dict(msg="ok", code=200, product=p.to_json())
        else:
            return dict(msg=p, code=422)
    

    def show(self, id):
        p  = Product.query.filter_by(id=id, hide=False).first()
        if not p:
            return dict(msg="未找到该产品", code=404)
        return dict(msg="ok", code=200, product=p.to_json())


    def update(self, id):
        p = Product.query.filter_by(id=id).first()
        kwargs = request.form.to_dict()
        if not p:
            return dict(msg="无效的产品", code=404)
        ok, msg = p.update(**kwargs)
        if not ok:
            return dict(msg=msg, code=422)
        return dict(msg="ok", code=200, product=p.to_json())


    def destroy(self, id):
        p = Product.query.filter_by(id=id).first()
        if not p:
            return dict(msg="无效的产品", code=404)
        p.delete_product()
        return dict(msg="ok", code=200)
