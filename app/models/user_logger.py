# coding:utf-8
# File Name: user_logger.py
# Created Date: 2018-02-27 14:57:20
# Last modified: 2018-02-27 15:23:41
# Author: yeyong
from app.extra import *
class UserLogger(db.Model, Timestamp, Serialize):
    __tablename__  = 'user_loggers'
    event = db.Column(db.String)
    user_name = db.Column(db.String)
    text = db.Column(db.Text)
    body = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True)
    klass = db.Column(db.String)
    klass_no = db.Column(db.String)

