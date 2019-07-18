#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/17 16:16
# @Author  : bxf
# @File    : REGRESS_OPT.py
# @Software: PyCharm
from model.util.TMP_PAGINATOR import *
from model.util.PUB_RESP import *

class REGRESS_OPT:
    def get_lists(self, data,token):
        '''
        获取规则列表
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')
            sql = 'SELECT * FROM t_regress_case_info WHERE'
            case_lists = GET_RECORDS(sql, page, records,group_id=group_id,token=token)
            return_data = respdata().sucessResp(case_lists)
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
            get_data = json.loads(data)
            group_id=getCode(get_data['group_id'])
            del get_data['group_id']
            get_data['group_id']=group_id
            insert_result = insertToDatabase('t_regress_case_info', get_data)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + insert_result)
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
            get_data = json.loads(data)
            case_id = data.get('case_id')
            update_result = updateToDatabase('t_regress_case_info', get_data, case_id=case_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：'+str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def delete(self, data):
        '''
        删除
        :param data:
        :return:
        '''
        case_id = data.get('case_id')
        sql = 'DELETE FROM t_regress_case_info WHERE case_id ="' + case_id + '"'
        DB_CONN().db_Update(sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

if __name__ == '__main__':
    a=REGRESS_OPT().insert('a')
    print(a)