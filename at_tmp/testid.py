#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 10:40
# @Author  : bxf
# @File    : testid.py
# @Software: PyCharm

import wrapt
# def getName(func):
#     def cc(*args,**kwargs):
#         print("装饰器调试"+func.__name__)
#         return func(*args,**kwargs)
#
#     return cc

def getUser(token):
    @wrapt.decorator
    def getNamea(wrapped,instance,args,kwargs):
        print("装饰器调试"+wrapped.__name__)
        print(token)
        return wrapped(*args,**kwargs)
    return getNamea


@getUser("tt")
def test(data):
    print("函数内容:"+data)
    return




if __name__ == '__main__':
    test("111")