#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 18:14
# @Author  : bxf
# @File    : TASKT_INFO_OPT.py
# @Software: PyCharm

from model.util.TMP_PAGINATOR import *
from model.util.PUB_RESP import *
from model.util.newID import *


class TASK_INFO_OPT:
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
            group_id = data.get('group_id')
            sql_doc = ''
            for i in kwargs:
                col = i
                val = kwargs[i]
                sql_doc = ' WHERE ' + col + '="' + str(val) + '" GROUP BY rqmt_task_id And '
            sql = 'SELECT * FROM ' + self.table + '     ' + sql_doc
            case_lists = GET_RECORDS(sql, page, records)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)



    def get_lists_regress(self, data,token):
        '''
        获取需求列表
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')
            sql = 'SELECT * FROM ' + self.table + '   where online_time =(select max(online_time) from '+self.table+')    AND '
            case_lists = GET_RECORDS_SQL(sql, page, records,group_id,token)
            data=case_lists[0]
            task_sql = case_lists[1]
            print("任务查询sql")
            print(task_sql)
            tb_data=[]
            task_lsits=case_lists[2]#getJsonFromDatabase(task_sql)
            if task_lsits:
                for i in task_lsits:
                    tb_data.append(i)
            else:
                tb_data=[]
            data['tb_data']=tb_data

            return_data = respdata().sucessResp(data)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def insert(self, data, **kwargs):
        '''
        新增
        :param data: 新增数据
        :return:
        '''
        try:
            get_data = json.loads(data)
            get_data.update(kwargs)
            case_id = newID().CASE_ID()
            insert_result = insertToDatabase(self.table, get_data, case_id=case_id, )
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
            case_id = data.get('case_id')
            update_result = updateToDatabase(self.table, get_data, case_id=case_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def delete(self, task_id):
        '''
        删除
        :param data:
        :return:
        '''
        delete_sql = "delete A,B,C  from rqmt_task_info A left join t_task_to_case B on B.task_id=A.rqmt_task_id left join rqmt_case_result C on C.task_id=A.rqmt_task_id where A.rqmt_task_id='" + task_id + "'"
        DB_CONN().db_Update(delete_sql)
        exeLog("***********需求任务删除成功*******")
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def delete_regress(self, task_id):
        '''
                删除
                :param data:
                :return:
                '''
        delete_sql = "delete A,B,C  from regress_task_info A left join t_task_to_case B on B.task_id=A.task_id left join regress_case_result C on C.task_id=A.task_id where A.task_id='" + task_id + "'"
        DB_CONN().db_Update(delete_sql)
        exeLog("***********任务删除成功*******")
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def delete_core(self, task_id):
        '''
                删除
                :param data:
                :return:
                '''
        delete_sql = "delete A,B,C  from core_task_info A left join t_task_to_case B on B.task_id=A.task_id left join core_case_result C on C.task_id=A.task_id where A.task_id='" + task_id + "'"
        DB_CONN().db_Update(delete_sql)
        exeLog("***********任务删除成功*******")
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)