# coding:utf-8
# File Name: communicate.py
# Created Date: 2018-02-27 11:57:35
# Last modified: 2018-03-05 10:12:34
# Author: yeyong
from app.extra import *
from app.models.user import User


class Communicate(db.Model, BaseModel):
    __tablename__ = 'communicates'

    remark = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), index=True)

    def __repr__(self):
        return "<Communicate id: {}, customer_id: {}, user_id: {}>".format(self.id, self.customer_id, self.user_id)


    def to_json(self):
        args = {
                "user_info": self.user_info()
                }
        return super().to_json(**args)

    
    def user_info(self):
        user = User.query.filter_by(id=self.user_id).first()
        if not user: 
            return {}
        return user.to_json()



