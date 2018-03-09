# coding:utf-8
# File Name: node.py
# Created Date: 2018-02-27 13:34:51
# Last modified: 2018-03-07 11:10:42
# Author: yeyong
from app.extra import *
import app.models.extends.validator as Validator
class Node(db.Model, BaseModel):
    __tablename__ = 'nodes'

    
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), index=True, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    remark = db.Column(db.String)
    node_type = db.Column(db.Integer, default=0)
    account_id = db.Column(db.Integer, nullable=False, index=True)

    _remark = Validator.NonBlank("_remark")
    _remark = Validator.Presented("_remark")
    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)
        self.remark = kwargs.get("remark", kwargs.get("_remark"))



    def __repr__(self):
        return "<Node id: {}, order_id: {}, remark: {}, user_name: {}>".format(self.id, self.order_id, self.remark, self.user_name)



        

