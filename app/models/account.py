# coding:utf-8
# File Name: account.py
# Created Date: 2018-02-27 10:43:43
# Last modified: 2018-03-14 13:28:01
# Author: yeyong
from app.extra import *
from .user_account import user_accounts
from app.models.role import Role

class Account(db.Model, BaseModel):
    __tablename__ = "accounts"
    title = db.Column(db.String, nullable=False, index=True, unique=True)
    manager_id = db.Column(db.Integer, index=True)
    address = db.Column(db.String)
    nickname = db.Column(db.String)
    serial_no = db.Column(db.String, index=True)
    token = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, index=True, unique=True)
    code = db.Column(db.String, index=True)
    image = db.Column(db.String)
    users = db.relationship("User", secondary=user_accounts, lazy="dynamic", backref=db.backref("accounts", lazy="dynamic"))
    roles = db.relationship("Role", backref="account", lazy="dynamic")
    permissions = db.relationship("Permission", backref="account", lazy="dynamic")
    orders = db.relationship("Order", backref="account", lazy="dynamic")
    categories = db.relationship("Category", backref="account", lazy="dynamic")
    products = db.relationship("Product", backref="account", lazy="dynamic")
    communicates = db.relationship("Communicate", backref="account", lazy="dynamic")
    companies = db.relationship("Company", backref="company", lazy="dynamic")
    customers = db.relationship("Customer", backref="account", lazy="dynamic")
    



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


    ## 添加用户, 分配角色, 设置价格
    def add_user_and_allcate_roles(self, **kwargs):
        from app.models.user import User
        try:
            phone = kwargs.get("phone", None)
            roles = kwargs.get("roles", [])
            raty_price = kwargs.get("raty_price", 0)
            user = User.query.filter_by(phone=phone).first()
            if not user:
                return False, "该手机号的用户没有找到"
            user.raty_price = raty_price
            r = Role.query.filter(Role.id.in_(tuple(roles)), Role.account_id==self.id)
            if not r.first():
                return False, "无效的角色"
            ok, msg = self.add_user_to_account(user)
            if not ok:
                return False, msg
            roles = [role for role in r if not role in user.roles]
            user.roles.extend(roles)
            db.session.add(user)
            db.session.commit()
            return True, self
        except Exception as e:
            app.logger.warn("分配角色失败: {}".format(e))
            db.session.rollback()
            return False, "分配角色失败"
        



    ##将用户添加进公司
    def add_user_to_account(self, user=None):
        try:
            u = user in self.users
            if u:
                return False, "该用户已经添加过了"
            self.users.append(user)
            return True, user
        except Exception as e:
            app.logger.warn("加入失败: {}".format(e))
            return False, "加入失败"

    def searach_user_from_account(self, **kwargs):
        from app.models.user import User
        page = kwargs.get("page", 1)
        role = kwargs.get("role", None)
        args = dict(
                name = kwargs.get("name", None),
                phone = kwargs.get("phone", None),
                account_id = self.id
                )
        args = [getattr(User, k) == v for k, v in args.items() if v and hasattr(User, k)]
        if role:
            results = User.query.filter(User.roles.any(id=role, account_id=self.id)).filter(and_(*args)).paginate(int(page), per_page=25, error_out=False)
        else:
            results  = User.query.filter(and_(*args))

    
    ##检查公司名字和品牌名字
    @staticmethod
    def validate_column(mapper, connection, target):
        if not target.title:
            raise ValueError("公司名称不能为空")
        if not target.nickname:
            raise ValueError("品牌名称必填")
        a1 = Account.query.filter_by(title=target.title).first()
        a2 = Account.query.filter_by(nickname=target.nickname).first()
        if a1 or a2:
            raise ValueError("品牌及公司名称被使用了")

    def create_roles(self):
        rs = {"技工", "司机", "销售", "审核"}
        for r in rs:
            role  = Role(title=r, account_id=self.id)
            db.session.add(role)
            db.session.commit()

    def create_region(self):
        ts = {"电商", "门户网站", "门店", "家装公司", "设计师", "经销商"}
        for t in ts:
            re = Region(title=t, account_id=self.id)
            db.session.add(re)
            db.session.commit()

db.event.listen(Account, "before_insert", Account.validate_column)













