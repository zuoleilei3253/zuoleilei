#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-4-19 下午2:18
# @Author  : bxf
# @File    : SQL_OPT.py
# @Software: PyCharm

# 通过ID获取环境参数
import json
import pymssql
from model.util.PUB_DATABASEOPT import *

# 通过ID获取环境参数
def getEnv(id):
    sql = 'select * from p_env_database_confg where id ="' + str(id) + '"'
    data = get_JSON(sql)

    return data[0]


# 读取数据库
class getEnvData:
    def __init__(self, id):
        self.id = id
        self.sqlParams = json.loads(getEnv(self.id))
        self.type = self.sqlParams['database_type']

    def getConn(self):
        if self.type == 'mysql':
            try:
                conn = pymysql.Connect(
                    host=self.sqlParams['database_host'],
                    port=int(self.sqlParams['database_port']),
                    user=self.sqlParams['database_user'],
                    passwd=self.sqlParams['database_pwd'],
                    db=self.sqlParams['database_name'],
                    charset='utf8'
                )
                return conn
            except Exception as e:
                # print(self.sqlParams['host'], self.sqlParams['db'], self.sqlParams['port'], self.sqlParams['passwd'])
                dataOptLog("Mysqldb Error:%s" % e)
                return False
        elif self.type == 'sqlserver':
            try:
                conn = pymssql.connect(host=self.sqlParams['database_host'],
                                       user=self.sqlParams['database_user'],
                                       passwd=self.sqlParams['database_pwd'],
                                       database=self.sqlParams['database_name'],
                                       charset="utf-8",
                                       as_dict=True)
                return conn
            except Exception as e:
                dataOptLog("Sqlserverdb Error:%s" % e)
                return False

    def exeQuery(self, sql):
        try:
            conn = self.getConn()
            # print(conn)
            if self.type == 'mysql':
                cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
                cur.execute(sql)
                # print('ccc')
                return cur
            else:
                cur = conn.cursor()
                cur.execute(sql)
                return cur
            # fco = cur.fetchall()
        except Exception as e:
            dataOptLog("Mysqldb Error:%s" % e)
        finally:
            cur.close()
            conn.close()

