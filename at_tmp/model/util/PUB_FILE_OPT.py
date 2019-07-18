#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/19 21:36
# @Author  : bxf
# @File    : PUB_FILE_OPT.py
# @Software: PyCharm


import sys
sys.path.append("/opt/AT")

import os
from model.util.GET_FilePath import *


class file_OPT:
    def __init__(self):
        self.filepath=get_FilePath()

    def newFolder(self,task_id):
        folder_path=getCurruntpath()+'/model/output/report/' + task_id
        folder_path=folder_path.strip()
        folder_path=folder_path.rstrip("/")
        isExists=os.path.exists(folder_path)
        # print(isExists)
        # print(folder_path)
        if not isExists:
            os.makedirs(folder_path)
            return  True

        else:
            return False




if __name__ == '__main__':
    print(file_OPT().newFolder('123'))

