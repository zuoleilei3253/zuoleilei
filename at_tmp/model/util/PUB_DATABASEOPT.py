#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/16 15:11
# @Author  : bxf
# @File    : PUB_DATABASEOPT.py
# @Software: PyCharm
import pymysql
import json
from model.util import md_Config
from model.util.TMP_DB_OPT import *
from model.util.PUB_LOG import *
from model.util.ArrToJson import *
from datetime import date,datetime



class getJsonMysql:
    # 获取数据库连接
    def __init__(self):
        self.db = DB_CONN()
    '''
    def getConJson(self):
        try:
            conn = pymysql.Connect(
                host=md_Config.getConfig("DATABASE1", "IP"),
                port=int(md_Config.getConfig("DATABASE1", "port")),
                user=md_Config.getConfig("DATABASE1", "user"),
                passwd=md_Config.getConfig("DATABASE1", "password"),
                db=md_Config.getConfig("DATABASE1", "db"),
                charset=md_Config.getConfig("DATABASE1", "charset")
            )
            return conn
        except Exception as e:
            dataOptLog("Mysqldb Error:%s" % e)
    '''
    # 查询方法，使用con.cursor(MySQLdb.cursors.DictCursor),返回结果为字典
    def exeQueryJson(self, sql):
        '''
        conn = self.getConJson()
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cur.execute(sql)
            # fco = cur.fetchall()
            return cur
        except Exception as e:
            dataOptLog("Mysqldb Error:%s" % e)
        finally:
            cur.close()
            conn.close()
        '''
        return self.db.db_Query_Json(sql)

    def exeQuery(self, sql):
        '''
        conn = self.getConJson()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            # fco = cur.fetchall()
            return cur
        except Exception as e:
            dataOptLog("Mysqldb Error:%s" % e)
        finally:
            cur.close()
            conn.close()
        '''
        return self.db.db_Query_tuple(sql)
    # 带参数的更新方法,eg:sql='insert into pythontest values(%s,%s,%s,now()',params=(6,'C#','good book')

    def exeUpdateByParamJson(self, sql, params):
        '''
        con = self.getConJson()
        cur = con.cursor()
        try:
            count = cur.execute(sql, params)
            con.commit()
            return count
        except Exception as e:
            con.rollback()
            dataOptLog("Mysqldb Error:%s" % e)
            raise Exception('执行失败！')
        finally:
            cur.close()
            con.close()
        '''
        return self.db.db_Update(sql,params)
    # 不带参数的更新方法
    def exeUpdate(self, sql):
        '''
        con = self.getConJson()
        cur = con.cursor()
        try:
            count = cur.execute(sql)
            con.commit()
            return count
        except Exception as e:
            con.rollback()
            dataOptLog("Mysqldb Error:%s" % e)
        finally:
            cur.close()
            con.close()
        '''
        return self.db.db_Update(sql)
    def get_data(self, sql):
        '''
        con = self.getConJson()
        cur = con.cursor()
        try:
            cur.execute(sql)
            # result = cur.fetchone()
            result = cur.fetchall()
            return result
        except Exception as e:
            con.rollback()
            dataOptLog("Mysqldb Error:%s" % e)
        finally:
            cur.close()
            con.close()
        '''
        result=self.db.db_Query_tuple(sql)
        if result:
            return result.fetchall()


##获取数据库数据LIST[{},{}]格式
def get_JSON(sql):
    db = getJsonMysql()
    a = db.exeQueryJson(sql)
    # 默认获取查询的所有数据
    b = a.fetchall()
    return b


def get_data(sql):
    db = getJsonMysql()
    a = db.exeUpdate(sql)
    b = a.fetchall()

    return b


def changRaw(jsondata, type):
    key = jsonTokey(jsondata)
    restful = []
    for i in key:
        field = []
        field.append(i)
        field.append('NULL')
        if type == 'api':
            field.append({})
        restful.append(field)
    return restful


# 时间转换
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
