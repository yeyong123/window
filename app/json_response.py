# coding:utf-8
# File Name: json_response.py
# Created Date: 2018-02-26 10:52:35
# Last modified: 2018-02-26 14:49:21
# Author: yeyong
from flask import Response, jsonify, Flask
from werkzeug.datastructures import Headers
class JSONResponse(Response):

    def __init__(self, response=None, **kwargs):
        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        headers = ('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, Authorization, Token')
        h = Headers([origin, methods, headers])
        kwargs["headers"] = h
        return super().__init__(response, **kwargs)

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JSONResponse, cls).force_type(response, environ)

class MyFlask(Flask):
    response_class = JSONResponse
