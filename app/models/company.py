# coding:utf-8
# File Name: company.py
# Created Date: 2018-02-27 12:41:54
# Last modified: 2018-02-27 12:46:01
# Author: yeyong
from app.extra import *
class Company(db.Model, serialize):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForignKey("accounts.id"), nullable=False, index=True)
    title = db.Column(db.String)
    logo = db.Column(db.String)
    remark = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

