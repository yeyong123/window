# coding:utf-8
# File Name: stores.py
# Created Date: 2018-03-26 17:02:39
# Last modified: 2018-03-26 17:17:42
# Author: yeyong
from flask import request, g
from app.models.account import Account
from app.models.product import Product
class StoresView:

    def stores_list(self):
        key = request.args.get("key")
        q = request.args.get("q")
        page = request.args.get("page", 1)
        kind = None
        if q:
            kind = "name"
            key =  q
        else:
            kind="near"
        results, page = Account.search_store(key=key, kind=kind, page=page)
        return dict(msg="ok", code=200, stores=[result.to_json() for result in results], page=page)

    def stores(self):
        _id = request.args.get("store_id")
        args = dict(account_id=_id)
        products, page = Product.model_search(**args)
        return dict(msg="ok", code=200, page=page, products=[p.to_json() for p in products])

    def store(self, id):
        p = Product.query.filter_by(id=id).first()
        if not p:
            return dict(msg="该产品已下架", code=404)
        return dict(msg="ok", code=200, product=p.to_json())
        


        
    
