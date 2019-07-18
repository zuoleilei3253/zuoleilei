#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 16:59
# @Author  : bxf
# @File    : REPORT_DATA.py
# @Software: PyCharm
'''
report_data:报告日期  data now
report_er:报告人
report_env_type:环境类型  case_info
report_exe_time:执行起止时间 case_result
report_exe_counts:用例总数
report_exe_pass:通过数
report_exe_fail:用例失败数
report_test_result:测试结论


case_id:用例ID
case_path:用例路径
case_desc:用例描述
case_exe_type:类型
case_prev_data:预期结果
case_real_result:实际结果
case_result:测试结论
case_detail:执行详情

'''
from model.util.TMP_DB_OPT import *
from model.FUNC.USERINFO.LOG_IN import *
from model.FUNC.GROUP_OPT import *


class REPORT_DATA():
    def __init__(self,token):
        self.token=token

# 回归测试报告--按照时间
    def getReportData(self, group_id, parmas,TimeOrTask,table):
        '''

        :param group_id: 分组ID
        :param parmas: onglinetiome,task_id,batch_id
        :param TimeOrTask: 1-上线时间，2-任务，3-定时批次号
        :param table: 表类型：1-回归用例，2-线上任务
        :return:
        '''
        try:
            #判断是否是定时任务：定时任务无token 传送
            if self.token== None:
                userName="定时任务"
            else:
                userName = getRealName(self.token)
            sql=''
            report_info_sql=''
            report_lists_sql=''
            report_lists_fail_sql=''
            #判断分组级别：获取该分组及分组下的所有级别的分组报告数据
            if group_id==0:
                sql_doc=''
            else:
                sql_doc= "'  AND B.group_id LIKE '" + str(group_id) + "%'"
            #判断读取表格：1为回归报告 2 为线上数据
            if table ==1:
                regress_task_info='regress_task_info'
                regress_case_info='regress_case_info'
                regress_case_result='regress_case_result'
            elif table ==2:
                regress_task_info = 'core_task_info'
                regress_case_info = 'core_case_info'
                regress_case_result = 'core_case_result'
