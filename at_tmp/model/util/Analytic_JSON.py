#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/27 9:31
# @Author  : kimmy-pan
# @File    : Analytic_JSON.py



import sys
sys.path.append("/opt/ATEST")


import json
# 解析字典、列表各种组合的数据
def returnDict1(dicty,dickey):
    try:
        # 创建a列表
        a = []
        for k, v in dicty.items():
            # print(k)
            # 判断dickey是否为key，如果是返回对应的value
            if k == dickey:
                return v
            # 如果不是，把value添加到a列表
            else:
                a.append(v)

        # 循环a列表里的数据
        for j in a:
            if type(j) is dict and dickey in j:
                return j[str(dickey)]
            if type(j) is dict:
                returnDict1(j, dickey)
            if type(j) is list:
                for i in j:
                    if type(i) is not dict:
                        pass
                    if dickey in i and type(i) is dict:
                        return i[str(dickey)]
                    if type(i) is dict:
                        data = returnDict1(i, dickey)
                        return data
                    else:
                        pass
            if type(j) is not dict:
                pass
        # 返回值None时，dickey不存在dicty
        return
    except BaseException as msg:
        print(msg)
if __name__ == "__main__":
    dicty = {"isSQL":"0","diffSQL":["SQLSERVER","","SELECT id FROM dbo.UserBasicInfo  WHERE TelNo='18118111811'"],"prevData":{"ceshi":"1234"}}
    dicty1 = {"status": 1, "message": "success", "response": ["test3",{"test": "1", "haha":{"fee_desc": "还款费用明细", "service_fee": 365000, "period_amount": 100000}},"test2"]}
    dicty2 = {'response_result': {"code": "BAD_REQUEST", "message": "platformUserNo 平台用户编号格式不对,requestNo 流水号格式不对", "requestUri": "/account/personBindBankcardReq"}}
    a = returnDict1(dicty1, "fee_desc")

    # b = returnDict1(dicty1, "fee_desc")
    print(a)