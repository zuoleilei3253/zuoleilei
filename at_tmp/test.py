#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/16 17:43
# @Author  : bxf
# @File    : test.py
# @Software: PyCharm
from model.util.GET_PARAM import *
import json
from model.FUNC.python_shell.CONNECT_LINUX import *

def apiParams(data):

    params_init1 = []
    for i in data["params"]:
        params_init = GET_Variable(i)
        params_init1.extend(params_init)

    params = list(set(params_init1))
    params_list = []
    for i in params:
        param = [i, None, {}]
        params_list.append(param)
    return params_list

def jsonTO(data):
    a=json.dumps(data)
    return a

def get():
    param = {"${userId}": "TD", "${bankId}": "123"}
    aa="/bankcardInfo/"
    # replaceValue = "/monitor/bankFile/unZip/${systemName}/${date}"
    replaceValue = {'Data': {"userId": "${use1rId}", "bankId": "${ban1kId}"}, 'Token': ""}

    a = GET_PARAM(param,replaceValue).GET_INIT_DATA()
    return  a
def changeData(key,val):
    params={}
    akey="${"+key+"}"
    params[akey]=val
    return params
def giveData(initpa):
    paramList = initpa
    newparam = {}
    for i in range(len(paramList)):
        if len(paramList[i]) != 2:
            key = paramList[i][0]
            param = paramList[i][2]
            if param == {}:
                newparam.update({})
            elif param['assign_type'] == 'upload':
                case_id = param['upload_id']
                tkey = param["field"]
                value ="123"
                newparam.update(changeData( key, value))
            elif param['assign_type'] == 'database':
                fcol = param['database_field']
                sql = param['sql']
                dataparamid = param['database']
                value = 123
                newparam = changeData( key, value)
            elif param['assign_type'] == 'normal':
                num = param['const_no']
                value = 444
                newparam = changeData( key, value)
            elif param['assign_type'] == 'custom':
                val = param['custom_val']
                newparam.update( changeData(key, val))
    print(newparam)
    return newparam

if __name__ == '__main__':
    # a={'Content-Type': 'application/json', 'Accept': '', 'version': '5.3.5'}
    # c="/a/${fdfas}"
    # param={"${fdfas}":"1231"}
    # init_data=[["subscribeId", "", {}], ["projectId", "CD186F41-B036-4DC7-8615-3D8F659FFBDC", {"custom_val": "4AD85816-B82B-49E1-9761-6F16EC4C8002", "assign_type": "custom"}], ["userId", "44CACAB8-8A38-4048-8820-35C2A305E248", {"custom_val": "4332A90D-5855-4A38-9174-AA3684521A55", "assign_type": "custom"}], ["borrowUserId", "FF2F8D15-DACC-4355-A71D-2178A6E15322", {"custom_val": "89881A8E-DA7B-4235-A653-7D0E33351C16", "assign_type": "custom"}], ["cdcType", "P2P", {}]]
    # b=GET_PARAM(param,c).GET_INIT_DATA()
    # print(giveData(init_data))
    # d="/appuser/user_updateuserdetail"
    # paramaa={"${test}": "1312"}
    # print(GET_PARAM(paramaa, d).GET_INIT_DATA())
    tail = 'tail -f /root/redis6388.log'
    Connect().link_server_IM(tail)

