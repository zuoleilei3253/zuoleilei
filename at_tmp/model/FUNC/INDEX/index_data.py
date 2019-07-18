#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 8:47
# @Author  : bxf
# @File    : index_data.py
# @Software: PyCharm
from model.util.TMP_DB_OPT import *
import json
from model.util.PUB_RESP import *


class INDEX_DATA:
    def __init__(self,token):
        self.token=token

    def getData(self):
        sql="SELECT CURDATE() AS today,WEEKDAY(CURDATE())+1 AS wday,a.total AS reg,b.total AS online,0 AS oper FROM (SELECT '1' AS id,COUNT(1) AS total FROM p_user_info WHERE 1=1) a INNER JOIN (SELECT '1' AS id,COUNT(1) AS total FROM p_user_info WHERE DATE(login_time)=CURDATE()) b ON b.id=a.id"
        index_data=getJsonFromDatabase(sql)
        if index_data:
            return_data = json.dumps(respdata().sucessMessage(index_data[0], ''),cls=MyEncoder ,ensure_ascii=False)
            return return_data
        else:
            data=dict()
            data['today']=''
            data['wday']=''
            data['reg']=0
            data['online']=0
            data['oper']=0
            return_data=json.dumps(respdata().sucessMessage(data,''),ensure_ascii=False)
            return return_data