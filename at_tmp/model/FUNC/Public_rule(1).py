#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/13 10:50
# @Author  : kimmy-pan
# @File    : Public_rule.py
from model.util.PUB_DATABASEOPT import *
from model.util.PUB_LOG import *
import re
"""
从根据规则ID数据库获取'rule_import_project'字段返回
"""


def get_rule_data(rule_id):
    sql = "select rule_import_project from t_rule_info where rule_id = '{}'".format(rule_id)
    result = eval(get_JSON(sql)[0]['rule_import_project'])
    sql1 = "select rule_case_desc from rule_case_info where rule_id = '{}'".format(rule_id)
    resultall = get_JSON(sql1)
    a = []
    for i in range(len(resultall)):
        result1 = resultall[i]["rule_case_desc"].replace("${","").replace("}","")
        for k,v in result.items():
            if k in result1:
                pass
            else:
                exeLog('rule_id:{},{}字段不存在rule_case_info表'.format(rule_id,k))
                return False

        rx = re.compile('|'.join(map(re.escape, result)))

        def one_xlat(match):
            # print(match)
            return result[match.group(0)]
        a.append(rx.sub(one_xlat, result1))
    return a


if __name__ == '__main__':
    print(get_rule_data('RULE-1807170001'))


# def get_rule_data(idict,result):
#
#     rx = re.compile('|'.join(map(re.escape, idict)))
#
#     def one_xlat(match):
#         # print(match)
#         return idict[match.group(0)]
#
#     return rx.sub(one_xlat, result)
#
# idict = {"page": "test1", "type": "test2", "field": "test3", "value": "test4"}
# result = '${page}${type}${field}${value}'
# get_rule_data(idict,result)