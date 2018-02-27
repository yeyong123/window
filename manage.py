# coding:utf-8
# File Name: manage.py
# Created Date: 2018-02-26 10:43:45
# Last modified: 2018-02-27 11:22:55
# Author: yeyong

import os
from app.flask_init import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models.user import User
from app.models.photo import Photo
from app.models.account import Account


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app,
            db=db,
            User = User,
            Photo=Photo,
            Account = Account
            )

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
