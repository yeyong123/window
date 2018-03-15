# coding:utf-8
# File Name: raty_price.py
# Created Date: 2018-03-15 13:50:55
# Last modified: 2018-03-15 14:12:02
# Author: yeyong
from app.extra import *
class RatyPrice(db.Model, BaseModel):
    __tablename__ = 'raty_prices'
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    raty = db.Column(db.Float, default="0.00")
    raty_type = db.Column(db.String, default="price")
    level = db.Column(db.Integer, default=0, index=True)
    

    def __repr__(self):
        return "<RatyPrice id: {}, title: raty: {}, user_id: {}>".format(self.id, self.raty, self.user_id)
