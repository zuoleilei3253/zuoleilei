#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/31 14:09
# @Author  : bxf
# @File    : OPT_INFO.py
# @Software: PyCharm

from model.FUNC.USERINFO.USER_OPT_INFO import *
import wrapt
from flask import request
from concurrent.futures import ThreadPoolExecutor
'''
操作数据：
{
"opt_uri":"",
"opt_common":"",
"opt_user":"",
"opt_ip":"",

}
'''
def userOpt():
    @wrapt.decorator
    def optInsert(wrapped, instance, args, kwargs):
        opt_uri=request.path
        try:
            opt_common=request.get_data().decode()
        except Exception as e:
            opt_common={"opt":"该操作为文件请求"}
        opt_user=getUserid(request.headers.get('Token'))
        opt_ip=request.remote_addr
        data=dict()
        method=request.method
        common=dict()
        common['method']=method
        common['opt_data']=toDict(opt_common)
        data["opt_uri"]=opt_uri
        data["opt_common"]=toStr(common)
        data["opt_user"]=opt_user
        data["opt_ip"]=opt_ip
        with ThreadPoolExecutor(max_workers=10) as executor:
            future = executor.submit(USER_OPT().insertUserOpt,data)
        return wrapped(*args, **kwargs)

    return optInsert