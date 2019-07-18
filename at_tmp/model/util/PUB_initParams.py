#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/23 16:10
# @Author  : bxf
# @File    : pub_exetask.py
# @Software: PyCharm


import sys

sys.path.append("/opt/ATEST")

from model.util.Analytic_JSON import *
from model.util.GET_PUB_DATA import *
from model.util.GET_DATA_FROM_SQLSERVER import *
from model.util.resultDiff import *
from model.util.PUB_REPL_JSON import *
from model.util.SQL_OPT import *
from model.util.GET_PARAM import *

"""
根据模块ID 执行模块内容
1.数据获取及赋值：
将获取的key值重新赋值给另一个字段key的值
 getTOvalue(tkey,fkey)  
 :return value
2.数据库读取及输出
fcol 需要返回的字段
 getFromsql(fcol,sql)
 :return sqldata

参数配置：


{isgive:  1,
data[
	{ceky:"key",cdata:[1获取方式,2参数1,3参数2]}
	{ceky:"key",cdata:[2,]}
]

}
例如：
{'isgive': 1,
            'data': [
                {'ckey': "a", 'cdata': [1, 'API-201801150010', "message"]},
                {'ckey': "key", 'cdata': [2, 'select * from ddd','mysql','213123']}

                {'ckey': "key", 'cdata': [3, '1']}
            ]
            }





isgive: 0-不需要赋值  1- 需要赋值
ckey:需要赋值的参数
cdata[1获取方式，2方式参数1，方式参数2]
获取方式：1.上行数据，2.数据库数据，3.常量，4.其他

1.上行数据  需要参数：case_id,key
2.数据库数据   需要参数：fcol 字段，sql 语句,database数据库类型
3.常量   需要参数： num  常量编号
1）.获取随机手机号
2）.获取身份证号
3）.获取UUID
4）.获取工行卡号
5).获取int类型数字
6).获取中文名字
4.通过手机号获取userID
需要参数：fcol字段，
5.默认，获取网页的callback值  UI专用
6.获取UI返回值专用

  {"restful": [
    ["form1", 
    1,
     {
      "assign_type": "upload",
      "upload_id": 777,
      "field": "name1"
    }
    ],

    ["form2",
     2,
      {
      "assign_type": "database",
      "database_field": "",
      "sql": "SQL语句",
      "database_type": "mysql",
      "database": 301144446
    }],
    ["form3",
     3,
      {"assign_type": "normal","const_no": "chinese_name"}
    ]
  ]}

"""

# 判断函数


'''
param  请求参数
dict 赋值参数配置

'''


def assData(requestParam, initpa):
    paramList = json.loads(initpa)
    newparam = requestParam
    for i in range(len(paramList)):
        if len(paramList[i]) != 2:
            key = paramList[i][0]
            param = paramList[i][2]
            if param == {}:
                newparam = requestParam
            elif param['assign_type'] == 'upload':
                case_id = param['upload_id']
                tkey = param["field"]
                value = getTovalue(case_id, tkey)
                newparam = giveValue(requestParam, key, value)
            elif param['assign_type'] == 'database':
                fcol = param['database_field']
                sql = param['sql']
                dataparamid = param['database']
                value = getFsql(fcol, sql, dataparamid)  # 需要增加参数，数据库配置ID-------------
                newparam = giveValue(requestParam, key, value)
            elif param['assign_type'] == 'normal':
                num = param['const_no']
                value = getcdata(num)
                # print(num)
                newparam = giveValue(requestParam, key, value)
            elif param['assign_type'] == 'custom':
                val = param['custom_val']
                newparam = giveValue(requestParam, key, val)
    return newparam


