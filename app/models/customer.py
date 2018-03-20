# coding:utf-8
# File Name: customer.py
# Created Date: 2018-02-27 12:46:14
# Last modified: 2018-03-20 17:02:15
# Author: yeyong
from app.extra import *
from app.models.communicate import Communicate
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
    server = db.relationship("User", foreign_keys=[server_id])


    def __repr__(self):
        return "<Customer id: {}, name: {}, phone: {}>".format(self.id, self.name, self.phone)

    
    ## 生成客户
    @classmethod
    def generate_customer(cls, **kwargs):
        try:
            customer = cls.query.filter_by(phone=kwargs["phone"], account_id=kwargs["account_id"]).first()
            if not customer:
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

    def delete_customer(self):
        Customer.query.filter_by(id=id).update({'close': True})


    def as_json(self):
        kwargs = dict(
                communicates=self.communicate_info(),
                server=self.server_info()
                )
        return self.to_json(**kwargs)



    ## 搜索客户
    @classmethod 
    def searach_customers(cls, key=None):
        results = cls.query.filter(or_(cls.name.like("%{}%".format(key)), cls.phone.like("%{}%".format(key))))
        return results

    
    @classmethod
    def filter_customer(cls, user=None, **kwargs):
        start = kwargs.get("start_time", None)
        end = kwargs.get("end_time", None)
        page = kwargs.get("page", 1)
        args = [getattr(cls, k) == v for k, v in kwargs.items() if v and hasattr(cls, k)]
        if start or end:
            args.extend(cls.parser_time(start, end))
        if not user.is_admin:
            u = [cls.customer_type == 0, cls.server_id == user.id]
            p = [cls.customer_type != 0]
            results = cls.query.filter(or_(*p, *u)).filter(and_(*args))
        else:
           results = cls.query.filter_by(colse=False,account_id=user.account_id).filter(and_(*args))
        temp = results.paginate(int(page), per_page=25, error_out=False)
        page = cls.res_page(temp)
        return temp.items, page 

    @classmethod
    def create_customer(self, **kwargs):
        try:
            args = set(Customer.__table__.columns.keys())
            kwargs = {k: v for k, v in kwargs.items() if v and k in args}
            cust = cls(**kwargs)
            db.session.add(cust)
            db.session.commit()
            return True, cust
        except Exception as e:
            msg = "添加客户失败"
            app.logger.warn("{}{}".format(msg, e))
            db.session.rollback()
            return False, msg

    def create_commoncation(self, **kwargs):
        try:
            kwargs.update(customer_id=self.id)
            comm = Communicate(**kwargs)
            db.session.add(comm)
            db.session.commit()
            return True, comm
        except Exception as e:
            msg = "添加交流记录失败"
            app.logger.warn("{}{}".format(msg, e))
            db.session.rollback()
            return False, msg















