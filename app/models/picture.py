# coding:utf-8
# File Name: picture.py
# Created Date: 2018-02-27 14:35:17
# Last modified: 2018-03-01 14:00:25
# Author: yeyong
from app.extra import *
class Picture(db.Model, BaseModel):
    __tablename__ = 'pictures'
    image = db.Column(db.String)
    image_type = db.Column(db.String)
    pictureable_type = db.Column(db.String, index=True)
    pictureable_id = db.Column(db.BigInteger, index=True)
    

    def __repr__(self):
        return "<Picture id: {}, image: {}, pictureable_id: {}, pictureable_type: {}>".format(self.id, self.image, self.pictureable_id, self.pictureable_type)

    @classmethod
    def create_image(cls, **kwargs):
        try:
            klass = kwargs["pictureable_type"].lower()
            kwargs.update(pictureable_type=klass)
            p = cls(**kwargs)
            db.session.add(p)
            db.session.commit()
            return True, p
        except Exception as e:
            app.logger.warn("图片创建失败{}".format(e))
            db.session.rollback()
            return False, "图片创建失败"

    @classmethod
    def fetch(cls, klass=None, klass_id=None, image_type=None):
        return cls.query.filter_by(pictureable_id=klass_id, pictureable_type=klass, image_type=image_type)


