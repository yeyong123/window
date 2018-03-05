# coding:utf-8
# File Name: validator.py
# Created Date: 2018-03-05 09:50:30
# Last modified: 2018-03-05 15:11:50
# Author: yeyong
import abc
class AutoStorage:

    def __init__(self, name=None, key=None):
        self.name = name


    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Validated(abc.ABC, AutoStorage):
    
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)


    @abc.abstractmethod
    def validate(self, instance, value):
        """ 验证值的有效性"""


class Quantity(Validated):
    def validate(self, instance, value):
        if value < 0:
            raise ValueError("{}值必须大于0".format(self.name))
        return value


class NonBlank(Validated):
    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError("{}不能为空".format(self.name))
        return value


class Presented(Validated):

    def validate(self, instance, value):
        column = self.name
        cls = type(instance)
        arg = [getattr(cls, column) == value]
        print("??????????????", column, cls,  arg, value)
        temp = cls.query.filter(getattr(cls, column) == value).first()
        print(temp)
        if temp and getattr(temp, column) == value:
            raise ValueError("值已经存在")
        else:
            return value


