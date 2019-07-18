#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/7 10:56
# @Author  : kimmy-pan
# @File    : GET_SERVER.py
import os,requests


class getServer(object):
    def __init__(self,serveradd):
        self.serveradd = serveradd

    def returnResult(self):
        if "http" not in self.serveradd:
            return_code = os.system('ping -c 1 -w 1 %s'%self.serveradd)
            # print(return_code)
            if return_code:
                return 404
            else:
                return 200
        else:
            r = requests.get(self.serveradd)
            if r.status_code == 200:
                """返回200，以及响应时间，单位：ms"""
                return 200,r.elapsed.microseconds /1000
            else:
                return 404


if __name__ == "__main__":
    print(getServer("http://10.100.14.48:13002/swagger-ui.html#!").returnResult())