# coding:utf-8
# File Name: role_permission.py
# Created Date: 2018-02-27 15:06:41
# Last modified: 2018-02-27 16:25:20
# Author: yeyong
from app.extra import db, datetime
role_permissions = db.Table("role_permissons", 
            db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), index=True),
            db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), index=True),
            db.Column("created_at", db.DateTime, default=datetime.utcnow),
            db.Column("updated_at", db.DateTime, default=datetime.utcnow)
        )
