# coding:utf-8
# File Name: category.py
# Created Date: 2018-02-27 11:55:15
# Last modified: 2018-03-19 17:09:52
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


    @staticmethod
    def check_title(mapper, connection, target):
        data = Category.query.filter_by(title=target.title, account_id=target.account_id).first()
        if data:
            raise ValueError("已经存在这个值了")


    @staticmethod
    def validate_column(target, value, oldvalue, initiator):
        cated = Category.query.filter_by(title=value, account_id=target.account_id).first()
        if cated:
            raise ValueError("已经存在{}".format(value))
        

db.event.listen(Category, "before_insert", Category.check_title)
db.event.listen(Category.title, "set", Category.validate_column)
