# coding:utf-8
# File Name: material.py
# Created Date: 2018-02-27 12:57:39
# Last modified: 2018-02-28 14:47:50
# Author: yeyong
from app.extra import *
class Material(db.Model, BaseModel):
    __tablename__ = 'materials'
    title = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    price = db.Column(db.Integer)
    remark = db.Column(db.String)
    region_id = db.Column(db.Integer, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), index=True)


