# coding:utf-8
# File Name: order_detail.py
# Created Date: 2018-02-27 13:47:32
# Last modified: 2018-03-01 11:31:48
# Author: yeyong
from app.extra import *
class OrderDetail(db.Model, BaseModel):
    __tablename__ = 'order_details'
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), index=True, nullable=False)
    account_id = db.Column(db.Integer, nullable=False, index=True)
    width = db.Column(db.String)
    height = db.Column(db.String)
    cube = db.Column(db.String)
    weight = db.Column(db.String)
    cache_size = db.Column(db.String)
    lift = db.Column(db.Boolean, default=False)
    stairs = db.Column(db.Boolean, default=False)
    lift_size = db.Column(db.String)
    stairs_size = db.Column(db.String)
    center = db.Column(db.Boolean, default=False)
    floor = db.Column(db.String)

