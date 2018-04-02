# coding:utf-8
# File Name: category.py
# Created Date: 2018-02-27 11:55:15
# Last modified: 2018-03-30 10:03:18
# Author: yeyong
from app.extra import *
from app.models.extends.title_validate import TitleValidate

class Category(db.Model, BaseModel, TitleValidate):
    __tablename__ = 'categories'
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    remark= db.Column(db.String)
    title = db.Column(db.String)

    def __repr__(self):
        return "<Category id: {}, title: {}>".format(self.id, self.title)



db.event.listen(Category, "before_insert", Category.check_title)
db.event.listen(Category.title, "set", Category.validate_column)
