# coding:utf-8
# File Name: category.py
# Created Date: 2018-02-27 11:55:15
# Last modified: 2018-02-27 15:44:11
# Author: yeyong
from app.extra import *

class Category(db.Model, Timestamp, Serialize):
    __tablename__ = 'categories'
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    remark= db.Column(db.String)

