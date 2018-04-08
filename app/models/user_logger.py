# coding:utf-8
# File Name: user_logger.py
# Created Date: 2018-02-27 14:57:20
# Last modified: 2018-04-08 13:57:09
# Author: yeyong
from app.extra import *
from app.ext import app
class UserLogger(db.Model, BaseModel):
    __tablename__  = 'user_loggers'
    event = db.Column(db.String)
    user_name = db.Column(db.String)
    text = db.Column(db.Text)
    body = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), index=True)
    klass = db.Column(db.String)
    klass_no = db.Column(db.String)



    @classmethod
    def create_logger(cls, **kwargs):
        try:
            valid = set(cls.__table__.columns.keys())
            kwargs = {k: v for k, v in kwargs.items() if v and k in valid}
            ul = cls(**kwargs)
            db.session.add(ul)
            db.session.commit()
            return True, ul
        except Exception as e:
            db.session.rollback()
            app.logger.warn("无效的保存： {}".format(e))
            return False, e
        
