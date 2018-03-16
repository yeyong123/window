# coding:utf-8
# File Name: base.py
# Created Date: 2018-03-12 10:21:19
# Last modified: 2018-03-16 12:08:03
# Author: yeyong
from flask import Blueprint, g
from werkzeug.utils import find_modules

temp = find_modules("app.controllers.api_v2")
class TempRecord:
    pass
temp_record = TempRecord()
view_set = TempRecord()
for r in temp:
    base_path = "app.controllers.api_v2."
    if not r in {"{}{}".format(base_path, u) for u in {"base", "api_routes", "intercept", "auth"}}:
        t_name = r.split(".")[-1]
        cap_name = "".join(map(lambda c: c.capitalize(), t_name.split("_"))) + "View"
        t_module = __import__(r, fromlist=[cap_name])
        bp = Blueprint("{}_v2".format(t_name), __name__, url_prefix="/api_v2/{}".format(t_name))
        setattr(temp_record, t_name, bp)
        setattr(view_set, t_name + "_view", (getattr(t_module, cap_name)()))

route_api = temp_record.__dict__
view_api = view_set.__dict__

from .api_routes import *

