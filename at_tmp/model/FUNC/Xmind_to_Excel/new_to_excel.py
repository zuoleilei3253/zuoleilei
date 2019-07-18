#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 14:56
# @Author  : kimmy-pan
# @File    : new_to_excel.py
from collections import OrderedDict
import json
from model.FUNC.ENUM_OPT import *
from xmindparser import xmind_to_dict
from model.util.TMP_DB_OPT import *
from model.util.newID import *
from model.util.PUB_LOG import *

class translate_to_excel():
    def __init__(self,xmind_file,group_id,table,rqmt_id=None):
        # self.template_path = template_path
        self.xmind_file = xmind_file
        self.table = table
        # self.sasve_path = sasve_path
        self.group_id =group_id
        if rqmt_id == None:
            self.rqmt_id = ""
        else:
            self.rqmt_id = rqmt_id
        self.all_case = {}


    def xmind_to_dict(self,):
        """
        xmind转化成dict
        :return:
        """
        out = xmind_to_dict(self.xmind_file)
        b = out[0]["topic"]["topics"]
        return b

    def parse(self,b):
        """
        解析以测试目录为单位的case
        :param b: 测试目录为单位的case
        :return:
        """
        for i in range(len(b["topics"])):
            self.all_case[str(i)+ "_" + b["title"]] = []
            self.all_case[str(i)+"_" + b["title"]].append(b["title"])
            # 用例名称
            self.all_case[str(i)+"_" + b["title"]].append(b["topics"][i]["title"])
            self.parse_more(b["topics"][i]["topics"],self.all_case[str(i)+"_" + b["title"]])

    def parse_more(self,b,c):
        """
        深层解析以测试目录为单位的case
        :param b: 测试目录为单位的case
        :param c: 收集测试用例的字典
        :return:
        """
        if type(b) is str:
            c.append(b)
            # print(c)
        if type(b) is list:
            for i in b:
                self.parse_more(i,c)
        if type(b) is dict:
            for k, v in b.items():
                if type(v) is str:
                    c.append(v)
                if type(v) is list:
                    for i in v:
                        self.parse_more(i, c)

    def parse_all(self):
        """
        解析所有测试目录的测试用例
        :return: 返回所有测试用例的字典
        """
        for i in self.xmind_to_dict():
            # print(i)
            self.parse(i)
        return self.all_case
# print(d)
#
    def write(self):
        """
        写入Excel文件
        :return:
        """
        self.parse_all()
        param = []
        for k,v in self.all_case.items():
            exeLog("用例" + str(v))
            plugin = ENUM_OPT("case_exe_plugin").get_items()
            pluginList= []
            for i in plugin:
                pluginList.append(i[0])
            if len(v) == 12 and v[-1] in pluginList:
                v.insert(0,newID().CS_ID())
                v.insert(3,self.rqmt_id)
                v.append(self.group_id)
                # print(v)
                v[7]=ENUM_OPT("case_type").get_val(v[7])
                v[8]=ENUM_OPT("case_exe_status").get_val(v[8])
                v[9] = ENUM_OPT("case_level").get_val(v[9])
                # v[10] = ENUM_OPT("case_exe_env").get_val(v[11])
                v[11] = ENUM_OPT("case_exe_env").get_val(v[11])
                v[12] = ENUM_OPT("case_exe_type").get_val(v[12])
                v[13] = ENUM_OPT("case_exe_plugin").get_val(v[13])
                param.append(tuple(v))
            elif len(v) < 12 and v[-1] in pluginList:
                v.insert(0,newID().CS_ID())
                v.insert(3,self.rqmt_id)
                v.append(self.group_id)
                v.insert(5, "")
                # print(v)
                v[7]=ENUM_OPT("case_type").get_val(v[7])
                v[8]=ENUM_OPT("case_exe_status").get_val(v[8])
                v[9] = ENUM_OPT("case_level").get_val(v[9])
                # v[10] = ENUM_OPT("case_exe_env").get_val(v[11])
                v[11] = ENUM_OPT("case_exe_env").get_val(v[11])
                v[12] = ENUM_OPT("case_exe_type").get_val(v[12])
                v[13] = ENUM_OPT("case_exe_plugin").get_val(v[13])
                param.append(tuple(v))
            if len(v) == 12 and v[2] in pluginList:
                newV = [newID().CS_ID()]
                newV.append(v[0])
                newV.append(v[1])
                newV.append(self.rqmt_id)
                # newV.append(v[12])
                newV.append(v[11])
                newV.append(v[10])
                newV.append(v[9])
                newV.append(v[8])
                newV.append(v[7])
                newV.append(v[6])
                newV.append(v[5])
                newV.append(v[4])
                newV.append(v[3])
                newV.append(v[2])
                newV.append(self.group_id)
                newV[7]=ENUM_OPT("case_type").get_val(newV[7])
                newV[8]=ENUM_OPT("case_exe_status").get_val(newV[8])
                newV[9] = ENUM_OPT("case_level").get_val(newV[9])
                newV[11] = ENUM_OPT("case_exe_env").get_val(newV[11])
                newV[12] = ENUM_OPT("case_exe_type").get_val(newV[12])
                newV[13] = ENUM_OPT("case_exe_plugin").get_val(newV[13])
                param.append(tuple(newV))

            elif len(v) <12 and v[2] in pluginList:
                newV = [newID().CS_ID()]
                newV.append(v[0])
                newV.append(v[1])
                # newV.append("")
                newV.append(self.rqmt_id)
                newV.append("")
                newV.append(v[10])
                newV.append(v[9])
                newV.append(v[8])
                newV.append(v[7])
                newV.append(v[6])
                newV.append(v[5])
                newV.append(v[4])
                newV.append(v[3])
                newV.append(v[2])
                newV.append(self.group_id)
                newV[7]=ENUM_OPT("case_type").get_val(newV[7])
                newV[8]=ENUM_OPT("case_exe_status").get_val(newV[8])
                newV[9] = ENUM_OPT("case_level").get_val(newV[9])
                newV[11] = ENUM_OPT("case_exe_env").get_val(newV[11])
                newV[12] = ENUM_OPT("case_exe_type").get_val(newV[12])
                newV[13] = ENUM_OPT("case_exe_plugin").get_val(newV[13])
                param.append(tuple(newV))
        param = eval((str(param).replace('[Blank]', "")))
        print(param)
        # param = [("测试工程师","[8, 9, 10, 1]","2018-08-14 18:22:36","11")]
        sql = "INSERT INTO {} ( case_id,case_path,case_desc,rqmt_id,case_init,case_step,case_prev_data,case_type,case_exe_status,case_level,case_builder,case_exe_env,case_exe_type,case_exe_plugin,group_id)" \
" VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(self.table)
        print(sql)
        DB_CONN().db_Batch(sql, param)


if __name__ == "__main__":
    print(translate_to_excel(xmind_file="C:\\Users\\Administrator\Desktop\\1_0125103336.xmind",table="regress_case_info",group_id="11").write())