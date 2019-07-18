#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/16 11:50
# @Author  : bxf
# @File    : TMP_PAGINATOR.py
# @Software: PyCharm
from concurrent.futures import ThreadPoolExecutor

from model.FUNC.GROUP_OPT import *
from model.util.TMP_DB_OPT import *
from model.util.PUB_LOG import *

class Paginator:
    """
    分页模块
主要是解决前端分页问题
输入 分页的每页记录数，分组id即可完成分页的数据返回
    """

    def __init__(self, records, sql, group_id=None,token=None):
        '''
        初始化分页类
        :param records:  每页显示数量
        :param sql: 要查询的sql
        :param group_id: 分组ID
        '''
        self.records = int(records)
        self.sql = sql
        self.group_id = group_id
        self.token=token
        self.pagesql=self.get_page_sql()


    def get_page_sql(self):
        '''
        获取数据查询sql语句
        :param group_id:分组ID
        :return: 数据查询sql
        '''

        page_sql=''
        if self.group_id == None :

            page_sql = self.sql[:-5] + ' order by adddate desc'
        elif self.group_id == '0':
            groupid=GROP_OPT(self.token).getGroupID()
            if groupid:
                if groupid=='1':
                    # 如果是最高权限 -1 的话 查询该表所有值
                    page_sql = self.sql[:-6] + ' order by adddate desc'
                else:
                    # 非最高权限查询该分组下下的数据
                    group_code=getCode(groupid)
                    page_sql = self.sql +' group_id like "' +str(group_code)+ '%" order by adddate desc'
        else:
            group_code = getCode(self.group_id)
            page_sql = self.sql + ' group_id like "' + str(group_code) + '%" order by adddate desc'
        # print(page_sql)
        return page_sql

    #@property
    def get_pages_num(self):
        '''
        根据records 分页数获取总页数
        :return: 页数
        '''
        countlist=getJsonFromDatabase(self.pagesql)
        if countlist:
            rec = len(countlist)
        else:
            rec = 0
        pages_num = rec % self.records
        if pages_num == 0:
            pages_num = rec // self.records
        else:
            pages_num = rec // self.records + 1
        return pages_num
    def get_num(self,countlist):
        '''
        根据records 分页数获取总页数
        :return: 页数
        '''
        count=int(countlist)
        if count==0:
            pages_num =0
        else:
            pages_num = count % self.records
            if pages_num == 0:
                pages_num = count // self.records
            else:
                pages_num = count // self.records + 1
        return pages_num
    def get_records_by_page(self, page):
        '''
        回去指定页的数据sql语句
        :param page: 指定页
        :return: 指定页的sql语句
        '''
        if page == 0:
            records_sql = self.pagesql
        else:
            records_start = str((int(page) - 1) * self.records)
            size = str(self.records)
            records_sql = self.pagesql + ' limit ' + records_start + ',' + size
        # print(records_sql)
        return records_sql

    #@property
    def get_records_counts(self):
        '''
        获取记录总数
        :return:
        '''
        records_cur = DB_CONN().db_Query_tuple(self.pagesql)
        records_counts = records_cur.rowcount
        return records_counts


# 返回格式
def GET_RECORDS(sql, page, records, group_id=None,token=None):
    '''
    返回分页后的数据
    :param sql: 查询的sql
    :param group_id: 分组ID
    :param pag: 查询页
    :param records: 每页记录数
    :return: 分页后的数据
    '''
    data = dict()
    paginator = Paginator(records, sql, group_id,token)
    data['page'] = page
    #exeLog("******获取页数成功，")
    data['group_id'] = group_id
    #exeLog("******获取分组ID 成功")
    execute=ThreadPoolExecutor(max_workers=20)
    try:
        records_list = execute.submit(getJsonFromDatabase, paginator.get_records_by_page(page))
        count=execute.submit(paginator.get_records_counts)
        #num=execute.submit(paginator.get_pages_num)
        data['total'] = int(count.result())
        num=paginator.get_num(data['total'])
        #data['total']=int(count.result())
        #data['pages']=num.result()
        data['pages'] = num
        td_data=records_list.result()
        data['tb_data']=td_data if td_data else []
        exeLog("******数据拼装成功")
    except Exception as e:
        exeLog("***返回分页数据异常，异常信息"+str(e))
    # data['page'] = page
    # exeLog("******获取页数成功，")
    # data['group_id'] = group_id
    # exeLog("******获取分组ID 成功")
    # data['total'] = int(paginator.get_records_counts())
    # exeLog("******获取总条数成功")
    # data['pages'] = paginator.get_pages_num()
    # exeLog("******获取总页数成功")
    # records_list = getJsonFromDatabase(paginator.get_records_by_page(page))
    # exeLog("******获取记录总数成功")
    # if records_list:
    #     data['tb_data'] = records_list
    # else:
    #     data['tb_data'] = []
    # exeLog("******数据拼装成功")
    return data


def GET_RECORDS_SQL(sql, page, records, group_id=None,token=None):
    '''
        返回分页后的数据
        :param sql: 查询的sql
        :param group_id: 分组ID
        :param pag: 查询页
        :param records: 每页记录数
        :return: 分页后的数据
        '''
    data = dict()
    paginator = Paginator(records, sql, group_id,token)
    # print(paginator.get_page_sql())
    data['page'] = int(page)
    #exeLog("******获取页数成功，")
    data['group_id'] = group_id
    #exeLog("******获取分组ID 成功")
    execute = ThreadPoolExecutor(max_workers=20)
    sqlresult=paginator.get_records_by_page(page)
    #sqlresult=''
    caselists=[]
    try:
        count = execute.submit(paginator.get_records_counts)
        execase=execute.submit(getJsonFromDatabase,sqlresult)
        #num = execute.submit(paginator.get_pages_num)
        #sql = execute.submit(paginator.get_records_by_page, page)
        data['total'] = int(count.result())
        num = paginator.get_num(data['total'])
        #data['pages'] =num.result()
        data['pages']=num
        caselists = execase.result()
        #sqlresult = sql.result()
        exeLog("******返回分页数据成功")
    except Exception as e:
        exeLog("***返回分页数据异常，异常信息" + str(e))

    # data['total'] = int(paginator.get_records_counts())
    # exeLog("******获取总条数成功")
    # data['pages'] = paginator.get_pages_num()
    # exeLog("******获取总页数成功")
    # records_sql = paginator.get_records_by_page(page)
    # print(records_sql)

    return data, sqlresult,caselists
