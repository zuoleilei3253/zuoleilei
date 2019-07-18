#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 15:02
# @Author  : bxf
# @File    : FRAME_OPT.py
# @Software: PyCharm

# from model.FUNC.PLUGIN_OPT import *
import requests

from model.FUNC.WARNING.CHECK_DB import *
from model.util.newID import *


class COLLECT_DATA():
    def __init__(self, data):
        self.data = json.loads(data)

    def get_case_lists(self):
        case_lists = self.data['result_lists']
        return case_lists

    def save_result(self,fromdata=None):
        insert_data = dict()
        insert_data['task_id'] = self.data.get('task_id')
        #plugin_id = self.data.get('plugin_id')
        case_type = self.data.get('case_type')
        #batch_id = newID().BatchId()
        batch_id=self.data.get('batch_id')
        insert_data['batch_id'] = batch_id
        case_lists = self.get_case_lists()

        table = ''
        k = 0
        try:
            if case_type == '1':
                table = 'rqmt_case_result'
            elif case_type == '2':
                table = 'regress_case_result'
            elif case_type == '3':
                table = 'core_case_result'
            for i in case_lists:
                insert_data.update(i)
                insert_result = insertToDatabase(table, insert_data)
                k = k + insert_result
                exeLog("*****+=========框架插入测试结果成功，插入案例编号为： " + i["case_id"])
            exeLog("******+======测试结果插入成功，共插入用例：【" + str(k) + '】条！！')
            return_data = respdata().sucessMessage('', '插入成功')
            if fromdata:
                fromdict = json.loads(fromdata)
                type = fromdict.get('type')
            else:
                type = None
            if type==1:
                email_id = fromdict.get('email_id')
                batch_id = fromdict.get('batch_id')
                task_type = fromdict.get('taskType')
                group_id = fromdict.get('group_id')
                report_data = getHTML().get_html_rqmt(6, group_id, batch_id, task_type)
                Email_send(email_id).send_text(report_data)
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            exeLog("******+========插入失败，错误代码为: " + str(e))
            #plugin_status_t(0, plugin_id)
            return_data = respdata().failMessage('', '插入失败！~失败原因：' + str(e))
            return json.dumps(return_data, ensure_ascii=False)
def plugin_status_t(status, plugin_id):
    '''
    0-空闲中
    1-执行中
    2-执行完成
    3-插件异常

    :param status:
    :param plugin_id:
    :return:
    '''
    if status == 0:
        sql = "update t_plugin_info set plugin_status= 0 WHERE plugin_id='" + plugin_id + "'"
    elif status == 1:
        sql = "update t_plugin_info set plugin_status= 1 WHERE plugin_id='" + plugin_id + "'"
    elif status == 2:
        sql = "update t_plugin_info set plugin_status=2 WHERE plugin_id='" + plugin_id + "'"
    else:
        sql = "update t_plugin_info set plugin_status=3 WHERE plugin_id='" + plugin_id + "'"
    a = DB_CONN().db_Update(sql)
    return a