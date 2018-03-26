# coding:utf-8
# File Name: order_module.py
# Created Date: 2018-03-14 11:03:01
# Last modified: 2018-03-23 15:21:36
# Author: yeyong
from app.extra import and_, or_
from itertools import groupby
from app.models.user import User
class OrderModule:

    @classmethod
    def fetch_order_date(cls, month=None, range_month=None):
        """
        # 根据用户角色及企业的不同获取不同的订单
        # 查询前需要设置 _account_id 以及 _current_user
        # month 是获取当月 值为:  True
        # range_month 格式为: "2018-1-1", 获取提供日期内的月份的订单
        """
        account = cls.get_account_value() #仅获取当前账户
        user = cls.current_user() #获取查询用户
        orders = cls.query.filter(cls.account_id == account)
        args = [] #时间字段选项, and
        if month: #获取当月的数据
            m, _ = cls.get_month_day_range()
            args = [cls.created_at >= m]
        if range_month: #根据提供月份来计算当月的范围
            s, t = cls.get_month_day_range(range_month)
            args = [cls.created_at >= s, cls.created_at <= t]
        user_args = cls.filter_user_role(user=user)
        return orders.filter(and_(*args)).filter(or_(*user_args)).order_by(cls.created_at.desc())

    #换分不同的用户的角色,根据用户的角色来进行订单查询
    # 一个用户会有多个角色
    @classmethod
    def filter_user_role(cls, user=None):
        """
        # 如果有特别查询指定的用户就直接查询
        # 没有指定查询用户就根据当前用户角色来查询
        # user 为当前查询用户
        """
        user_args = []
        if user is None:
            return user_args
        if user.is_admin:
            return user_args
        if user.is_server:
            user_args.extend([cls.install_id == req.id, cls.server_id == req.id])
        if user.is_driver:
            user_args.append(cls.driver_id == req.id)
        if user.is_sale:
            user_args.append(cls.user_id == req.id)
        return user_args


    @classmethod
    def total_income_amount(cls, current=None, kind=None):
        """
        # 累计收益
        # current 为 True, 获取当月
        # 其他为获取全部
        # 获取不同类型的总数
        # install 安装费
        # server 服务费
        # measure 测量费
        # intro 介绍费
        # ship 运输费
        """
        map_key = dict(
                install="install_amount",
                server="server_amount",
                ship="ship_amount",
                intro="intro_amount",
                other = "other_amount",
                measure = "measure_amount"
                )
        key = map_key.get(kind, "total_amount")
        return sum(getattr(o, key) for o in cls.fetch_order_date(month=current))

    @classmethod
    def expense_total_amount(cls, current=None, profit=None):
        """
        # 总支出
        # current 为 True, 是当月
        # profit 为利润, 总收入 减去 总支出
        """

        keys = {"install", "ship", "intro", "server", "other", "measure"}
        total = sum(cls.total_income_amount(current=current, kind=key) for key in keys)
        if not profit:
            return total
        expense_total = cls.total_income_amount(current=current)
        return expense_total - total


    @classmethod
    def total_orders_count(cls, current=None):
        """
        ## 获取订单数
        ## current True 获取当月
        ## 其他为获取全部
        """
        return cls.fetch_order_date(month=current).count()


    ##根据提供的月份来计算分组订单
    @classmethod
    def group_income_orders(cls, kind="income"):
        """
        # 根据月份来进行分组
        # kind=income 为收益
        # 其他的 kind 为订单增长量
        """
        temp_orders = cls.fetch_order_date()
        h = {}
        for date, items in groupby(temp_orders, lambda o: o.created_at.strftime("%Y-%m")):
            if kind == "income":
                value = sum(v.total_amount for v in items)
                h[date] = value
            else:
                h[date] = len(list(items))
        return h


    ##根据不同的身份划分出不同的订单
    @classmethod
    def group_service_orders(cls, kind="server", date=None):
        """
        # 根据不同的用户的身份划分不同的订单
        # kind 参数:
        # 1. server 技工
        # 2. ship 运输司机
        # 3. intro 介绍人
        """
        user_args = []
        temp_orders = cls.fetch_order_date(range_month=date)
        if temp_orders.first() is None:
            return user_args
        user_ids  = cls.classify_from_orders(orders=temp_orders, kind=kind)
        if len(user_ids) < 1:
            return user_args
        for u in user_ids:
            if u is None:
                continue
            user_args.append(cls.fetch_signle_user_order(orders=temp_orders, user_id=u, kind=kind))
        return user_args

    ## 找出订单
    @classmethod
    def fetch_signle_user_order(cls, orders=None, user_id=None, kind="server"):
        """ 根据不同的类别来找出关于这个用户的单子 """
        user = cls.fetch_role_user(user_id)
        user_info = dict(name=user.name, phone=user.phone)
        if kind == "server":
            orders = orders.filter(or_(cls.server_id == user_id, cls.install_id == user_id))
        elif kind == "ship":
            orders = orders.filter(cls.driver_id == user_id)
        else:
            orders = orders.filter(cls.intro_id == user_id)
        if kind == "server":
            measure_count = orders.filter_by(server_id=user_id).count()
            install_count = orders.filter_by(install_id=user_id).count()
            amount_total = sum(o.measure_amount + o.install_amount for o in orders)
            user_info.update(dict(server_count=measure_count, 
                install_count=install_count,
                total_amount=amount_total))
        elif kind == "ship":
            count = orders.count()
            amount = sum(o.ship_amount for o in orders)
            user_info.update(dict(
                ship_count=count,
                total_amount=amount
                ))
        else:
            count = orders.count()
            amount = sum(o.intro_amount for o in orders)
            user_info.update(dict(
                deduct_count=count,
                total_amount=amount
                ))
        return user_info



    #把订单下的用户区分开来
    @classmethod
    def classify_from_orders(cls, orders=None, kind="server"):
        """ 根据不同的角色区分不同的用户 """
        user_ids = set()
        if kind == "server":
            user_ids = set(sum(([o.server_id, o.install_id] for o in orders), []))
        elif kind == "ship":
            user_ids = {o.driver_id for o in orders}
        else:
            user_ids = {o.intro_id for o in orders}
        return user_ids

    @classmethod
    def fetch_role_user(cls,user_id=None):
        """找出这个用户的信息"""
        return User.query.filter_by(id=user_id).first()





    







