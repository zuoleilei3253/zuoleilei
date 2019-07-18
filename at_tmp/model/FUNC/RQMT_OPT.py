#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/16 17:11
# @Author  : bxf
# @File    : RQMT_OPT.py
# @Software: PyCharm

from model.util.TMP_PAGINATOR import *
from model.util.PUB_RESP import *
from model.util.newID import *


class RQMT_OPT:
    def get_lists(self, data,token):
        '''
        获取需求列表
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id=data.get('group_id')
            sql = 'SELECT * FROM t_requirements_info  WHERE'
            rqmt_lists = GET_RECORDS(sql, page, records,group_id=group_id,token=token)
            return_data = respdata().sucessResp(rqmt_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def insert(self, data):
        '''
        新增
        :param data: 新增数据
        :return:
        '''
        try:
            rqmt_id=newID().RQMT_ID()
            get_data=json.loads(data)
            rqmt_dever=get_data['rqmt_dever']
            rqmt_tester=get_data['rqmt_tester']
            rqmt_desc=get_data['rqmt_desc']
            group_id =getCode(get_data['group_id'])
            rqmt_end_date=get_data['rqmt_end_date']
            rqmt_begin_date = get_data['rqmt_begin_date']
            rqmt_status = get_data['rqmt_status']
            sql='INSERT INTO t_requirements_info (rqmt_dever, rqmt_tester, rqmt_desc, rqmt_end_date, rqmt_id,group_id,rqmt_begin_date,rqmt_status) VALUE(%s,%s,%s,%s,%s,%s,%s,%s)'
            params=(rqmt_dever, rqmt_tester, rqmt_desc, rqmt_end_date, rqmt_id,group_id,rqmt_begin_date,rqmt_status)
            insert_result = DB_CONN().db_Insert(sql,params)
            # insert_result=insertToDatabase('t_requirements_info',get_data,rqmt_id=rqmt_id)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))

            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('','新增失败，请检查！错误信息为：'+str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def update(self, data):
        '''
        修改
        :param data:
        :return:
        '''
        try:
            get_data=json.loads(data)
            rqmt_id = get_data['rqmt_id']
            update_result = updateToDatabase('t_requirements_info', get_data, rqmt_id=rqmt_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数：'+str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def delete(self, rqmt_id):
        '''
        删除
        :param data:
        :return:
        '''
        sql = 'DELETE A,B FROM t_requirements_info A LEFT JOIN rqmt_case_info B ON A.rqmt_id=B.rqmt_id WHERE A.rqmt_id="' + rqmt_id + '"'
        DB_CONN().db_Update(sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)


    def rqmtToregress (self,data):
        rqmt_id=json.loads(data)['rqmt_id']
        counts = int()
        try:
            rqmt_case_sql="SELECT * FROM rqmt_case_info WHERE rqmt_id= '"+rqmt_id+"'"
            rqmt_case=getJsonFromDatabase(rqmt_case_sql)
            if rqmt_case:
                rqmt_case=rqmt_case
            else:
                rqmt_case=[]
                return_data = respdata().failMessage('', '同步失败~~未获取到该需求下的用例，请检查是否有用例存在！～')
                return json.dumps(return_data, ensure_ascii=False)
            case_list =[]
            case_list_no_group_id =[]
            for i in rqmt_case:
                if i.get('group_id') == None or i.get('group_id') == '':
                    case_list_no_group_id.append(i.get('case_id'))
                else:
                    del i['adddate']
                    case_list.append(i)
            if case_list_no_group_id !=[]:
                return_data=respdata().failMessage('','同步失败，用例中存在未分组用例，清单如下：【'+str(case_list_no_group_id)+'】,请修改添加分组后提交')
                return json.dumps(return_data,ensure_ascii=False)
            else:
                for j in case_list:
                    case_id = j.get('case_id')
                    selectsql = "SELECT * FROM regress_case_info WHERE case_id='%s'" % ( case_id)
                    count = DB_CONN().db_Update(selectsql)
                    if count > 0:
                        update_counts = updateToDatabase('regress_case_info', j,case_id=case_id)
                        counts=counts+update_counts
                    else:
                        insert_counts =insertToDatabase('regress_case_info', j)
                        counts = counts + insert_counts
                return_data=respdata().sucessMessage('','同步成功,!~~请确认!~')
                return  json.dumps(return_data,ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '同步失败~~异常信息为~'+str(e))
            return json.dumps(return_data, ensure_ascii=False)
