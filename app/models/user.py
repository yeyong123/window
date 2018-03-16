# coding:utf-8
# File Name: user.py
# Created Date: 2018-02-26 11:06:00
# Last modified: 2018-03-16 13:31:38
# Author: yeyong
from app.extra import *
import hashlib
from flask_bcrypt import Bcrypt
from app.models.send_code import SendCode
from app.models.account import Account
from app.models.role import Role
from app.models.raty_price import RatyPrice
import re
bcrtpt = Bcrypt(app)
class User(db.Model, BaseModel):
    __tablename__ = 'users'
    name = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(128), nullable=False, index=True, unique=True)
    password_digest = db.Column(db.String(128))
    image  = db.Column(db.String)
    amount = db.Column(db.Integer, default=0)
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
    customers = db.relationship("Customer", foreign_keys="Customer.server_id", lazy="dynamic")
    raty_prices = db.relationship("RatyPrice", backref="user", lazy="dynamic")


    def __init__(self, **kwargs):
        self._account_id = None
        super().__init__(**kwargs)
        self.token = self.serialize_token()

    @classmethod
    def set_account(cls, value):
        cls._account_id = value

    @classmethod
    def get_account_value(cls):
        if hasattr(cls, "_account_id"):
            return cls._account_id
        return None

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

    @classmethod
    def conver_token(cls, token):
        temp = Serializer(app.config["SECRET_KEY"])
        try:
            result = temp.loads(token)
            item = cls.query.filter_by(id=result.get("user_id"), token=result.get("token"), password_digest=result.get("password")).first()
            if not item:
                return False
            return item
        except:
            return False


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


    #简化用户的角色
    @property
    def is_admin(self):
        return self.role == 5

    @property
    def all_roles(self):
        acc = self._account_id if User.get_account_value() else self.account_id
        results = self.roles.filter_by(account_id = acc)
        temp = [r.title for r in results]
        return set(map(self.roles_hash, temp))

    @property
    def is_audit(self):
        return 4 in self.all_roles
        

    @property
    def is_driver(self):
        return 2 in self.all_roles


    @property
    def is_server(self):
        return 3 in self.all_roles

    @property
    def is_sale(self):
        return 1 in self.all_roles


    ## 用户切换的设置更新用户的 account_id
    def set_account_id(self, account_id=None):
        type(self).set_account(account_id)
        User.query.filter_by(id=self.id).update({"account_id": account_id})

    ##找到不同类型的用户
    @classmethod
    def searach_role_users(cls, account_id=None, key="销售", page=1):
        r = cls.query.filter(cls.roles.any(title=key)).paginate(int(page), per_page=25, error_out=False)
        page = cls.res_page(r)
        return r.items, page

    @property
    def current_account(self):
        return Account.query.filter_by(id=type(self)._account_id).first()
    
    ## 企业信息
    def account_info(self):
        a = Account.query.filter_by(id=self.account_id).first()
        if not a:
            return {}
        return a.to_json()

    def owner_roles(self):
        if self.roles.first():
            return [r.to_json() for r in self.roles.all()]
        return []

    def as_json(self):
        args = dict(
                account= self.account_info(),
                all_roles = list(self.all_roles),
                raty_price=self.raty_price()
                )
        return self.to_json(**args)


    ## 分配角色
    def allocation_role(self, role_id=None):
        try:
            if self.is_admin:
                return False, "该用户禁止修改角色"
            self.roles = [] # 先清空原有的角色
            temps = Role.query.filter(Role.id.in_(tuple(role_id)), Role.account_id==self.account_id)
            if not temps.first():
                return False, "无效的角色选择"
            for element in temps:
                has_role = self.roles.filter_by(id=element.id).first()
                if has_role:
                    continue
                value = self.roles_hash(key=element.title)
                if not value:
                    continue
                self.role = int(value)
                self.roles.append(element)
            db.session.add(self)
            db.session.commit()
            return True, self
        except Exception as e:
            app.logger.warn("分配角色失败:{}".format(e))
            db.session.rollback()
            return False, "分配角色失败"



    def roles_hash(self, key=None, resver=False):
        args = {
                "普通成员": 0,
                "销售": 1,
                "司机": 2,
                "技工": 3,
                "审核" : 4,
                "管理员" : 5
                }
        if resver:
            args = {v: k for k, v in args.items()}
        return args.get(key, None)


    ## 加入公司
    def add_account(self, account_id=None):
        """加入公司"""
        a = Account.query.filter_by(id=account_id).first()
        joined = self.accounts.filter_by(id=a.id).first()
        if not a:
            return False, "该公司设置了隐藏"
        if joined:
            return False, "已经加入了该公司"
        self.accounts.append(a)
        return True, self

    def accounts_list(self, page=1):
        """列出我加入的公司"""
        a = self.accounts.paginate(int(page), per_page=25, error_out=False)
        page = Account.res_page(a)
        return a.items, page

    def toggle_and_remove_account(self, account_id=None, kind="remove"):
        """
        退出我加入的公司
        1: 检查公司是否在不在
        2: 检查我有没有加入这个公司
        3: 退出公司
        """
        acc = Account.query.filter_by(id=account_id).first()
        if not acc:
            return False, "该公司设置了隐藏"
        owner_acc = self.accounts.filter_by(id=account_id).first()
        if not owner_acc:
            return False, "您还未加入这个公司"
        if kind == "toggle":
            self.set_account_id(account_id)
        else:
            self.accounts.remove(owner_acc)
        return True, self

    ##获取我在这个公司的提成
    def raty_price(self, account_id=None):
        acc = account_id if account_id else type(self).get_account_value()
        raty = self.raty_prices.filter_by(account_id=acc).first()
        if not raty: return 0.0
        return float(raty.raty)


    ## 设置该在这个公司的提成
    def set_current_account_raty(self, raty=0):
        try:
            for r in self.raty_prices.filter_by(account_id=self.account_id):
                db.session.delete(r)
            raty = RatyPrice(account_id=self.account_id, user_id=self.id, raty=raty)
            db.session.add(raty)
            db.session.commit()
            return True, raty
        except Exception as e:
            app.logger.warn("设置提成失败: {}".format(e))
            db.session.rollback()
            return False, "设置提成失败"




    @staticmethod
    def validate_column(mapper, connection, target):
        if not target.phone_format(target.phone):
            raise ValueError("手机号无效")
        user = User.query.filter_by(phone=target.phone).first()
        if user:
            raise ValueError("手机号被使用")




db.event.listen(User, "before_insert", User.validate_column)