# 赋值
def getParams(initpa):
    paramList = initpa
    newparam = {}
    for i in range(len(paramList)):
        if len(paramList[i]) != 2:
            key = paramList[i][0]
            param = paramList[i][2]
            if param == {}:
                newparam.update({})
            elif param['assign_type'] == 'upload':
                case_id = param['upload_id']
                tkey = param["field"]
                value = getTovalue(case_id, tkey)
                newparam.update(changeData(key, value))
            elif param['assign_type'] == 'database':
                fcol = param['database_field']
                sql = param['sql']
                dataparamid = param['database']
                value = getFsql(fcol, sql, dataparamid)  # 需要增加参数，数据库配置ID-------------
                newparam = changeData(key, value)
            elif param['assign_type'] == 'normal':
                num = param['const_no']
                value = getcdata(num)
                newparam = changeData(key, value)
            elif param['assign_type'] == 'custom':
                val = param['custom_val']
                newparam.update(changeData(key, val))
    return json.dumps(newparam, ensure_ascii=False)


def giveData(data, params):
    if params == '{}':
        return data
    else:
        return GET_PARAM(params, data).GET_INIT_DATA()


def changeData(key, val):
    params = {}
    akey = key
    params[akey] = val
    return params


def giveData1(param, dict):
    isgive = returnDict1(dict, 'isgive')
    if isgive == 0:
        return param
    else:
        exdata = dict['data']

        for i in exdata:
            fkey = i['ckey']
            cdata = i['cdata']
            newparam = ''

            if cdata[0] == 1:
                case_id = cdata[1]
                tkey = cdata[2]
                value = getTovalue(case_id, tkey)
                newparam = giveValue(param, fkey, value)

            elif cdata[0] == 2:
                fcol = cdata[1]
                sql = cdata[2]
                database = cdata[3]
                value = getFromsql(fcol, sql, database)
                newparam = giveValue(param, fkey, value)
            elif cdata[0] == 3:
                num = cdata[1]
                value = getcdata(num)
                newparam = giveValue(param, fkey, value)
            elif cdata[0] == 4:
                case_id = cdata[1]
                sql = "SELECT * FROM UI_response WHERE case_id = '{}' ORDER BY adddate DESC LIMIT 1".format(case_id)
                telno = json.loads(getFromsql('resp_data', sql, 'MYSQL'))
                # print(telno['telno'])
                sqla = "select * from UserBasicInfo  where telno ='{}'".format(telno['telno'])
                userId = getFromsql('Id', sqla, '')
                # print(userId)
                newparam = giveValue(param, fkey, userId)
            elif cdata[0] == 5:
                case_id = cdata[1]
                sql = "SELECT * FROM UI_response WHERE case_id = '{}' ORDER BY adddate DESC LIMIT 1".format(case_id)
                resq = getFromsql('resp_data', sql, 'MYSQL')
                nparam = json.loads(resq)
                newparam = nparam['callback']
                # print(newparam)
            elif cdata[0] == 6:
                case_id = cdata[1]
                fcol = cdata[2]
                resq = json.loads(getFromUIsql(case_id))
                newparam = giveValue(param, fkey, resq[fcol])

        return newparam


# 获取上一步数据

'''
输入  key要获取的字段值
     sn 当前要赋值的 顺序号
输出   字段值

实现方式：
获取上一步返回值里的某个字段值

'''


def getToup(key, batch_id, sn):
    val = ''
    upSN = str(int(sn) - 1)
    sql = 'select response_data from test_result where batch_id="' + batch_id + '" and sn="' + upSN + '"'
    val = json.loads(get_JSON(sql)[0]['response_data'])

    getval = returnDict1(val, key)
    return getval


# 获取上行数据
def getTovalue(case_id, tkey):
    try:
        sql = "SELECT * FROM api_test_case_response WHERE case_id = '{}' ORDER BY adddate DESC LIMIT 1".format(case_id)
        responesdata = json.loads(getFromsql('response_result', sql, 'MYSQL'))
        back = returnDict1(responesdata, tkey)
        return back
    except Exception as e:
        print(e)


# 获取数据库数据
def getFromsql(fcol, sql, database):
    if database == 'MYSQL':
        try:
            db = getJsonMysql().exeQueryJson(sql)
            data = db.fetchone()[fcol]
            return data
        except Exception as e:
            return e
    else:
        try:
            a = sqlExquery(sql)[0][fcol]
            return a.__str__()  # UUID转换成str
        except Exception as e:
            return e


