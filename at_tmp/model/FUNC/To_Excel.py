#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 15:07
# @Author  : kimmy-pan
# @File    : To_Excel.py
from model.FUNC.Xmind_to_Excel.new_to_excel import *
from model.FUNC.Xmind_to_Excel.translate_to_xmind import *


def translate_format(format_type,group_id=None,xmind_file=None, table=None,OUTPUT=None,excel_path=None,rqmt_id=None):
    """
    思维导图跟Excel互转
    :param format_type:转化类型 1：xmind_to_Excel 2:Excel_to_xmind
    :return:
    """
    if format_type == 1:
        try:
            translate_to_excel(xmind_file, group_id,table,rqmt_id=rqmt_id).write()
            return_data =respdata().sucessMessage('',"导入数据库成功")
            return return_data
        except Exception as e:
            print("转换失败" + "**** " + str(e))
            return_data = respdata().failMessage('', "转换失败！～")
            return return_data
    elif format_type == 2:
        try:
            to_XMIND(OUTPUT,excel_path,group_id)
            return_data = respdata().sucessMessage('', "导出成功")
            return return_data
        except Exception as e:
            return_data = respdata().failMessage('', "转换失败！～")
            return return_data

if __name__ == "__main__":
    template_file = "D:/转换包/Xmind_to_Excel/测试用例模板（final）.xlsx"
    xmind_file ="D:/转换包/test.xmind"
    save_path = "./"
    OUTPUT = "D:\转换包\\test.xmind"
    excel_path = "D:\转换包\\测试用例_20180803-10-26-59.xlsx"
    translate_format(1,xmind_file=xmind_file,template_file=template_file,save_path=save_path)
    # translate_format(2,OUTPUT=OUTPUT,excel_path=excel_path)