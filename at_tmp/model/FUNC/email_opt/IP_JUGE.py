#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 11:49
# @Author  : bxf
# @File    : IP_JUGE.py
# @Software: PyCharm

def ipcheck(args):
    def check(func):
        def wapper():
            allowlist=['10']
            if args  in allowlist:
                func()
            else:
                print('ip 被禁止')
                return False
        return wapper
    return check