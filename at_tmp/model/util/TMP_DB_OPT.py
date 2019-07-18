#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/15 16:16
# @Author  : bxf
# @File    : P_DB_OPT.py
# @Software: PyCharm

import pymysql
import json
from datetime import date, datetime
from model.util import md_Config
from model.util.PUB_LOG import *
from DBUtils.PooledDB import PooledDB

'''
提供数据的增删改查功能:



'''
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class DB_CONN(object):
    #__pool = None

    def __init__(self):
        #DB_CONN.get_mysql_conn()
        self.__pool = PooledDB(creator=pymysql,
                                              maxusage=None,
                                              maxconnections=200,
                                              mincached=20,
                                              maxcached=180,
                                              maxshared=180,
                                              blocking=True,
                                              host=md_Config.getConfig("DATABASE1", "IP"),
                                              port=int(md_Config.getConfig("DATABASE1", "port")),
                                              user=md_Config.getConfig("DATABASE1", "user"),
                                              passwd=md_Config.getConfig("DATABASE1", "password"),
                                              db=md_Config.getConfig("DATABASE1", "db"),
                                              charset=md_Config.getConfig("DATABASE1", "charset")
                                              )
        #exeLog("******创建连接池成功**************************")
        exeLog("数据库:【 " + md_Config.getConfig("DATABASE1", "db") + "】 连接成功！数据库环境为： " + md_Config.getConfig(
                        "DATABASE1",
                        "IP"))

    # @staticmethod
    # def get_mysql_conn():
    #     '''
    #     建立连接池
    #     :return: 返回连接池连接
    #     '''
    #     try:
    #         # print("test")
    #         if DB_CONN.__pool is None:
    #             DB_CONN.__pool = PooledDB(creator=pymysql,
    #                                       maxusage=None,
    #                                       maxconnections=200,
    #                                       mincached=20,
    #                                       maxcached=180,
    #                                       maxshared=180,
    #                                       host=md_Config.getConfig("DATABASE1", "IP"),
    #                                       port=int(md_Config.getConfig("DATABASE1", "port")),
    #                                       user=md_Config.getConfig("DATABASE1", "user"),
    #                                       passwd=md_Config.getConfig("DATABASE1", "password"),
    #                                       db=md_Config.getConfig("DATABASE1", "db"),
    #                                       charset=md_Config.getConfig("DATABASE1", "charset")
    #                                       )
    #             exeLog("******创建连接池成功**************************")
    #             exeLog("数据库:【 " + md_Config.getConfig("DATABASE1", "db") + "】 连接成功！数据库环境为： " + md_Config.getConfig(
    #                 "DATABASE1",
    #                 "IP"))
    #     except Exception as e:
    #         exeLog("***数据库:【 " + md_Config.getConfig("DATABASE1",
    #                                                  "db") + "】 连接失败，请检查连接参数！错误信息：%s" % e + "数据库环境为：" + md_Config.getConfig(
    #             "DATABASE1", "IP"))

    def db_Query_Json(self, sql,params=None):
        '''
        获取数据json格式游标，使用需要fetchall()或fetchone()fetchmany()
        :param sql: 查询语句
        :return: 游标json格式 使用时需要使用fetchall()或fetchone()fetchmaeeny()
        '''
        #self.conn = DB_CONN.__pool.connection()
        conn = self.__pool.connection()
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            if params:
                cur.execute(sql,params)
            else:
                cur.execute(sql)
            exeLog("***查询获取游标成功！查询语句为：" + sql)
            return cur
        except Exception as e:
            dataOptLog('***执行查询失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql)
        finally:
            cur.close()
            #self.conn.close()
            conn.close()

    #
    def db_Query_tuple(self, sql,params=None):
        '''
        获取数据元组格式游标，使用需要fetchall()或fetchone()fetchmany()
        :param sql: 查询语句
        :return: 元组格式游标，使用需要fetchall()或fetchone()fetchmany()
        '''
        #self.conn = DB_CONN.__pool.connection()
        conn = self.__pool.connection()
        cur = conn.cursor()
        try:
            if params:
                cur.execute(sql,params)
            else:
                cur.execute(sql)
            exeLog("***查询获取游标成功！查询语句为：" + sql)
            return cur
        except Exception as e:
            dataOptLog('***执行查询失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql)
        finally:
            cur.close()
            #self.conn.close()
            conn.close()

    # 数据库插入
    def db_Insert(self, sql, params):
        '''
        数据库插入
        :param sql: 插入语句
        :param params: 插入数据
        :return: 插入成功数目
        '''
        #self.conn = DB_CONN.__pool.connection()
        conn = self.__pool.connection()
        cur = conn.cursor()
        try:
            data_counts = cur.execute(sql, params)
            conn.commit()
            exeLog("***数据插入成功！执行语句为：" + sql)
            return data_counts
        except Exception as e:
            conn.rollback()
            exeLog('***插入失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql)
        finally:
            cur.close()
            #self.conn.close()
            conn.close()

    # 数据库更新
    def db_Update(self, sql,params=None):
        '''

        :param sql:
        :return:
        '''
        #self.conn = DB_CONN.__pool.connection()
        conn = self.__pool.connection()
        cur = conn.cursor()
        try:
            if params:
                data_counts=cur.execute(sql,params)
            else:
                data_counts = cur.execute(sql)
            conn.commit()
            exeLog("***更新数据成功！更新语句为：" + sql)
            return data_counts
        except Exception as e:
            conn.rollback()
            exeLog('***执行更新失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql)
        finally:
            cur.close()
            #self.conn.close()
            conn.close()

    def db_Batch(self, sql, params):

        #self.conn = DB_CONN.__pool.connection()
        conn = self.__pool.connection()
        cur = conn.cursor()
        try:
            data_counts = cur.executemany(sql, params)
            conn.commit()
            exeLog("***更新数据成功！更新语句为：" + sql)
            return data_counts
        except Exception as e:
            conn.rollback()
            exeLog('***执行更新失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql)
            return False, '***执行更新失败，请检查数据！错误信息：%s' % e + "查询语句为：" + sql
        finally:
            cur.close()
            #self.conn.close()
            conn.close()


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
    if  cur == None:
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


def insertToDatabase(table, data, **kwargs):
    '''

    :param table: 表名
    :param data: 插入数据
    :return: 插入成功数
    '''
    col_list = dict()
    col_list.update(data)
    col_list.update(kwargs)
    #table_data = {k: v for k, v in col_list.items() if v}
    table_data={}
    for k, v in col_list.items():
        if v:
            if isinstance(v,dict):
                v=json.dumps(v,ensure_ascii=False)
            elif not isinstance(v,str):
                v=str(v)

            table_data[k]=v
    key = ",".join(table_data.keys())
    value=tuple(table_data.values())
    sql = 'INSERT INTO ' + table + ' ( ' + key + ' ) VALUES %s'
    result = DB_CONN().db_Update(sql,(value,))
    # col_lists = col_list.keys()
    # col = ''
    # val = []
    # c = []
    # for i in col_lists:
    #     val_one = col_list[i]
    #     if val_one != None:
    #         val.append(str(val_one).replace("'","\\'"))
    #     else:
    #         c.append(i)
    # # 删除值为NONE的字段
    # for g in c:
    #     del col_list[g]
    #
    # for j in col_lists:
    #     col = col + j + ','
    # var_lists = tuple(val)
    # sql = 'INSERT INTO ' + table + ' ( ' + col[:-1] + ' ) VALUE ' + str(var_lists)
    # exeLog("******生成添加语句成功！~~***")
    # result = DB_CONN().db_Update(sql)
    exeLog("******记录新增成功******")
    return result


def updateToDatabase(table, data, **kwargs):
    '''

    :param table:表名
    :param data: 更新数据
    :param col: 定位
    :param val:定位值
    :return: 更新成功数
    '''
    table_data = {}
    for k, v in data.items():
        if v:
            if isinstance(v, dict):
                v = json.dumps(v, ensure_ascii=False)
            elif not isinstance(v,str):
                v=str(v)
            table_data[k] = v
    col_lists = tuple(table_data.keys())
    col_values=tuple(table_data.values())
    setvalue='=%s,'.join(col_lists)+'=%s'

    wherekey = tuple(kwargs.keys())
    where_value=tuple(kwargs.values())
    wherevalue='=%s AND '.join(wherekey)+'=%s'
    sql = "UPDATE " + table + ' SET ' + setvalue + ' WHERE '+wherevalue
    params=col_values+where_value
    result = DB_CONN().db_Update(sql,params)
    # list_one = ""
    # c = []
    # for i in col_lists:
    #     val_one = data[i]
    #     if val_one != None:
    #         list_one = list_one + i + "= '" + str(val_one).replace("'","\\'") + "',"
    #     else:
    #         c.append(i)
    #     # 删除值为NONE的字段
    # for g in c:
    #     del data[g]
    # sql_doc = ''
    # for i in kwargs:
    #     col = i
    #     val = kwargs[i]
    #     sql_doc = ' WHERE ' + col + "='" + str(val) + "' "
    # sql = "UPDATE " + table + ' SET ' + list_one[:-1] + sql_doc
    # exeLog("******生成更新语句成功！~~***")
    # # print(sql)
    # result = DB_CONN().db_Update(sql)
    exeLog("******记录更新成功******")
    return result


def searchToDatabase(table, data):
    '''
    生成like语句
    :param data:
    :return:
    '''
    col = ''
    for i in data.keys():
        key = i
        val = data[key]
        col = col + key + ' like "%' + val + '%" ' + ' and '
    return col
