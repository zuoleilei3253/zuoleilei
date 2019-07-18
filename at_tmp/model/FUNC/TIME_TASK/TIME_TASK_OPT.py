#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/8 11:24
# @Author  : bxf
# @File    : TIME_TASK_OPT.py
# @Software: PyCharm
import requests
from model.util.newID import *
from model.util.PUB_RESP import *


'''
执行数据：
{"task_id":"TASK_181105000054","plugin_id":"P-1810160012","exe_type":2,"env_id":"ENV-2018100004"}

执行接口
http://10.100.99.192:5000/timing_task 
POST
数据格式：
{"task_id":"TASK-20180711141704",
"timing_title":"测试调试",
"host_id":"ENV-2018100004",
"email_id":"41850",
"plugin_id":"P-1808160009",
"timing_data":{"timing_cycle":"hour  week  day","start_time":"2"},
"timing_count":"1" 执行次数,
"is_run":"0-启动，1-停止"}

删除
http://10.100.98.163:7802/timing_task/delete?jobName=TASK-20180711141704

'''
HOST='http://127.0.0.1:7802'
HEADER={'Content-Type': 'application/json', 'Token': 'ATest'}

class TIME_TASK_OPT:
    def __init__(self,token):
        self.token=token

    def timetaskInert(self,data):
        '''
        {"task_id":"TASK-20180711141704","timing_title":"测试调试","host_id":"ENV-2018100004","email_id":"41850","plugin_id":"P-1808160009","timing_data":{"timing_cycle":"hour","start_time":"2"},"timing_count":1,"is_run":"0-启动，1-停止"}
        :param data:
        :return:
        '''
        get_data=json.loads(data)
        time_id = newID().TIME_Id()
        result = insertToDatabase('t_time_task', get_data, time_id=time_id,is_run=0)
        return_data=respdata().sucessMessage('','保存成功！~')
        return json.dumps(return_data,ensure_ascii=False)

    def timetaskDELETE(self, time_id):
        '''
        删除
        :param data:
        :return:
        '''
        send_auto = requests.get(HOST + '/timing_task/delete?jobName='+time_id)
        if send_auto.status_code==200:
            sql = 'DELETE FROM t_time_task  WHERE time_id="'+time_id+'"'
            DB_CONN().db_Update(sql)
            return_data = respdata().sucessMessage('', '删除成功！')
            exeLog("***【定时任务】**************任务删除成功******任务编号为：" + time_id + "*****************")
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        else:
            exeLog(
                "***【定时任务】**************任务启动失败！******任务编号为：" + time_id + "*****************错误信息为：定时服务处理失败，请检查定时服务连接状态！~")
            return_data = respdata().failMessage('', "启动失败~请检查定时服务！~")
            return json.dumps(return_data, ensure_ascii=False)
    def timetaskUpdate(self, data):
        '''
        修改
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)
            time_id = get_data['time_id']
            update_result = updateToDatabase('t_time_task', get_data, time_id=time_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
    def getTask_Info(self,time_id,exe_type):
        '''
        {"task_id":"TASK-20180711141704",
"timing_title":"测试调试",
"host_id":"ENV-2018100004",
"email_id":"41850",
"plugin_id":"P-1808160009",
"timing_data":{"timing_cycle":"hour  week  day","start_time":"2"},
"timing_count":"1" 执行次数,
"is_run":"0-启动，1-停止"}
        :param time_id:
        :return:
        '''
        task_sql='select * from t_time_task WHERE time_id="'+str(time_id)+'"'
        time_data=getJsonFromDatabase(task_sql)
        time_info=dict()
        if time_data:
            timing_data=dict()
            timing_data["timing_cycle"]=time_data[0]['timing_cycle']
            timing_data["start_time"] = time_data[0]['start_time']
            time_info['task_id']=time_data[0]['task_id']
            time_info['env_id'] = time_data[0]['env_id']
            time_info['time_id'] = time_data[0]['time_id']
            time_info['timing_title']=time_data[0]['time_title']
            time_info['host_id']=time_data[0]['host_id']
            time_info['email_id']=time_data[0]['email_id']
            time_info['plugin_id']=time_data[0]['plugin_id']
            time_info['timing_data']=timing_data
            time_info['timing_count']=time_data[0]['timing_count']
            time_info['exe_type'] = exe_type
            time_info['is_run']=time_data[0]['is_run']
            time_info['group_id'] = time_data[0]['group_id']
            time_info['taskType'] = time_data[0]['taskType']

        else:
            timing_data = dict()
            timing_data["timing_cycle"] = ''
            timing_data["start_time"] = ''
            time_info['task_id'] = ''
            time_info['env_id'] = ''
            time_info['time_id'] = ''
            time_info['timing_title'] = ''
            time_info['host_id'] = ''
            time_info['email_id'] =''
            time_info['plugin_id'] = ''
            time_info['timing_data'] = timing_data
            time_info['timing_count'] = ''
            time_info['is_run'] = ''
            time_info['exe_type'] = exe_type
            time_info['group_id'] = ''
            time_info['taskType'] = ''
        return time_info
    def timeTaskIsrun(self,data):
        getdata = json.loads(data)
        timing_id = getdata['time_id']
        try:
            timing_isrun = getdata['is_run']
            exe_type=getdata['exe_type']
            timing_info=self.getTask_Info(timing_id,exe_type)
            timing_info['is_run']=timing_isrun
            send_auto = requests.post(HOST + '/timing_task', data=json.dumps(timing_info), headers=HEADER)
            if send_auto.status_code ==200:
                resultdata=send_auto.json()
                if str(resultdata.get('code'))==str(200):
                    exeLog("***【定时任务】**************任务启动成功******任务编号为："+timing_id+"*****************")
                    updatesql = 'update t_time_task set is_run=%s ,timing_status=%s  WHERE time_id="' + timing_id + '"'
                    params = (timing_isrun, timing_isrun)
                    DB_CONN().db_Insert(updatesql,params)
                    return_data = respdata().sucessMessage(timing_isrun, "")
                else:
                    return_data = respdata().failMessage(resultdata, "启动失败 请检查定时服务")
                #return json.dumps(return_data, ensure_ascii=False)
            else:
                exeLog("***【定时任务】**************任务启动失败！******任务编号为：" + timing_id + "*****************错误信息为：定时服务处理失败，请检查定时服务连接状态！~")
                return_data = respdata().failMessage('',"启动失败~请检查定时服务！~")
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e :
            exeLog(
                "***【定时任务】**************任务启动失败！******任务编号为：" + timing_id + "*****************错误信息为：~"+str(e))
            return_data = respdata().failMessage('', "启动失败~~错误信息为"+str(e))
            return json.dumps(return_data, ensure_ascii=False)

    def timeTaskBatchNo(self,data):
        time_id=data.get('time_id')
        sql="select batch_id from t_time_batch where time_id='"+time_id+"'"
        batch_ids=getTupleFromDatabase(sql)
        if batch_ids:
            batch_ids=loop_api(batch_ids)
            return_data=respdata().sucessMessage(batch_ids,'')
            return json.dumps(return_data,ensure_ascii=False)
        else:
            return_data = respdata().sucessMessage([], '')
            return json.dumps(return_data, ensure_ascii=False)


def loop_api(api_t):
    api_l = []
    for i in range(len(api_t)):
        api_l.append(api_t[i][0])
    return api_l