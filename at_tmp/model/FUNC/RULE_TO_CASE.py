#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 10:24
# @Author  : bxf
# @File    : RULE_TO_CASE.py
# @Software: PyCharm
from model.util.TMP_DB_OPT import *
from model.FUNC.CASE_INFO_OPT import *
import re
from model.util.PUB_RESP import *
import time
from model.util.PUB_LOG import *

'''
规则转化

'''

class RULE_TO_CASE():
    def __init__(self, import_data):
        '''
        初始化规则ID
        :param rule_id:规则ID
        '''
        self.import_data = json.loads(import_data)
    def get_case_model(self, rule_id):
        '''
        获取用例模板
        :return:
        '''
        sql = "SELECT * FROM rule_case_info WHERE rule_id='{}'".format(rule_id)
        case = getJsonFromDatabase(sql)
        exeLog("***获取案例模板成功********")
        return case

    def transform_rule(self):
        '''
        用例转换
        :return:
        '''
        exeLog("***开始用例转换********")
        num = 0
        # exeLog(self.import_data)
        case_lists = []
        for g in self.import_data['rule_data']:
            rule_id = g['rule_id']
            # rule = self.get_import_prj()
            rule = g['rule_import_project']
            b = {}
            if rule == []:
                case_list = []
                case_model = self.get_case_model(rule_id)
                if case_model:
                    for j in range(len(case_model)):
                        num+=1
                        case_model[j]['case_desc'] = case_model[j]['rule_case_desc']
                        case_model[j]['case_path'] = case_model[j]['rule_case_path']
                        del case_model[j]['rule_case_desc']
                        del case_model[j]['c_id']
                        del case_model[j]['adddate']
                        del case_model[j]['rule_id']
                        del case_model[j]['rule_case_id']
                        del case_model[j]['rule_case_path']
                        del case_model[j]['rule_case_step']
                        case_list.append(case_model[j])
                    return_data = respdata().sucessMessage(case_list, "***转换用例成功********共计生成用例： " + str(num) + " 条。")
                    return return_data
                else:
                    exeLog("***转换用例失败，请检查规则数据*****，规则ID 为：" + rule_id)
                    return_data = respdata().failMessage('', "***转换用例失败，请检查规则数据*****，规则ID 为：" + rule_id)
                    return return_data
            else:
                for i in rule:
                    for k, v in i.items():
                        key = "${" + k + "}"
                        b[key] = v
                    case_model = self.get_case_model(rule_id)
                    if case_model:
                        for j in range(len(case_model)):
                            case_list = case_model[j]['rule_case_step']
                            case_model[j]['case_desc'] = case_model[j]['rule_case_desc']
                            case_model[j]['case_path'] = case_model[j]['rule_case_path']
                            del case_model[j]['rule_case_desc']
                            del case_model[j]['c_id']
                            del case_model[j]['adddate']
                            del case_model[j]['rule_id']
                            del case_model[j]['rule_case_id']
                            del case_model[j]['rule_case_path']
                            # for k, v in i.items():
                            #     if k in case_list:
                            #         pass
                            #     else:
                            #         exeLog("***rule_id:{},{}字段不存在rule_case_info表".format(rule_id, k))
                            #         return_data = respdata().failMessage('', "***rule_id:{},{}字段不存在rule_case_info表".format(
                            #             rule_id, k))
                            #         return return_data
                            rx = re.compile('|'.join(map(re.escape, b)))

                            def one_xlat(match):
                                # exeLog(match)
                                return b[match.group(0)]
                            num += 1
                            case_step = rx.sub(one_xlat, case_list)
                            case_model[j]['case_step'] = case_step
                            del case_model[j]['rule_case_step']
                            case_lists.append(case_model[j])
                    else:
                        exeLog("***转换用例失败，请检查规则数据*****，规则ID 为：" + rule_id)
                        return_data = respdata().failMessage('', "***转换用例失败，请检查规则数据*****，规则ID 为：" + rule_id)
                        return return_data
        exeLog("***转换用例成功********共计生成用例： " + str(num) + " 条。")
        return_data = respdata().sucessMessage(case_lists, "***转换用例成功********共计生成用例： " + str(num) + " 条。")
        return return_data
    def rule_to_case(self,token):
        '''
        将转换结果添加到需求用例数据库
        :return:
        '''
        start_time=time.time()
        case_lists = self.transform_rule()
        rqmt_id = self.import_data['rqmt_id']
        # group_id=self.import_data['group_id']
        num = 0
        if case_lists['code'] == 200:
            exeLog("***判断是否可以插入数据库****")
            for i in case_lists['data']:
                exeLog("***开始插入数据库*****")
                case_id = newID().RQMT_CASE_ID()
                i['case_exe_type']=1
                i['case_exe_env'] = 1
                i['group_id'] = 1
                # i['group_id'] = group_id
                case_data = json.dumps(i)
                result = CASE_INFO_OPT('rqmt_case_info',token).auto_insert(case_data, case_id=case_id, rqmt_id=rqmt_id)
                exeLog("***插入数据库完成*****")
                num += 1
            end_time=time.time()
            exe_time=str(end_time-start_time)[0:6]
            return_data = respdata().sucessMessage('', '转换用例成功，共转换用例：【' + str(num) + '】 条,用时：' + exe_time + '秒')
            exeLog("****======End======****转换用例成功，已插入数据库****,共用时："+exe_time)
            return json.dumps(return_data, ensure_ascii=False)
        else:
            exeLog("****插入数据库失败，请检查数据********")
            return_data = case_lists
            return json.dumps(return_data, ensure_ascii=False)
