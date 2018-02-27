# coding:utf-8
# File Name: category.py
# Created Date: 2018-02-27 11:55:15
# Last modified: 2018-02-27 11:57:24
# Author: yeyong
from app.extra import *

class Category(db.Model, serialize):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, index=True, nullable=False)
    remark= db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

