# coding:utf-8
# File Name: timestamp.py
# Created Date: 2018-02-27 12:59:36
# Last modified: 2018-02-27 15:34:47
# Author: yeyong
from app.extra import db, datetime
class Timestamp:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



