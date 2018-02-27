# coding:utf-8
# File Name: permisson.py
# Created Date: 2018-02-27 14:33:27
# Last modified: 2018-02-27 15:37:46
# Author: yeyong
from app.extra import *
class Permission(db.Model, Timestamp, Serialize):
    __tablename__ = 'permissions'
    level = db.Column(db.Integer, default=0, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    title = db.Column(db.String)

