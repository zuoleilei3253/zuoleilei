#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 10:06
# @Author  : kimmy-pan
# @File    : REPORT_DATA.py


import sys
sys.path.append("/opt/ATEST")
import json



from model.util.PUB_DATABASEOPT import *


def table_num(report_data):
    '''

    :param report_data:
    {
        "batchNo" : "1243214",
        "table": "api_test_case_response",
        "field": "case_id",
        "value": "API-201711100001"
    }
    :return:
    '''
    try:
        sql = "SELECT * from {} WHERE batchNo = '{}'".format(report_data["table"], report_data["batchNo"])
        num = len(get_JSON(sql))
        return num
    except Exception as e:
        dataOptLog(e)


def Field_num(report_data):
    '''

    :param report_data:
    {
        "batchNo" : "1243214",
        "table": "api_test_case_response",
        "field": "case_id",
        "value": "API-201711100001"
    }
    :return:
    '''
    try:
        sql = "SELECT * from {} where {} = '{}'".format(report_data["table"], report_data["field"],
                                                        report_data["value"])
        num = len(get_JSON(sql))
        return num
    except Exception as e:
        dataOptLog(e)


def return_JSON(report_data):
    '''

    :param report_data:
    {
        "batchNo" : "1243214",
        "table": "api_test_case_response",
        "field": "case_id",
        "value": "API-201711100001"
    }
    :return: {"counts": 2, "batchNo": "1243214", "records": 34}
    '''
    try:
        result = {}
        # 批次号
        result["batchNo"] = report_data["batchNo"]
        # 表的总数目
        result["records"] = table_num(report_data)
        # 字段值的总数目
        result["counts"] = Field_num(report_data)
        return json.dumps(result)
    except Exception as e:
        dataOptLog(e)


def getRecords(bathcNo, type):
    db=getJsonMysql()
    sql = 'SELECT count(*) from t_test_result where batch_id="' + bathcNo + '"' + ' and diff_result ="' + type + '"'
    da = db.exeQuery(sql)
    count=da.fetchall()
    return count[0][0]


def getReport(batchNo):

    sql = 'SELECT A.case_id ,B.case_title,A.case_type,A.case_desc,A.response_data,A.diff_result,A.remark,A.exe_type from t_test_result A INNER JOIN task_list B ON A.case_id =B.case_id and A.sn=B.sn where A.batch_id ="'+batchNo+'"'
    # print(sql)
    records = get_JSON(sql)
    report = {}
    record = []
    for i in records:
        record.append(i)

    if record == []:
        return False
    else:

        report['records'] = record
        report['counts'] = len(records)

        report['passcounts'] = getRecords(batchNo, 'pass')
        report['failcounts'] = getRecords(batchNo, 'fail')
        report['errorcounts'] = getRecords(batchNo, 'error')

        return report


if __name__ == "__main__":
    print(getReport('BATCH-20180329-15045'))

