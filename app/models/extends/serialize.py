# coding:utf-8
# File Name: serialize.py
# Created Date: 2018-02-26 11:21:17
# Last modified: 2018-02-26 14:27:22
# Author: yeyong
import time
from datetime import datetime
class Serialize():

    def to_json(self):
        json_post = {n: self.parse_column(n) for n in self.__table__.columns.keys()}
        return json_post

    def parse_column(self, n):
        if n == "created_at" or n == "updated_at":
            return time.mktime(getattr(self, n).timetuple())
        else:
            return getattr(self, n)

    def to_date(self, key=0):
        return datetime.fromtimestamp(key)



