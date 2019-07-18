#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 14:50
# @Author  : kimmy-pan
# @File    : to_xmind.py
from model.util.Third_XMIND.mekk.xmind.document import XMindDocument
from model.FUNC.Xmind_to_Excel.explainExcel import *
from model.FUNC.TAPD.GET_TAPD import *

# OUTPUT = "D:\转换包\\test.xmind"
# excel_path = "D:\转换包\\测试用例_20180803-10-26-59.xlsx"


def to_XMIND(OUTPUT,excel_path,group_id):
    all_case = read_excel(excel_path)
    try:
        title = cloud_to_TAPD(group_id,tapd_id=None).get_cloud_category(group_id)
    except Exception:
        title = "测试用例"
    # if "_" in all_case[0][0]:
    #     title = all_case[0][0].split("_")[0]
    # else:
    #     title = str(excel_path).split("\\")[-1].split(".")[0]
    xmind = XMindDocument.create(title, title)
    first_sheet = xmind.get_first_sheet()
    root_topic = first_sheet.get_root_topic()
    test = {}
    case_name = []
    casedir = []
    for i in range(len(all_case)):
        exeLog("用例：{}".format(all_case[i]))
        if all_case[i][1] not in casedir:
            casedir.append(all_case[i][1])

    for i in range(len(casedir)):
        test[casedir[i]] = root_topic.add_subtopic(casedir[i])

    for i in range(len(all_case)):
        if all_case[i][4] == "无" or all_case[i][4] == "":
            test[all_case[i][1]].add_subtopic(all_case[i][2]).add_subtopic(all_case[i][5])\
                .add_subtopic(all_case[i][6]).add_subtopic(all_case[i][7]).add_subtopic(all_case[i][8])\
                .add_subtopic(all_case[i][9]).add_subtopic(all_case[i][10]).add_subtopic(all_case[i][11]).add_subtopic(all_case[i][12]).add_subtopic(all_case[i][13])
        else:
            test[all_case[i][1]].add_subtopic(all_case[i][2]).add_subtopic(all_case[i][4]).add_subtopic(all_case[i][5])\
                .add_subtopic(all_case[i][6]).add_subtopic(all_case[i][7]).add_subtopic(all_case[i][8])\
                .add_subtopic(all_case[i][9]).add_subtopic(all_case[i][10]).add_subtopic(all_case[i][11]).add_subtopic(all_case[i][12]).add_subtopic(all_case[i][13])

    # for i in range(len(casedir)):
    #     test[casedir[i]] = root_topic.add_subtopic(all_case[i][3]).add_subtopic(all_case[i][4]).add_subtopic(all_case[i][5])\
    #         .add_subtopic(all_case[i][6]).add_subtopic(all_case[i][7]).add_subtopic(all_case[i][8])\
    #         .add_subtopic(all_case[i][9]).add_subtopic(all_case[i][10]).add_subtopic(all_case[i][11]).add_subtopic(all_case[i][12]).add_subtopic(all_case[i][13])
    #     case_name.append(test[casedir[i]])
    xmind.save(OUTPUT)
    exeLog("=============Excel转Xmind成功！=============")


if __name__ == "__main__":
    OUTPUT = "D:\转换包\\test.xmind"
    excel_path = "D:\转换包\\1040101_0111160625.xlsx"
    to_XMIND(OUTPUT, excel_path,'2222')