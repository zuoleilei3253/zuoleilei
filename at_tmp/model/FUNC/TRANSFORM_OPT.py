#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 10:48
# @Author  : bxf
# @File    : TRANSFORM_OPT.py
# @Software: PyCharm
from concurrent.futures import ThreadPoolExecutor

from model.util.newID import *
from model.util.PUB_RESP import *
from model.FUNC.GROUP_OPT import *
import threading
import time

'''
"case_exe_type": "执行类型（1-手工、2-自动化）"
"case_type": "用例类型（1-功能测试，2-性能测试，3-安全测试，4-接口测试，5-压力测试，6-其他）"
"case_exe_plus-in": "执行插件（1-Platform，2-JMeter，3-Appium，4-Python，5-UIAutomation，6-无）",

rqmt_task_type:1-手工，2-自动化(JMeter)，3-自动化(Appium)，4-性能，5-安全

手工   执行类型

自动化 执行插件

用例类型

先以插件分类  生成自动任务  按照插件分类

将 插件分类为  无的
按照用例类型分类   生成  性能   安全 接口 压力等任务

再将  功能测试和接口测试类型的数据结合  生成  手工用例

'''


class TRANSFORM_OPT:
    '''
    转换基类
    '''

    def __init__(self, id, table,token):
        self.id = id
        self.table = table
        self.token=token
        self.lock=threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=100)

    @staticmethod
    def _get_rqmt_desc(rqmt_id):
        '''
        获取需求基本信息
        :return:
        '''
        sql = 'SELECT rqmt_desc FROM t_requirements_info WHERE rqmt_id="' + rqmt_id + '"'
        rqmt_desc = getJsonFromDatabase(sql)[0]['rqmt_desc']

        return rqmt_desc

    def transform_opt(self, **kwargs):
        '''
        case_exe_type 执行类型  1-手动 2-自动化
        case_exe_plugin 执行插件
        case_id 测试用例

         switch (val) {
                      case '100':
                        return '平台，对应手工测试'
                      case '200':
                        return '接口测试(平台)'
                      case '201':
                        return '接口测试(Python)'
                      case '202':
                        return '接口测试(JMeter)'
                      case '301':
                        return 'PC端UI测试(Python)'
                      case '401':
                        return '安卓端UI测试(Appium)'
                      case '402':
                        return '安卓端UI测试(UIAutomation)'
                      case '501':
                        return 'IOS端UI测试(Appium)'
                      case '901':
                        return '综合测试(RobotFramework)'
                    }

        '''
        sql_doc = ''
        #task_lists = dict()
        for i in kwargs:
            col = i
            val = kwargs[i]
            sql_doc = ' WHERE ' + col + ' like "' + str(val) + '%" and  case_exe_status = 1'
        case_lists_sql = 'SELECT * FROM ' + self.table + ' ' + sql_doc + ' '
        case_lists = getJsonFromDatabase(case_lists_sql)
        return case_lists
        # manual_lists = []
        # API_platform_lists = []#'接口测试(平台)'200
        # API_python_lists=[]#'接口测试(Python)'201
        # JMeter_lists = []#'接口测试(JMeter)'202
        # PC_AT_lists = []  # 'PC端UI测试(Python)'301
        # Appium_lists = []#'安卓端UI测试(Appium)'401
        # UIAutomation_lists = []#'安卓端UI测试(UIAutomation)'402
        # IOS_lists=[]#'IOS端UI测试(Appium)'501
        # RTF_lists=[]#'综合测试(RobotFramework)'901
        # if case_lists:
        #     for i in case_lists:
        #
        #         case_exe_plugin = i['case_exe_plugin']
        #         case_exe_type = i['case_exe_type']
        #         if case_exe_type == 1 or case_exe_plugin==100 :
        #             manual_lists.append(i)
        #         #else:
        #             #case_exe_plugin = i['case_exe_plugin']
        #         elif case_exe_plugin==200:
        #             API_platform_lists.append(i)
        #         elif case_exe_plugin==201:
        #             API_python_lists.append(i)
        #         elif case_exe_plugin==202:
        #             JMeter_lists.append(i)
        #         elif case_exe_plugin==401:
        #             Appium_lists.append(i)
        #         elif case_exe_plugin==301:
        #             PC_AT_lists.append(i)
        #         elif case_exe_plugin==402:
        #             UIAutomation_lists.append(i)
        #         elif case_exe_plugin==501:
        #             IOS_lists.append(i)
        #         elif case_exe_plugin==901:
        #             RTF_lists.append(i)
        #             # if case_exe_plugin == 1:
        #             #     platform_lists.append(i)
        #             # elif case_exe_plugin == 2:
        #             #     JMeter_lists.append(i)
        #             # elif case_exe_plugin == 3:
        #             #     Appium_lists.append(i)
        #             # elif case_exe_plugin == 4:
        #             #     Python_lists.append(i)
        #             # elif case_exe_plugin == 5:
        #             #     UIAutomation_lists.append(i)
        # else:
        #     pass
        # task_lists['manual_lists'] = manual_lists
        # task_lists['API_platform_lists'] = API_platform_lists
        # task_lists['API_python_lists'] = API_python_lists
        # task_lists['JMeter_lists'] = JMeter_lists
        # task_lists['Appium_lists'] = Appium_lists
        # task_lists['PC_AT_lists'] = PC_AT_lists
        # task_lists['UIAutomation_lists'] = UIAutomation_lists
        # task_lists['IOS_lists'] = IOS_lists
        # task_lists['RTF_lists'] = RTF_lists
        # return task_lists

    def insert_to_casetable(self, online_timea,group_id):
        if self.table == 'rqmt_case_info':
            online_time = ''
            task_lists = self.transform_opt(rqmt_id=self.id)
        elif self.table == 'regress_case_info':
            online_time = online_timea
            task_lists = self.transform_opt(group_id=group_id)
        elif self.table == 'core_case_info':
            online_time = online_timea
            task_lists = self.transform_opt(group_id=group_id)
        if task_lists:
            groupdict={}
            for i in task_lists:
                case_exe_plugin = i.get('case_exe_plugin')
                task_id=groupdict.get(str(case_exe_plugin))
                if not task_id:
                    task_id = newID().TK_ID()
                    groupdict[str(case_exe_plugin)]=task_id
                    self.insert_task_lists(task_id, case_exe_plugin, online_time, group_id)
                self.executor.submit(self.insert_case, task_id, i)

        # for key, val in task_lists.items():
        #     #listcase = task_lists.get(key)
        #     if len(val) == 0:
        #         pass
        #     else:
        #         task_id = newID().TK_ID()
        #         #time.sleep(1)
        #         for i in range(len(val)):
        #             #casedict = val[i]
        #             self.executor.submit(self.insert_case,task_id, val[i])
        #             #self.insert_case(task_id, val[i])
        #         if key == 'manual_lists':
        #             self.insert_task_lists(task_id, 100, online_time,group_id)
        #         elif key == 'API_platform_lists':
        #             self.insert_task_lists(task_id, 200, online_time,group_id)
        #         elif key == 'API_python_lists':
        #             self.insert_task_lists(task_id, 201, online_time,group_id)
        #         elif key == 'JMeter_lists':
        #             self.insert_task_lists(task_id, 202, online_time,group_id)
        #         elif key == 'Appium_lists':
        #             self.insert_task_lists(task_id, 401, online_time,group_id)
        #         elif key == 'PC_AT_lists':
        #             self.insert_task_lists(task_id, 301, online_time,group_id)
        #         elif key == 'UIAutomation_lists':
        #             self.insert_task_lists(task_id, 402, online_time,group_id)
        #         elif key == 'IOS_lists':
        #             self.insert_task_lists(task_id, 501, online_time,group_id)
        #         elif key == 'RTF_lists':
        #             self.insert_task_lists(task_id, 901, online_time,group_id)
        #         else:
        #             pass
        return_data = respdata().sucessMessage('', '任务转换完成，请查看！~')
        return json.dumps(return_data, ensure_ascii=False)

    def insert_task_lists(self, task_id, type, online_time,group_id):
        # group_id=GROP_OPT(self.token).getGroupID()
        try:
            if self.table == 'rqmt_case_info':
                rqmt_desc = TRANSFORM_OPT._get_rqmt_desc(self.id)
                rqmt_desc = rqmt_desc + '_需求测试用例'
                insert_sql_rqmt_task_info = 'INSERT INTO rqmt_task_info (rqmt_id,rqmt_task_id,rqmt_task_desc,rqmt_task_type,group_id) VALUES ("' + self.id + '" , "' + task_id + '" , "' + rqmt_desc + '" , "' + str(type)+'" , "' + str(group_id) + '" )'
            elif self.table == 'regress_case_info':
                rqmt_desc = '回归测试任务('+getGroupName(group_id)+')-'
                task_exe_env = '1'
                insert_sql_rqmt_task_info = 'INSERT INTO regress_task_info (task_id,task_desc,task_type,group_id,online_time,task_exe_env) VALUES ("' + task_id + '" , "' + rqmt_desc + '" , "' + str(
                    type) + '" , "' + str(group_id) + '" , "' + str(online_time) + '" , "' + task_exe_env + '" )'
            elif self.table == 'core_case_info':
                rqmt_desc = '核心测试任务('+getGroupName(group_id)+')-'
                task_exe_env = '1'
                insert_sql_rqmt_task_info = 'INSERT INTO core_task_info (task_id,task_desc,task_type,group_id,online_time,task_exe_env) VALUES ("' + task_id + '" , "' + rqmt_desc + '" , "' + str(
                    type) + '" , "' + str(group_id) + '" , "' + str(online_time) + '" , "' + task_exe_env + '" )'

            # num = DB_CONN().db_Update(insert_sql_rqmt_task_info)
            t = threading.Thread(target=DB_CONN().db_Update, args=(insert_sql_rqmt_task_info,))
            t.start()
            return True

        except Exception as e:
            exeLog("**********转换错误！！请检查，错误代码：" + str(e))
            return False

    def insert_case(self, task_id, case_list):
        '''
       插入数据库
        :param case_list:
        :param type:
        :return:
        '''
        try:
            case_id = case_list['case_id']
            insert_sql_task_to_case = 'INSERT INTO t_task_to_case (task_id,case_id) VALUES ("' + task_id + '","' + case_id + '" )'
            with self.lock:
                DB_CONN().db_Update(insert_sql_task_to_case)
            #t = threading.Thread(target=DB_CONN().db_Update, args=(insert_sql_task_to_case,))
            #t.start()
            # if self.table == 'rqmt_case_info':
            #     rqmt_desc = TRANSFORM_OPT._get_rqmt_desc(self.id)
            #     rqmt_desc = rqmt_desc + '_需求测试用例'
            #     insert_sql_rqmt_task_info = 'INSERT INTO rqmt_task_info (rqmt_id,rqmt_task_id,rqmt_task_desc,rqmt_task_type) VALUES ("' + self.id + '" , "' + task_id + '" , "' + rqmt_desc + '" , "' + str(
            #     type) + '" )'
            # else:
            #     rqmt_desc='回归测试用例——'
            #     task_exe_env='1'
            #     insert_sql_rqmt_task_info = 'INSERT INTO regress_task_info (task_id,task_desc,task_type,group_id,online_time,task_exe_env) VALUES ("'  + task_id + '" , "' + rqmt_desc + '" , "' + str(type) + '" , "' + str(self.id)+'" , "' + str(online_time)+'" , "' + task_exe_env+'" )'
            # num = DB_CONN().db_Update(insert_sql_rqmt_task_info)
            # exeLog("**********按照 " + str(type) + " 分类任务转换成功")
            return_data = respdata().sucessMessage('', '任务转换成功')
            return True
        except Exception as e:
            exeLog("**********转换错误！！请检查，错误代码：" + str(e))
            return False