# 判断获取报告的类型：1-上线时间，2-任务，3-定时批次号
            if TimeOrTask ==1:
                sql="SELECT C.case_id,A.online_time,MIN(C.case_time) AS report_start_time,MAX(C.case_time) AS report_end_time,NOW() AS report_date,(CASE B.case_exe_env WHEN '1' THEN '测试环境' WHEN '2' THEN '灰度环境' ELSE '线上环境' END) AS report_env_type,COUNT(1) AS report_exe_counts,SUM(CASE C.case_result WHEN '1' THEN 1 ELSE 0 END) AS report_exe_pass,SUM(CASE C.case_result WHEN '2' THEN 1 WHEN '2' THEN 1 ELSE 0 END) AS report_exe_fail,SUM(CASE WHEN C.case_result IS NULL THEN 1 ELSE 0 END) AS report_exe_not FROM t_task_to_case M LEFT JOIN  "+regress_task_info+" A ON A.task_id=M.task_id LEFT JOIN "+regress_case_info+" B ON B.case_id=M.case_id LEFT JOIN (SELECT 1 AS num,T.* FROM "+regress_case_result+" T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,1 AS num FROM "+regress_case_result+" GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE A.online_time='" + parmas +sql_doc

                report_info_sql = "SELECT M.group_desc,IFNULL(N.total,0) AS total_api,IFNULL(O.total,0) AS auto_api,IFNULL(P.tc_total,0) AS total_regress,IFNULL(Q.tc_total,0) AS total_auto,IF(IFNULL(N.total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(O.total,0)/IFNULL(N.total,0))*100,5),'%')) AS rate_api,IF(IFNULL(P.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(Q.tc_total,0)/IFNULL(P.tc_total,0))*100,5),'%')) AS rate_cover,IF(IFNULL(P.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(R.tc_total,0)/IFNULL(P.tc_total,0))*100,5),'%')) AS rate_exec,IF(IFNULL(R.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(S.tc_total,0)/IFNULL(R.tc_total,0))*100,5),'%')) AS rate_pass FROM p_group_info M LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM api_case_info A INNER JOIN p_group_info B ON B.code=A.group_id GROUP BY LEFT(B.code,3)) N ON N.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM api_case_info A INNER JOIN p_group_info B ON B.code=A.group_id INNER JOIN (SELECT info_id FROM case_suite_info WHERE case_id IN (SELECT case_id FROM "+regress_case_info+") GROUP BY info_id HAVING COUNT(1)>0) C ON C.info_id=A.api_id GROUP BY LEFT(B.code,3)) O ON O.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM "+regress_case_info+" A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('200','201','202') GROUP BY LEFT(B.code,3)) P ON P.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM "+regress_case_info+" A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('200','201','202') AND A.case_exe_type='2' GROUP BY LEFT(B.code,3)) Q ON Q.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM "+regress_case_result+" GROUP BY case_id) A INNER JOIN "+regress_case_info+" B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('200','201','202') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) R ON R.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM "+regress_case_result+" WHERE case_result='1' GROUP BY case_id) A INNER JOIN "+regress_case_info+" B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('200','201','202') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) S ON S.group_code=M.code WHERE LENGTH(M.code)='3' AND M.code LIKE '" + str(group_id) + "%'   ORDER BY M.code"




                report_lists_sql = "SELECT M.case_id,B.case_path,B.case_desc,(CASE B.case_exe_type WHEN '1' THEN '手工' WHEN '2' THEN '自动' END) case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS case_exe_num,IFNULL(C.case_result,0) AS case_exe_result,IFNULL(C.case_real_result,'') AS case_exe_realresult FROM t_task_to_case M LEFT JOIN "+regress_task_info+" A ON A.task_id=M.task_id LEFT JOIN "+regress_case_info+" B ON B.case_id=M.case_id LEFT JOIN (SELECT 1 AS num,T.* FROM "+regress_case_result+" T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,1 AS num FROM "+regress_case_result+" GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE A.online_time='" + parmas + "'  AND B.group_id LIKE '" + str(group_id) + "%'"
                report_lists_fail_sql = "SELECT M.case_id,B.case_path,B.case_desc,(CASE B.case_exe_type WHEN '1' THEN '手工' WHEN '2' THEN '自动' END) case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS case_exe_num,IFNULL(C.case_result,0) AS case_exe_result,IFNULL(C.case_real_result,'') AS case_exe_realresult FROM t_task_to_case M LEFT JOIN "+regress_task_info+" A ON A.task_id=M.task_id LEFT JOIN "+regress_case_info+" B ON B.case_id=M.case_id LEFT JOIN (SELECT 1 AS num,T.* FROM "+regress_case_result+" T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,1 AS num FROM "+regress_case_result+" GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE C.case_result!='1' AND A.online_time='" + parmas + "'  AND B.group_id LIKE '" + str(group_id) + "%'"



            elif TimeOrTask ==2:
                group_id_sql = "SELECT * FROM ((SELECT * FROM core_task_info) UNION ALL (SELECT * FROM regress_task_info)) T WHERE T.task_id='" + parmas + "'"
                task_data = getJsonFromDatabase(group_id_sql)
                group_id = task_data[0]['group_id'][0:3]
                sql = "SELECT C.case_id,A.online_time,MIN(C.case_time) report_start_time,MAX(C.case_time) report_end_time,NOW() report_date,COUNT(1) report_exe_counts,(CASE B.case_exe_env  WHEN '1' THEN '测试环境' WHEN '2' THEN '灰度环境' ELSE '线上环境' END) report_env_type,SUM(CASE C.case_result WHEN '1' THEN 1 ELSE 0 END ) report_exe_pass,SUM(CASE C.case_result WHEN '2' THEN 1 ELSE 0 END) report_exe_fail,SUM(CASE C.case_result WHEN '3' THEN 1 ELSE 0 END) report_exe_exception,SUM(CASE WHEN C.case_result IS NULL THEN 1 ELSE 0 END) report_exe_not FROM t_task_to_case M LEFT JOIN "+regress_task_info+" A ON A.task_id=M.task_id LEFT JOIN "+regress_case_info+" B ON B.case_id=M.case_id LEFT JOIN (SELECT 1 AS num,T.* FROM "+regress_case_result+" T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,1 AS num FROM "+regress_case_result+" GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE A.task_id='" + parmas + "'"
                report_info_sql="SELECT M.group_desc,IFNULL(N.total,0) AS total_api,IFNULL(O.total,0) AS auto_api,IFNULL(P.tc_total,0) AS total_regress,IFNULL(Q.tc_total,0) AS total_auto,IF(IFNULL(N.total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(O.total,0)/IFNULL(N.total,0))*100,5),'%')) AS rate_api,IF(IFNULL(P.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(Q.tc_total,0)/IFNULL(P.tc_total,0))*100,5),'%')) AS rate_cover,IF(IFNULL(P.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(R.tc_total,0)/IFNULL(P.tc_total,0))*100,5),'%')) AS rate_exec,IF(IFNULL(R.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(S.tc_total,0)/IFNULL(R.tc_total,0))*100,5),'%')) AS rate_pass FROM p_group_info M LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM api_case_info A INNER JOIN p_group_info B ON B.code=A.group_id GROUP BY LEFT(B.code,3)) N ON N.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM api_case_info A INNER JOIN p_group_info B ON B.code=A.group_id INNER JOIN (SELECT info_id FROM case_suite_info WHERE case_id IN (SELECT case_id FROM "+regress_case_info+") GROUP BY info_id HAVING COUNT(1)>0) C ON C.info_id=A.api_id GROUP BY LEFT(B.code,3)) O ON O.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM "+regress_case_info+" A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('200','201','202') GROUP BY LEFT(B.code,3)) P ON P.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM "+regress_case_info+" A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('200','201','202') AND A.case_exe_type='2' GROUP BY LEFT(B.code,3)) Q ON Q.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM "+regress_case_result+" GROUP BY case_id) A INNER JOIN "+regress_case_info+" B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('200','201','202') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) R ON R.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM "+regress_case_result+" WHERE case_result='1' GROUP BY case_id) A INNER JOIN "+regress_case_info+" B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('200','201','202') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) S ON S.group_code=M.code WHERE LENGTH(M.code)='3' AND M.code LIKE '" + str(group_id) + "%'   ORDER BY M.code"
                report_lists_sql="SELECT M.case_id,B.case_path,B.case_desc,(CASE B.case_exe_type WHEN '1' THEN '手工' WHEN '2' THEN '自动' END) case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS case_exe_num,IFNULL(C.case_result,0) AS case_exe_result,IFNULL(C.case_real_result,'') AS case_exe_realresult FROM t_task_to_case M LEFT JOIN "+regress_task_info+" A ON A.task_id=M.task_id LEFT JOIN "+regress_case_info+" B ON B.case_id=M.case_id LEFT JOIN (SELECT 1 AS num,T.* FROM "+regress_case_result+" T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,1 AS num FROM "+regress_case_result+" GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE A.task_id='" + parmas + "' "
                report_lists_fail_sql="SELECT M.case_id,B.case_path,B.case_desc,(CASE B.case_exe_type WHEN '1' THEN '手工' WHEN '2' THEN '自动' END) case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS case_exe_num,IFNULL(C.case_result,0) AS case_exe_result,IFNULL(C.case_real_result,'') AS case_exe_realresult FROM t_task_to_case M LEFT JOIN "+regress_task_info+" A ON A.task_id=M.task_id LEFT JOIN "+regress_case_info+" B ON B.case_id=M.case_id LEFT JOIN (SELECT 1 AS num,T.* FROM "+regress_case_result+" T INNER JOIN (SELECT task_id,case_id,MAX(case_time) AS happen_time,1 AS num FROM "+regress_case_result+" GROUP BY task_id,case_id) S ON (T.task_id=T.task_id AND S.case_id=T.case_id AND S.happen_time=T.case_time)) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE C.case_result!='1' AND  A.task_id='" + parmas + "' "


