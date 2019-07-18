#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-01-07 17:53
# @Author  : bxf
# @File    : GET_INIT_PARAMS.py
# @Software: PyCharm
from model.util.TMP_DB_OPT import *
from model.util.GET_PARAM import *
from model.util.PUB_RESP import *

class INIT_OPT:
    def __init__(self,token):
        self.token=token
    def getInit(self,id):
        try:
            id=id.get('info_id')
            caseInit_sql="select * from case_suite_info where info_id ='"+id+"'"
            caseInit=getJsonFromDatabase(caseInit_sql)
            if caseInit:
                if caseInit[0]['init_data']:
                    caseInit=json.loads(caseInit[0]['init_data'])
                else:
                    caseInit=[]
            else:
                caseInit = []
            sql=''
            if id[0:3] =='API':
                sql = "select * from api_case_info WHERE  api_id ='" + id + "'"
            if id[0:3] =='DBC':
                sql = "select * from dbc_case_info WHERE  dbc_id ='" + id + "'"
            if id[0:3] =="SHL":
                sql = "select * from shell_case_info WHERE  shell_id ='" + id + "'"
            info_data = getJsonFromDatabase(sql)
            if info_data:
                if info_data[0]['init_data']:
                    infoInit=json.loads(info_data[0]['init_data'])
                else:
                    infoInit=[]
            else:
                infoInit=[]
            infoKeys=self.getKeys(infoInit)
            caseKeys=self.getKeys(caseInit)
            init_data=[]
            for i in caseKeys:
                if i in infoKeys:
                    index = caseKeys.index(i)
                    init_data.append(caseInit[index])
                else:
                    continue
            for j in infoKeys:
                if j in caseKeys:
                    continue
                else:
                    index = infoKeys.index(j)
                    init_data.append(infoInit[index])
            return_data=respdata().sucessMessage(init_data,'更新完成，请检查！～')
            return json.dumps(return_data,ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '獲取參數錯誤，請檢查！~~'+str(e))
            return json.dumps(return_data, ensure_ascii=False)

    def getKeys(self,data):
        '''
        [
        ["requestTime", "手工输入: 1524201463568", {"key": "requestTime", "arr_index": 0, "custom_val": "1524201463568", "assign_type": "custom"}],
        ["machineCode", "手工输入: 4ccc6aecb3f38863", {"key": "machineCode", "arr_index": 1, "custom_val": "4ccc6aecb3f38863", "assign_type": "custom"}]
        ]
        :param data:
        :return:
        '''
        keys_list=[]
        for i in data:
            keys_list.append(i[0])
        return keys_list
def test(caseKeys,infoKeys):
    caseInit=[["registerIp", "手工输入: 192.168.2.15", {"key": "registerIp", "arr_index": 0, "custom_val": "192.168.2.15", "assign_type": "custom"}], ["registerFrom", "手工输入: TUANDAI_BORROW_APP_ANDROID", {"key": "registerFrom", "arr_index": 1, "custom_val": "TUANDAI_BORROW_APP_ANDROID", "assign_type": "custom"}], ["telNo", "常用数据: 随机手机号", {"key": "telNo", "const_no": "1", "arr_index": 2, "assign_type": "normal"}], ["password", "手工输入: 123456a", {"key": "password", "arr_index": 3, "custom_val": "123456a", "assign_type": "custom"}]]
    infoInit=[["callBackParams", '', {}], ["registerFrom", "手工输入: TUANDAI_BORROW_APP_ANDROID测试", {"key": "registerFrom", "arr_index": 1, "custom_val": "TUANDAI_BORROW_APP_ANDROID测试", "assign_type": "custom"}], ["creditGrantingStatus", '', {}], ["password", "NULL", {"key": "password", "arr_index": 3, "custom_val": "123456a", "assign_type": "custom"}], ["telNo", "NULL", {"key": "telNo", "const_no": "1", "arr_index": 2, "assign_type": "normal"}], ["registerIp", "NULL", {"key": "registerIp", "arr_index": 0, "custom_val": "192.168.2.15", "assign_type": "custom"}]]

    init_data = []
    for i in caseKeys:
        if i in infoKeys:
            index = caseKeys.index(i)
            init_data.append(caseInit[index])
        else:
            continue
    for j in infoKeys:
        if j in caseKeys:
            continue
        else:
            index = infoKeys.index(j)
            init_data.append(infoInit[index])
    return init_data


if __name__ == '__main__':
    # data=[["callBackParams", null, {}], ["registerFrom", "手工输入: TUANDAI_BORROW_APP_ANDROID测试", {"key": "registerFrom", "arr_index": 1, "custom_val": "TUANDAI_BORROW_APP_ANDROID测试", "assign_type": "custom"}], ["creditGrantingStatus", null, {}], ["password", "NULL", {"key": "password", "arr_index": 3, "custom_val": "123456a", "assign_type": "custom"}], ["telNo", "NULL", {"key": "telNo", "const_no": "1", "arr_index": 2, "assign_type": "normal"}], ["registerIp", "NULL", {"key": "registerIp", "arr_index": 0, "custom_val": "192.168.2.15", "assign_type": "custom"}]]
    # # data=[]
    # a=INIT_OPT('').getKeys(data)
    # print(a)

    a=["registerIp","registerFrom","telNo","password"]
    b = ["callBackParams","registerFrom","creditGrantingStatus","password","telNo","registerIp"]
    print(test(a,b))