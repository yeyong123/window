# coding:utf-8
# File Name: validator.py
# Created Date: 2018-03-05 09:50:30
# Last modified: 2018-03-07 11:14:33
# Author: yeyong
import abc
class AutoStorage:
    __counter = 0

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

   
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
        print("sasda", self.name)
        value = value.strip()
        if len(value) == 0:
            raise ValueError("{}不能为空".format(self.name))
        return value


class Presented(Validated):
    def validate(self, instance, value):
        cls = type(instance)
        key = self.name.split("_")[-1]
        t = cls.query.filter(getattr(cls, key) == value).first()
        print(">>>>>>>>>", t)
        if t:
            raise ValueError("exited ", value)
        else:
            return value


