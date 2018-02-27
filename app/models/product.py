# coding:utf-8
# File Name: product.py
# Created Date: 2018-02-27 14:45:17
# Last modified: 2018-02-27 15:23:26
# Author: yeyong
from app.extra import *
class Product(db.Model, Timestamp, Serialize):
    __tablename__ = 'products'
    title = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    category_id= db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False, index=True)
    price = db.Column(db.Integer, default=0)
    material = db.Column(db.String)
    kind = db.Column(db.String)
    product_type = db.Column(db.String)
    color = db.Column(db.String)
    metal = db.Column(db.String)
    pro_set = db.Column(db.String)
    unit = db.Column(db.String)
    price_type = db.Column(db.String, default="元")

