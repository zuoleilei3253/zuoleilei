#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 17:17
# @Author  : bxf
# @File    : WARNING_OPT.py
# @Software: PyCharm
from model.util.TMP_PAGINATOR import *
from model.util.newID import *


class WARNING_OPT:
    def __init__(self,table):
        self.table=table

    def warningInsert(self,data,**kwargs):

        '''
        新增
        :param data: 新增数据
        :return:
        '''
        try:
            get_data = json.loads(data)
            warning_id=newID().WN_ID()
            warning_email_id=json.dumps(get_data["warning_email_id"])
            warning_desc=get_data["warning_desc"]
            warning_info=json.dumps(get_data["warning_info"])
            warning_type=get_data['warning_type']
            warning_sql="INSERT INTO w_warning_info ( warning_id,warning_email_id,warning_desc,warning_info,warning_type ) VALUE (%s,%s,%s,%s,%s)"
            params = (warning_id,warning_email_id,warning_desc,warning_info,warning_type )
            insert_result = DB_CONN().db_Insert(warning_sql,params)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def get_lists(self, data, **kwargs):
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id=data.get('group_id')
            sql_doc = ''
            for i in kwargs:
                col = i
                val = kwargs[i]
                sql_doc = ' WHERE ' + col + '="' + str(val) + '" And '
            sql = 'SELECT * FROM ' + self.table + '     ' + sql_doc
            case_lists = GET_RECORDS(sql, page, records)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
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
    def delete(self, **kwargs):
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
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)