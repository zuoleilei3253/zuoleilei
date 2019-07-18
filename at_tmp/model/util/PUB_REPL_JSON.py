# -*- coding: utf-8 -*-
# @Time : 2018/3/5 11:02
# @Author : sunlin
# @File : ceshi.py
# @Software: PyCharm
# 函数入参


import sys
sys.path.append("/opt/ATEST")


def replace_keyvalue(jn, ky, val):
    """

    :param jn: 传入的json
    :param ky: 想要改变的json键名
    :param kv: 改变后的josn键值
    :return: 返回改变后的json
    """
    for key in jn.keys():
        if key == ky:
            jn[key] = val
        else:
            if type(jn[key]) == dict:
                for key2 in jn[key].keys():
                    if key2 == ky:
                        jn[key][key2] = val
    return jn


if __name__ == '__main__':
    a = {
        "reqData": {
            "platformUserNo": "string",
            "requestNo": "string"
        },
        "serverName": "string",
        "sourceDevice": "PC",
        "systemName": "TDSYSTEM"
    }
    aa = {"status": 1, "sunlin": "shuai", "message": "success", "response": ["test3", {"test": "1",
                                                                                       "haha": {"fee_desc": "还款费用明细",
                                                                                                "service_fee": 365000,

                                                                                                "period_amount": 100000}},
                                                                             "test2"]}
    aaa = {"status": 1, "message": "success", "response": ["test3", {"test": "1",
                                                                     "haha": {"fee_desc": "还款费用明细",
                                                                              "service_fee": 365000,
                                                                              "period_amount": 100000},
                                                                     "sunlin": "shuai"}, "test2"]}

    aaaa = {"status": 1, "message": "success", "response": ["test3", {"test": "1", "sunlin": "shuai",
                                                                      "haha": {"fee_desc": "还款费用明细",
                                                                               "service_fee": 365000,
                                                                               "period_amount": 100000}}, "test2"]}

    bb = 'requestNo'
    b = "platformUserNo"
    bbb = "systemName"
    c = "多层JSO5fff参"

    # 返回：

    print(replace_keyvalue(a, b, c))
