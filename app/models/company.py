# coding:utf-8
# File Name: company.py
# Created Date: 2018-02-27 12:41:54
# Last modified: 2018-02-27 15:42:01
# Author: yeyong
from app.extra import *
class Company(db.Model, Timestamp,  Serialize):
    __tablename__ = 'companies'
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    title = db.Column(db.String)
    logo = db.Column(db.String)
    remark = db.Column(db.String)

