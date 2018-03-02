# coding:utf-8
# File Name: customer.py
# Created Date: 2018-02-27 12:46:14
# Last modified: 2018-03-02 15:11:11
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
    communicates = db.relationship("Communicate", backref="customer", lazy="dynamic")
    sever = db.relationship("User", foreign_keys=[server_id])


    def __repr__(self):
        return "<Customer id: {}, name: {}, phone: {}>".format(self.id, self.name, self.phone)

    
    ## 生成客户
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


    ## 对接的销售
    def server_info(self):
        if self.server:
            return self.server.to_json()
        else:
            return {}

    ## 交流记录
    def communicate_info(self):
        c = self.communicates
        if c.first():
            return [co.to_json() for co in c]
        else:
            return []

    ## 切换为正式客户
    def toggle_normal(self):
        Customer.query.filter_by(id=self.id).update({'customer_type': 1})


    ## 搜索客户
    @classmethod 
    def searach_customers(cls, key=None):
        results = cls.query.filter(or_(cls.name.like("%{}%".format(key)), cls.phone.like("%{}%".format(key))))
        return results












