#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 10:12
# @Author  : bxf
# @File    : testcode.py
# @Software: PyCharm



import configparser
from model.util.GET_FilePath import *
from model.FUNC.ENUM_OPT import*
import requests
import json
from datetime import datetime
from model.util.TMP_DB_OPT import *
from model.FUNC.REPORT_HTML_OPT import *
from testid import *

@getUser("调试")
def cc ():
    print("测试")






#
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# CSRF_ENABLED = True
# # 密钥
# SECRET_KEY = 'ATest'
#
#
# PATH=getCurruntpath() + '/model/util/enum.ini'
#
#
# config=configparser.ConfigParser()
#
# config.read(PATH,encoding='utf-8')
# b=config.items('case_type')
#
#
# b =ENUM_OPT('case_type').get_key(1)
# print(b)
# s={'a':'ff'}
#
#
# c=[['/用户/登录', '系统中存在用户登录', '${user}=获取随机用户(是否存在=是)', '1.${result}=用户登录(账号=${user.账号},密码=${user.密码})', '1.判断相等(预期=1,实际=${result.标志})', '功能测试', '正常', '高', '张三丰', '线上', '自动', 'jmeter'], ['/用户/登录', '输入一个系统中不存在用户登录', '${user}=获取随机用户(是否存在=否)', '1.${result}=用户登录(账号=${user.账号},密码=${user.密码})', '1.判断相等(预期=0,实际=${result.标志})', '功能测试', '正常', '高', '张三丰', '线上', '自动', 'jmeter']]
#
# print(c[0][0])


# def getUserName(token):
#     s = Serializer(SECRET_KEY)
#     try:
#         data = s.loads(token)
#         user_name = data['user_id']
#         return user_name
#     except Exception as e:
#         return "获取 权限失败！～～～"
#
# def get_code(url):
#     plugin_url = url + '/check'
#     try:
#         return_data = requests.get(plugin_url, timeout=5)
#         check_result = return_data.json()['code']
#     except Exception as e:
#         check_result = '-9999'
#     return check_result


# def post_code(url,task_id,data):
#     test_info = dict()
#     plug_url = url + '/run_task'
#     test_info['task_id'] = task_id
#     test_info['case_lists']=data
#     headers={'Content-Type':'application/json'}
#     print(test_info)
#     send_auto=requests.post(plug_url,data=json.dumps(test_info),headers=headers)
#     print(send_auto)
#     return_data=send_auto.text
#     return return_data

# def data_compare():
#     d1=datetime(2018,8,8)
#     d2=datetime(2018,8,7)
#     if d1>d2:
#         print("d1>d2")
#     else:
#         print("d1<d2")
#     current_time=datetime.strptime(datetime.now().strftime("%Y,%m,%d"),"%Y,%m,%d")
#     print(current_time>d1)


# def get_case():
#     insert_data = dict()
#     task_id = '11111'
#     batch_id = 'b12312313'
#     insert_data['batch_id'] = batch_id
#     case_lists = [{'fdsf':'12312313'}]
#     for i in case_lists:
#         insert_data.update(i)
#         print(insert_data)
#
#
# def transform_opt():
#     '''
#     case_exe_type 执行类型  1-手动 2-自动化
#     case_exe_plugin 执行插件
#     case_id 测试用例
#     '''
#     task_lists=dict()
#
#     case_lists_sql='select * from rqmt_case_info '
#     case_lists=getJsonFromDatabase(case_lists_sql)
#     manual_lists=[]
#     platform_lists=[]
#     JMeter_lists=[]
#     Appium_lists=[]
#     Python_lists=[]
#     UIAutomation_lists=[]
#     for i in case_lists:
#         case_exe_type=i['case_exe_type']
#         case_exe_plugin=i['case_exe_plugin']
#         if case_exe_type==1:
#             manual_lists.append(i)
#         else:
#             if case_exe_plugin==1:
#                 platform_lists.append(i)
#             elif case_exe_plugin==2:
#                 JMeter_lists.append(i)
#             elif case_exe_plugin==3:
#                 Appium_lists.append(i)
#             elif case_exe_plugin==4:
#                 Python_lists.append(i)
#             elif case_exe_plugin==5:
#                 UIAutomation_lists.append(i)
#     task_lists['manual_lists'] = manual_lists
#     task_lists['platform_lists'] = platform_lists
#     task_lists['JMeter_lists'] = JMeter_lists
#     task_lists['Appium_lists'] = Appium_lists
#     task_lists['Python_lists'] = Python_lists
#     task_lists['UIAutomation_lists'] = UIAutomation_lists
#     return task_lists
#
#
#

# def get_data_rqmt( rqmt_id, **kwargs):
#     sql = "select A.case_id,min(A.adddate) report_start_time,max(A.adddate) report_end_time ,NOW() report_date ,count(B.case_id) report_exe_counts ,(CASE B.case_exe_env  WHEN '1' THEN '测试环境' WHEN '2' THEN '灰度环境' ELSE '线上环境' END) report_env_type,sum(case A.case_result when '1' then 1 else 0 end ) Pass,sum(case A.case_result when '2' then 1 else 0 end) Fail,sum(case A.case_result when '3' then 1 else 0 end) Error,sum(case A.case_result when '4' then 1 else 0 end) Other from  rqmt_case_info B   LEFT JOIN rqmt_case_result A ON B.case_id=A.case_id WHERE B.rqmt_id= '"+rqmt_id+" '"
#     case_lists = getJsonFromDatabase(sql)
#     report_info=case_lists[0]
#     report_info['Pass']=str(report_info['Pass'])
#     report_info['Fail'] =str(report_info['Fail'])
#     report_info['Error'] =str(report_info['Error'] )
#     report_info['Other'] =str(report_info['Other'])
#     print(report_info)
#     if report_info['case_id'] != None:
#         report_lists_sql = "select A.case_id,A.case_path,A.case_desc,(CASE A.case_exe_type  WHEN '1' THEN '手工' WHEN '2' THEN '自动' END) case_exe_type ,A.case_prev_data,B.case_real_result,(CASE B.case_result   WHEN '1' THEN '通过' WHEN '2' THEN '不通过' WHEN '3' THEN '失败' ELSE '未执行' END) case_result FROM rqmt_case_info A left JOIN rqmt_case_result B ON A.case_id=B.case_id WHERE A.rqmt_id='" + rqmt_id + "'"
#         report_lists = getJsonFromDatabase(report_lists_sql)
#         report_info['records'] = report_lists
#         return (json.dumps(report_info,cls=MyEncoder,ensure_ascii=False))
#     else:
#         return False







if __name__ == '__main__':
    # url='http://10.100.99.8:7706'
    # task_id='TASK-000003203'
    # data=['case-00001000','test_jie']
    # post_code(url,
    #           task_id,
    #           data)
    #
    # transform_opt()
    # print(get_data_rqmt('RQMT-1808070045'))
    print(cc())