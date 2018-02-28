# coding:utf-8
# File Name: manage.py
# Created Date: 2018-02-26 10:43:45
# Last modified: 2018-02-28 13:56:08
# Author: yeyong

import os
from app.flask_init import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models.user import User
from app.models.photo import Photo
from app.models.account import Account
from app.models.material import Material
from app.models.role import Role
from app.models.permission import Permission
from app.models.order  import Order
from app.models.product import Product
from app.models.company import Company
from app.models.category import Category
from app.models.customer import Customer
from app.models.node import Node


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app,
            db=db,
            User = User,
            Photo=Photo,
            Account = Account,
            Material = Material,
            Role = Role,
            Company=Company,
            Order = Order,
            Permisson = Permission,
            Product = Product,
            Customer=Customer,
            Node=Node
            )

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
