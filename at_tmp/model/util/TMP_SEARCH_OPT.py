#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-16 下午5:14
# @Author  : bxf
# @File    : SEARCH_OPT.py
# @Software: PyCharm


from model.util.TMP_PAGINATOR import *


class SEARCH_OPT:
    '''
    数据库搜索模块，主要是根据查询条件模糊搜索
    '''

    def __init__(self, sql, data):
        '''
        初始化参数
        :param sql:查询sql
        :param data: 查询数据
        '''
        self.data = data
        self.sql = sql + ' WHERE '

    @property
    def get_sql_doc(self):
        '''
        将查询内容转换成sql语句
        :return:
        '''
        del self.data['_page']
        del self.data['_limit']
        del self.data['group_id']
        sql_doc = ''
        for i in self.data.keys():
            key = i
            val = self.data[key]
            sql_doc = sql_doc + key + ' like "%' + val + '%"' + ' and '
        exeLog("模糊查询语句生成")
        return sql_doc[:-4]

    @property
    def searchByCol(self):
        '''
        查询模块
        :return:
        '''
        records = int(self.data['_limit'])
        page = int(self.data['_page'])
        sql_doc = self.get_sql_doc
        if sql_doc == '':
            sql = self.sql
        else:
            sql = self.sql + sql_doc + ' AND '
        result = GET_RECORDS(sql, page, records)
        return result


if __name__ == '__main__':
    sql = ''
    data = ''
    a = SEARCH_OPT(sql, data).searchByCol
    print(a)
