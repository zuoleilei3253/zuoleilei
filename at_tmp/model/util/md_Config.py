#encoding:utf-8
#name:md_config.py


import sys
sys.path.append("/opt/AT_UTIL")



import configparser

from model.util.GET_FilePath import *


def getConfig (session,key):
    config=configparser.ConfigParser()
    path = getCurruntpath() + '/model/util/config.ini'
    config.read(path)
    return  config.get(session,key)

def getpath():
    # print(getCurruntpath())
    return getCurruntpath()
if __name__=="__main__":
    value=getConfig("LOGGING","format")
    print (getpath())
