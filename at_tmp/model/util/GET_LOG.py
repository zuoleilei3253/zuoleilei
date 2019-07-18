
import sys
sys.path.append("/opt/ATEST")

import time
import json
import os
from model.util.Public.GET_FilePath import *
from model.util.Public.PUB_findKey import *
from model.util.Public.PUB_RESP import *

class getLog:
    def __init__(self,level):
        self.level=level
        self.filename = '/opt/AT/model/output/log/TEST-' + time.strftime('%Y-%m-%d',
                                                                               time.localtime(time.time())) + '.log'
        # print(self.filename)

    # 判断是否存在log文件
    def getlst(self):

        if os.path.exists(self.filename):

            rd = open(self.filename, 'r')
            try:
                log=text_query(self.filename,self.level)
                if log==[]:
                    return ["未生成该日志，请检查是否执行，或联系管理员！"]
                else:
                    return log
            finally:
                rd.close()
        else:
            return "日志尚未建立，请重新处理"

# 获取日志
def getLogDetail(data):
    try:
        getdata = json.loads(data)
        task_id = getdata['task_id']
        # print("cesuo")
        log_data = getLog(task_id).getlst()
        # print(log_data)
        return_data=respdata().sucessResp(log_data)
        return json.dumps(return_data, ensure_ascii=False)
    except Exception as e:
        return_data = respdata().exceptionResp(e)
        return json.dumps(return_data, ensure_ascii=False)


if __name__ == '__main__':
    readlog = getLog('ces11hi').getlst()
    print(readlog)
