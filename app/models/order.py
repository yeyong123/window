# coding:utf-8
# File Name: order.py
# Created Date: 2018-02-27 13:52:39
# Last modified: 2018-02-28 15:44:22
# Author: yeyong
from app.extra import *
from app.models.customer import Customer
from app.models.account import Account
from app.models.node import Node
from app.models.picture import Picture

class Order(db.Model, BaseModel):
    __tablename__  = 'orders'
    user_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    server_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    install_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), index=True)
    customer_id = db.Column(db.Integer, index=True)
    factory_id = db.Column(db.Integer, index=True)
    intro_id = db.Column(db.Integer, index=True)
    product_id = db.Column(db.Integer, index=True, nullable=False)
    region_id = db.Column(db.Integer, index=True)
    sale_id = db.Column(db.Integer, index=True)
    category_id = db.Column(db.Integer)
    material_id = db.Column(db.Integer)
    title = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    province = db.Column(db.String)
    district = db.Column(db.String)
    kind  = db.Column(db.String)
    width = db.Column(db.Float, default=0.0)
    height = db.Column(db.Float, default=0.0)
    weight = db.Column(db.Float, default=0.0)
    cube = db.Column(db.Float, default=0.0)
    square = db.Column(db.Float, default=0.0)
    material = db.Column(db.String)
    remark = db.Column(db.String)
    serial_no = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    total_amount = db.Column(db.Integer, default=0)
    intro_amount = db.Column(db.Integer, default=0)
    raty_price = db.Column(db.Integer, default=0)
    region = db.Column(db.String)
    store = db.Column(db.String)
    customer_name = db.Column(db.String)
    customer_phone = db.Column(db.String)
    server_date = db.Column(db.Integer, default=0)
    handle_date = db.Column(db.Integer, default=0)
    install_date = db.Column(db.Integer, default=0)
    arrive_date = db.Column(db.Integer, default=0)
    express_no = db.Column(db.String)
    express_name = db.Column(db.String)
    geohash = db.Column(db.String, index=True)
    status = db.Column(db.Integer, default=0, index=True)
    factory_name = db.Column(db.String)
    factory_status = db.Column(db.String)
    level = db.Column(db.Integer, default=0, index=True)
    order_type = db.Column(db.Integer, default=0, index=True)
    hide = db.Column(db.Boolean, default=False, index=True)
    server_amount = db.Column(db.Integer, default=0)
    product_amount = db.Column(db.Integer, default=0)
    measure_amount = db.Column(db.Integer, default=0)
    install_amount = db.Column(db.Integer, default=0)
    ship_amount = db.Column(db.Integer, default=0)
    other_amount = db.Column(db.Integer, default=0)
    measure_confirm = db.Column(db.Boolean, default=False)
    factory_confirm = db.Column(db.Boolean, default=False)
    install_confirm = db.Column(db.Boolean, default=False)
    nodes = db.relationship("Node", backref="order", lazy="dynamic")

    ## 区分不同的用户
    server = db.relationship("User", foreign_keys=[server_id])
    driver = db.relationship("User", foreign_keys=[driver_id])
    installer = db.relationship("User", foreign_keys=[install_id])
    user = db.relationship("User", foreign_keys=[user_id])



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serial_no = self.generate_number()


    def __repr__(self):
        return "<Order id: {}, serial_no: {}, server_id: {}, user_id: {}, install_id: {}>".format(self.id, self.serial_no, self.server_id, self.user_id, self.install_id)

    #生成单号
    def generate_number(self):
        account = Account.query.filter_by(id=self.account_id).first()
        if account is None:
            raise AttributeError("账户无效")
        prefix = account.serial_no if account.serial_no is not None else "XX"
        basic = account.orders.count()
        temp  = 1
        while True:
            if temp > 99:
                raise AttributeError("创建失败订单用尽")
            t = basic + temp
            res = str(prefix) + str(t).zfill(9)
            if not type(self).query.filter_by(serial_no=res).first():
                return res


    #生成客户
    def generate_customer(self):
        return Customer.generate_customer(server_id=self.user_id,phone=self.customer_phone, name=self.customer_name,account_id=self.account_id, customer_type=1)

    #订单创建时处理新的客户以及转为正式客户
    @classmethod
    def create_order(cls, **kwargs):
        try:
            kwargs = {key: value for key, value in kwargs.items() if hasattr(cls, key)}
            o = cls(**kwargs)
            ok, c = o.generate_customer()
            if not ok:
                db.session.rollback()
                return False, c
            o.customer_id = c.id
            db.session.add(o)
            db.session.commit()
            return True, o
        except Exception as e:
            app.logger.warn("订单处理失: {}".format(e))
            db.session.rollback()
            return False, "创建订单失败"


    def increment(self):
        return self.owner_self.update({'status': self.status + 1})

    def decrement(self):
        return self.owner_self.update({'status': self.status - 1})

    def toggle_status(self, event="next"):
        if self.status <= 7 and self.status >= 0:
            if event == "prev" and self.status > 0:
                self.decrement()
                return self.status
            elif event == "next":
                self.increment()
                return self.status
            else:
                return self.status
        else:
            return self.status

    ##查找自己进行进一步处理
    @property
    def owner_self(self):
        return Order.query.filter_by(id=self.id)

    ##根据事件来处理
    #######################
    def record_event_to_node(self, **kwargs):
        try:
            event = kwargs["event"]
            user = kwargs["user"]
            content = kwargs["content"]
            self.swicth(event)
            node = Node(user_name=user.name, remark=content, account_id=user.account_id, order_id=self.id)
            db.session.add(node)
            db.session.commit()
            return True, self
        except Exception as e:
            app.logger.warn("事件记录失败: {}".format(e))
            db.session.rollback()
            return False, "事件记录失败"

    def create_event(self):
        return None

    def back_event(self):
        if self.status == 1:
            self.owner_self.update({'server_id': None})
        elif self.status == 4:
            self.owner_self.update({'driver_id': None})
        elif self.status == 5:
            self.owner_self.update({'install_id': None})
        return self.toggle_status("prev")

    def reset_event(self):
        if self.status == 1:
            self.owner_self.update({'server_date': 0})
        elif self.status == 4:
            self.owner_self.update({'arrive_date': 0})
        elif self.status == 5:
            self.owner_self.update({'install_date': 0})
        return None

    def cancel_event(self):
        return self.toggle_status("prev")

    def arrive_event(self):
        if self.status == 4:
            return self.default_event()

    def install_event(self):
        if self.status == 5:
            return self.toggle_status()

    def measure_event(self):
        if self.status == 1:
            return self.default_event()

    def default_event(self):
        return self.toggle_status()

    def swicth(self, key=None):
        values = dict(
                create=self.create_event,
                back=self.back_event,
                reset=self.reset_event,
                cancel=self.cancel_event,
                arrive=self.arrive_event,
                install_upload=self.install_event,
                measure_upload=self.measure_event
                )
        return values.get(key, self.default_event)()

    ####################

    ## 获取图片
    def pictures(self):
        return Picture.fetch(klass="order", klass_id=self.id)
    
    # 添加图片
    def insert_pictures(self, image, t=None):
        ok, p = Picture.create_image(pictureable_type="order", pictureable_id=self.id, image=image, image_type=t)
        if not ok:
            return False, "添加图片失败"
        return True, p


    #################
    ##################
    ## 根据用户的角色过滤订单
    @classmethod
    def filter_orders(cls, user=None, event=None, **kwargs):
        pass

    @classmethod
    def pending_orders(cls):
        return cls.query.filter_by(order_type=0)

    @classmethod
    def base_regular_order(cls):
        return cls.query.filter_by(order_type=1)

    @classmethod
    def owner_order(cls, user=None):
        if user.is_admin:
            return cls.base_regular_order()
        else:
            if user.is_audit:
                return cls.base_regular_order().filter(or_(
                    cls.status >= 2, 
                    cls.user_id == user.id, 
                    cls.server_id == user.id, 
                    cls.install_id == user.id,
                    cls.driver_id == user.id,
                    cls.intro_id == user.id
                    ))
            else:
                return cls.base_regular_order().filter(or_(
                    cls.user_id == user.id,
                    cls.server_id == user.id,
                    cls.install_id == user.id,
                    cls.driver_id == user.id,
                    cls.intro_id == user.id
                    ))
        
        
    
    @classmethod
    def assion_order(cls, sub=None):
        if sub is None:
          return  cls.base_regular_order().filter(or_(
               cls.server_id == None,
               cls.driver_id == None,
               cls.install_id == None
               ))
        if str(sub) == "1":
            return cls.base_regular_order().filter(cls.server_id == None, cls.status.in_((0, 1)))
        elif str(sub) == "2":
            return cls.base_regular_order().filter(cls.driver_id == None, cls.status == 4)
        else:
            return cls.base_regular_order().filter(cls.install_id == None, cls.status == 5)


    @classmethod
    def audit_order(cls):
        pass
    
    @classmethod
    def appoint_order(cls):
        pass

    @classmethod
    def ship_order(cls):
        pass

    @classmethod
    def default_order(cls):
        pass


    def swicth_event(cls, user=None, event=None, sub=None):
        values = dict(
                pending_orders = cls.pending_order,
                order = cls.owner_order,
                assion= cls.assion_order,
                audit= cls.audit_order,
                confirm= cls.confirm_order,
                appoint= cls.appoint_order,
                ship= cls.ship_order
                )
        return values.get(event, cls.default_order)(user=user, sub=None)
    ###################
    ####################
















