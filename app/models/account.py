# coding:utf-8
# File Name: account.py
# Created Date: 2018-02-27 10:43:43
# Last modified: 2018-02-27 11:55:06
# Author: yeyong
from app.extra import *
class Account(db.Model, Serialize):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, index=True, unique=True)
    manager_id = db.Column(db.Integer, index=True)
    address = db.Column(db.String)
    nickname = db.Column(db.String)
    serial_no = db.Column(db.String, index=True)
    token = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, index=True, unique=True)
    code = db.Column(db.String, index=True)
    image = db.Column(db.String, )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return "<Account id: {}, title: {}, serial_no: {}>".format(self.id, self.title, self.serial_no)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serial_no = self.generate_no()


    ## 创建公司
    @classmethod
    def create_account(cls, **kwargs):
        try:
            validate = {"title", "manager_id", "address", "nickname", "serial_no", "token", "phone", "image"}
            kwargs = {key: value for key, value in kwargs.items() if key in validate}
            account = cls(**kwargs)
            db.session.add(account)
            db.session.commit()
            return True, account
        except Exception as e:
            app.logger.warn("创建公司失败, {}".format(e))
            db.session.rollback()
            return False, "{}".format(e)

    
    def generate_no(self):
        import random
        import string
        if self.serial_no is None:
            while True:
                letter = list(string.ascii_uppercase) 
                digit = list(string.digits)
                result = random.choice(letter) + random.choice(letter + digit)
                temp = type(self).query.filter_by(serial_no=result).first()
                if temp is None:
                    return result
        else:
            return self.serial_no





