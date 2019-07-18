#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 11:09
# @Author  : bxf
# @File    : SEARCH_OPT.py
# @Software: PyCharm
from model.util.TMP_PAGINATOR import *
from model.FUNC.USERINFO.LOG_IN import *
from concurrent.futures import ThreadPoolExecutor
class SEARCH_OPT:
    def __init__(self,token,table):
        self.token=token
        self.table=table

    def searchOpt(self,data,cid=None):
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')
            data=data. to_dict()
            del data['_page']
            del data['_limit']
            del data['group_id']
            search_sql=''

            if 'info_id'in data:
                info_id=data['info_id']
                del data['info_id']
                search_sql="select * from regress_case_info A left JOIN case_suite_info B on B.case_id = A.case_id where B.info_id LIKE '%"+info_id+"%'    And" +searchToDatabase(self.table, data)
            elif self.table=='api_case_info':
                search_sql='SELECT IFNULL(b.case_total,0) AS case_total,a.* FROM api_case_info a LEFT JOIN (SELECT info_id,COUNT(1) AS case_total FROM (SELECT info_id,case_id FROM case_suite_info GROUP BY info_id,case_id) X GROUP BY info_id) b ON b.info_id=a.api_id WHERE '+searchToDatabase(self.table, data)
            elif self.table=='core_task':
                search_sql = "SELECT * FROM (SELECT A.task_id AS task_id ,B.group_id, C.batch_id,C.case_exe_result,M.case_id,B.case_path,B.case_desc,B.case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS num,IFNULL(C.case_result,0) AS case_result,IFNULL(C.case_real_result,'') as case_real_result,C.case_time,C.adddate FROM t_task_to_case M LEFT JOIN core_task_info A ON A.task_id=M.task_id LEFT JOIN core_case_info B ON B.case_id=M.case_id LEFT JOIN (SELECT S.num,T.* FROM core_case_result T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,COUNT(1) AS num FROM core_case_result GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) ) X WHERE task_id='" + cid + "'  AND " + searchToDatabase(self.table,data)
            elif self.table == 'regress_task':
                search_sql="SELECT * FROM (SELECT A.task_id AS task_id ,B.group_id, C.batch_id,C.case_exe_result,M.case_id,B.case_path,B.case_desc,B.case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS num,IFNULL(C.case_result,0) AS case_result,IFNULL(C.case_real_result,'') as case_real_result,C.case_time,C.adddate FROM t_task_to_case M LEFT JOIN regress_task_info A ON A.task_id=M.task_id LEFT JOIN regress_case_info B ON B.case_id=M.case_id LEFT JOIN (SELECT S.num,T.* FROM regress_case_result T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,COUNT(1) AS num FROM regress_case_result GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id)) X WHERE task_id='"+cid+ "'  AND " + searchToDatabase(self.table,data)
            else:
                search_sql ="SELECT * FROM "+self.table+"   WHERE " + searchToDatabase(self.table, data)
            with ThreadPoolExecutor(max_workers=10) as executor:
                future = executor.submit(GET_RECORDS, search_sql, page, records, group_id, self.token)
            result = future.result()
            # result = GET_RECORDS(search_sql, page, records, group_id=group_id, token=self.token)
            return_data = respdata().sucessResp(result)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
