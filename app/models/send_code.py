# coding:utf-8
# File Name: send_code.py
# Created Date: 2018-02-26 16:25:23
# Last modified: 2018-03-26 16:53:01
# Author: yeyong
import random
from app.ext import redis, app
import requests
import json

class SendCode:
    @staticmethod
    def code(phone=None):
        if phone is None:
            return False, "手机号不能为空"
        temp = redis.get(phone)
        if temp and redis.ttl(phone) > 200:
            return False, "请求过于频繁"
        redis.delete(phone)
        code = SendCode.generate_code()
        redis.set(phone, code)
        redis.expire(phone, 180)
        return True, code


    @staticmethod
    def generate_code():
        temp = [n for n in range(9)]
        random.shuffle(temp)
        code = "".join(str(n) for n in temp[:6])
        return code


    @staticmethod
    def send(**kwargs):
        args = dict(
                appid=app.config.get("SMS_KEY"),
                project=app.config.get("SMS_PROJECT"),
                signature=app.config.get("SMS_SIGN"),
                to=""
                )
        args.update(kwargs)
        headers = {"content-type": "application/json"}
        res = requests.post(app.config.get("SMS_URL"),data=json.dumps(args), headers=headers)
        if res.status_code != 200:
            return False, "链接短信服务器失败"
        status = json.loads(res.text)
        if status.get("status") == "success":
            return True, "发送成功"
        else:
            return False, status['status']
        
        

        



