# coding:utf-8
# File Name: user.py
# Created Date: 2018-02-26 11:06:00
# Last modified: 2018-02-28 15:16:36
# Author: yeyong
from app.extra import *
import hashlib
from flask_bcrypt import Bcrypt
from app.models.send_code import SendCode
import re
bcrtpt = Bcrypt(app)
class User(db.Model, BaseModel):
    __tablename__ = 'users'
    name = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(128), nullable=False, index=True, unique=True)
    password_digest = db.Column(db.String(128))
    image  = db.Column(db.String)
    amount = db.Column(db.Integer, default=0)
    raty_price = db.Column(db.Integer, default=0)
    role = db.Column(db.Integer, default=0)
    orders_count = db.Column(db.Integer, default=0)
    geohash = db.Column(db.String, index=True)
    token = db.Column(db.String)
    text = db.Column(db.String)
    code = db.Column(db.String)
    pwd = db.Column(db.String)
    account_id = db.Column(db.Integer, index=True)
    address = db.Column(db.String)
    province = db.Column(db.String)
    city = db.Column(db.String)
    district = db.Column(db.String)

    driver_orders = db.relationship("Order", foreign_keys="Order.driver_id", lazy="dynamic")
    server_orders = db.relationship("Order", foreign_keys="Order.server_id", lazy="dynamic")
    install_orders = db.relationship("Order", foreign_keys="Order.install_id", lazy="dynamic")
    orders = db.relationship("Order", foreign_keys="Order.user_id", lazy="dynamic")



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = self.serialize_token()


    def serialize_token(self):
        return hashlib.sha1(app.config["SECRET_KEY"].encode("utf-8")).hexdigest()

    def reset_token(self):
        self.token = self.serialize_token()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<User id: {}, name: {}, phone: {}>".format(self.id, self.name, self.phone)

    @property
    def password(self):
        raise AttributeError("密码解析失败")

    @password.setter
    def password(self, password):
        self.password_digest = bcrtpt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrtpt.check_password_hash(self.password_digest, password)


    ##生成 Token
    @property
    def generate_token(self):
        serial = Serializer(app.config["SECRET_KEY"], expires_in=3600*24*365*20)
        payload = serial.dumps(dict(user_id=self.id, password=self.password_digest, token=self.token))
        return payload.decode("utf-8")


    @property
    def as_json(self):
        json = self.to_json()
        return json


    ## 用户注册
    @classmethod
    def user_create(cls, **kwargs):
        try:
            code = kwargs.get("code", None)
            if code is None:
                return False, "验证码不能为空"
            validate = {"password", "phone", "name", "image"}
            args = {key: value for key, value in kwargs.items() if key in validate and hasattr(cls, key)}
            generate_code = SendCode()
            if code != generate_code():
                return False, "验证码无效"
            user = cls(**agrs)
            db.session.add(user)
            db.session.commit()
            return True, user
        except Exception as e:
            app.logger.warn("用户注册失败: {}".format(e))
            db.session.rollback()
            return False, "注册失败: {}".format(e)


    def phone_format(self, phone):
        match = re.compile('^0\d{2,3}\d{7,8}$|^1[35678]\d{9}$|^147\d{8}')
        if match.match(phone):
            return True
        else:
            return False


    @staticmethod
    def validate_column(mapper, connection, target):
        if not target.phone_format(target.phone):
            raise ValueError("手机号无效")
        user = User.query.filter_by(phone=target.phone).first()
        if user:
            raise ValueError("手机号被使用")


    #简化用户的角色
    @property
    def is_admin(self):
        return self.role == 5

    def r(self, key=None):
        t = self.roles.filter_by(title=key).first()
        return True if t else False

    @property
    def is_audit(self):
        return self.r(key="审核")

    @property
    def is_driver(self):
        return self.r("司机")

    @property
    def is_server(self):
        return self.r("技工")


db.event.listen(User, "before_insert", User.validate_column)







