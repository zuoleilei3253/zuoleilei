#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/2 16:43
# @Author  : bxf
# @File    : PUB_RESP.py
# @Software: PyCharm

def resp(code,message,data):
    a=dict()
    a['code']=code
    a['message']=message
    a['data']=data
    return a



class respdata:
    def sucessResp(self,data):
        return_data= dict()
        return_data['code'] = 200
        return_data['message'] = "操作成功!"
        return_data['data'] = data
        return return_data
    def failResp(self):
        return_data = dict()
        return_data['code'] = 201
        return_data['message'] = " 操作失败，请检查操作日志!"
        return_data['data'] = ''
        return return_data

    def exceptionResp(self,e):
        return_data = dict()
        return_data['code'] = 202
        return_data['message'] = "操作异常，请检查日志!"
        return_data['data'] = str(e)
        return return_data

    def otherResp(self,e,message):
        return_data = dict()
        return_data['code'] = 203
        return_data['message'] = message
        return_data['data'] = str(e)
        return return_data
    def sucessMessage(self,data,message):
        return_data = dict()
        return_data['code'] = 200
        return_data['message'] = message
        return_data['data'] =data
        return return_data

    def failMessage(self, data, message):
        return_data = dict()
        return_data['code'] = 201
        return_data['message'] = message
        return_data['data'] = data
        return return_data