# coding:utf-8
# File Name: communicate.py
# Created Date: 2018-02-27 11:57:35
# Last modified: 2018-02-28 14:34:58
# Author: yeyong
from app.extra import *
class Communicate(BaseModel):
    __tablename__ = 'communicates'
    
    remark = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)