# 通过参数获取数据库数据
def getFsql(fcol, sql, id):
    db = getEnvData(id).exeQuery(sql)
    data = db.fetchall()[0][fcol]
    # print(data)
    return data.__str__()


# 给请求参数赋值
def giveValue(dict, key, val):
    try:
        a = replace_keyvalue(dict, key, val)
        return a
    except Exception as e:
        return e


# 获取UI返回值

def getFromUIsql(case_id):
    sql = "SELECT * FROM UI_response WHERE case_id = '{}' ORDER BY adddate DESC LIMIT 1".format(case_id)
    resq = getFromsql('resp_data', sql, 'MYSQL')
    return resq


"""
判断上行数据处理方式
isspec  1.特殊处理(使用如下的判断方式比对)，2.不特殊处理（返回值与预期值 直接比对，json_tools）
1.预期字段与实际返回字段比对  [field1,field2,field3] , dict1,dict2
# 2.预期数据库 与实际数据库字段比对 sql
3.预期字段与数据库数据比对 [ [key1,dict],[col,sql],[key1,dict],[col,sql],[key1,dict],[col,sql]]

入参
{
"data":[
{"type":"1","cdata":[[field1,field2,field3],dict1,dict2]}, 
{"type":"2","cdata":[sql1,sql2]},---另做
{"type":"3","cdata":["dict",["sql","type"],[[key1,col1],[key2,col2],....]]}

],
"isspec":1
}

输出

返回值：
{"result":
"true"/
"false"/
"error"
}

"""

'''
预期与实际字段比对


diffield(conm 字段,dict1 预期结果,dict2实际结果JSON)

数据库字段比对

diffsql(codict 要比对字段,sql实际结果)

预期结果与数据库字段比对
difftosql(prev预期结果字段,sql 实际结果)


'''

'''{
"data":[
{"type":"1","cdata":[field1,field2,field3]}, 
{"type":"2","cdata":[sql1,sql2]},---另做
{"type":"3","cdata":[["sql","type"],[[key1,col1],[key2,col2],....]]}
{"type":"4","cdata":[field1,field2]},
],
"isspec":1
}



"result":

 完全匹配
        {
          "judge_type": "complete",
          "prev_data": "返回结果"
        } 





        "result":
         预期与实际  字段匹配
         {
          "judge_type": "expect_match",
          "match_field": "匹配字段",（数组）
          "prev_data": "返回结果"
        }



        "result": 
        预期与数据库字段比对
        {
          "judge_type": "database_match",
          "database_field": "数据库字段",
          "sql": "SQL语句",
          "database_type": "数据库类型",
          "database": "数据库配置",
          "return_key": "返回结果KEY",
          "prev_data": "返回结果"
        } 
      ,
        "result":
         执行前后字段比对
         {
          "judge_type": "execute_match",
          "execute_before_key": "",
          "execute_before_val": "",
          "execute_after_key":  "",
          "execute_after_val":  "",
          "prev_data": "返回结果"
        } 









'''


# 判断入口

def diff(prev, resp, dict):
    if dict == {}:
        result = {'result': False}
        return result
    else:
        diff_params = dict

        diff_type = diff_params['judge_type']

        if diff_type == 'complete':
            # print('到这里了么？')
            result = diff_compelte(prev, resp)
            return result
        elif diff_type == 'expect_match':
            keys = dict['match_field']
            key_result = dif_key(resp, keys)
            if key_result['result']:
                result = diff_execute_match(prev, resp, keys)
            else:
                result = {'result': False}
            return result

        elif diff_type == 'database_match':
            data_field = dict['database_field']
            keys = dict['return_key']
            sql = dict['sql']
            database_id = dict['database']
            key_result = dif_key(resp, keys)
            if key_result['result']:
                result = diff_database_match(data_field, keys, sql, database_id, prev)
            else:
                result = {'result': False}
            return result

        else:
            a = '暂时无法支持先阶段判断方式'
            return a


