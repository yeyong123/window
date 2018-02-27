# coding:utf-8
# File Name: user_accounts.py
# Created Date: 2018-02-27 15:01:05
# Last modified: 2018-02-27 15:21:08
# Author: yeyong
from app.extra import db, datetime

user_accounts = db.Table("user_accounts", 
            db.Column("user_id", db.Integer, db.ForeignKey("users.id"), index=True),
            db.Column("account_id", db.Integer, db.ForeignKey("accounts.id"), index=True),
            db.Column("created_at", db.DateTime, default=datetime.utcnow),
            db.Column("updated_at", db.DateTime, default=datetime.utcnow)
        )
