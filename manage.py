# coding:utf-8
# File Name: manage.py
# Created Date: 2018-02-26 10:43:45
# Last modified: 2018-03-27 17:15:58
# Last modified: 2018-03-12 10:07:33
# Last modified: 2018-03-12 10:11:13
# Author: yeyong

import os
from app.flask_init import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from werkzeug.utils import find_modules
models = find_modules("app.models")
models_class = set()
for model in models:
    if not model in {"app.models.base", "app.models.user_role", "app.models.user_account", "app.models.role_permission"}:
        name = "".join(map(lambda c: c.capitalize(), model.split(".")[-1].split("_")))
        m = __import__(model, fromlist=[name])
        models_class.add(getattr(m, name))
app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
def make_shell_context():
    args = {k.__name__: k for k in models_class}
    args.update(dict(app=app, db=db))
    return args
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if not app.debug:
    import logging
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

