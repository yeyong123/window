# coding:utf-8
# File Name: base_model.py
# Created Date: 2018-02-28 14:30:16
# Last modified: 2018-02-28 15:52:04
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







