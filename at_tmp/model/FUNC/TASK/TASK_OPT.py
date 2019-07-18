#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/5 10:58
# @Author  : bxf
# @File    : TASK_OPT.py
# @Software: PyCharm

from model.util.TMP_DB_OPT import *
from model.util.PUB_RESP import *


class TASK_OPT:
    def __init__(self,token):
        self.token=token

    def getTaskStatus(self,data):
        task_id = data.get('task_id')
        status_sql = "SELECT * FROM ((SELECT * FROM core_task_info) UNION ALL (SELECT * FROM regress_task_info)) T WHERE T.task_id='" + task_id + "'"
        task_data = getJsonFromDatabase(status_sql)
        if task_data:
            status_data = dict()
            status_data['status'] = task_data[0]['status']
            status_data['process_data'] = task_data[0]['process']
            status_data['exe_data']=task_data[0]['adddate']
        else:
            status_data = dict()
            status_data['status'] = 0
            status_data['process_data'] = 0
            status_data['exe_data'] = ''
        return_data = respdata().sucessMessage(status_data, '')
        return json.dumps(return_data,cls=MyEncoder, ensure_ascii=False)
