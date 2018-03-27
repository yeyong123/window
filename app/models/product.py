# coding:utf-8
# File Name: product.py
# Created Date: 2018-02-27 14:45:17
# Last modified: 2018-03-27 16:34:13
# Author: yeyong
from app.extra import *
from app.models.picture import Picture
class Product(db.Model, BaseModel):
    __tablename__ = 'products'
    title = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    category_id= db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False, index=True)
    price = db.Column(db.Integer, default=0)
    material = db.Column(db.String)
    kind = db.Column(db.String)
    product_type = db.Column(db.String)
    color = db.Column(db.String)
    metal = db.Column(db.String)
    pro_set = db.Column(db.String)
    unit = db.Column(db.String)
    price_type = db.Column(db.String, default="元")
    content= db.Column(db.Text)
    hide = db.Column(db.Boolean, default=False, index=True)
    #orders = db.relationship("Order", backref="product", lazy="dynamic")

    
    def __repr__(self):
        return "<Product id: {}, title: {}>".format(self.id,self.title)

    def delete_product(self):
        Product.query.filter_by(id=self.id).update({'hide': True})


    @classmethod
    def create_product(cls, **kwargs):
        from app.models.account import Account
        try:
            valid = set(cls.__table__.columns.keys())
            p = dict()
            pic = "pictures"
            if pic in kwargs:
                p[pic] = kwargs.pop(pic)
            kwargs = {k: v for k, v in kwargs.items() if v and k in valid}
            a = Account.query.get(kwargs.get("account_id"))
            kwargs.update(category_id=a.categories[0].id)
            pro = cls(**kwargs)
            db.session.add(pro)
            db.session.commit()
            cls.create_pictures(p=p[pic], key=pro.id)
            db.session.commit()
            return True, pro
        except Exception as e:
            db.session.rollback()
            return False, "操作失败, 原因为: {}".format(e)

        

    @classmethod
    def create_pictures(cls, p=None, key=None):
        args = []
        for k in p:
            pic = Picture(pictureable_type="Product", pictureable_id=key, image=k)
            db.session.add(pic)

    def pictures(self):
        ps = Picture.query.filter_by(pictureable_id=self.id, pictureable_type="Product")
        return [p.to_json() for p in ps]

    def to_json(self):
        return super().to_json(pictures=self.pictures())


        
    


