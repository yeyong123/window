# coding:utf-8
# File Name: customer.py
# Created Date: 2018-02-27 12:46:14
# Last modified: 2018-02-27 15:23:36
# Author: yeyong
from app.extra import *
class Customer(db.Model, Timestamp, Serialize):
    __tablename__ = 'customers'
    name = db.Column(db.String, index=True, nullable=False)
    phone = db.Column(db.String, index=True, nullable=False)
    province  = db.Column(db.String)
    city  = db.Column(db.String)
    district = db.Column(db.String)
    address = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    customer_type = db.Column(db.Integer, default=0, index=True)
    remark = db.Column(db.String)
    server_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    colse = db.Column(db.Boolean, default=False, index=True)

