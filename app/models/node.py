# coding:utf-8
# File Name: node.py
# Created Date: 2018-02-27 13:34:51
# Last modified: 2018-02-28 14:45:54
# Author: yeyong
from app.extra import *
class Node(db.Model, BaseModel):
    __tablename__ = 'nodes'
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), index=True, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    remark = db.Column(db.String)
    node_type = db.Column(db.Integer, default=0)
    account_id = db.Column(db.Integer, nullable=False, index=True)

    def __repr__(self):
        return "<Node id: {}, order_id: {}, remark: {}, user_name: {}>".format(self.id, self.order_id, self.remark, self.user_name)
