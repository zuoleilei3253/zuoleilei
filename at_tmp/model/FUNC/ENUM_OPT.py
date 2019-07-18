#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 11:36
# @Author  : bxf
# @File    : ENUM_OPT.py
# @Software: PyCharm


import configparser
from model.util.GET_FilePath import *
'''
解决枚举值配置问题
问题：
项目中枚举值太多，获取将枚举值直接写在脚本中判断，影响脚本运行效率及枚举值的集中管理


将枚举值做成可配置的ini文件，通过本脚本获取枚举值的


使用方法：
ENUM_OPT(section).get_val(key)获取 section 下的key的值

ENUM_OPT(section).get_key(val)获取section下的val对应的key值


'''
PATH=getCurruntpath() + '/model/util/enum.ini'

class ENUM_OPT:
    def __init__(self, sections):
        '''
        初始化数据
        '''
        self.cnfig = configparser.ConfigParser()
        self.cnfig.read(PATH, encoding='utf-8')
        self.sections = sections

    def get_items(self):
        '''
        获取session下的值集合
        :param session: session
        :return: 集合
        '''
        items = self.cnfig.items(self.sections)
        return items


    def get_val(self, key):
        '''
        获取枚举值数值val
        :param key: 枚举值中文
        :return: 枚举值 数值
        '''
        val = self.cnfig.get(self.sections, key)
        return val


    def get_key(self, val):
        '''
        获取枚举值中文
        :param val: 枚举值数值
        :return: 枚举值中文
        '''
        items = self.get_items()
        for i in items:
            if str(val) == i[1]:
                return i[0]
            else:
                pass
