# coding:utf-8
# File Name: region.py
# Created Date: 2018-02-27 14:51:15
# Last modified: 2018-03-20 09:32:34
# Author: yeyong
from app.extra import *
from app.models.extends.title_validate import TitleValidate
class Region(db.Model, BaseModel, TitleValidate):
    __tablename__  = 'regions'
    title = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    ramark = db.Column(db.String)


db.event.listen(Region, "before_insert", Region.check_title)
db.event.listen(Region.title, "set",Region.validate_column)