# 完全匹配
def diff_compelte(prev, resp):
    prev = json.loads(prev)
    resp = json.loads(resp)
    diff = resultDiff().json_cmp(prev, resp)

    result = {}
    result['result'] = diff
    return result


# 字段匹配
def diff_expect_match(prev, resp, key):
    result = {}
    for i in key:
        pre = returnDict1(prev, i)
        res = returnDict1(resp, i)

        if res == pre:
            result['result'] = True
        else:
            result['result'] = False
            break
    return result


# 数据库匹配
def diff_database_match(data_field, key, sql, database_id, prev):
    db = getEnvData(database_id).exeQuery(sql)
    data = db.fetchall()[0]
    result = {}
    for i in range(len(key)):
        res = returnDict1(data, data_field[i])
        pre = returnDict1(prev, key[i])
        if res == pre:
            result['result'] = True
        else:
            result['result'] = False
            break

    return result


# 判断KEY值是否存在
def dif_key(resp, keys):
    result = {}
    for i in keys:
        if i in resp:
            result['result'] = True
        else:
            result['result'] = False
            break
    return result


# 执行前后比对
def diff_execute_match(prev, resp, keys):
    res = returnDict1(resp, keys)
    pre = returnDict1(prev, keys)
    result = dict()
    if res == pre:
        result['result'] = True
    else:
        result['result'] = False

    return result


#
#
# # 判断入口
# def diff_result(prev, resp, dict):
#     isspec = returnDict1(dict, 'isspec')
#     if isspec == '0':
#         result = {}
#         diff = resultDiff().json_cmp(prev, resp)
#         result['result'] = diff
#         return result
#
#     else:
#         exedata = returnDict1(dict, 'data')
#         for i in exedata:
#             type = i['type']
#
#             if type == '1':
#                 cdata = i['cdata']
#                 result = diff_expect_match(cdata, prev, resp)
#                 return result
#
#             elif type == '3':
#                 cdata = i['cdata']
#                 sqltype = cdata[0]
#                 field = cdata[1]
#                 result = dif_key_sql(resp, sqltype, field)
#                 return result
#             elif type == '4':
#                 cdata = i['cdata']
#                 result = dif_key(resp, cdata)
#                 return result
#

# 数据库比对
# def diff_bysql(sql,sqltype):
#     result={}
#     for i in sql:
#         if sqltype=='MYSQL':
#             db = getDataJson().exeQueryJson(sql)
#             prev=db.fetchone()
#
# # 字段与数据库数据比对 {"type":"3","cdata":["dict",["sql","type"],[[key1,col1],[key2,col2],....]]}
# def dif_key_sql(resp, sqltype, field):
#     result = {}
#     sql = sqltype[0]
#     type = sqltype[1]
#     pre = resp
#     if type == "MYSQL":
#         db = getDataJson().exeQueryJson(sql)
#         res = db.fetchone()
#     else:
#         res = sqlExquery(sql)[0]
#
#     for i in field:
#         pr = returnDict1(pre, i[0])
#         re = returnDict1(res, i[1])
#         if re == pr:
#             result['result'] = True
#         else:
#             result['result'] = False
#             break
#     return result


# 判断KEY值是否存在


# 任务数据插入：

'''
time_id：定时任务编号  newID().TIME_Id()
task_id:任务编号
timing_url:定时任务环境
timing_status：任务状态
timing_progress：任务进度
timing_count：执行次数
timing_cycle：周期
start_time：起始时间
isrun：是否启动定时
adddate：添加时间
content：备注
'''

if __name__ == '__main__':


    request={}
    #
    # print(getToup('redirectUrl','BATCH-20180329-93543','1'))

    # prev={"requestUri": "/recharge/threeAccount", "message": "第三方订单已经存在，请勿重复提交", "code": "RECHARGE_ORDER_EXISTS"}

    #
    # resp={"code": "RECHARGE_ORDER_EXISTS", "requestUri": "/recharge/threeAccount", "message": "第三方订单已经存在，请勿重复提交"}
    # dictf={'judge_type': 'complete'}
    # result = diff(prev, resp, dictf)
    # print(result)
