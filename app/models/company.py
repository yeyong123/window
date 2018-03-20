# coding:utf-8
# File Name: company.py
# Created Date: 2018-02-27 12:41:54
# Last modified: 2018-03-20 09:24:08
# Author: yeyong
from app.extra import *
from app.models.extends.title_validate import TitleValidate
class Company(db.Model, BaseModel, TitleValidate):
    __tablename__ = 'companies'
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    title = db.Column(db.String)
    logo = db.Column(db.String)
    remark = db.Column(db.String)
    orders = db.relationship("Order", backref="company", lazy="dynamic")
    materials = db.relationship("Material", backref="company", lazy="dynamic")

    def __repr__(self):
        return "<Company id: {}, title: {}>".format(self.id, self.title)



db.event.listen(Company.title, "set", Company.validate_column)
db.event.listen(Company, "before_insert", Company.check_title)

       

    
