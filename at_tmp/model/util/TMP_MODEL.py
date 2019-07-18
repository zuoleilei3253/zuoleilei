#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 9:27
# @Author  : bxf
# @File    : TMP_MODEL.py
# @Software: PyCharm


import json

# 转换成Dict
def toDict(data):
    if data=='':
        return None
    elif isinstance(data,dict):
        return data
    elif isinstance(data,str):
        return json.loads(data)
    elif isinstance(data, list) or isinstance(data, tuple):
        Dict = {}
        for i in data:
            """data = ["key:value","key1:value1"]  or  data = ("key:value","key1:value1")"""
            if ":" in i and len(i.split(":")) == 2:
                Dict[i.split(":")[0]] = i.split(":")[1]
                """data = ["a","b"]  or  data = ("a","b")"""
            else:
                return False
        return Dict
    else:
        return False
# 转换成str
def toStr(data):
    if data=='':
        return None
    elif isinstance(data,str):
        return data
    elif isinstance(data,dict):
        return json.dumps(data,ensure_ascii=False)
    elif isinstance(data, list) or isinstance(data, tuple) or \
            isinstance(data, int) or isinstance(data, float) or isinstance(data, bool):
        return str(data)
    else:
        return False


if __name__ == "__main__":
    d = {"a":"a"}
    print(type(toStr(d)))