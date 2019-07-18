#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 10:54
# @Author  : bxf
# @File    : REGRESS_TO_CASE.py
# @Software: PyCharm
import json
from model.FUNC.CASE_INFO_OPT import *
import time
from model.util.PUB_RESP import *


class REGRESS_TO_CASE():
    def __init__(self, import_data):
        '''
        初始化参数
        :param import_data:
        '''
        self.import_data = json.loads(import_data)

    def process_data(self):
        '''
        加工数据
        :return:
        '''
        try:
            num = 0
            case_lists = []
            case_list = self.import_data['rqmt_data']
            if case_list!=[]:
                exeLog("******数据加工开始")
                start = time.time()
                for i in case_list:
                    del i['adddate']
                    del i['id']
                    del i['rqmt_id']
                    case_lists.append(i)
                end = time.time()
                time_num = str(end - start)[0:6]
                exeLog("*****数据加工完成，共加工数据：【" + str(num) + '】 条,用时：' + time_num)
                return_data=respdata().sucessMessage(case_lists,'cc')
                return json.dumps(return_data,ensure_ascii=False)
            else:
                return_data=respdata().failMessage('','无回归用例导入！~')
                return json.dumps(return_data,ensure_ascii=False)
        except Exception as e:
            exeLog("*****数据加工失败，错误为" + str(e))
            return False

    def regress_case(self,token):
        '''
        将数据添加到需求用例表中
        :return:
        '''
        rqmt_id = self.import_data['rqmt_id']
        case_lists = json.loads(self.process_data())
        num = 0
        # print(case_lists)
        if case_lists['code']==200:
            start = time.time()
            exeLog("*****插入数据库开始******")
            for i in case_lists['data']:
                # case_id = newID().RQMT_CASE_ID()
                # del i['group_id_arr']
                if i['group_id_arr']:
                    i['group_id_arr'] = []
                case_data = json.dumps(i)
                print(case_data)
                result = CASE_INFO_OPT('rqmt_case_info',token).auto_insert(case_data,  rqmt_id=rqmt_id)
                num += 1
            end = time.time()
            exe_time = str(end - start)[0:6]
            return_data = respdata().sucessMessage('', '回归用例插入完成，共插入用例：【' + str(num) + '】条，用时:' + exe_time)
            exeLog("****======END======*****回归用例插入完成*****")
            return json.dumps(return_data, ensure_ascii=False)
        else:
            exeLog("****插入数据库失败，请检查数据********")
            return_data = case_lists
            return json.dumps(return_data,ensure_ascii=False)
