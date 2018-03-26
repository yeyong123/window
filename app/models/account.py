# coding:utf-8
# File Name: account.py
# Created Date: 2018-02-27 10:43:43
# Last modified: 2018-03-26 16:50:29
# Author: yeyong
from app.extra import *
from .user_account import user_accounts
from app.models.role import Role
from app.models.permission import Permission
from app.models.region import Region
from app.models.company import Company
from app.models.category import Category
from app.models.material import Material

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
    lon=db.Column(db.String)
    lat= db.Column(db.String)
    location = db.Column(db.String, index=True)
    users = db.relationship("User", secondary=user_accounts, lazy="dynamic", backref=db.backref("accounts", lazy="dynamic"))
    roles = db.relationship("Role", backref="account", lazy="dynamic")
    permissions = db.relationship("Permission", backref="account", lazy="dynamic")
    orders = db.relationship("Order", backref="account", lazy="dynamic")
    categories = db.relationship("Category", backref="account", lazy="dynamic")
    products = db.relationship("Product", backref="account", lazy="dynamic")
    communicates = db.relationship("Communicate", backref="account", lazy="dynamic")
    companies = db.relationship("Company", backref="company", lazy="dynamic")
    customers = db.relationship("Customer", backref="account", lazy="dynamic")
    raty_prices = db.relationship("RatyPrice", backref="account", lazy="dynamic")
    materials = db.relationship("Material", backref="account", lazy="dynamic")
    regions = db.relationship("Region", backref="account", lazy="dynamic")
    



    def __repr__(self):
        return "<Account id: {}, title: {}, serial_no: {}>".format(self.id, self.title, self.serial_no)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serial_no = self.generate_no()


    ## 创建公司
    @classmethod
    def create_account(cls, user=None, **kwargs):
        """
        用户创建企业
        简称用户的输入的值
        如果企业名称, 手机号/电话, 简称已存在就返回错误信息
        每次创建就将这个的当前企业修改新的企业,并设置为管理员
        每次创建新的公司就添加新的渠道, 新的角色
        """
        try:
            validate = {"title", "manager_id", "address", "nickname", "serial_no", "token", "phone", "image"}
            kwargs = {key: value for key, value in kwargs.items() if key in validate}
            kwargs.update(manager_id=user.id, phone= kwargs.get("phone") if kwargs.get("phone", None) else user.phone, token=user.id, nickname=kwargs.get("title"))
            title = kwargs.get("title")
            temp = cls.query.filter_by(title=title).first()
            if temp:
                return False, "这个企业的名字, 手机号, 简称已被使用"
            account = cls(**kwargs)
            db.session.add(account)
            db.session.commit()
            user.account_id = account.id
            user.role = 5
            user.accounts.append(account)
            db.session.add(user)
            db.session.commit()
            account.create_roles()
            account.create_region()
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
        """
        为用户分配角色, 用户查找使用手机号码
        需要参数: 
            phone=手机
            roles: 角色列表
            raty_price: 设置提成比率
        如果用户已添加了就不需要操作
        用户是管理员也不操作
        检查用户角色
        """
        from app.models.user import User
        try:
            phone = kwargs.get("phone", None)
            roles = kwargs.get("roles", [])
            raty_price = kwargs.get("raty_price",  None)
            user = User.query.filter_by(phone=phone).first()
            if not user:
                return False, "该手机号的用户没有找到"
            if user.is_admin:
                return False, "禁止修改管理员的角色"
            r = Role.query.filter(Role.id.in_(tuple(roles)), Role.account_id==self.id)
            if not r.first():
                return False, "无效的角色"
            #将这个用户添加到公司中
            ok, msg = self.add_user_to_account(user)
            if not ok:
                return False, msg
            roles = [role for role in r if not role in user.roles]
            if not user.account_id:
                user.account_id = self.id
            user.roles.extend(roles) #将这个用户添加角色
            if raty_price:
                raty = RatyPrice(user_id=user.id, account_id=user.account_id, raty=raty_price)
                db.session.add(raty)
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
            if user in self.users:
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
        page = type(self).res_page(results)

        return results.items, page


    ## 获取这个账户下的角色的所有人员
    def searach_role(self, title=None, page=1):
        from .user import User
        """
        从账户的角色获取用户
        """
        results = User.query.filter(User.roles.any(title=title, account_id=self.id)).paginate(int(page), per_page=25, error_out=False)
        page = type(self).res_page(results)
        return results.items, page

    
 
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


    #获取有关企业的品牌数据
    def fetch_data_from_account(self, key=None, page=1):
        """品牌, 渠道, 品牌, 材质"""
        results = getattr(self, key).paginate(int(page), per_page=25, error_out=False)
        page = type(self).res_page(results)
        items = results.items
        return items, page


    #模糊搜索用户
    def searach_account_users(self, key=None, page=1):
        from .user import User
        temps = self.users.filter(or_(User.name.like("%{}%".format(key)), User.phone.like("%{}%".format(key)))).paginate(int(page), per_page=25, error_out=False)
        results = temps.items
        page = type(self).res_page(temps)
        return results, page


    ## 创建物料品牌的基本参数
    def base_create_data(self, key=None, **kwargs):
        """创建"""
        try:
            klass = self.find_relation(key)
            if not klass:
                return False, "无效的参数"
            kwargs.update(account_id=self.id)
            temp = klass(**kwargs)
            db.session.add(temp)
            db.session.commit()
            return True, temp
        except Exception as e:
            app.logger.warn("添加物料失败{}".format(e))
            db.session.rollback()
            return False, "创建物料失败"

    def delete_relation(self, key=None, id=None):
        """删除有关物料"""
        klass = self.find_relation(key)
        if not klass:
            return False, "无效的 Key"
        ok, result = self.find_only_date(klass=klass, id=id)
        if not ok:
            return False, result
        return result

    def update_relation(self, key=None, id=None, **kwargs):
        """修改物料"""
        klass = self.find_relation(key)
        if not klass:
            return False, "无效的 Key"
        ok, result = self.find_only_date(klass=klass, id=id)
        if not ok:
            return False, result
        ok, temp = result.update(**kwargs)
        if not ok:
            return False, temp
        return True, temp

    ##去除重复的代码
    def find_only_date(self, klass=None, id=None):
        """找出有关物料的单个数据"""
        result = klass.query.filter_by(id=id, account_id=self.id).first()
        if not result:
            return False, "无效的 ID"
        return True, result

    ## 跟这个品牌有关的物料
    def find_relation(self, key):
        """序列化跟这个账户有关的物料, 品类, 角色, 材质, 品牌, 渠道, 权限"""
        args = dict(category=Category,role=Role, material=Material, product=Product,company=Company, region=Region, permissions=Permission)
        return args.get(key, None)



    def delete_user(self, user_id):
        user = self.users.filter_by(id=user_id).first()
        if not user:
            return False, "该用户还没有加入该企业"
        if user.is_admin or user_id == self.manager_id:
            return False, "管理员不能退"
        self.users.remove(user)
        return True, self



    def parse_location(self, target=None, key=None):
        """解析地址到经纬度"""
        import requests, geohash
        from app.ext import app
        args = dict(
                key=app.config.get("AMAP_KEY"),
                address= target if target else self.address
                )
        res = requests.get(app.config.get("AMAP_URL"), params=args)
        result = res.json()
        status, info, codes = result.get("status", None), result.get("info", None), result.get("geocodes", None)
        if status == "1" and info == "OK" and len(codes) > 0:
            lon, lat = codes[0]["location"].split(",")
            loc = geohash.encode(float(lat), float(lon))
            _id = key if key else self.id
            Account.query.filter_by(id=_id).update(dict(lon=lon, lat=lat, location=loc))
        else:
            return info

    @classmethod
    def search_store(cls, key=None, kind="near", page=1):
        """
        搜索
        kind:
        near: 附近的门店
        name: 门店名称已经别名, 或者地址
        """
        if kind == "near":
            temps= cls.query.filter(cls.location.like("{}%".format(key))).paginate(int(page), per_page=25, error_out=False)
        else:
            args = [getattr(cls, val).like("%{}%".format(key)) for val in {"title", "nickname", "address"}]
            temps = cls.query.filter(or_(*args)).paginate(int(page), per_page=25, error_out=False)
        page = cls.res_page(temps)
        return temps.items, page




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

    @staticmethod
    def handle_address(mapper, connection, target):
        if target.address:
            target.parse_location(target=target.address, key=target.id)


    @staticmethod
    def set_address(target, value, oldvalue, initiator):
        target.parse_location(target=value, key=target.id)



db.event.listen(Account, "before_insert", Account.validate_column)
db.event.listen(Account, "after_insert", Account.handle_address)
db.event.listen(Account.address, "set", Account.set_address)