# 定时
            elif TimeOrTask == 3:
                group_id=group_id[0:3]
                sql="SELECT C.case_id,A.online_time,MIN(C.case_time) report_start_time,MAX(C.case_time) report_end_time,NOW() report_date,COUNT(1) report_exe_counts,(CASE B.case_exe_env  WHEN '1' THEN '测试环境' WHEN '2' THEN '灰度环境' ELSE '线上环境' END) report_env_type,SUM(CASE C.case_result WHEN '1' THEN 1 ELSE 0 END ) report_exe_pass,SUM(CASE C.case_result WHEN '2' THEN 1 ELSE 0 END) report_exe_fail,SUM(CASE C.case_result WHEN '3' THEN 1 ELSE 0 END) report_exe_exception,SUM(CASE WHEN C.case_result IS NULL THEN 1 ELSE 0 END) report_exe_not FROM t_task_to_case M LEFT JOIN "+regress_task_info+" A ON A.task_id=M.task_id LEFT JOIN "+regress_case_info+" B ON B.case_id=M.case_id LEFT JOIN (SELECT 1 AS num,T.* FROM "+regress_case_result+" T) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE C.batch_id='"+parmas+"'"
                report_info_sql="SELECT M.group_desc,IFNULL(N.total,0) AS total_api,IFNULL(P.tc_total,0) AS total_regress,IFNULL(O.total,0) AS auto_api,IFNULL(Q.tc_total,0) AS total_auto,IF(IFNULL(N.total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(O.total,0)/IFNULL(N.total,0))*100,5),'%')) AS rate_api,IF(IFNULL(P.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(Q.tc_total,0)/IFNULL(P.tc_total,0))*100,5),'%')) AS rate_cover,IF(IFNULL(P.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(R.tc_total,0)/IFNULL(P.tc_total,0))*100,5),'%')) AS rate_exec,IF(IFNULL(R.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(S.tc_total,0)/IFNULL(R.tc_total,0))*100,5),'%')) AS rate_pass FROM p_group_info M LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM api_case_info A INNER JOIN p_group_info B ON B.code=A.group_id GROUP BY LEFT(B.code,3)) N ON N.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM api_case_info A INNER JOIN p_group_info B ON B.code=A.group_id INNER JOIN (SELECT info_id FROM case_suite_info WHERE case_id IN (SELECT case_id FROM "+regress_case_info+") GROUP BY info_id HAVING COUNT(1)>0) C ON C.info_id=A.api_id GROUP BY LEFT(B.code,3)) O ON O.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM "+regress_case_info+" A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('200','201','202') GROUP BY LEFT(B.code,3)) P ON P.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM "+regress_case_info+" A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('200','201','202') AND A.case_exe_type='2' GROUP BY LEFT(B.code,3)) Q ON Q.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM "+regress_case_result+" GROUP BY case_id) A INNER JOIN "+regress_case_info+" B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('200','201','202') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) R ON R.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM "+regress_case_result+" WHERE case_result='1' GROUP BY case_id) A INNER JOIN "+regress_case_info+" B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('200','201','202') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) S ON S.group_code=M.code WHERE LENGTH(M.code)='3' AND M.code  LIKE  '" + str(group_id) + "%'   ORDER BY M.code"
                report_lists_fail_sql="SELECT M.case_id,B.case_path,B.case_desc,(CASE B.case_exe_type WHEN '1' THEN '手工' WHEN '2' THEN '自动' END) case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS case_exe_num,IFNULL(C.case_result,0) AS case_exe_result,IFNULL(C.case_real_result,'') AS case_exe_realresult FROM t_task_to_case M LEFT JOIN "+regress_task_info+" A ON A.task_id=M.task_id LEFT JOIN "+regress_case_info+" B ON B.case_id=M.case_id LEFT JOIN (SELECT 1 AS num,T.* FROM "+regress_case_result+" T) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE  C.case_result!='1' AND C.batch_id='"+parmas+"'"
                report_lists_sql ="SELECT M.case_id,B.case_path,B.case_desc,(CASE B.case_exe_type WHEN '1' THEN '手工' WHEN '2' THEN '自动' END) case_exe_type,B.case_prev_data,IFNULL(C.num,0) AS case_exe_num,IFNULL(C.case_result,0) AS case_exe_result,IFNULL(C.case_real_result,'') AS case_exe_realresult FROM t_task_to_case M LEFT JOIN "+regress_task_info+" A ON A.task_id=M.task_id LEFT JOIN "+regress_case_info+" B ON B.case_id=M.case_id LEFT JOIN (SELECT 1 AS num,T.* FROM "+regress_case_result+" T) C ON (C.task_id=M.task_id AND C.case_id=M.case_id) WHERE C.batch_id='"+parmas+"'"
            case_lists = getJsonFromDatabase(sql)
            report_info_detail = getJsonFromDatabase(report_info_sql)
            report_lists = getJsonFromDatabase(report_lists_sql)
            report_lists_fail = getJsonFromDatabase(report_lists_fail_sql)
            report_info = case_lists[0]
            report_info['report_exe_counts'] = str(report_info['report_exe_counts'])
            report_info['report_exe_pass'] = str(report_info['report_exe_pass'])
            report_info['report_exe_fail'] = str(report_info['report_exe_fail'])
            # report_info['report_exe_exception'] = str(report_info['report_exe_exception'])
            report_info['report_exe_not'] = str(report_info['report_exe_not'])
            report_info['report_er'] = userName
            if report_info['report_start_time'] is not None:
                report_test_result = ''
                if int(report_info['report_exe_not']) > 0:
                    report_test_result = '未完成'
                # elif int(report_info['report_exe_fail']) > 0 or int(report_info['report_exe_exception']) > 0:
                #     report_test_result = 'Fail'
                elif int(report_info['report_exe_pass']) == int(report_info['report_exe_counts']):
                    report_test_result = 'Pass'
                report_info['report_test_result'] = report_test_result

                if report_info['case_id'] != None:
                    report_info['report_info'] = report_info_detail[0]
                    report_info['records'] = report_lists
                    report_info['records_fail'] = report_lists_fail
                    exeLog("*******REPORT 获取报告数据成功*******")
                    return (json.dumps(report_info, cls=MyEncoder, ensure_ascii=False))
                else:
                    return False
            else:
                return False
        except Exception as e:
            exeLog("*******REPORT 获取报告失败，错误代码为：" + str(e))
            return False

        # 回归测试报告--按照任务