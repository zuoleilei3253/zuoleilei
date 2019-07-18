#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 10:27
# @Author  : bxf
# @File    : DBC_EXE.py
# @Software: PyCharm
'''
DBC执行模块

通过dbc_env_id获取数据库环境配置
根据判断不同的数据库类型，执行不同的连接

'''

import pymssql
from model.util.TMP_DB_OPT import *
from model.util.PUB_initParams import *
from model.util.PUB_RESP import *

'''
{"pwd": "123123", "url": "32131", "name": "312312", "port": "3213", "type": "mysql", "user": "3213"}
'''
class DBC_EXE:
    def __init__(self,env_id):
        self.env_id=env_id
        self.sqlParams = getConfig(self.env_id)
        self.type = self.sqlParams['type']
        self.sTime = time.time()


    def getConn(self):
        if self.type == 'mysql':
            try:
                conn = pymysql.Connect(
                    host=self.sqlParams['url'],
                    port=int(self.sqlParams['port']),
                    user=self.sqlParams['user'],
                    passwd=self.sqlParams['pwd'],
                    db=self.sqlParams['name'],
                    charset='utf8'
                )
                return conn
            except Exception as e:
                exeLog("*********MYSQL数据库连接失败，请检查数据库连接Mysqldb Error:%s" % e)
                return False
        elif self.type == 'sqlserver':
            try:
                conn = pymssql.connect(host=self.sqlParams['url'],
                                       user=self.sqlParams['user'],
                                       password=self.sqlParams['pwd'],
                                       database=self.sqlParams['name'],
                                       charset="utf8",
                                       as_dict=True)
                return conn
            except Exception as e:
                exeLog("*********SQLSERVER数据库连接失败，请检查数据库连接sqlserver== Error:%s" % e)
                return False

    def exeQuery(self, sql):
        try:
            conn = self.getConn()
            if self.type == 'mysql':
                cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
                print(sql)
                cur.execute(sql)
                conn.commit()
                # print('ccc')
                return cur
            else:
                if "SELECT" not in str(sql).upper():
                    cur = conn.cursor()
                    cur.execute(sql)
                    conn.commit()
                    return cur
                else:
                    cur = conn.cursor()
                    cur.execute(sql)
                    return cur
            # fco = cur.fetchall()
        except Exception as e:
            dataOptLog("Mysqldb Error:%s" % e)
            raise Exception("请输入正确的SQL语句")
        # finally:
        #     cur.close()
        #     conn.close()


    def getDBCResult(self,sql):
        cur = self.exeQuery(sql)
        count = cur.rowcount
        totalTime = (time.time() - self.sTime) * 1000
        if self.type == 'mysql':
            try:
                result = cur.fetchall()
                if result == () and count != 0:
                    """
                    update insert语句情况，影响行数为1，返回结果为()
                    返回前端结果为：{"result":cur.rowcount}
                    """

                    exeLog("***数据库更新成功")
                    return [{"result": cur.rowcount, "msg": 200}], totalTime
                elif result != () and count != 0:
                    """
                    select语句情况，查询有数据
                    返回前端结果为：result
                    """

                    exeLog("***返回JSON数据成功")
                    return result, totalTime
                elif result == () and count == 0:
                    """
                    select语句情况，查询无数据
                    返回前端结果为：{"result":None}
                    """
                    exeLog("***数据库内容为空")
                    return [{"result": 0, "msg": 200}], totalTime
            except Exception as e:
                dataOptLog("获取结果 Error:%s" % e)
                return [{"result": "None", "msg": 404}], totalTime
            finally:
                cur.close()


        else:
            try:
                result = cur.fetchall()
                if "SELECT" not in str(sql).upper():
                    return [{"result": count, "msg": 200}], totalTime
                else:
                    if result != [] and count != 0:
                        """
                        select语句情况，查询有数据
                        返回前端结果为：result
                        """
                        exeLog("***返回JSON数据成功")
                        return result, totalTime
                    elif result == [] and count == 0:
                        """
                        select语句情况，查询无数据
                        返回前端结果为：{"result":None}
                        """
                        exeLog("***数据库内容为空")
                        return [{"result": 'None', "msg": 200}], totalTime
            except Exception as e:
                if "Statement" in str(e):
                    return [{"result": count, "msg": 200}], totalTime
                else:
                    return [{"result": str(e), "msg": 404}], totalTime



def getConfig(env_id):
    '''
    去环境配置表中读取环境配置
    :return:
    '''
    env_sql = "select env_d_params from t_env_detail where env_d_id ='" + env_id + "'"

    env_info = get_JSON(env_sql)

    if env_info:
        url = json.loads(env_info[0]["env_d_params"])
        return url
    else:
        return False

def dbcDebug(data):

    replaceDict = {}
    get_data=json.loads(data)
    sql_a=get_data["dbc_sql"]
    sql=sql_a.replace("‘","'").replace("’","'")
    try:
        init_data = get_data["init_data"]
        env_id = get_data["env_d_id"]

        if init_data == []:
            exeLog("----------------------")
            exeLog(str(init_data))
            exeLog(str(sql))
            exeLog(str(env_id))
            response_result = {}
            DB_result = DBC_EXE(env_id).getDBCResult(sql)
            for i in DB_result[0]:
                for k,v in i.items():
                    i[k] = str(v).replace("UUID(","").replace(")","")
            response_result["result"] = DB_result[0]
            response_result["comment"] = str(sql)
            response_result["exeTime"] = str(int(DB_result[1])) + "ms"
            response_result["status"] = 200
            result = respdata().sucessResp(response_result)
            return json.dumps(result, cls=MyEncoder, ensure_ascii=False)

        elif init_data != []:
            giveParam = json.loads(getParams(init_data))
            updateSql = GET_PARAM(giveParam,sql).GET_INIT_DATA()
            DB_result = DBC_EXE(env_id).getDBCResult(updateSql)
            exeLog("----------------------")
            exeLog(str(replaceDict))
            exeLog(str(updateSql))
            exeLog(str(env_id))
            response_result = {}
            for i in DB_result[0]:
                for k,v in i.items():
                    i[k] = str(v).replace("UUID(","").replace(")","")
            response_result["result"] = DB_result[0]
            response_result["comment"] = str(updateSql)
            response_result["status"] = 200
            response_result["exeTime"] = str(int(DB_result[1])) + "ms"
            result=respdata().sucessResp(response_result)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print(response_result)
            return json.dumps(result,cls=MyEncoder,ensure_ascii=False)
    except Exception as e:
        init_data = get_data["init_data"]
        giveParam = json.loads(getParams(init_data))
        response_result = {}
        updateSql = GET_PARAM(giveParam, sql).GET_INIT_DATA()
        print(updateSql)
        response_result["result"] = [{"异常执行结果":str(e)+"执行语句为："+str(updateSql)+"。请检查是否错误！~"}]
        response_result["comment"] =str(updateSql)
        response_result["status"] = 200
        response_result["exeTime"] = ""
        return_data = respdata().sucessMessage(response_result, '调试失败，请检查！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)


