#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/27 14:33
# @Author  : bxf
# @File    : CASE_RESULT_OPT.py
# @Software: PyCharm

'''
测试结果操作：
测试结果的列表获取 get_lists
测试结果的更新 insert_info
测试结果的数据统计 stats_info


'''

from model.util.TMP_PAGINATOR import *
from model.util.PUB_RESP import *
from model.util.TMP_DB_OPT import *
import time

class CASE_RESULT_OPT():
    def __init__(self, table):
        self.table = table

    def get_lists(self, data, **kwargs):
        '''
        获取需求列表
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql_doc = ''
            for i in kwargs:
                col = i
                val = kwargs[i]
                sql_doc = ' WHERE ' + col + '="' + str(val) + '" And '
            sql = 'SELECT * FROM ' + self.table + '     ' + sql_doc
            # print(sql)
            case_lists = GET_RECORDS(sql, page, records)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def insert_info(self, data):
        '''
        插入信息到数据库
        :return:
        '''
        try:
            get_data = json.loads(data)
            localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            insert_result = insertToDatabase(self.table, get_data,case_time=localTime)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def update(self, data):
        '''
        修改
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)
            case_id = get_data['case_id']
            update_result = updateToDatabase(self.table, get_data, case_id=case_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def result_update(self,data):
        '''
        修改用例结果状态
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)
            case_id = get_data['case_id']
            task_id = get_data['task_id']
            case_exe_type=get_data['case_exe_type']
            case_real_result=get_data['case_real_result']
            case_result=get_data['case_result']
            localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            #update_result_sql = updateToDatabase(self.table, get_data, case_id=case_id)
            update_result_sql = "update " +self.table+ " set case_exe_type ='"+str(case_exe_type)+"',case_time='"+str(localTime)+"',case_real_result='"+case_real_result+"',case_result='"+str(case_result)+"' where case_id ='"+case_id+"' And task_id ='"+task_id+"'  ORDER BY r_id DESC LIMIT 1"
            # print(update_result_sql)
            update_result=DB_CONN().db_Update(update_result_sql)

            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)




