# coding:utf-8
# File Name: order.py
# Created Date: 2018-02-27 13:52:39
# Last modified: 2018-04-08 15:02:21
# Author: yeyong
from app.extra import *
from app.models.customer import Customer
from app.models.account import Account
from app.models.user import User
from app.models.node import Node
from app.models.picture import Picture
from app.models.product import Product
from app.models.region import Region
from app.models.category import Category
from app.models.company import Company
from app.models.material import Material
from app.models.order_detail import OrderDetail
from app.models.extends.order_module import OrderModule

class Order(db.Model, BaseModel, OrderModule):
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
   # product_id = db.Column(db.Integer, db.ForeignKey("products.id"), index=True)
    product_detail = db.column(db.String)
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
    order_details = db.relationship("OrderDetail", backref="order", lazy="dynamic")
    product_metal = db.Column(db.String)
    product_color = db.Column(db.String)
    product_glass = db.Column(db.String)
    glass_config = db.Column(db.String)

    ## 区分不同的用户
    server = db.relationship("User", foreign_keys=[server_id])
    driver = db.relationship("User", foreign_keys=[driver_id])
    installer = db.relationship("User", foreign_keys=[install_id])
    user = db.relationship("User", foreign_keys=[user_id])



    def __init__(self, **kwargs):
        self._account_id = None
        self._current_user = None
        super().__init__(**kwargs)
        self.serial_no = self.generate_number()
        #self.product_amount = self._set_product_amount()

    
    @classmethod
    def set_account(cls, value):
        cls._account_id = value

    @classmethod
    def set_current_user(cls, user):
        cls._current_user = user
        user.set_account(cls.get_account_value())

    @classmethod
    def current_user(cls):
        if hasattr(cls, "_current_user"):
            return cls._current_user
        return None

    @classmethod
    def get_account_value(cls):
        if hasattr(cls, "_account_id"):
            return cls._account_id
        return None


    def __repr__(self):
        return "<Order id: {}, serial_no: {}, server_id: {}, user_id: {}, install_id: {}>".format(self.id, self.serial_no, self.server_id, self.user_id, self.install_id)


    @classmethod
    def complete_orders(cls, page=1):
        """
        完成的订单
        """
        results = cls.query.filter_by(status=7, account_id=cls.get_account_value()).paginate(int(page), per_page=25, error_out=False)
        page = cls.res_page(results)
        return results.items, page


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
                raise AttributeError("创建失败订单号用尽")
            t = basic + temp
            res = str(prefix) + str(t).zfill(9)
            if not type(self).query.filter_by(serial_no=res).first():
                return res


    #生成客户
    def generate_customer(self, ip=None, name=None):
        return Customer.generate_customer(
                server_id=self.user_id,
                phone=self.customer_phone, 
                name=self.customer_name,
                account_id=self.account_id, 
                province=self.province,
                city=self.city,
                district=self.district,
                customer_type=self.order_type,
                ip = ip,
                u_name = name
                )

    #订单创建时处理新的客户以及转为正式客户
    @classmethod
    def create_order(cls, **kwargs):
        """
        创建订单生产客户, 如果用户已经是正式用户就不处理, 
        如果不是正式用户就转为正式用户, 如果没有这个用户就新建一个正式用户
        """
        try:
            ip = kwargs.get("ip")
            u_name = kwargs.get("u_name")
            kwargs = {key: value for key, value in kwargs.items() if hasattr(cls, key)}
            temp_dict = dict()
            temp_key = 'pictures'
            if temp_key in kwargs:
                temp_dict[temp_key] = kwargs.pop('temp_key')
            o = cls(**kwargs)
            ok, c = o.generate_customer(ip=ip, name=u_name)
            if not ok:
                db.session.rollback()
                return False, c
            o.customer_id = c.id
            db.session.add(o)
            db.session.commit()
            o.record_option(
                    body="创建了订单",
                    ip=ip,
                    user_name = u_name
                    )
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
            node = Node(
                    user_name=user.name, 
                    remark=content, 
                    account_id=user.account_id, 
                    order_id=self.id
                    )
            db.session.add(node)
            db.session.commit()
            return True, self
        except Exception as e:
            app.logger.warn("事件记录失败: {}".format(e))
            db.session.rollback()
            return False, "事件记录失败"

    def record_node(self, **kwargs):
        """
        记录节点信息
        """
        node = Node(**kwargs)
        db.session.add(node)
        db.session.commit()

    def handle_order_event(self, key=None, user=None, content=None, ip=None):
        """
        处理事件
        """
        args = dict(
                audit="审核通过",
                complete="确认完成",
                arrive="司机送达",
                dismiss="关闭订单",
                back="退回",
                cancel="驳回"
                )
        if not key in args.keys():
            return False, "无效的参数"
        ok, node = self.record_event_to_node(event=key, user=user, content=args.get(key) if content is None else content)
        if not ok:
            return False, node
        self.record_option(
                body=args.get(key),
                name=user.name,
                event="update",
                ip=ip
                )
        return True, self



    def create_event(self):
        return None

    def back_event(self):
        """
        退回事件: 根据状态将测量, 司机, 安装的 ID 设为空
        """
        if self.status == 1:
            self.owner_self.update({'server_id': None})
        elif self.status == 4:
            self.owner_self.update({'driver_id': None})
        elif self.status == 5:
            self.owner_self.update({'install_id': None})
        return None

    def reset_event(self):
        """
        重置事件: 根据状态, 将安装时间, 运输时间, 安装时间设为空
        """
        if self.status == 1:
            self.owner_self.update({'server_date': 0})
        elif self.status == 4:
            self.owner_self.update({'arrive_date': 0})
        elif self.status == 5:
            self.owner_self.update({'install_date': 0})
        return None

    def cancel_event(self):
        """退回一个状态"""
        return self.toggle_status("prev")

    def arrive_event(self):
        """运输抵达状态"""
        if self.status == 4:
            return self.default_event()

    def install_event(self):
        """安装完成事件"""
        if self.status == 5:
            return self.toggle_status()

    def measure_event(self):
        """测量完成事件"""
        if self.status == 1:
            return self.default_event()

    def default_event(self):
        """默认事件, 向前一个状态"""
        return self.toggle_status()

    def dismiss_event(self):
        return self.owner_self.update({"status": 10})

    def swicth(self, key=None):
        values = dict(
                create=self.create_event,
                back=self.back_event,
                reset=self.reset_event,
                cancel=self.cancel_event,
                arrive=self.arrive_event,
                install_upload=self.install_event,
                measure_upload=self.measure_event,
                dismiss=self.dismiss_event
                )
        return values.get(key, self.default_event)()

    ####################

   

    #################
    ##################
    ## 根据用户的角色过滤订单
    @classmethod
    def filter_orders(cls, user=None, event=None, **kwargs):
        page = kwargs.get("page", 1)
        valid = {"category_id", "customer_name",  "serial_no", "status", "order_type"}
        args = [getattr(cls, key) == value for key, value in kwargs.items() if key in valid and value]
        start = kwargs.get("start_time", None)
        end = kwargs.get("end_time", None)
        if start or end:
            args.extend(cls.parser_time(start, end))
        temp = cls.swicth_event(user=user, event=event, sub=kwargs.get("sub", None))
        results = temp.filter(and_(*args)).order_by(cls.created_at.desc()).paginate(int(page), per_page=25, error_out=False)
        temp_page = cls.res_page(results)
        return results.items, temp_page 


    #意向订单
    @classmethod
    def pending_order(cls, user=None, sub=None):
        """意向订单 order_type = 1"""
        return cls.logic_query().filter_by(order_type=0)

    @classmethod
    def logic_query(cls):
        """过滤掉订单状态为删除的, 订单状态100为删除"""
        return cls.query.filter(cls.status < 100, cls.account_id == cls.get_account_value())

    #基本的查询
    @classmethod
    def base_regular_order(cls):
        """过滤状态小于100, 并且不是意向订单的单子"""
        return cls.logic_query().filter_by(order_type=1)

    #我的订单
    @classmethod
    def owner_order(cls, user=None, sub=None):
        """
        我的订单
        1. 管理员角色就区分用户
        2. 其他用户区分这个订单相关的用户(测量工, 安装工, 司机, 介绍人)
        """
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
        
        
    
    #指派订单
    @classmethod
    def assion_order(cls, user=None, sub=None):
        """
        找出需要指派的单子
        1, 测量指派
        2, 运输指派
        3, 安装指派
        """
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

    
    #待审核
    @classmethod
    def audit_order(cls, user=None, sub=None):
        """待审核"""
        return cls.base_regular_order().filter_by(status=2)
        
    
    #待确认
    @classmethod
    def confirm_order(cls, user=None, sub=None):
        return cls.base_regular_order().filter(or_(cls.status == 6, cls.status == 3))

    #待预约
    @classmethod
    def appoint_order(cls, user=None, sub=None):
        if user.is_admin:
            return cls.base_regular_order().filter(cls.status > 0).filter(or_(
                cls.arrive_date == 0,
                cls.install_date == 0,
                cls.server_date == 0
                ))
        elif user.is_driver:
            return cls.base_regular_order().filter(cls.driver_id == user.id, cls.arrive_date == None, cls.status == 4)
        else:
            return cls.base_regular_order().filter(or_(
                    and_(cls.status == 1, cls.server_id == user.id, cls.server_date == 0),
                    and_(cls.status == 5, cls.install_id == user.id, cls.install_date == 0)
                ))

    #待运输
    @classmethod
    def ship_order(cls, user=None, sub=None):
        if user.is_admin:
            return cls.base_regular_order().filter_by(status=4)
        else:
            return cls.base_regular_order().filter(
                    cls.status == 4, 
                    cls.driver_id == user.id, 
                    cls.arrive_date > 0
                    )
    
    #待施工
    @classmethod
    def work_order(cls, user=None, sub=None):
        return cls.base_regular_order().filter(or_(
                and_(cls.status == 1, cls.server_id == user.id, cls.server_date > 0),
                and_(cls.status == 5, cls.install_date > 0, cls.install_id == user.id)
            ))

    @classmethod
    def default_order(cls, user=None, sub=None):
        return cls.query


    #事件集合
    @classmethod
    def swicth_event(cls, user=None, event=None, sub=None):
        values = dict(
                pending_orders = cls.pending_order,
                order = cls.owner_order,
                assion= cls.assion_order,
                audit= cls.audit_order,
                confirm= cls.confirm_order,
                appoint= cls.appoint_order,
                ship= cls.ship_order,
                work= cls.work_order
                )
        return values.get(event, cls.default_order)(user=user, sub=None)
    ###################
    ####################

    ## 当技工修改时修改状态
    ## 当测量师傅修改的时候, 以及状态是0的时候, 移到下一个状态
    ## 当安装师傅修改的时候, 以及状态为4的时候移到下一个状态
    ## 当司机修改的时候, 以及状态为3的时候移到下一个状态
    @staticmethod
    def watch_user_event_changed(target, value, oldvalue, initiator):
        users = {"server_id", "install_id", "driver_id"}
        if not initiator.key in users:
            return None
        if initiator.key == "server_id":
            if target.status == 0:
                target.status = 1
        elif initiator.key == "install_id":
            if target.status == 4:
                target.status = 5
        else:
            if target.status == 3:
                target.status = 4


    ## 当前端每一次界面修改的时候就修改一次总价
    @staticmethod
    def wacth_price_changed(target, value, oldvalue, initiator):
        target.total_amount = target.order_total_amount(key=initiator.key, value=value)


    ## 计算总价
    def order_total_amount(self, key=None, value=None):
        ts = {"measure_amount", "install_amount", "ship_amount", "product_amount", "server_amount", "other_amount"}
        if key:
            if type(key) is list: #如果是多个值
                for k in key:
                    ts.remove(k)
            else:
                ts.remove(key)
        if value is None:
            value = 0
        else:
            if type(value) is list:
                value = sum(value)
            else:
                value = value
        temp = sum([getattr(self, key) for key in ts])
        return temp + value


    ##计算介绍人金额
    def royalties(self):
        if self.intro_amount and self.intro_amount  > 0:
            return self.intro_amount
        else:
            temp = float(self.product_amount) * float(self.user.raty_price())
            return temp


   
    # def _set_product_amount(self):
    #   return self.product_info().get("price", 0)

    ############################################
    #############################################
    ## 订单中的关联的信息查找, 在序列化到 JSON
     ## 订单中的产品信息
    def product_info(self):
        p = Product.query.filter_by(id=self.product_id).first()
        if not p:
            return {}
        return p.to_json()

    ## 产品信息
    def account_info(self):
        if not self.account:
            return {}
        return self.account.to_json()
    
    ## 渠道
    def region_info(self):
        r = Region.query.filter_by(id=self.region_id).first()
        if not r:
            return {}
        return r.to_json()
    
    ## 运输环境
    def detail_info(self):
        if self.order_details.first():
            return [d.to_json() for d in self.order_details]
        
    ## 司机
    def driver_info(self):
        if not self.driver:
            return {}
        return self.driver.to_json()

    ## 销售
    def user_info(self):
        if not self.user:
            return {}
        return self.user.to_json()
    
    ## 技工
    def server_info(self):
        if not self.server:
            return {}
        return self.server.to_json()
   
   ## 介绍人
    def intro_info(self):
        u = User.query.filter_by(id=self.intro_id).first()
        if not u:
            return {}
        return u.to_json()
    
    ## 安装工
    def install_info(self):
        if not self.installer:
            return {}
        return self.installer.to_json()
    
    ## 大类
    def category_info(self):
        c = Category.query.filter_by(id=self.category_id).first()
        if not c:
            return {}
        return c.to_json()

    ## 材质
    def material_info(self):
        m = Material.query.filter_by(id=self.material_id).first()
        if not m:
            return {}
        return m.to_json()
    ## 品牌
    def company_info(self):
        c = Company.query.filter_by(id=self.company_id).first()
        if not c:
            return {}
        return c.to_json()
    ## 

    def nodes_info(self):
        if self.nodes.first():
            return [n.to_json() for n in self.nodes]
        else:
            return []

    def install_pictures(self):
        if self.pictures("install_pictures").first():
            return [p.to_json() for p in self.pictures("insert_pictures")]
        else:
            return []

    def measure_pictures(self):
        if self.pictures().first():
            return [p.to_json() for p  in self.pictures()]
        return []
    

    def show_json(self):
        methods = {
                "category_info",
                "company_info", 
                "material_info",
                "user_info",
                "install_info",
                "server_info",
                "driver_info",
                "account_info",
                "intro_info",
                "region_info",
                "detail_info",
                "royalties",
                "install_pictures",
                "measure_pictures"
                }
        args = {"nodes": self.nodes_info()}
        for v in methods:
            args.update({v: getattr(self, v)()})
        return self.to_json(**args)


    #############
    #############


    #######################
    ## 订单上传图片处理
    ## 有测量图, 安装图
    #######################

     ## 获取图片
    def pictures(self, kind="measure_pictures"):
        return Picture.fetch(klass="order", klass_id=self.id, image_type=kind)
    
    # 添加图片
    def insert_pictures(self, image=None, t=None):
        ok, p = Picture.create_image(pictureable_type="order", pictureable_id=self.id, image=image, image_type=t)
        if not ok:
            return False, "添加图片失败"
        return True, p

    #修改图片
    def change_upload(self, user=None, **kwargs):
        measure = kwargs.get("measure_pictures", None)
        install = kwargs.get("install_pictures", None)
        try:
            if measure:
                self.pictures_type().delete()
                image = measure.get("image")
                ok, p = self.insert_pictures(image=image, t="measure_pictures")
                if not ok:
                    return False, p
                return True, p
            elif install:
                self.pictures(kind="install_pictures").delete()
                image = install.get("image")
                ok, p = self.insert_pictures(iamge=image, t="install_pictures")
                if not ok:
                    return False, p
                return True, p
        except Exception as e:
            app.logger.warn("图片创建出现错误, {}".format(e))
            db.session.rollback()
            return False, "图片处理失败"

    def toggle_order(self):
        """将意向订单切换为正式订单"""
        self.owner_self.update({"order_type": 1})
    
    def create_detail(self, **kwargs):
        try:
            args = set(OrderDetail.__table__.columns.keys())
            kwargs = {k: v for k, v in kwargs.items() if v and k in args}
            kwargs.update(account_id=self.account_id, order_id=self.id)
            detail = OrderDetail(**kwargs)
            db.session.add(detail)
            db.session.commit()
            return True, detail
        except Exception as e:
            msg = "添加运输安装环境失败"
            app.logger.warn("{}{}".format(msg,e))
            db.session.rollback()
            return False, msg

    def update_detail(self, **kwargs):
        detail = self.order_details.first()
        return detail.update(**kwargs)








for e in {"server_id", "install_id", "driver_id"}:
    db.event.listen(getattr(Order, e), "set", Order.watch_user_event_changed)

## 检查价格变动
for t in {"measure_amount", "install_amount", "ship_amount", "product_amount", "server_amount", "other_amount"}:
    db.event.listen(getattr(Order, t), "set", Order.wacth_price_changed)
















