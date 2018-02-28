# coding:utf-8
# File Name: permisson.py
# Created Date: 2018-02-27 14:33:27
# Last modified: 2018-02-28 14:45:48
# Author: yeyong
from app.extra import *
from .role_permission import role_permissions
class Permission(db.Model, BaseModel):
    __tablename__ = 'permissions'
    level = db.Column(db.Integer, default=0, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    title = db.Column(db.String)
    roles = db.relationship("Role", secondary=role_permissions, lazy="subquery", backref=db.backref("permissions", lazy=True))

