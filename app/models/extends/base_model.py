# coding:utf-8
# File Name: base_model.py
# Created Date: 2018-02-28 14:30:16
# Last modified: 2018-03-06 10:55:06
# Author: yeyong
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



    @classmethod
    def parser_time(cls, start=1696, end=4646):
        s_time = cls.conver_time(start)
        e_time = cls.conver_time(end)
        args = [
                cls.created_at >= s_time,
                cls.created_at <= e_time
                ]
        return args

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
        args = [getattr(cls, k) == v for k, v in kwargs.items() if v and hasattr(cls, k)]
        start_time = kwargs.get("start_time", None)
        end_time = kwargs.get("end_time", None)
        if start_time or end_time:
            args.extend(cls.parser_time(start_time=start_time, end_time=end_time))
        args.extend([cls.account_id == cls.get_account_value()])
        temp = cls.query.filter(*args).order_by(cls.created_at.desc()).paginate(int(page), per_page=5, error_out=False)
        page = cls.res_page(temp)
        results = temp.items
        return results, page







