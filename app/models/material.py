# coding:utf-8
# File Name: material.py
# Created Date: 2018-02-27 12:57:39
# Last modified: 2018-03-23 14:15:41
# Author: yeyong
from app.extra import *
from app.models.extends.title_validate import TitleValidate
class Material(db.Model, BaseModel, TitleValidate):
    __tablename__ = 'materials'
    title = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True, nullable=False)
    price = db.Column(db.Integer)
    remark = db.Column(db.String)
    region_id = db.Column(db.Integer, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), index=True)


    def __repr__(self):
        return "<Material id: {}, title: {}, price: {}>".format(self.id, self.title, self.price)


db.event.listen(Material.title, "set", Material.validate_column)
db.event.listen(Material, "before_insert", Material.check_title)


