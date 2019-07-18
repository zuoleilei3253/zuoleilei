#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 17:26
# @Author  : bxf
# @File    : test_get_id.py
# @Software: PyCharm
'''

获取ID 方法

尾数=当天的用例总数+1取4位

'''

from model.util.TMP_DB_OPT import *

sql = "SELECT total ,a.group_id,(b.num/a.total) AS cover_rate,IF(c.num IS NULL,0,(c.num/a.total)) AS exe_rate,IF(d.num IS NULL,0,(d.num/a.total)) AS bug_rate FROM (SELECT group_id,COUNT(1) AS total FROM regress_case_info WHERE 1=1 GROUP BY group_id) a LEFT JOIN (SELECT group_id,COUNT(1) AS num FROM regress_case_info WHERE case_exe_type!=1 GROUP BY group_id) b ON b.group_id=a.group_id LEFT JOIN (SELECT group_id,COUNT(1) AS num FROM regress_case_result x1 INNER JOIN regress_case_info x2 ON x2.case_id=x1.case_id WHERE batch_id=(SELECT MAX(batch_id) FROM regress_case_result) GROUP BY group_id) c ON c.group_id=a.group_id LEFT JOIN (SELECT group_id,COUNT(1) AS num FROM regress_case_result x1 INNER JOIN regress_case_info x2 ON x2.case_id=x1.case_id WHERE case_result=3 GROUP BY group_id) d ON d.group_id=a.group_id "

result = dict()
stat_list = []
a = getJsonFromDatabase(sql)
for i in a:

    static_list = dict()

    group_info_sql = 'select * from p_group_info WHERE id ="' + str(i['group_id']) + '"'
    group_info = getJsonFromDatabase(group_info_sql)[0]
    group_id = str(group_info['code'])[0:3]
    group_desc_sql = 'select * from p_group_info where code="' + str(group_id) + '"'
    group_desc = getJsonFromDatabase(group_desc_sql)
    if group_desc:
        group_descs = group_desc[0]['group_desc']
    else:
        group_descs = '分组信息不存在'

    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    static_list['total'] = str(i['total'])
    # 覆盖率
    static_list['cover_rate'] = str(float(i['cover_rate']) * 100) + '%'
    # 执行率
    static_list['exe_rate'] = str(float(i['exe_rate']) * 100) + '%'
    # 问题率
    static_list['bug_rate'] = str(float(i['bug_rate']) * 100) + '%'
    static_list['group_desc'] = group_descs
    static_list['time'] = time_now
    stat_list.append(static_list)

print(stat_list)
[{'user_verify': None, 'group_role_arr': '[272, 276]', 'user_email': '', 'id': 10, 'user_mobile': '',
  'user_partment': '', 'adddate': datetime.datetime(2018, 8, 15, 10, 47, 52), 'login_time': None, 'user_pwd': None,
  'user_real_name': '3123', 'group_role': '276', 'user_status': '1',
  'user_password': 'e13dd289d6380b83a1c78ef3d8b959ea', 'usr_ipaddr': None, 'data_role': None, 'user_sex': '',
  'user_name': '3123', 'user_role_id': 2},
 {'user_verify': None, 'group_role_arr': None, 'user_email': '1', 'id': 6, 'user_mobile': '1', 'user_partment': '1',
  'adddate': datetime.datetime(2018, 8, 14, 19, 42, 56), 'login_time': datetime.datetime(2018, 8, 14, 19, 42, 56),
  'user_pwd': None, 'user_real_name': '张三', 'group_role': '101', 'user_status': '1',
  'user_password': '0a97b19294a175c77376b417c692b9ac', 'usr_ipaddr': None, 'data_role': '1', 'user_sex': '1',
  'user_name': 'admin', 'user_role_id': 2},
 {'user_verify': None, 'group_role_arr': None, 'user_email': None, 'id': 5, 'user_mobile': None, 'user_partment': None,
  'adddate': datetime.datetime(2018, 8, 8, 14, 56, 53), 'login_time': datetime.datetime(2018, 8, 8, 14, 56, 53),
  'user_pwd': None, 'user_real_name': '李四', 'group_role': None, 'user_status': None,
  'user_password': '5441f2c6d5f0fcc979d50e204d790fc6', 'usr_ipaddr': None, 'data_role': '1', 'user_sex': None,
  'user_name': 'admin123', 'user_role_id': 2},
 {'user_verify': None, 'group_role_arr': None, 'user_email': '312', 'id': 8, 'user_mobile': '312',
  'user_partment': '312', 'adddate': datetime.datetime(2018, 8, 8, 14, 56, 34), 'login_time': None, 'user_pwd': None,
  'user_real_name': 'tiaoshi', 'group_role': None, 'user_status': '1',
  'user_password': '5441f2c6d5f0fcc979d50e204d790fc6', 'usr_ipaddr': None, 'data_role': None, 'user_sex': '23',
  'user_name': '31231', 'user_role_id': 2},
 {'user_verify': None, 'group_role_arr': None, 'user_email': 'test@tuandai.com', 'id': 7, 'user_mobile': '186000001123',
  'user_partment': '测试一部', 'adddate': datetime.datetime(2018, 8, 7, 10, 59, 21),
  'login_time': datetime.datetime(2018, 8, 7, 10, 59, 21), 'user_pwd': None, 'user_real_name': '测试人员一',
  'group_role': None, 'user_status': '1', 'user_password': '0a97b19294a175c77376b417c692b9ac', 'usr_ipaddr': None,
  'data_role': '1', 'user_sex': '女', 'user_name': 'user1', 'user_role_id': 4}]
