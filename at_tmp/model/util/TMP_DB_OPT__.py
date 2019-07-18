#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/15 16:36
# @Author  : bxf
# @File    : P_DB_OPT.py
# @Software: PyCharm

import pymysql
import json
from datetime import date, datetime
from model.util import md_Config
from model.util.PUB_LOG import *

'''
提供数据的增删改查功能:



'''


class DB_CONN():

    def __init__(self):
        '''
        初始化连接数据，并输出连接步骤
        '''
        try:
            conn = pymysql.Connect(
                host=md_Config.getConfig("DATABASE1", "IP"),
                port=int(md_Config.getConfig("DATABASE1", "port")),
                user=md_Config.getConfig("DATABASE1", "user"),
                passwd=md_Config.getConfig("DATABASE1", "password"),
                db=md_Config.getConfig("DATABASE1", "db"),
                charset=md_Config.getConfig("DATABASE1", "charset")
            )
            exeLog(
                "数据库:【 " + md_Config.getConfig("DATABASE1", "db") + "】 连接成功！数据库环境为： " + md_Config.getConfig("DATABASE1",
                                                                                                            "IP"))
            self.conn = conn

        except Exception as e:
            dataOptLog("***数据库:【 " + md_Config.getConfig("DATABASE1",
                                                         "db") + "】 连接失败，请检查连接参数！错误信息：%s" % e + "数据库环境为：" + md_Config.getConfig(
                "DATABASE1", "IP"))

    def db_Query_Json(self, sql):
        '''
        获取数据json格式游标，使用需要fetchall()或fetchone()fetchmany()
        :param sql: 查询语句
        :return: 游标json格式 使用时需要使用fetchall()或fetchone()fetchmany()
        '''
        cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cur.execute(sql)
            exeLog("***查询获取游标成功！查询语句为：" + sql)
            return cur
        except Exception as e:
            dataOptLog('***执行查询失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql)
        finally:
            cur.close()
            self.conn.close()

    #
    def db_Query_tuple(self, sql):
        '''
        获取数据元组格式游标，使用需要fetchall()或fetchone()fetchmany()
        :param sql: 查询语句
        :return: 元组格式游标，使用需要fetchall()或fetchone()fetchmany()
        '''
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            exeLog("***查询获取游标成功！查询语句为：" + sql)
            return cur
        except Exception as e:
            dataOptLog('***执行查询失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql)
        finally:
            cur.close()
            self.conn.close()

    # 数据库插入
    def db_Insert(self, sql, params):
        '''
        数据库插入
        :param sql: 插入语句
        :param params: 插入数据
        :return: 插入成功数目
        '''
        cur = self.conn.cursor()
        try:
            data_counts = cur.execute(sql, params)
            self.conn.commit()
            exeLog("***数据插入成功！执行语句为：" + sql)
            return data_counts
        except Exception as e:
            self.conn.rollback()
            dataOptLog('***插入失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql)
        finally:
            cur.close()
            self.conn.close()

    # 数据库更新
    def db_Update(self, sql):
        '''

        :param sql:
        :return:
        '''
        cur = self.conn.cursor()
        try:
            data_counts = cur.execute(sql)
            self.conn.commit()
            exeLog("***更新数据成功！更新语句为：" + sql)
            return data_counts
        except Exception as e:
            self.conn.rollback()
            dataOptLog('***执行更新失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql)
        finally:
            cur.close()
            self.conn.close()


# 数据库中时间转换json格式  在返回的json方法里加上cls=MyEncoder
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        '''
        针对datetime格式的转换
        :param obj: 参数数据
        :return: 返回json格式
        '''
        try:
            # if isinstance(obj, datetime.datetime):
            #     return int(mktime(obj.timetuple()))
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, obj)
        except Exception as e:
            return False


# 数据库数据直接转换成json格式输出 无数据 返回FALSE
def getJsonFromDatabase(sql):
    cur = DB_CONN().db_Query_Json(sql)
    if cur.rowcount == 0:
        exeLog("***数据库内容为空")
        return False
    else:
        exeLog("***返回JSON数据成功")
        return cur.fetchall()


def getTupleFromDatabase(sql):
    cur = DB_CONN().db_Query_tuple(sql)
    if cur.rowcount == 0:
        exeLog("***数据库内容为空")
        return False
    else:
        exeLog("***返回JSON数据成功")
        return cur.fetchall()


def insertToDatabase(table,data,**kwargs):
    '''

    :param table: 表名
    :param data: 插入数据
    :return: 插入成功数
    '''
    col_list=dict()
    # print(type(data))
    # print(type(kwargs))
    col_list.update(data)
    col_list.update(kwargs)
    col_lists=col_list.keys()
    col=''
    for j in col_lists:
        col=col+j+','

    val=[]
    for i in col_lists:
        val_one=col_list[i]
        val.append(val_one)
    var_lists=tuple(val)
    sql='INSERT INTO '+table +' ( '+ col[:-1] +' ) VALUE '+str(var_lists)
    exeLog("******生成添加语句成功！~~***")
    result=DB_CONN().db_Update(sql)
    exeLog("******记录新增成功******")
    return result

def updateToDatabase(table, data, col, val):
    '''
    更新
    :param table:表名
    :param data: 更新数据
    :param col: 定位
    :param val:定位值
    :return: 更新成功数
    '''
    col_lists = tuple(data.keys())
    list_one = ""
    for i in col_lists:
        val_one = data[i]
        list_one = list_one + i + '= "' + str(val_one) + '",'
    sql = "UPDATE " + table + ' SET ' + list_one[:-1] + ' WHERE ' + col + ' = "' + str(val) + '"'
    exeLog("生成更新语句成功！")
    return sql

