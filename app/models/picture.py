# coding:utf-8
# File Name: picture.py
# Created Date: 2018-02-27 14:35:17
# Last modified: 2018-02-27 14:44:37
# Author: yeyong
from app.extra import *
class Picture(db.Model, Timestamp, Serialize):
    __tablename__ = 'pictures'
    image = db.Column(db.String)
    image_type = db.Column(db.String)
    pictureable_type = db.Column(db.String, index=True)
    pictureable_id = db.Column(db.BigInteger, index=True)
