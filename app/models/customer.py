# coding:utf-8
# File Name: customer.py
# Created Date: 2018-02-27 12:46:14
# Last modified: 2018-02-27 12:52:00
# Author: yeyong
from app.extra import *
class Customer(db.Model, Serialize):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, nullable=False)
    phone = db.Column(db.String, index=True, nullable=False)
    province  = db.Column(db.String)
    city  = db.Column(db.String)
    district = db.Column(db.String)
    address = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForignKey("accounts.id"), nullable=False, index=True)
    customer_type = db.Column(db.Integer, default=0, index=True)
    remark = db.Column(db.String)
    server_id = db.Column(db.Integer, db.ForignKey("users.id"), index=True)
    colse = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

