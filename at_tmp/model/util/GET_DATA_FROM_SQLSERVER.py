#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/27 9:31
# @Author  : bxf
# @File    : GET_DATA_FROM_SQLSERVER.py
# @Software: PyCharm


import sys
sys.path.append("/opt/ATEST")


import pymssql
import json

from model.util import md_Config
from model.util.PUB_LOG import  *



class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8",as_dict=True)
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):

        try:
            cur = self.__GetConnect()
            cur.execute(sql)
            resList = cur.fetchall()
            # 查询完毕后必须关闭连接

            return resList
        except Exception as e:
            dataOptLog(e)
        finally:
            cur.close()
            self.conn.close()

    def ExecNonQuery(self, sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

        """
        获取字段名
        """

    def getTableName(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        a = cur.description
        return a


# 获取连接
def sqlExquery(sql):
    try:
        ms = MSSQL(
            host=md_Config.getConfig("SQLSERVER", "host"),
            user=md_Config.getConfig("SQLSERVER", "user"),
            pwd=md_Config.getConfig("SQLSERVER", "password"),
            db=md_Config.getConfig("SQLSERVER", "db")
        )
        relist = ms.ExecQuery(sql)
        return relist
    except Exception as e:
        dataOptLog("SQL SERVER 连接错误  " + str(e))


# def main(sql):
#     ms = MSSQL(host="10.100.11.129",user="td_fqb",pwd="tuandaiisverygood.0.2123",db="www_JunTe_com")
#     #获取数据库单元数据
#     resList = ms.ExecQuery(sql)
#     # print(range(len (resList)))
#     # print(resList)
#     #获取字段名称
#     lis=ms.getTableName(sql)
#     #将sqlserver数据库值转换成JSON
#     c=[]
#     for i in resList:
#         a = {}
#         for j in range(len(lis)):
#             a[str(lis[j][0])]=str(i[j])
#         c.append (json.dumps(a,ensure_ascii=False))
#         b=json.dumps(c)
#     return b





if __name__ == '__main__':
    a=sqlExquery("select id from UserBasicInfo where telno ='18416078394'")
    # b=json.dumps(a)
    print(a[0]['id'])
    print()
