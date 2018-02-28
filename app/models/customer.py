# coding:utf-8
# File Name: customer.py
# Created Date: 2018-02-27 12:46:14
# Last modified: 2018-02-28 14:47:44
# Author: yeyong
from app.extra import *

class Customer(db.Model, BaseModel):
    __tablename__ = 'customers'
    name = db.Column(db.String, index=True, nullable=False)
    phone = db.Column(db.String, index=True, nullable=False)
    province  = db.Column(db.String)
    city  = db.Column(db.String)
    district = db.Column(db.String)
    address = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    customer_type = db.Column(db.Integer, default=0, index=True)
    remark = db.Column(db.String)
    server_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    colse = db.Column(db.Boolean, default=False, index=True)


    def __repr__(self):
        return "<Customer id: {}, name: {}, phone: {}>".format(self.id, self.name, self.phone)

    
      #生成客户
    @classmethod
    def generate_customer(cls, **kwargs):
        try:
            customer = cls.query.filter_by(phone=kwargs["phone"], account_id=kwargs["account_id"]).first()
            if customer is None:
                customer = Customer(**kwargs)
            else:
                customer.customer_type  = 1
            db.session.add(customer)
            db.session.flush()
            return True, customer
        except Exception as e:
            return False, "处理客户事件失败"


