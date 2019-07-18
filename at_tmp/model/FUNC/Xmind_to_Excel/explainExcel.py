#-*- coding:utf-8 -*-
import xlrd
import os
import copy
from model.util.PUB_LOG import *

def read_excel(file_path):
    '''
    此方法用于读取excel，把excel每一行作为一个列表元素，返回一个列表
    param:   file_path  excel 文件的路径
    return:  list
    '''
    if not os.path.exists(file_path):
        exeLog("文件不存在：{}".format(file_path))
        return '文件不存在'
    case_list = []
    all_case_list = []
    return_case_list = []
    key = []
    value = []
    workbook = xlrd.open_workbook(file_path) # 打开文件
    exeLog("=============导入Excel用例成功=============")
    # for i in range(len(workbook.sheets())):
    #     sheet1_name = workbook.sheet_names()[i]  # 获取sheet1
    sheet1 = workbook.sheet_by_index(0)   # 根据sheet索引或者名称获取sheet内容

    for row in range(1, sheet1.nrows):
        for col in range(sheet1.ncols):
            # key.append(sheet1.cell(0, col).value)
            value.append(str(str(sheet1.cell(row, col).value).replace("\n","")).replace("\\\\n","\\n"))
            # print((sheet1.cell(row, col).value))
        # row_dict = dict(zip(key,value))
            # row_dict[sheet1.cell(1, col).value] = (sheet1.cell(row, col).value).replace("\n", "") # 读取excel每一行，{"调用方法":"post", "访问网址":""}
        case_list.append(copy.deepcopy(value))
        value.clear()
    all_case_list.append(case_list)
    for i in all_case_list:
        for j in i:
            return_case_list.append(j)
        return return_case_list


if __name__ == '__main__':
    path = "D:\转换包\\测试用例_20180803-10-26-59.xlsx"
    print(read_excel(path))

