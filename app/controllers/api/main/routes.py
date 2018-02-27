# coding:utf-8
# File Name: routes.py
# Created Date: 2018-02-26 11:14:31
# Last modified: 2018-02-26 15:36:09
# Author: yeyong
from flask import request, jsonify, g
from . import main
from .home import *

main.add_url_rule("/", view_func=home)
main.add_url_rule("/upload", view_func=upload, methods=["POST"])
