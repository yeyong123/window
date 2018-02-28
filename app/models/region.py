# coding:utf-8
# File Name: region.py
# Created Date: 2018-02-27 14:51:15
# Last modified: 2018-02-28 14:46:32
# Author: yeyong
from app.extra import *
class Region(db.Model, BaseModel):
    __tablename__  = 'regions'
    title = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    remark = db.Column(db.String)

