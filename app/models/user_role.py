# coding:utf-8
# File Name: user_role.py
# Created Date: 2018-02-27 15:08:28
# Last modified: 2018-02-27 15:47:09
# Author: yeyong
from app.extra import db, datetime

user_roles = db.Table("user_roles", 
            db.Column("user_id", db.Integer, db.ForeignKey("users.id"), index=True),
            db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), index=True),
            db.Column("created_at", db.DateTime, default=datetime.utcnow),
            db.Column("updated_at", db.DateTime, default=datetime.utcnow)
        )
