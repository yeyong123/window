# coding:utf-8
# File Name: node.py
# Created Date: 2018-02-27 13:34:51
# Last modified: 2018-02-27 15:23:49
# Author: yeyong
from app.extra import *
class Node(db.Model, Timestamp, Serialize):
    __tablename__ = 'nodes'
    order_id = db.Column(db.Integer, db.ForeignKey("nodes.id"), index=True, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    remark = db.Column(db.String)
    node_type = db.Column(db.Integer, default=0)
    account_id = db.Column(db.Integer, nullable=False, index=True)

