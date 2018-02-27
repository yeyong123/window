# coding:utf-8
# File Name: photo.py
# Created Date: 2018-02-26 15:23:24
# Last modified: 2018-02-26 16:00:52
# Author: yeyong
from app.extra import *
from qiniu import Auth, put_file
import uuid
class Photo(db.Model, Serialize):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)


    def __repr__(self):
        return "<Photo id: {}, image: {}>".format(self.id, self.image)


    @classmethod
    def upload(cls, f, name):
        extend_name = name.split(".")[-1]
        q = Auth(access_key=app.config.get("QINIU_AK"), secret_key=app.config.get("QINIU_SK"))
        key = uuid.uuid4()
        bucket_name = app.config.get("BUCKET_NAME")
        base_url = app.config.get("QINIU_URL")
        token = q.upload_token(bucket_name, key, 3600)
        res, info = put_file(token, key, f)
        if info.status_code == 200:
            image = base_url + res.get("key") + '.' + extend_name
            p = cls(image=image)
            db.session.add(p)
            db.session.commit()
            return True, p
        else:
            return False, "上传失败"




