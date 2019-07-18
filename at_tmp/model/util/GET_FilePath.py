#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/6 9:11
# @Author  : kimmy-pan
# @File    : GET_FilePath.py


import sys
sys.path.append("/opt/ATEST")
import os
def get_FilePath():
    filename = (os.getcwd().split("/util/Public"))[0]
    return filename
def getCurruntpath():
    filename=sys.path[0]
    return filename
if __name__ == "__main__":
    print(getCurruntpath())
