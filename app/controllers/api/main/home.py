# coding:utf-8
# File Name: home.py
# Created Date: 2018-02-26 11:18:20
# Last modified: 2018-02-26 16:02:22
# Author: yeyong
from flask import request
from app.models.photo import Photo
def home():
    return dict(msg="创管家欢迎您!", code=200)


def upload():
    f = request.files.get("image")
    name = f.filename
    if not f:
        return dict(msg="图片文件不能为空", code=422)
    f.save("/tmp/file")
    ok, photo = Photo.upload("/tmp/file", name)
    if not ok:
        return dict(msg=photo, code=422)
    return dict(photo=photo.to_json(), msg="ok", code=200)
