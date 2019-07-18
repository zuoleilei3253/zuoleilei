#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 11:09
# @Author  : bxf
# @File    : PLUGIN_OPT.py
# @Software: PyCharm
import requests

from model.FUNC.ENUM_OPT import ENUM_OPT
from model.util.TMP_PAGINATOR import *
from model.FUNC.FRAME_OPT import *

'''



'''


class PLUGIN_OPT():
    def __init__(self, table):
        self.table = table

    def get_lists(self, data, **kwargs):
        '''
        获取环境列表
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql_doc = ''
            for i in kwargs:
                col = i
                val = kwargs[i]
                sql_doc = ' WHERE ' + col + '="' + str(val) + '" And '
            sql = 'SELECT * FROM ' + self.table + '     ' + sql_doc
            # print(sql)
            case_lists = GET_RECORDS(sql, page, records)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def get_lists_a(self, data):
        '''
        获取环境列表
        :return:
        '''
        try:
            plugin_id=data.get('plugin_id')
            page = data.get('_page')
            records = data.get('_limit')
            sql = 'SELECT * FROM ' + self.table + ' WHERE  plugin_status != 1  AND plugin_type="'+str(plugin_id)+'"      '
            # print(sql)
            case_lists = GET_RECORDS(sql, page, records)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def insert(self, data, **kwargs):
        '''

            {
	"plugin_desc": "调试",
	"plugin_type": 1,
	"exe_node": "10.100.100.1",
	"plugin_host": "10.100.100.33",
	"token": "kb55x",
	"deviceID": "3",
	"task_type": "",
	"projectname": "21312312",
	"taskname": "123",
	"ispar": "312312",
	"scriptname": "3213",
	"type": "321"
}
"remark": {
    "testip": "10.100.98.90",
    "token": "ATest",
    "deviceID","PJQDU15B09010310",
    "task_type": "3",
    "projectname": "BJJJ",
    "taskname": "TriggerTask",
    "ispar": "YES",
    "scriptname": "wg",
    "type": "2"

  }


        添加环境组信息
        :return:
        '''
        try:
            get_data = json.loads(data)
            plugin_id = newID().PLUGIN_ID()
            get_data["plugin_status"] = '0'
            insert_result = insertToDatabase(self.table, get_data, plugin_id=plugin_id)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def update(self, data):
        '''
        修改
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)
            '''
            remark_list = dict()
            remark = dict()
            remark_list["token"] = get_data.get("token")
            remark_list["deviceID"] = get_data.get("deviceID")
            remark_list["task_type"] = get_data.get("task_type")
            remark_list["projectname"] = get_data.get("projectname")
            remark_list["taskname"] = get_data.get("taskname")
            remark_list["ispar"] = get_data.get("ispar")
            remark_list["scriptname"] = get_data.get("scriptname")
            remark_list["type"] = get_data.get("type")
            remark_list["testip"] = get_data.get("exe_node")
            del get_data["token"]
            del get_data["deviceID"]
            del get_data["task_type"]
            del get_data["projectname"]
            del get_data["taskname"]
            del get_data["ispar"]
            del get_data["scriptname"]
            del get_data["type"]
            remark['remark'] = json.dumps(remark_list)
            '''

            get_data["plugin_status"] = '0'
            #get_data = json.loads(data)
            plugin_id = get_data['plugin_id']
            del get_data['plugin_id']
            update_result = updateToDatabase(self.table, get_data, plugin_id=plugin_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def delete(self, **kwargs):
        '''
        删除
        :param data:
        :return:
        '''
        sql_doc = ''
        for i in kwargs:
            col = i
            val = kwargs[i]
            sql_doc = ' WHERE ' + col + '="' + str(val) + '"'
        sql = 'DELETE FROM ' + self.table + sql_doc
        DB_CONN().db_Update(sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)


    def getTestScenario(self,data=None):
        #datadict=json.loads(data)
        #group_id=datadict.get("group_id")
        sql="SELECT case_id,case_path,case_desc FROM "+ self.table +" WHERE group_id ='10103'"
        try:
            cur=DB_CONN().db_Query_Json(sql)
            casedata=cur.fetchall()
            casepath = set()
            for case in casedata:
                casepath.add(case.get('case_path'))
            allcase = []
            count=0
            for case_path in casepath:
                features = []
                count+=1
                for feature in casedata:
                    if feature.get('case_path') == case_path:
                        features.append(feature)
                if features:
                    casefeatrue = {}
                    casefeatrue['name'] = case_path
                    casefeatrue['scenario']=count
                    childrens = []
                    for f in features:
                        casechren = {}
                        casechren['name'] = f.get('case_desc')
                        casechren['scenario'] = f.get('case_id')
                        childrens.append(casechren)
                    casefeatrue['childrens'] = childrens
                allcase.append(casefeatrue)
            result= respdata().sucessMessage(allcase,'获取数据成功')
        except Exception as e:
            result= respdata().failMessage('','获取数据失败,错误信息：'+str(e))
            return json.dumps(result, cls=MyEncoder, ensure_ascii=False)
        return json.dumps(result, cls=MyEncoder, ensure_ascii=False)



def getMoblieJobStatus(data):
    '''
    以下是移动端任务job名
    测试：
    安卓：Tuandai_UI_Debug
    ios：Tuandai_UI_Debug_Ios
    线上：
    安卓：UiTest_Android_yundun
    ios：UiTest_ios_yundun
    :param data:
    :return:

    :param data:
    :return:
    '''
    params={}
    params['job']=data.get('job')
    url=ENUM_OPT('moblie_api').get_val('jobstatus')
    response = requests.get(url,params=params)
    return response.json()
    # if (response.status_code==200):
    #     return json.dumps(response.json(),cls=MyEncoder, ensure_ascii=False)
    # else:
    #     result = respdata().failMessage('', '移动端接口返回失败，返回状态值为：' + str(response.status_code))
    #     return json.dumps(result, cls=MyEncoder, ensure_ascii=False)

def buildMobileJob(data):
    getdata=json.loads(data)
    params = {}
    params['job'] = getdata.get('job')
    params['tags']=getdata.get('tags')
    url = ENUM_OPT('moblie_api').get_val('jobbuild')
    response = requests.post(url, params=params)
    if (response.status_code == 200):
        return json.dumps(response.json(), cls=MyEncoder, ensure_ascii=False)
    else:
        result = respdata().failMessage('', '移动端接口返回失败，返回状态值为：' + str(response.status_code))
        return json.dumps(result, cls=MyEncoder, ensure_ascii=False)

def plugin_status(url):
    plugin_url = url + '/check'
    try:
        # print(plugin_url)
        return_data = requests.get(plugin_url, timeout=5)
        # print(return_data)
        check_result = return_data.status_code
    except Exception as e:
        check_result = '-9999'
        exeLog("*****插件状态获取成功，状态代码为：" + str(check_result) + "异常信息：" + str(e))
    return str(check_result)


def plugin_status_check():
    '''
    状态检查：
    0--正常可用
    1-无法使用
    2-运行中
    3-连接状态异常
    :return:
    '''
    try:
        plugin_info_sql = 'select * from t_plugin_info'
        plugin_info = getJsonFromDatabase(plugin_info_sql)
        if plugin_info:
            for i in plugin_info:
                url = i['plugin_host']
                status = plugin_status(url)
                plugin_id = i['plugin_id']
                if status == '200':
                    sql = "update plugin_info set plugin_status= 0 WHERE plugin_id='" + plugin_id + "'"
                elif status == '201':
                    sql = "update plugin_info set plugin_status= 1 WHERE plugin_id='" + plugin_id + "'"
                elif status == '300':
                    sql = "update plugin_info set plugin_status=2 WHERE plugin_id='" + plugin_id + "'"
                else:
                    sql = "update plugin_info set plugin_status=3 WHERE plugin_id='" + plugin_id + "'"
                DB_CONN().db_Update(sql)
        else:
            pass
        return_data = respdata().sucessMessage('', '状态更新完成')
        return json.dumps(return_data, ensure_ascii=False)
    except Exception as e:
        return_data = respdata().failMessage('', '更新失败，请检查日志！')
        return json.dumps(return_data, ensure_ascii=False)


def plugin_status_opt(status, plugin_id):
    '''
    0-空闲中
    1-执行中
    2-执行完成
    3-插件异常

    :param status:
    :param plugin_id:
    :return:
    '''
    # if status == 0:
    #     sql = "update t_plugin_info set plugin_status= 0 WHERE plugin_id='" + plugin_id + "'"
    # elif status == 1:
    #     sql = "update t_plugin_info set plugin_status= 1 WHERE plugin_id='" + plugin_id + "'"
    # elif status == 2:
    #     sql = "update t_plugin_info set plugin_status=2 WHERE plugin_id='" + plugin_id + "'"
    # else:
    #     sql = "update t_plugin_info set plugin_status=3 WHERE plugin_id='" + plugin_id + "'"
    if status==0 or status==1 or status==2:
        sql = "update t_plugin_info set plugin_status="+str(status) +" WHERE plugin_id='" + plugin_id + "'"
    else:
        sql = "update t_plugin_info set plugin_status=3 WHERE plugin_id='" + plugin_id + "'"
    a = DB_CONN().db_Update(sql)
    return a


def get_auto_caselists(task_id):
    case_list_sql = 'select case_id from t_task_to_case where task_id="' + task_id + '"'
    case_list = getJsonFromDatabase(case_list_sql)
    case_lists = []
    if case_list:
        for i in case_list:
            case_lists.append(i['case_id'])
        exeLog("******获取自动化执行用例列表成功****")
        return case_lists
    else:
        return False


def platfarmExetest(data):
    '''
    {"case_id":"","env_id":""}
    :param data:
    :return:
    '''
    case_ids=data.get('case_lists')
    plugin_id=data.get('plugin_id')
    #case_ids=get_auto_caselists(task_id)
    if case_ids:
        plugin_status_opt(1, plugin_id)
        # data = dict()
        # data["case_id"] = case_ids
        # data["env_id"] = env_id
        # data['case_type']=case_type
        # data['plugin_id']=plugin_id
        # data['task_id']=task_id
        # data['batch_id']=batch_id
        url = "http://127.0.0.1:3302/exesuite"
        send_data = json.dumps(data)
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        result_data = requests.post(url, data=send_data, headers=headers)
        plugin_status_opt(0, plugin_id)
        if result_data.status_code != 200:
            return_data = respdata().failMessage('', '执行服务出现问题，请检查执行服务，apt_exe 目前配置地址为：' + str(url))
            return json.dumps(return_data, ensure_ascii=False)
        else:
            return json.dumps(result_data.json())
    else:
        result_data = respdata().failMessage('', '无用例执行，请检查用例下的步骤')
    return json.dumps(result_data, ensure_ascii=False)

def executeMobileUi(data):
    '''

    调用移动组UI的任务方法
    :param data: 数据字典
    :return:
    '''
    paramsdata=data
    plugin_id = paramsdata.get('plugin_id')
    plugin_status_opt(1, plugin_id)

    try:
        if paramsdata.get('case_lists'):
            remark=paramsdata.get('remark')
            jobparams = {}

            jobparams['job'] = remark.get('job')
            jobparams['tags'] = ','.join(paramsdata.get('case_lists'))
            del paramsdata['case_lists']

            # params['batch_id']=data.get('batch_id')
            # params['task_id']=data.get('task_id')
            # params['case_type']=data.get('case_type')
            jobparams['params']=json.dumps(paramsdata,ensure_ascii=False)
            #params['type']=data.get('type')
            # url = ENUM_OPT('moblie_api').get_val('jobbuild')
            # response = requests.post(url, params=params)
            url = ENUM_OPT('moblie_api').get_val('jobbuild')
            response = requests.request("POST",url, params=jobparams)
            return_data=response.json()
            if return_data.get('code')==0:
                return_data = respdata().sucessMessage('', '执行成功')
            else:
                return_data = respdata().failMessage('', '执行失败，请检查jenkins job是否正常')
            #plugin_status_opt(0, plugin_id)
            #return json.dumps(return_data, ensure_ascii=False)
        else:
            return_data = respdata().failMessage('', '没有要执行的用例，请检查数据')
        plugin_status_opt(0, plugin_id)
        return json.dumps(return_data, ensure_ascii=False)
    except Exception as e:
        exeLog("###############独立自动化测试框架发送数据【异常】##########异常信息为：" + str(e))
        return_data = respdata().failMessage('', '连接错误，请检查地址有效性！')
        plugin_status_opt(0, plugin_id)
        return json.dumps(return_data, ensure_ascii=False)

def executeShenzheng(data):
    '''
     调用深圳的任务方法
    :param data: 数据字典
    :return:
    '''
    plugin_id = data.get('plugin_id')
    plugin_status_opt(1, plugin_id)
    try:
        if data.get('case_lists'):
            url = 'http://10.100.13.59:8088/run_task'
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            return_status = response.status_code
            if return_status == 200:
                exeLog("###############独立自动化测试框架发送数据【成功】###########")
                return_data = respdata().sucessMessage('', '发送成功')
            else:
                return_data = response.json()
                message = return_data['message']
                exeLog("###############独立自动化测试框架发送数据【失败】###########")
                return_data = respdata().failMessage('', '发送失败！，请检查插件~ 返回错误为：' + str(message))
            #plugin_status_opt(0, plugin_id)
            #return json.dumps(return_data, ensure_ascii=False)
        else:
            return_data = respdata().failMessage('', '没有要执行的用例，请检查数据')
        plugin_status_opt(0, plugin_id)
        return json.dumps(return_data, ensure_ascii=False)
    except Exception as e:
        exeLog("###############独立自动化测试框架发送数据【异常】##########异常信息为：" + str(e))
        return_data = respdata().failMessage('', '连接错误，请检查地址有效性！')
        plugin_status_opt(0, plugin_id)
        return json.dumps(return_data, ensure_ascii=False)





def plugin_run(data, token,type=None):
    '''
    {
	"plugin_desc": "调试",
	"plugin_type": 1,
	"exe_node": "10.100.100.1",
	"plugin_host": "10.100.100.33",
	"token": "kb55x",
	"deviceID": "3",
	"task_type": "",
	"projectname": "21312312",
	"taskname": "123",
	"ispar": "312312",
	"scriptname": "3213",
	"type": "321"
}


{
  "task_id": "TASK-0008",
  "case_lists": ["login_018", "login_024", "login_017"],
  "plugin_id":"插件编号",
  "remark": {
    "testip": "10.100.98.90",
    "token": "ATest",
    "deviceID","PJQDU15B09010310",
    "task_type": "3",
    "projectname": "BJJJ",
    "taskname": "TriggerTask",
    "ispar": "YES",
    "scriptname": "wg",
    "type": "2"

  }
}
执行插件中的插件类型数据字典定义：
100-平台，对应手工测试
200-接口测试(平台)
201-接口测试(Python)
202-接口测试(JMeter)
301-PC端UI测试(Python)
401-安卓端UI测试(Appium)
402-安卓端UI测试(UIAutomation)
501-IOS端UI测试(Appium)
502-移动端UI测试框架(Behave)
901-综合测试(RobotFramework)

:type 执行类型，None or 0 --手动
                1-定时任务

    :param data:
    :return:
    '''
    get_data = json.loads(data)
    emil_id=get_data.get('email_id')
    plugin_id = get_data.get('plugin_id')
    exe_type = str(get_data.get('exe_type'))
    task_id = get_data.get('task_id')
    env_id=get_data.get('env_id')
    plugin_info_sql = 'select * from t_plugin_info where plugin_id ="' + plugin_id + '"'
    plugin_info = getJsonFromDatabase(plugin_info_sql)
    if plugin_info:
        test_info = dict()
        batch_id=newID().BatchId()
        exe_name = getRealName(token)
        test_info['task_id'] = task_id
        test_info['exe_name'] = exe_name
        test_info['plugin_id'] = plugin_id
        test_info['remark'] = json.loads(plugin_info[0].get('remark'))
        test_info['case_type'] = exe_type
        test_info['case_lists'] = get_auto_caselists(task_id)
        test_info['batch_id'] = batch_id
        test_info['taskType'] = str(get_data.get('taskType'))
        test_info['group_id'] = str(get_data.get('group_id'))
        if type ==1:
            test_info['type'] = type
            test_info['email_id']=emil_id
            a=insertTimingBatchId(get_data['time_id'],task_id,batch_id)
            if a is None:
                return_data=respdata().failMessage(a[1],'插入批次号到定时任务表发生错误，请检查！')
                return  json.dumps(return_data,ensure_ascii=False)
        if plugin_info[0]['plugin_type']=='200':
            test_info['env_id'] = env_id
            #plugin_status_opt(1, plugin_id)
            #return platfarmExe(task_id,env_id,exe_type,plugin_id)
            #return platfarmExetest(task_id,env_id,exe_type,plugin_id,batch_id)
            return platfarmExetest(test_info)
        elif plugin_info[0]['plugin_type']=='202' or plugin_info[0]['plugin_type']=='401':
            return executeShenzheng(test_info)
        elif str(plugin_info[0]['plugin_type'])=='502':

            status=getMoblieJobStatus(test_info['remark'])
            if status.get('code')!=0:
                return_data = respdata().sucessMessage('', 'jenkins任务执行中，请稍后执行')
                return json.dumps(return_data,ensure_ascii=False)
            else:
                return executeMobileUi(test_info)
        else:
            plugin_host = plugin_info[0]['plugin_host']
            #test_info = dict()
            plug_url = plugin_host + '/run_task'
            # exe_name = getRealName(token)
            # test_info['task_id'] = task_id
            # test_info['exe_name'] = exe_name
            # test_info['plugin_id'] = plugin_id
            # test_info['case_type'] = exe_type
            # test_info['remark'] = json.loads(plugin_info[0]['remark'])
            if plugin_status(plugin_host) == '200':
                try:
                    if test_info.get('case_lists'):
                        #test_info['case_lists'] = get_auto_caselists(task_id)
                        headers = {'Content-Type': 'application/json', 'Token': 'ATest'}
                        exeLog("###############独立自动化测试框架发送数据【开始】###########")
                        # print("******++++++++++++++++++===========插件请求参数+++++++++++++++++++")
                        # print(test_info)
                        send_auto = requests.post(plug_url, data=json.dumps(test_info), headers=headers)
                        return_status = send_auto.status_code
                        if return_status == 200:
                            exeLog("###############独立自动化测试框架发送数据【成功】###########")
                            return_data = respdata().sucessMessage('', '发送成功')
                            plugin_status_opt(1, plugin_id)
                        else:
                            return_data = send_auto.json()
                            message = return_data['message']
                            exeLog("###############独立自动化测试框架发送数据【失败】###########")
                            return_data = respdata().failMessage('', '发送失败！，请检查插件~ 返回错误为：' + str(message))
                            plugin_status_opt(3, plugin_id)
                        return json.dumps(return_data, ensure_ascii=False)
                    else:
                        return_data = respdata().failMessage('', '没有要执行的用例，请检查数据')
                        return json.dumps(return_data, ensure_ascii=False)
                except Exception as e:
                    exeLog("###############独立自动化测试框架发送数据【异常】##########异常信息为：" + str(e))
                    return_data = respdata().failMessage('', '连接错误，请检查地址有效性！')
                    return json.dumps(return_data, ensure_ascii=False)
            else:
                return_data = respdata().failMessage('', '框架服务连接错误，请检查连接状态！~~')
                return json.dumps(return_data, ensure_ascii=False)
    else:
        return_data = respdata().failMessage('', '无可用插件配置，请检查公共配置信息！~~')
        return json.dumps(return_data, ensure_ascii=False)

def insertTimingBatchId(time_id,task_id,batch_id):
    insert_sql= "INSERT INTO t_time_batch (time_id,task_id,batch_id) values (%s,%s,%s)"
    params=time_id,task_id,batch_id
    #try:
    return DB_CONN().db_Insert(insert_sql,params)
    #     return True
    # except Exception as e:
    #     return False , str(e)

#
# def platfarmExe(task_id,env_id,case_type,plugin_id):
#     '''
#     {"case_id":"","env_id":""}
#     :param data:
#     :return:
#     '''
#
#     plugin_status_opt(1, plugin_id)
#     case_ids=get_auto_caselists(task_id)
#     if case_ids:
#         case_list = dict()
#         case_lists = []
#         for i in case_ids:
#             result = dict()
#             case_id=i
#             data = dict()
#             data["case_id"]=case_id
#             data["env_id"]=env_id
#             # url="http://10.100.99.99/exesuite" #开发联调环境
#             url="http://127.0.0.1:3302/exesuite"
#             send_data=json.dumps(data)
#             headers={'Content-Type':'application/json;charset=UTF-8'}
#             result_data=requests.post(url,data=send_data,headers=headers)
#             if result_data.status_code !=200:
#                 return_data = respdata().failMessage('', '执行服务出现问题，请检查执行服务，apt_exe 目前配置地址为：'+str(url))
#                 return json.dumps(return_data, ensure_ascii=False)
#             else:
#                 # print(result_data.status_code,case_id)
#                 response_lists=result_data.json()['data']['resp']
#                 exe_time = result_data.json()['data']['exe_time']
#                 if response_lists==[]:
#                     result["case_result"] = 2
#                     result["case_real_result"] = "此用例下无自动化执行内容！~"
#                 else:
#                     for j in response_lists:
#                         print(j)
#                         if j ["test_result"]=='Fail' or j["test_result"]=='Error':
#                             result["case_result"] = 2
#                             result["case_real_result"] = j["real_result"]
#                             result["case_exe_result"] = json.dumps(j["response_data"], ensure_ascii=False)
#                         else:
#                             result["case_result"] = 1
#                             result["case_real_result"] = j["real_result"]
#                             result["case_exe_result"] = json.dumps(j["response_data"], ensure_ascii=False)
#
#                 result["case_id"] = case_id
#                 result["case_exe_type"] = "200"
#                 # result["case_real_result"] = "执行成功！~"
#                 result["case_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#                 result["case_executor"] = '平台用户'
#                 result["case_exe_time"] = str(exe_time)
#                 case_lists.append(result)
#             case_list["task_id"] = task_id
#             case_list["case_type"] = case_type
#             case_list["plugin_id"] = plugin_id
#             case_list["result_lists"]=case_lists
#         save_data=json.dumps(case_list)#获取测试结果
#
#         COLLECT_DATA(save_data).save_result() #插入测试结果
#         return_data = respdata().sucessMessage('','执行完成')
#         plugin_status_opt(0, plugin_id)
#         return json.dumps(return_data, ensure_ascii=False)
#     else:
#
#         return_data=respdata().failMessage('','无用例执行，请检查用例下的步骤')
#         plugin_status_opt(0, plugin_id)
#         return json.dumps(return_data, ensure_ascii=False)