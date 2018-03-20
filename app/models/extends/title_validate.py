# coding:utf-8
# File Name: title_validate.py
# Created Date: 2018-03-19 17:28:18
# Last modified: 2018-03-20 09:25:52
# Author: yeyong
class TitleValidate:
    @classmethod
    def check_title(cls, mapper, connection, target):
        checked = cls.query.filter_by(title=target.title, account_id=target.account_id).first()
        if checked:
            raise ValueError("该{}已经存在".format(target.title))


    @classmethod
    def validate_column(cls, target, value, oldvalue, initiator):
        checked = cls.query.filter_by(account_id=target.account_id, title=value).first()
        if checked:
            raise ValueError("该名称{} 已经存在".format(value))



