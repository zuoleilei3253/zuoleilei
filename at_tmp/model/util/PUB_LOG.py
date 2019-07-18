#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 20:39
# @Author  : bxf
# @File    : PUB_LOG.py
# @Software: PyCharm
import time
import logging

from model.util.GET_FilePath import *
from model.FUNC.GROUP_OPT import *


class Log():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
# 以下三行为清空上次文件

# 将当前文件的handlers 清空
        self.logger.handlers = []
# 然后再次移除当前文件logging配置
        self.logger.removeHandler(self.logger.handlers)
        #  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        if not self.logger.handlers:
# loggger 文件配置路径
            log_dir=getCurruntpath()+'/model/output/log'
            if os.path.exists(log_dir) == False:
                os.mkdir(log_dir)
            log_filename=log_dir+'/' + "TEST-" + time.strftime(r'%Y-%m-%d', time.localtime(time.time())) + ".log"
            self.handler = logging.FileHandler(log_filename)
            self.streamhandler=logging.StreamHandler()
# logger 配置等级
            self.logger.setLevel(logging.DEBUG)
# logger 输出格式
            formatter = logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s',
                                          '%Y-%m-%d %H:%M:%S' )
# 添加输出格式进入handler
            self.streamhandler.setFormatter(formatter)
            self.handler.setFormatter(formatter)
# 添加文件设置金如handler
            self.logger.addHandler(self.streamhandler)
            self.logger.addHandler(self.handler)

# 以下皆为重写方法 并且每次记录后清除logger
    def info(self,message=None):
        self.__init__()
        self.logger.info(message)
        self.logger.removeHandler(self.logger.handlers)

    def debug(self,message=None):
        self.__init__()
        self.logger.debug(message)
        self.logger.removeHandler(self.logger.handlers)

    def warning(self,message=None):
        self.__init__()
        self.logger.warning(message)
        self.logger.removeHandler(self.logger.handlers)

    def error(self,message=None):
        self.__init__()
        self.logger.error(message)
        self.logger.removeHandler(self.logger.handlers)

    def critical(self, message=None):
        self.__init__()
        self.logger.critical(message)
        self.logger.removeHandler(self.logger.handlers)



def exeLog(message):

    Log().info('TestExcute Logging】----->'+message)

def errorLog(message):
    Log().error('【Exception Logging】----->' + message)
def dataOptLog(message):
    Log().info('【DataOpt Logging】----->' + message)








if __name__ == '__main__':
    errorLog('ceshiyixi')
