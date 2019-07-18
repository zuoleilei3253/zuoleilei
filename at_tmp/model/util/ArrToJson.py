#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/27 19:27
# @Author  : bxf
# @File    : ArrToJson.py
# @Software: PyCharm
import json
import re
import sys
import time

sys.path.append("/opt/ATEST")


def toJson(a):
    b = dict()
    if len(a) != 0:
        for i in range(len(a)):
            b[a[i][0]] = a[i][1]
        return b
    else:
        return None


# 获取KEY值列表
keyList = []


def jsonTofield(jsonb):
    jsona = jsonb
    for key in jsona:
        keyList.append(key)
        b = jsona[key]
        if isinstance(b, dict):
            jsonTofield(b)
    return keyList


def gobalDel():
    global keyList
    keyList = []
    return


def jsonTokey(jsonb):
    a = jsonTofield(jsonb)
    gobalDel()
    return a


# 将JSON value转换成LIST

def jsonToArr(jsona):
    jsonList = []
    for key in jsona:
        List = []
        List.append(key)
        List.append(jsona[key])
        jsonList.append(List)

    return jsonList

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
def analysicResultJson(requestfile,fromdata):
    resultjson = requestfile.read().decode()
    resultdict = json.loads(resultjson)
    fromdict=json.loads(fromdata)
    batch_id = fromdict.get('batch_id')
    case_type = fromdict.get('case_type')
    task_id = fromdict.get('task_id')
    case_exe_type = "UI测试"
    case_executor = "uiautotest"
    result_lists = []
    case_exe_data = {}
    case_exe_data['batch_id'] = batch_id
    case_exe_data['case_type'] = case_type
    case_exe_data['task_id'] = task_id
    assertFail = '(Assertion Failed:.*?)\''
    for feature in resultdict:
        elements = feature.get('elements')
        if elements:
            for scenario in elements:
                caseresult = {}
                case_id = scenario.get('tags')[0].get('name')
                caseresult['case_id'] = case_id
                caseresult['case_exe_type'] = case_exe_type
                caseresult['case_executor'] = case_executor
                steps = scenario.get('steps_S')
                case_exe_result = []
                case_exe_time = 0
                for step in steps:
                    keyword = step.get('keyword')
                    name = step.get('name')
                    result = step.get('result').get('status')
                    line = keyword + " " + name
                    case_exe_result.append(line+'\n')
                    if result == 'failed':
                        error_message = step.get('result').get('error_message')
                        faillist = re.findall(assertFail, error_message)
                        if faillist:
                            case_real_result = ','.join(faillist)
                        else:
                            case_real_result = '脚本执行错误'
                        #case_real_result = error_message
                        case_result = 2
                        case_exe_result.append(error_message+'\n')
                        break
                    else:
                        case_result = 1
                        case_real_result = "实际结果与预期结果一致"
                    duration = str(step.get('result').get('duration'))
                    if '.' in duration:
                        index = duration.index('.')
                        case_exe_time += float(duration[0:index + 2])
                    else:
                        duration
                        case_exe_time += float(duration)
                caseresult['case_exe_time'] = str('%.2f'%(case_exe_time*1000))+'ms'
                caseresult['case_real_result'] = case_real_result
                caseresult['case_exe_result'] = json.dumps(case_exe_result, ensure_ascii=False)
                caseresult['case_result'] = case_result
                caseresult['case_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                result_lists.append(caseresult)
    case_exe_data['result_lists'] = result_lists
    jsondata=json.dumps(case_exe_data, ensure_ascii=False)
    return jsondata





if __name__ == '__main__':
    # a = [['32131', '321'],['ssss1', '321'],['qqqqq', '321']]
    #
    # b = []
    # print(toJson(a))
    jsona = {'systemName': 'TDSYSTEM', 'sourceDevice': 'PC',
             'reqData': {'platfromUserName': 'string', 'requestNo': 'string', 'platformUserNo': 'string'},
             'serverName': 'string'}
    print(jsonTokey(jsona))
