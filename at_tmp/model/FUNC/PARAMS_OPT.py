#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 9:46
# @Author  : bxf
# @File    : PARAMS_OPT.py
# @Software: PyCharm
from model.util.TMP_DB_OPT import *
from model.FUNC.USERINFO.LOG_IN import *
from model.util.TMP_MODEL import *

class PARAMS_OPT:
    def __init__(self,token,info_id):
        self.userId=getUserid(token)
        self.info_id=info_id
    # 查询参数表中参数数据，有数据返回数据，无数据返回False
    def getData(self):
        sql="SELECT * FROM t_params_info WHERE info_id='"+str(self.info_id)+"' AND user_id ='"+str(self.userId)+"'"
        result=getJsonFromDatabase(sql)
        return result
    def insertData(self,init_data):

        init_dataa=toStr(init_data)
        sql= "INSERT INTO t_params_info (init_data,info_id,user_id) VALUE ('"+str(init_dataa)+"','"+self.info_id+"','"+str(self.userId)+"')"
        insert_result = DB_CONN().db_Update(sql)
        return insert_result
    def updateData(self,init_data):

        init_data = toStr(init_data)
        sql="UPDATE t_params_info SET init_data='"+init_data+"' WHERE info_id ='"+self.info_id+"' AND user_id ='"+self.userId+"'"
        insert_result = DB_CONN().db_Update(sql)
        return insert_result

    def saveParams(self,table,col,init_data):
        try:
            init_data=json.dumps(init_data,ensure_ascii=False)
            sql="UPDATE  "+table+"  SET init_data = '"+init_data+"' WHERE  "+col+"= '"+self.info_id+"'"
            insert_result = DB_CONN().db_Update(sql)
            return insert_result
        except Exception as e:
            print(str(e))


