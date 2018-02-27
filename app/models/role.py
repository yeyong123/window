# coding:utf-8
# File Name: role.py
# Created Date: 2018-02-27 14:52:55
# Last modified: 2018-02-27 15:46:24
# Author: yeyong
from app.extra import *
from .role_permission import role_permissions
from .user_role import user_roles

class Role(db.Model, Timestamp, Serialize):
    __tablename__ = 'roles'
    title = db.Column(db.String, index=True)
    level = db.Column(db.Integer, default=0)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    permissions = db.relationship("Permission", secondary=role_permissions, lazy="subquery", backref=db.backref("roles", lazy=True))
    users = db.relationship("User", secondary=user_roles, lazy="subquery", backref=db.backref("roles", lazy=True))




