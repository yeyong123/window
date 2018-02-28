# coding:utf-8
# File Name: setting.py
# Created Date: 2018-02-27 14:54:17
# Last modified: 2018-02-28 14:48:11
# Author: yeyong
from app.extra import *
class Setting(db.Model, BaseModel):
    __tablename__ = 'settings'
    title = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=False, nullable=False)
    key = db.Column(db.String)
    value = db.Column(db.String)
    classable = db.Column(db.String)

