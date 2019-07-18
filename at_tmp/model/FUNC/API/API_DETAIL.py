#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 11:04
# @Author  : bxf
# @File    : API_DETAIL.py
# @Software: PyCharm

from model.util.TMP_DB_OPT import *
from model.util.ArrToJson import *
from model.util.PUB_RESP import *

class getDatajson:
    def __init__(self, api_id):
        self.api_id = api_id
        sql = 'select * from t_api_info where api_id="' + self.api_id + '"'
        self.da = getJsonFromDatabase(sql)[0]
    def getDetail(self):
        try:
            data = dict()
            api_id = self.api_id
            uri = self.da['uri']
            method = self.da['method']
            title = self.da['title']
            headers = ''
            if self.da['headers'] == 'null':
                headers = []
            else:
                headers = (jsonToArr(json.loads(self.da['headers'])))
            if self.da['init_data']==None:
                restful=[]
            else:
                restful = json.loads(self.da['init_data'])
            raw = self.da['params']
            # return1 = self.da['return_1']
            # return2 = self.da['return_2']
            group_id = self.da['group_id']
            data['case_id'] = api_id
            data['uri'] = uri
            data['method'] = method
            data['case_desc'] = title
            data['headers'] = headers
            data['restful'] = restful

            data['raw'] = raw
            data['return_normal'] = return1
            data['return_abnormal'] = return2
            sql = 'select id from p_group_info where code ="' + group_id + '"'
            id = getJsonFromDatabase(sql)[0]['id']
            data['group_id'] = id
            return_data = resp(200, 'success', detail)
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            a = dict()
            a['response'] = '请求错误，错误信息为： ' + str(e)
            return json.dumps(resp(202, '请求失败', a), ensure_ascii=False)

    def getParams(self):
        try:
            data = dict()
            data["case_id"] = self.api_id

            data["init_data"] = changRaw(json.loads(self.da['params']), 'task')
            data["raw"] = self.da['params']
            # print(data)
            return_data = resp(200, 'success', data)
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            a = dict()
            a['response'] = '请求错误，错误信息为： ' + str(e)
            return json.dumps(resp(202, '请求失败', a), ensure_ascii=False)

    def initChange(self,data):
        getdata = json.loads(data)
        api_id = self.api_id
        sql = 'select init_data from t_api_info where api_id="' + api_id + '"'
        da = json.loads(getJsonFromDatabase(sql)[0]['init_data'])
        num = getdata['index']

        da[num][2] = getdata['params']
        init_param = dict()
        init_param = da
        init_data = json.dumps(init_param, ensure_ascii=False)
        asql = 'update t_api_info set init_data = %s where api_id = %s'
        params = (init_data, api_id)
        try:
            DB_CONN().db_Insert(asql, params)
            return_data = respdata().sucessResp('')
            return json.dumps(return_data)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data)