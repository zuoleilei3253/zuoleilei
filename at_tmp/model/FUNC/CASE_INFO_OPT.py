#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/18 17:29
# @Author  : bxf
# @File    : CASE_INFO.py
# @Software: PyCharm
import ast
import threading

from model.util.TMP_PAGINATOR import *
from model.util.PUB_RESP import *
from model.util.newID import *
from model.FUNC.SUITE.SUITE_OPT import *



class CASE_INFO_OPT:
    def __init__(self, table,token):
        self.table = table
        self.token=token
        self.username=getRealName(token)
        self.lock=threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=150)
    def get_lists(self, data, **kwargs):
        '''
        获取需求列表
        :return:
        '''
        try:

            page = data.get('_page')
            records = data.get('_limit')
            group_id=data.get('group_id')
            data = data.to_dict()
            del data['_page']
            del data['_limit']
            del data['group_id']
            sql_doc = ''
            for i in kwargs:
                col = i
                val = kwargs[i]
                sql_doc = ' WHERE ' + col + '="' + str(val) + '" And '
            sql = 'SELECT * FROM ' + self.table + '     ' + sql_doc +searchToDatabase('',data)
            case_lists = GET_RECORDS(sql, page, records)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
    def getDetail(self,data,**kwargs):
        '''
        获取明细
        :return:
        '''
        try:
            sql_doc = ''
            case_id=''
            for i in kwargs:
                col = i
                val = kwargs[i]
                case_id=str(val)
                sql_doc = ' WHERE ' + col + '="' + str(val)+'"  '
            sql = 'SELECT * FROM ' + self.table + '' + sql_doc
            # case_lists = GET_RECORDS(sql, page, records)
            detail=getJsonFromDatabase(sql)
            if detail:
                detail=detail[0]
                suite_data=SUITE_OPT().getLists(case_id)
                detail["suite_data"]=suite_data["suite_data"]
                return_data = respdata().sucessResp(detail)
            else:
                return_data = respdata().failMessage('','未找到该用例！~')
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)



    def getCoreLists(self,data):
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id=str(data.get('group_id'))
            sql = 'SELECT * FROM core_case_info  WHERE'
            case_lists = GET_RECORDS(sql, page, records,group_id=group_id,token=token)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def get_regress_lists(self,data):
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id=data.get('group_id')
            sql = 'SELECT * FROM regress_case_info  WHERE'
            regress_lists = GET_RECORDS_SQL(sql, page, records,group_id=group_id,token=self.token)
            data = regress_lists[0]
            case_list = regress_lists[2] #getJsonFromDatabase(regress_lists[1])
            tb_data = []
            if case_list:
                for i in case_list:
                    group_id_arr = i['group_id_arr']
                    #del i['group_id_arr']
                    i['group_id_arr'] = json.loads(group_id_arr)
                    tb_data.append(i)
            #else:
            #    tb_data = []
            data['tb_data'] = tb_data
            return_data = respdata().sucessResp(data)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
    def getRqmtCaseLists(self,data,**kwargs):
        try:

            page = data.get('_page')
            records = data.get('_limit')
            group_id=data.get('group_id')
            data = data.to_dict()
            del data['_page']
            del data['_limit']
            del data['group_id']
            sql_doc = ''
            for i in kwargs:
                col = i
                val = kwargs[i]
                sql_doc = ' WHERE ' + col + '="' + str(val) + '" And  '
            sql = 'SELECT * FROM ' + self.table + '     ' + sql_doc +searchToDatabase(' ',data)
            regress_lists = GET_RECORDS_SQL(sql, page, records, group_id=group_id, token=self.token)
            data = regress_lists[0]
            case_list = regress_lists[2]  # getJsonFromDatabase(regress_lists[1])
            tb_data = []
            if case_list:
                for i in case_list:
                    group_id_arr = i['group_id_arr']
                    # del i['group_id_arr']
                    if i['group_id_arr']:
                        i['group_id_arr']= json.loads(group_id_arr)
                    tb_data.append(i)
            # else:
            #    tb_data = []
            data['tb_data'] = tb_data
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
            case_id = newID().CS_ID()
            get_data.update(kwargs)
            group_id=getCode(get_data['group_id'])
            get_data['group_id']= group_id
            case_builder=self.username
            insert_result = insertToDatabase(self.table, get_data, case_id=case_id,case_builder=case_builder)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def regressInsert(self, data, **kwargs):
        '''
        新增
        :param data: 新增数据
        :return:
        '''
        try:
            get_data = json.loads(data)
            group_id_arr = get_data['group_id_arr']
            del get_data['group_id_arr']
            group_id_arr = json.dumps(group_id_arr)
            group_id = getCode(get_data['group_id'])
            get_data['group_id'] = group_id
            case_id = newID().CS_ID()
            get_data.update(kwargs)
            case_builder = self.username
            insert_result = insertToDatabase(self.table, get_data, case_id=case_id,group_id_arr=group_id_arr,case_builder=case_builder)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def coreInsert(self, data, **kwargs):
        '''
        新增
        :param data: 新增数据
        :return:
        '''
        try:
            get_data = json.loads(data)
            group_id_arr = get_data['group_id_arr']
            del get_data['group_id_arr']
            group_id_arr = json.dumps(group_id_arr)
            group_id = getCode(get_data['group_id'])
            get_data['group_id'] = group_id
            case_id = newID().CS_ID()
            get_data.update(kwargs)
            case_builder = self.username
            insert_result = insertToDatabase(self.table, get_data, case_id=case_id,group_id_arr=group_id_arr,case_builder=case_builder)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)





    def auto_insert(self, data, **kwargs):
        '''
        通过规则自动生成用例，插入数据库
        :param data:
        :param kwargs:
        :return:
        '''
        try:
            get_data = json.loads(data)
            get_data.update(kwargs)
            case_builder = self.username
            insert_result = insertToDatabase(self.table, get_data,case_builder=case_builder)
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
            del get_data['adddate']
            get_data['group_id'] =getCode(get_data['group_id'])
            update_result = updateToDatabase(self.table, get_data, case_id=case_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def rqmtCaseUpdate(self, data):
        '''
        修改
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)
            case_id = get_data['case_id']
            get_data['group_id'] = getCode(get_data['group_id'])
            del get_data['id']
            del get_data['adddate']
            update_result = updateToDatabase(self.table, get_data, case_id=case_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def delete(self,a,**kwargs):
        '''
        删除
        :param data:
        :return:
        '''
        sql_doc = ''
        for i in kwargs:
            col = i
            val = kwargs[i]
            sql_doc = ' WHERE ' + col + '="' + str(val) + '"'
        sql = 'DELETE FROM ' + self.table + sql_doc
        DB_CONN().db_Update(sql)
        if a==1:
            suite_sql='DELETE FROM ' + ' case_suite_info '+ sql_doc
            DB_CONN().db_Update(suite_sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def rqmtCaseDeleteOne(self,data,id):
        rqmt_id=data.get('rqmt_id')
        return self.deleteRqmtCase(rqmt_id,id)
    def deleteRqmtCase(self,rqmt_id,id):
        sql = 'DELETE FROM ' + self.table + ' WHERE case_id ="' + str(id) + '" AND rqmt_id="' + rqmt_id + '"'
        DB_CONN().db_Update(sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def regressDelete(self,data):

        get_data = json.loads(data)
        case_ids = get_data['case_ids']
        try:
            for i in case_ids:
                self.delete(1,case_id=i)
            return_data = respdata().sucessMessage('', '删除成功！')
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def rqmtCaseDelete(self,data):

        get_data = json.loads(data)
        case_ids = get_data['case_ids']
        rqmt_id=get_data['rqmt_id']
        try:
            for i in case_ids:
                self.deleteRqmtCase(rqmt_id, i)
            return_data = respdata().sucessMessage('', '删除成功！')
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)


    def rqmt_case_lists(self, data, **kwargs):
        '''
        手工任务获取
        :param kwargs:
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            id = kwargs['id']
            # sql='SELECT * FROM rqmt_case_info A INNER JOIN t_task_to_case B on  A.case_id = B.case_id  and B.task_id="'+id+'"      '

            sql = "SELECT C.case_real_result ,A.case_id,A.case_path,A.case_desc,A.case_exe_type,A.case_prev_data,IF(C.case_result,case_result,0) as case_result,A.adddate FROM rqmt_case_info A  INNER JOIN t_task_to_case B on  A.case_id = B.case_id  and B.task_id='" + id + "' LEFT JOIN rqmt_case_result C ON C.task_id=B.task_id and C.case_id =B.case_id     "
            case_lists = GET_RECORDS(sql, page, records)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def regress_case_lists(self,data,**kwargs):
        '''
               任务明细获取
                :param kwargs:
                :return:
                '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            id = kwargs['id']
            # sql='SELECT * FROM rqmt_case_info A INNER JOIN t_task_to_case B on  A.case_id = B.case_id  and B.task_id="'+id+'"      '

            # sql = "SELECT C.case_real_result,A.case_id,A.case_path,A.case_desc,A.case_exe_type,A.case_prev_data,IF(C.case_result,case_result,0) as case_result,A.adddate FROM regress_case_info A INNER JOIN t_task_to_case B on  A.case_id = B.case_id  and B.task_id='" + id + "' LEFT JOIN regress_case_result C ON C.task_id=B.task_id and C.case_id =B.case_id     "
            # sql="SELECT C.case_real_result,A.case_id,A.case_path,A.case_desc,A.case_exe_type,A.case_prev_data,IF(C.case_result,case_result,0) AS case_result,A.adddate FROM regress_case_info A INNER JOIN t_task_to_case B ON  A.case_id = B.case_id  AND B.task_id='"+id+"' LEFT JOIN (SELECT * FROM regress_case_result X WHERE ADDDATE=(SELECT MAX(ADDDATE) FROM regress_case_result Y WHERE X.task_id=Y.task_id AND X.case_id=Y.case_id)) C ON (C.task_id=B.task_id) AND C.case_id =B.case_id     "
            sql="SELECT C.batch_id,C.case_exe_result,M.case_id,B.case_path,B.case_desc,B.case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS num,IFNULL(C.case_result,0) AS case_result,IFNULL(C.case_real_result,'') as case_real_result,C.case_time,C.adddate FROM t_task_to_case M LEFT JOIN regress_task_info A ON A.task_id=M.task_id LEFT JOIN regress_case_info B ON B.case_id=M.case_id LEFT JOIN (SELECT S.num,T.* FROM regress_case_result T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,COUNT(1) AS num FROM regress_case_result GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE A.task_id='"+id+"'     "
            regress_lists = GET_RECORDS_SQL(sql, page, records)
            data = regress_lists[0]
            case_list =regress_lists[2] #getJsonFromDatabase(regress_lists[1])
            tb_data = []

            if case_list:
                for i in case_list:
                    group_id_arr = i.get('case_exe_result')
                    #del i['case_exe_result']
                    if group_id_arr==None or group_id_arr=='':
                        result_data ="该用例无日志数据，请检查数据库中regress_case_result 表中case_exe_result字段是否有值！"
                    else:
                        if "\\n'" in group_id_arr :
                            result_data=ast.literal_eval(group_id_arr.replace("\\n'",'\''))
                        else:
                            result_data=group_id_arr
                    i['case_exe_result'] = result_data
                    tb_data.append(i)

            data['tb_data'] = tb_data
            return_data = respdata().sucessResp(data)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def core_case_lists(self,data,**kwargs):
        '''
               任务明细获取
                :param kwargs:
                :return:
                '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            id = kwargs['id']
            # sql='SELECT * FROM rqmt_case_info A INNER JOIN t_task_to_case B on  A.case_id = B.case_id  and B.task_id="'+id+'"      '
            sql="SELECT C.batch_id,C.case_exe_result,M.case_id,B.case_path,B.case_desc,B.case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS num,IFNULL(C.case_result,0) AS case_result,IFNULL(C.case_real_result,'') as case_real_result,C.case_time,C.adddate FROM t_task_to_case M LEFT JOIN core_task_info A ON A.task_id=M.task_id LEFT JOIN core_case_info B ON B.case_id=M.case_id LEFT JOIN (SELECT S.num,T.* FROM core_case_result T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,COUNT(1) AS num FROM core_case_result GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE A.task_id='"+id+"'     "

            #sql = "SELECT C.case_real_result,A.case_id,A.case_path,A.case_desc,A.case_exe_type,A.case_prev_data,IF(C.case_result,case_result,0) as case_result,A.adddate FROM core_case_info A INNER JOIN t_task_to_case B on  A.case_id = B.case_id  and B.task_id='" + id + "' LEFT JOIN core_case_result C ON C.task_id=B.task_id and C.case_id =B.case_id     "
            #case_lists = GET_RECORDS(sql, page, records)
            regress_lists = GET_RECORDS_SQL(sql, page, records)
            data = regress_lists[0]
            case_list = regress_lists[2]  # getJsonFromDatabase(regress_lists[1])
            tb_data = []

            if case_list:
                for i in case_list:
                    group_id_arr = i['case_exe_result']
                    # del i['case_exe_result']
                    if group_id_arr == None or group_id_arr == '':
                        result_data = "该用例无日志数据，请检查数据库中regress_case_result 表中case_exe_result字段是否有值！"
                    else:
                        result_data = ast.literal_eval(group_id_arr.replace("\\n'", '\''))
                    i['case_exe_result'] = result_data
                    tb_data.append(i)

            data['tb_data'] = tb_data
            return_data = respdata().sucessResp(data)

            #return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
