

import sys
import threading

sys.path.append("/opt/ATEST")

import time

from model.util.TMP_DB_OPT import *
from model.util.PUB_RESP import *

"""
caseId : API- + 日期+时间+001
batchId: 日期+时间+001   ex:201710242059-00001
localTime = time.strftime("%Y%m%d%H%M%S",time.localtime())
"""
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton
@singleton
class newID:
    def __init__(self):
        self.lock = threading.Lock()
    def num(self,SQL):
        db = DB_CONN()
        fc = db.db_Query_tuple(SQL)
        result = fc.fetchall()
        # print(result[0][0])
        if result[0][0] == None:
            num = 1
        else:

            num = result[0][0] + 1

        s = "%04d" % num  # 四位数值
        return s

    def getId(self, doc_type):
        with self.lock:
            sql_no = "UPDATE t_doc_no SET doc_no=doc_no+1 WHERE doc_type='" + doc_type + "'"
            num = DB_CONN().db_Update(sql_no)
            sql = "select doc_no from t_doc_no where doc_type='" + doc_type + "'"
            cs_max_id = getJsonFromDatabase(sql)
        if cs_max_id:
            max_id = "%06d" % cs_max_id[0]['doc_no']
            id = max_id
        else:
            id = "000001"
        return id

    def timeData(self):
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    def apiId(self):
        id = "API-" + self.timeData()[2:8] + self.getId("api")
        return id

    def suiteId(self):
        id = "SUITE-" + self.timeData()[4:14]
        return id
    def task_id(self):
        id = self.timeData()[0:14]
        return id

    def appId(self):
        sql='select max(id) from t_api_info'
        id = "APP-" + self.timeData()[0:8] + self.num(sql)
        return id

    def timeID(self):
        id = "ExE-" + self.timeData()[0:14]
        return id

    def groupID(self):
        id = self.timeData()[9:14]
        return id

    def envID(self):
        sql = 'select max(id) from t_env_info'
        id = "ENV-" + self.timeData()[0:6] + self.num(sql)
        return id

    def task_ID(self):
        sql = 'select max(id) from rqmt_task_info'
        id = "TASK-" + self.timeData()[0:14] + self.num(sql)
        return id

    def BatchId(self):
        #id="BATCH-" + self.timeData()[0:8]+'-'+self.timeData()[9:]
        id = "BATCH-" + self.timeData()[0:8] + '-' + self.timeData()[9:] + self.getId("batch_id")
        return id
    def sqlID(self):
        sql = 'select max(id) from t_dbc_info'
        id = "SQL-" + self.timeData()[0:8] + self.num(sql)
        return id


    def TIME_Id(self):
        id = "TIME_" + self.timeData()[2:8] + self.getId("time_id")
        return id
    def CASE_ID(self):
        sql='select max(id) from t_case_info_all'
        id = "CS-" + self.timeData()[2:8] + self.num(sql)
        return id
    def RQMT_ID(self):
        sql='select max(id) from t_requirements_info'
        id ="RQMT-" +self.timeData()[2:8] + self.num(sql)
        return id
    def RULE_ID(self):
        sql='select max(id) from t_rule_info'
        id ="RULE-" +self.timeData()[2:8] + self.num(sql)
        return id
    def RULE_CASE_ID(self):
        sql = 'select max(c_id) from rule_case_info'
        id = "RC-" + self.timeData()[2:8] + self.num(sql)
        return id
    def RQMT_CASE_ID(self):

        sql = 'select max(id) from rqmt_case_info'
        id = "CS_" + self.timeData()[2:8] + self.num(sql)
        return id
    def CORE_CASE_ID(self):
        sql='select max(id) from t_case_info WHERE case_sign_type=1'
        id = "CS_C-" + self.timeData()[2:8] + self.num(sql)
        return id
    def REGRESS_CASE_ID(self):
        sql='select max(id) from t_case_info WHERE case_sign_type=2'
        id = "CS_R-" + self.timeData()[2:8] + self.num(sql)
        return id
    def PLUGIN_ID(self):
        sql='select max(id) from t_plugin_info'
        id ='P-'+self.timeData()[2:8]+self.num(sql)
        return id
    def ENV_ID_D(self):
        sql='select max(id) from t_env_detail'
        id ='P-'+self.timeData()[2:8]+self.num(sql)
        return id
    def FILT_ID(self):
        id=self.timeData()[4:14]
        return id
    def USER_ID(self):
        sql = 'select max(id) from p_user_info'
        id = 'U-' + self.timeData()[2:8] + self.num(sql)
        return idGITGI
    def nomal_time(self):
        time_num=self.timeData()[2:12]
        return time_num
    def CS_ID(self):
        id = "CASE_" + self.timeData()[2:8] + self.getId("cs_id")
        return id
    def TK_ID(self):
        id = "TASK_" + self.timeData()[2:8] +self.getId("test_task")
        return id
    def WN_ID(self):
        id="-WN_"+self.timeData()[2:8]+self.getId("wn_id")
        return id
    def DBC_ID(self):
        id="DBC_"+self.timeData()[2:8]+self.getId("dbc_id")
        return id

    def SHELL_ID(self):
        id = "SHL_" + self.timeData()[2:8] + self.getId("shell_id")
        return id
    def RD_ID(self):
        id = "RD_" + self.timeData()[2:8] + self.getId("rd_id")
        return id
    def getID(self,data):
        id =data.get('id')
        if id =='1':
            return_data=respdata().sucessMessage(self.apiId(),'')
            return json.dumps(return_data,ensure_ascii=False)
        elif id =='2':
            return_data=respdata().sucessMessage(self.SHELL_ID(),'')
            return json.dumps(return_data,ensure_ascii=False)
        elif id =='3':
            return_data=respdata().sucessMessage(self.DBC_ID(),'')
            return json.dumps(return_data,ensure_ascii=False)
        elif id =='4':
            return_data=respdata().sucessMessage(self.apiId(),'')
            return json.dumps(return_data,ensure_ascii=False)
        elif id =='5':
            return_data=respdata().sucessMessage(self.RD_ID(),'')
            return json.dumps(return_data,ensure_ascii=False)
        else:
            return_data = respdata().sucessMessage('调试', '')
            return json.dumps(return_data, ensure_ascii=False)


if __name__ == "__main__":
    print(newID().CASE_ID())


