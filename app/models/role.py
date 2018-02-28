# coding:utf-8
# File Name: role.py
# Created Date: 2018-02-27 14:52:55
# Last modified: 2018-02-28 15:12:22
# Author: yeyong
from app.extra import *
from .user_role import user_roles

class Role(db.Model, BaseModel):
    __tablename__ = 'roles'
    title = db.Column(db.String, index=True)
    level = db.Column(db.Integer, default=0)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    users = db.relationship("User", secondary=user_roles, lazy="subquery", backref=db.backref("roles", lazy="dynamic"))




