# coding:utf-8
# File Name: role.py
# Created Date: 2018-02-27 14:52:55
# Last modified: 2018-03-02 09:48:54
# Author: yeyong
from app.extra import *
from .user_role import user_roles

class Role(db.Model, BaseModel):
    __tablename__ = 'roles'
    title = db.Column(db.String, index=True)
    level = db.Column(db.Integer, default=0)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    users = db.relationship("User", secondary=user_roles, lazy="subquery", backref=db.backref("roles", lazy="dynamic"))


    def __repr__(self):
        return "<Role id: {}, title: {}>".format(self.id, self.title)

    
    #权限的列表
    def permissions_info(self):
        if self.permissions.first():
            return [p.to_json() for p in self.permissions]
        else:
            return []

    def to_json(self):
        args = {"permissions_info": self.permissions_info()}
        return super().to_json(**args)


    ##将用户添加进角色里面
    def allocation_user(self, user=None):
        try:
            if not user:
                return False, "用户不能为空"
            user = User.query.filter_by(id=user.id).first()
            if not user:
                return False, "无效的用户"
            role = self.users.filter_by(id=user.id).first()
            if role:
                return False, "该用户已经拥有这个角色"
            value = user.roles_hash(key=self.title)
            user.role = int(value)
            self.users.append(user)
            db.session.add(user)
            db.session.commit()
            return True, self
        except Exception as e:
            app.logger.warn("用户角色分配失败: {}".format(e))
            db.session.rollback()
            return False, "用户角色分配失败"





