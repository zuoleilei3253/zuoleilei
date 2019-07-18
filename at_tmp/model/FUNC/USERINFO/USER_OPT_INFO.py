#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/31 10:41
# @Author  : bxf
# @File    : USER_OPT_INFO.py
# @Software: PyCharm
from  model.util.TMP_DB_OPT import *
from  model.FUNC.USERINFO.LOG_IN import *
from model.util.TMP_MODEL import *


'''
操作数据：
{
"opt_uri":"",
"opt_common":"",
"opt_user":"",
"opt_ip":"",

}
'''

class USER_OPT:
    def insertUserOpt(self,data):
        try:
            return_data=insertToDatabase("t_user_opt_info",toDict(data))
        except Exception as e:
            return "用户操作信息插入失败，请检查"+str(e)
