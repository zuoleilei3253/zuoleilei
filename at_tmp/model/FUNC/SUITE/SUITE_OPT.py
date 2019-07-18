#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 14:28
# @Author  : bxf
# @File    : SUITE_OPT.py
# @Software: PyCharm

from model.util.TMP_DB_OPT import *
from model.util.PUB_RESP import *
from model.util.PUB_DATABASEOPT import *
from model.FUNC.CASE_INFO_OPT import *


class SUITE_OPT:
    '''
    套件新增
    1.判断是否存在用例ID，
    1）存在，则更新原有ID
    2）不存在，则插入新的ID
    '''

    def getLists(self,case_id):
        suite_info = dict()
        try:
            suite_lists_sql="SELECT * FROM case_suite_info  WHERE case_id='"+case_id+"'"

            suite_lists=getJsonFromDatabase(suite_lists_sql)
            suite_data = []
            if suite_lists:
                for i in suite_lists:
                    info_id=i ["info_id"]
                    info_desc_sql="SELECT * FROM (SELECT api_id AS info_id,title AS info_desc FROM api_case_info  UNION ALL SELECT dbc_id AS info_id,dbc_desc AS info_desc FROM dbc_case_info UNION ALL  SELECT shell_id AS info_id,shell_desc AS info_desc FROM shell_case_info) b WHERE info_id='"+info_id+"'"
                    info_list=getJsonFromDatabase(info_desc_sql)[0]
                    info_list["init_data"]=json.loads(i["init_data"])
                    info_list["step_id"]=i["step_id"]
                    if i["polling"] is None:
                        info_list["polling"] = {'num': None, 'time': None, 'isrun': False}
                        # print(tail_data)
                    else:
                        info_list["polling"] = json.loads(i["polling"])
                    if i["tail_data"]:
                        info_list["tail_data"]=json.loads(i["tail_data"])
                    else:
                        info_list["tail_data"]=None
                    suite_data.append(info_list)
            else:
                suite_data=[]
            suite_info["suite_data"]=suite_data
            return suite_info
        except Exception as e:
            suite_info["suite_data"] = str(e)
            return suite_info
    def suiteInsert(self,data,type):
        '''
        测试套件插入
        :param data:
        :return:
        '''

        try:
            get_data = json.loads(data)
            #case_lists = get_data['suite_data']
            if "env_id" in get_data:
                del get_data['env_id']
            del get_data['suite_data']
            if type == 3:
                case_id = newID().CS_ID()
            else:
                del get_data['id']
                case_id =get_data['case_id']
            if type == 1:
                updateToDatabase("core_case_info", get_data, case_id=case_id)
            elif type == 2:
                updateToDatabase("regress_case_info", get_data, case_id=case_id)
            elif type == 3 :
                group_id =getCode(get_data['group_id'])
                del get_data['group_id']
                insertToDatabase("regress_case_info",get_data,case_id=case_id,group_id=group_id)
            self.suitcase(case_id,data)
            # db = getJsonMysql()
            # sql = 'select * from case_suite_info where case_id="' + case_id + '"'
            # sn = db.exeQuery(sql).rowcount
            #
            # case_num = len(case_lists)
            # for i in range(case_num):
            #     case_list = case_lists[i]
            #     step_id=case_list['step_id']
            #     info_id = case_list['info_id']
            #     if 'init_data' in case_list:
            #         init_data = json.dumps(case_list['init_data'],ensure_ascii=False)
            #     else:
            #         case_sql="SELECT * FROM (SELECT api_id AS info_id,init_data  FROM api_case_info) a UNION ALL SELECT * FROM (SELECT dbc_id AS info_id,init_data FROM dbc_case_info) b  WHERE info_id='"+info_id+"'"
            #         case_list = get_JSON(case_sql)[0]
            #         init_data = case_list['init_data']
            #
            #     if 'tail_data' in case_list:
            #
            #         tail_data=json.dumps(case_list['tail_data'],ensure_ascii=False)
            #         # print(tail_data)
            #     else:
            #         tail_data=json.dumps(None)
            #     if i in range(sn):
            #         sql="update case_suite_info set info_id=%s ,step_id=%s,tail_data=%s,init_data=%s where case_id=%s and sn=%s"
            #         params = (str(info_id), step_id, tail_data, init_data, case_id, str(i))
            #         db.exeUpdateByParamJson(sql, params)
            #         #db.exeQuery(sql)
            #     else:
            #         sql = 'INSERT into case_suite_info (case_id,sn,info_id,init_data,tail_data,step_id) VALUES(%s,%s,%s,%s,%s,%s)'
            #         params = (case_id, i, info_id, init_data, tail_data,step_id)
            #         db.exeUpdateByParamJson(sql, params)
            # if int(sn) > int(case_num):
            #     cd = range(sn)
            #     lis = cd[case_num:]
            #     for i in lis:
            #         del_sql = 'delete from case_suite_info WHERE  case_id ="' + case_id + '"  and  sn ="' + str(i) + '"'
            #         db.exeUpdate(del_sql)
            return_data = respdata().sucessMessage('', '保存成功！～')
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, ensure_ascii=False)

    def suitcase(self,case_id,data):
        get_data = json.loads(data)
        case_lists = get_data['suite_data']
        db = getJsonMysql()
        sql = 'select * from case_suite_info where case_id="' + case_id + '"'
        sn = db.exeQuery(sql).rowcount
        case_num = len(case_lists)
        for i in range(case_num):
            case_list = case_lists[i]
            step_id = case_list['step_id']
            info_id = case_list['info_id']
            if 'init_data' in case_list:
                init_data = json.dumps(case_list['init_data'], ensure_ascii=False)
            else:
                case_sql = "SELECT * FROM (SELECT api_id AS info_id,init_data  FROM api_case_info) a UNION ALL SELECT * FROM (SELECT dbc_id AS info_id,init_data FROM dbc_case_info) b  WHERE info_id='" + info_id + "'"
                case_list = get_JSON(case_sql)[0]
                init_data = case_list['init_data']

            if 'tail_data' in case_list:
                tail_data = json.dumps(case_list['tail_data'], ensure_ascii=False)
                # print(tail_data)
            else:
                tail_data = json.dumps(None)
            if 'polling' in case_list:
                polling = json.dumps(case_list['polling'], ensure_ascii=False)
                # print(tail_data)
            else:
                polling = json.dumps({'num': None, 'time': None, 'isrun': False})
            if i in range(sn):
                sql = "update case_suite_info set info_id=%s ,step_id=%s,tail_data=%s,init_data=%s ,polling=%s where case_id=%s and sn=%s"
                params = (str(info_id), step_id, tail_data, init_data,polling, case_id, str(i))
                db.exeUpdateByParamJson(sql, params)
                # db.exeQuery(sql)
            else:
                sql = 'INSERT into case_suite_info (case_id,sn,info_id,init_data,tail_data,step_id,polling) VALUES(%s,%s,%s,%s,%s,%s,%s)'
                params = (case_id, i, info_id, init_data, tail_data, step_id,polling)
                db.exeUpdateByParamJson(sql, params)
        if int(sn) > int(case_num):
            cd = range(sn)
            lis = cd[case_num:]
            for i in lis:
                del_sql = 'delete from case_suite_info WHERE  case_id ="' + case_id + '"  and  sn ="' + str(i) + '"'
                db.exeUpdate(del_sql)