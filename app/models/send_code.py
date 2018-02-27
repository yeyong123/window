# coding:utf-8
# File Name: send_code.py
# Created Date: 2018-02-26 16:25:23
# Last modified: 2018-02-27 10:42:24
# Author: yeyong
import random
from app.ext import redis

class SendCode:
    def __call__(self, phone=None):
        if phone is None:
            return False, "手机号不能为空"
        temp = redis.get(phone)
        if temp and redis.ttl(phone) > 120:
            return False, "请求过于频繁"
        redis.delete(phone)
        code = self.generate_code()
        redis.set(phone, code)
        redis.expire(phone, 180)
        return True, code


    def generate_code(self):
        temp = [n for n in range(9)]
        random.shuffle(temp)
        code = "".join(str(n) for n in temp[:6])
        return code
        



