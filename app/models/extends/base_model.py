# coding:utf-8
# File Name: base_model.py
# Created Date: 2018-02-28 14:30:16
# Last modified: 2018-04-08 14:38:21
# Author: yeyong
from dateutil.relativedelta import relativedelta
from app.ext import db
from datetime import datetime
import time
class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_json(self, **kwargs):
        json_post = {n: self.parse_column(n) for n in self.__table__.columns.keys()}
        json_post.update(**kwargs)
        return json_post


    def parse_column(self, n):
        if n == "created_at" or n == "updated_at":
            return time.mktime(getattr(self, n).timetuple())
        else:
            return getattr(self, n)

    def to_date(self, key=0):
        return datetime.fromtimestamp(key)

    def record_option(self, event=None, name=None, body=None, ip=None):
        from app.models.user_logger import UserLogger
        klass = self.__class__.__name__
        if klass == "Order":
            klass_no = self.serial_no
        else:
            klass_no = self.id
        if klass == "Account":
            account_id  = self.id
        else:
            account_id = self.account_id
        if klass == "User":
            name = self.name
        else:
            name = name
        body = "从IP: {}{}".format(ip, body)
        kwargs = dict(
                user_name = name,
                account_id=account_id,
                event=event,
                body = body,
                klass = klass,
                klass_no = klass_no
                )
        ok, res = UserLogger.create_logger(**kwargs)
        return res

        



    @classmethod
    def parser_time(cls, start=1696, end=4646):
        s_time = cls.conver_time(start)
        e_time = cls.conver_time(end)
        args = [
                cls.created_at >= s_time,
                cls.created_at <= e_time
                ]
        return args

    ##时间戳转成时间
    @classmethod
    def conver_time(cls, time_key=1400):
        try:
            return datetime.fromtimestamp(int(time_key))
        except Exception:
            return datetime.utcnow()



        


    @staticmethod
    def res_page(cls):
        temp_page = dict(
                has_next=cls.has_next,
                has_prev=cls.has_prev,
                next_num=cls.next_num,
                total=cls.total,
                per_page=cls.per_page,
                pages=cls.pages
                )
        return temp_page


    @classmethod 
    def model_search(cls, **kwargs):
        page  = kwargs.get("page", 1)
        args = [getattr(cls, k) == v for k, v in kwargs.items() if not v  is None and hasattr(cls, k)]
        start_time = kwargs.get("start_time", None)
        end_time = kwargs.get("end_time", None)
        if start_time or end_time:
            args.extend(cls.parser_time(start_time=start_time, end_time=end_time))
        if hasattr(cls, "get_account_value"):
            args.extend([cls.account_id == cls.get_account_value()])
        temp = cls.query.filter(*args).order_by(cls.created_at.desc()).paginate(int(page), per_page=5, error_out=False)
        page = cls.res_page(temp)
        results = temp.items
        return results, page

    ##根据提供的时间来计算出当月的范围
    @classmethod
    def get_month_day_range(cls, date=None):
        if not date:
            t = datetime.utcnow()
        t = cls.to_date(date)
        last_day = t + relativedelta(day=1, months=+1, days=-1)
        first_day = t + relativedelta(day=1)
        return first_day, last_day

    #转换时间处理 如2018-1-1 => (2018, 1, 1)
    @staticmethod
    def to_date(date):
        try:
            return datetime.strptime(date, "%Y-%m-%d")
        except:
            return datetime.utcnow()


    def update(self, **kwargs):
        try:
            for k, v in kwargs.items():
                if v and hasattr(self, k):
                    setattr(self, k, v)
            db.session.add(self)
            db.session.commit()
            return True, self
        except Exception as e:
            return False, "错误:{}".format(e)






        







