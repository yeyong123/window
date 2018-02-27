# coding:utf-8
# File Name: communicate.py
# Created Date: 2018-02-27 11:57:35
# Last modified: 2018-02-27 12:41:46
# Author: yeyong
from app.extra import *
class Communicate(db.Model, serialize):
    __tablename__ = 'communicates'
    
    id = db.Column(db.Integer, primary_key=True)
    remark = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    account_id = db.Column(db.Integer, db.ForignKey("accounts.id"), index=True)
    customer_id = db.Column(db.Integer, db.ForignKey("users.id"), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


