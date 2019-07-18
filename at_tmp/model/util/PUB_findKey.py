#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/16 17:27
# @Author  : bxf
# @File    : findKey.py
# @Software: PyCharm


import sys
sys.path.append("/opt/ATEST")

def text_query(path, keyword):
    """

    :param path: 文件路径
    :param keyword: 查找的关键词
    :return: 返回一个包含关键字的列表
    """
    list_old = []
    list_xin = []
    with open(path) as f:
        for i in f:
            if keyword in i:
                list_old.append(i)
        for i in range(len(list_old)):
            list_xin.append(list_old[i])
        return list_xin

if __name__ == '__main__':
    print(text_query("D:\\AUTT\\model\\TDAP\\output\\report\\TASK-20180319142927\BATCH-20180320-93322.html", 'INFO'))