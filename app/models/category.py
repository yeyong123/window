# coding:utf-8
# File Name: category.py
# Created Date: 2018-02-27 11:55:15
# Last modified: 2018-03-02 13:16:35
# Author: yeyong
from app.extra import *

class Category(db.Model, BaseModel):
    __tablename__ = 'categories'
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    remark= db.Column(db.String)
    title = db.Column(db.String)
    products  = db.relationship('Product', backref="category", lazy="dynamic")

    def __repr__(self):
        return "<Category id: {}, title: {}>".format(self.id, self.title)

