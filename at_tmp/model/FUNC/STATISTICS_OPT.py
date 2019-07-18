#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 14:38
# @Author  : bxf
# @File    : STATISTICS_OPT.py
# @Software: PyCharm

from model.util.TMP_DB_OPT import *
from model.util.PUB_RESP import *
from model.FUNC.GROUP_OPT import *

'''

{
        "stat_list": [
            {
                "test_proj": "测试项目一",
                "test_user": "接口人",
                "test_counts_all": 10,
                "test_counts_auto": 2,
                "test_rate_cover": 0.1,
                "test_rate_exe": 0.9,
                "test_rate_bug": 0.5,
                "stat_time": "2018-08-01"
            },
            {
                "test_proj": "测试项目二",
                "test_user": "接口人",
                "test_counts_all": 21,
                "test_counts_auto": 14,
                "test_rate_cover": 0.9,
                "test_rate_exe": 1,
                "test_rate_bug": 0.2,
                "stat_time": "2018-08-01"
            }
        ],
        "counts": ['', '数据汇总', '31', '16', '40%', '75%', '10%']
    }


'''


class STATIC_OPT:
    def __init__(self,token):
        self.token=token
    def test_cover(self):
        sql = "SELECT (a.num1/b.total) data FROM (SELECT '1' AS id,COUNT(1) AS num1 FROM regress_case_result WHERE case_exe_type!=1) a INNER JOIN (SELECT '1' AS id,COUNT(1) AS total FROM regress_case_result WHERE 1=1) b ON b.id=a.id"
        rate_data = getJsonFromDatabase(sql)[0]
        result = str(float(rate_data['data']) * 100) + '%'
        return result

    def test_statics(self):
        sql = "SELECT total ,a.group_id,b.num atnum ,(b.num/a.total) AS cover_rate,IF(c.num IS NULL,0,(c.num/a.total)) AS exe_rate,1-IF(d.num IS NULL,0,(d.num/a.total)) AS bug_rate FROM (SELECT group_id,COUNT(1) AS total FROM regress_case_info WHERE 1=1 GROUP BY group_id) a LEFT JOIN (SELECT group_id,COUNT(1) AS num FROM regress_case_info WHERE case_exe_type!=1 GROUP BY group_id) b ON b.group_id=a.group_id LEFT JOIN (SELECT group_id,COUNT(1) AS num FROM regress_case_result x1 INNER JOIN regress_case_info x2 ON x2.case_id=x1.case_id WHERE batch_id=(SELECT MAX(batch_id) FROM regress_case_result) GROUP BY group_id) c ON c.group_id=a.group_id LEFT JOIN (SELECT group_id,COUNT(1) AS num FROM regress_case_result x1 INNER JOIN regress_case_info x2 ON x2.case_id=x1.case_id WHERE case_result=3 GROUP BY group_id) d ON d.group_id=a.group_id "

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
            if i['total']:
                static_list['test_counts_all'] = str(i['total'])
            else:
                static_list['test_counts_all'] = '0'

            if i['atnum']:
                static_list['test_counts_auto'] = str(i['atnum'])
            else:
                static_list['test_counts_auto'] = '0'
            # 覆盖率
            try:
                static_list['test_rate_cover'] = str(float(i['cover_rate']) * 100) + '%'
            except:
                static_list['test_rate_cover'] = '0'
            # 执行率
            try:
                static_list['test_rate_exe'] = str(float(i['exe_rate']) * 100) + '%'
            except:
                static_list['test_rate_exe'] = '0'
                # 问题率
            try:
                static_list['test_rate_bug'] = str(float(i['bug_rate']) * 100) + '%'
            except:
                static_list['test_rate_bug'] = '0'
            static_list['test_proj'] = group_descs
            static_list['stat_time'] = time_now
            static_list['test_user'] = ''
            stat_list.append(static_list)
        result['stat_list'] = stat_list
        result["counts"] = STATIC_OPT().test_all()
        return result

    def test_all(self):
        sql = "SELECT total,b.num atnum,(b.num/a.total) AS cover_rate,(c.num/a.total) AS exe_rate,(d.num/a.total) AS bug_rate FROM (SELECT '1' AS id,COUNT(1) AS total FROM regress_case_info WHERE 1=1) a INNER JOIN (SELECT '1' AS id,COUNT(1) AS num FROM regress_case_info WHERE case_exe_type!=1) b ON b.id=a.id INNER JOIN (SELECT '1' AS id,COUNT(1) AS num FROM regress_case_result WHERE batch_id=(SELECT MAX(batch_id) FROM regress_case_result)) c ON c.id=a.id INNER JOIN (SELECT '1' AS id,COUNT(1) AS num FROM regress_case_result WHERE case_result=3) d ON d.id=a.id "
        all_data = getJsonFromDatabase(sql)
        counts = []
        if all_data:
            counts.append('')
            counts.append('数据汇总')
            counts.append(str(all_data[0]['total']))
            counts.append(str(all_data[0]['atnum']))
            counts.append(str(float(all_data[0]['cover_rate']) * 100) + '%')
            counts.append(str(float(all_data[0]['exe_rate']) * 100) + '%')
            counts.append(str(float(all_data[0]['bug_rate']) * 100) + '%')

        return counts

    def iter_data(self):
        iter_sql="SELECT M.group_desc,IFNULL(N.tc_total,0) AS total_req,IFNULL(O.tc_total,0) AS total_rqmt,IFNULL(P.tc_total,0) AS exec_rqmt,IFNULL(Q.tc_total,0) AS total_regress,IFNULL(R.tc_total,0) AS exec_regress,IF((IFNULL(O.tc_total,0)+IFNULL(Q.tc_total,0))=0,'0.000%',CONCAT(LEFT(((IFNULL(P.tc_total,0)+IFNULL(R.tc_total,0))/(IFNULL(O.tc_total,0)+IFNULL(Q.tc_total,0)))*100,5),'%')) AS rate_exec,IF(IFNULL(R.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(S.tc_total,0)/IFNULL(R.tc_total,0))*100,5),'%')) AS rate_pass FROM p_group_info M LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM t_requirements_info A INNER JOIN p_group_info B ON B.code=A.group_id WHERE 1=1 GROUP BY LEFT(B.code,3)) N ON N.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM rqmt_case_info A INNER JOIN t_requirements_info B ON B.rqmt_id=A.rqmt_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE 1=1 GROUP BY LEFT(C.code,3)) O ON O.group_code=M.code LEFT JOIN (SELECT LEFT(E.code,3) AS group_code,COUNT(1) AS tc_total FROM t_task_to_case A INNER JOIN rqmt_task_info B ON B.rqmt_task_id=A.task_id INNER JOIN rqmt_case_info C ON C.case_id=A.case_id INNER JOIN t_requirements_info D ON D.rqmt_id=C.rqmt_id INNER JOIN p_group_info E ON E.code=D.group_id WHERE 1=1 GROUP BY LEFT(E.code,3)) P ON P.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM regress_case_info A INNER JOIN p_group_info B ON B.code=A.group_id WHERE 1=1 GROUP BY LEFT(B.code,3)) Q ON Q.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM regress_case_result GROUP BY case_id) A INNER JOIN regress_case_info B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE 1=1 GROUP BY LEFT(C.code,3)) R ON R.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM regress_case_result WHERE case_result='1' GROUP BY case_id) A INNER JOIN regress_case_info B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE 1=1 GROUP BY LEFT(C.code,3)) S ON S.group_code=M.code WHERE LENGTH(M.code)='3' ORDER BY M.code"

        iter_lists = getJsonFromDatabase(iter_sql)
        iter_data = dict()
        stat_lists = []
        if iter_lists:

            for i in iter_lists:
                try:
                    i['rate_cover'] = str(round(float(i['rate_cover'])* 100,1))+'%'
                except:
                    i['rate_cover']= '0'
                try:
                    i['rate_pass'] = str(round(float(i['rate_pass'])* 100,1))+'%'
                except:
                    i['rate_pass']= '0'
                stat_lists.append(i)
        else:
            stat_lists = []
        iter_data['stat_list'] = stat_lists
        iter_data["counts"] = ['', "", '', '', '', "", "", '']
        result = respdata().sucessMessage(iter_data, "查询成功")
        return json.dumps(result, ensure_ascii=False)

    def at_data(self):
        at_sql="SELECT M.group_desc,IFNULL(N.total,0) AS total_api,IFNULL(O.total,0) AS auto_api,IFNULL(P.tc_total,0) AS total_regress,IFNULL(Q.tc_total,0) AS total_auto,IF(IFNULL(N.total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(O.total,0)/IFNULL(N.total,0))*100,5),'%')) AS rate_api,IF(IFNULL(P.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(Q.tc_total,0)/IFNULL(P.tc_total,0))*100,5),'%')) AS rate_cover,IF(IFNULL(P.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(R.tc_total,0)/IFNULL(P.tc_total,0))*100,5),'%')) AS rate_exec,IF(IFNULL(R.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(S.tc_total,0)/IFNULL(R.tc_total,0))*100,5),'%')) AS rate_pass FROM p_group_info M LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM api_case_info A INNER JOIN p_group_info B ON B.code=A.group_id GROUP BY LEFT(B.code,3)) N ON N.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM api_case_info A INNER JOIN p_group_info B ON B.code=A.group_id INNER JOIN (SELECT info_id FROM case_suite_info WHERE case_id IN (SELECT case_id FROM regress_case_info) GROUP BY info_id HAVING COUNT(1)>0) C ON C.info_id=A.api_id GROUP BY LEFT(B.code,3)) O ON O.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM regress_case_info A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('200','201','202') GROUP BY LEFT(B.code,3)) P ON P.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM regress_case_info A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('200','201','202') AND A.case_exe_type='2' GROUP BY LEFT(B.code,3)) Q ON Q.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM regress_case_result GROUP BY case_id) A INNER JOIN regress_case_info B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('200','201','202') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) R ON R.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM regress_case_result WHERE case_result='1' GROUP BY case_id) A INNER JOIN regress_case_info B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('200','201','202') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) S ON S.group_code=M.code WHERE LENGTH(M.code)='3' ORDER BY M.code"
        iter_lists = getJsonFromDatabase(at_sql)
        at_data = dict()
        stat_lists = []
        if iter_lists:

            for i in iter_lists:
                stat_lists.append(i)
        else:
            stat_lists = []
        at_data['stat_list'] = stat_lists
        at_data["counts"] = ['', "", '', '', '', "", "", '']
        result = respdata().sucessMessage(at_data, "查询成功")
        return json.dumps(result, ensure_ascii=False)
    def UIdata(self):
        at_sql="SELECT M.group_desc,IFNULL(O.tc_total,0) AS total_regress,IFNULL(P.tc_total,0) AS total_auto,IF(IFNULL(O.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(P.tc_total,0)/IFNULL(O.tc_total,0))*100,5),'%')) AS rate_cover,IF(IFNULL(O.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(Q.tc_total,0)/IFNULL(O.tc_total,0))*100,5),'%')) AS rate_exec,IF(IFNULL(Q.tc_total,0)=0,'0.000%',CONCAT(LEFT((IFNULL(R.tc_total,0)/IFNULL(Q.tc_total,0))*100,5),'%')) AS rate_pass FROM p_group_info M LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM regress_case_info A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('301','401','402','501','502','901') GROUP BY LEFT(B.code,3)) O ON O.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS tc_total FROM regress_case_info A INNER JOIN p_group_info B ON B.code=A.group_id WHERE A.case_exe_plugin IN ('301','401','402','501','502','901') AND A.case_exe_type='2' GROUP BY LEFT(B.code,3)) P ON P.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM regress_case_result GROUP BY case_id) A INNER JOIN regress_case_info B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('301','401','402','501','502','901') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) Q ON Q.group_code=M.code LEFT JOIN (SELECT LEFT(C.code,3) AS group_code,COUNT(1) AS tc_total FROM (SELECT case_id FROM regress_case_result WHERE case_result='1' GROUP BY case_id) A INNER JOIN regress_case_info B ON B.case_id=A.case_id INNER JOIN p_group_info C ON C.code=B.group_id WHERE B.case_exe_plugin IN ('301','401','402','501','502','901') AND B.case_exe_type='2' GROUP BY LEFT(C.code,3)) R ON R.group_code=M.code WHERE LENGTH(M.code)='3' ORDER BY M.code"
        iter_lists = getJsonFromDatabase(at_sql)
        at_data = dict()
        stat_lists = []
        if iter_lists:

            for i in iter_lists:
                stat_lists.append(i)
        else:
            stat_lists = []
        at_data['stat_list'] = stat_lists
        at_data["counts"] = ['', "", '', '', '', "", "", '']
        result = respdata().sucessMessage(at_data, "查询成功")
        return json.dumps(result, ensure_ascii=False)

    def test_data(self,data):
        get_data = data.to_dict()
        group_role=GROP_OPT(self.token).getGroupID()
        if group_role == '1':
            group_sql =''
        else:
            group_sql=" And group_role="+str(group_role)
        if 'user_name' in get_data:
            user_name = data.get('user_name')
            if data.get('group_id')== '0':
                sql_doc = group_sql+" AND  M.user_real_name like '%" + user_name + "%'"
            else:
                code = getCode(data.get('group_id'))
                sql_doc = group_sql+" AND N.code  like '%" + str(code) + "%' AND M.user_real_name like '%" + user_name + "%'"
        else:
            if data.get('group_id')== '0':
                sql_doc = group_sql+''
            else:
                code = getCode(data.get('group_id'))
                sql_doc = group_sql+"AND N.code  like '%" + str(code) + "%'"
        test_sql="SELECT M.user_real_name as te_executor,IFNULL(O.tc_total,0) AS te_design_counts,IFNULL(P.tc_total,0) AS te_exe_counts,IFNULL(Q.tc_total,0) AS te_at_counts,IFNULL(R.tc_total,0) AS te_bug_counts,(IFNULL(O.tc_total,0)+IFNULL(P.tc_total,0)+IFNULL(Q.tc_total,0)+IFNULL(R.tc_total,0)) AS te_total FROM p_user_info M LEFT JOIN p_group_info N ON N.id=M.group_role LEFT JOIN (SELECT A.case_builder AS user_real_name,COUNT(1) AS tc_total FROM regress_case_info A WHERE 1=1 GROUP BY A.case_builder) O ON O.user_real_name=M.user_real_name LEFT JOIN (SELECT A.case_executor AS user_real_name,COUNT(1) AS tc_total FROM regress_case_result A GROUP BY A.case_executor) P ON P.user_real_name=M.user_real_name LEFT JOIN (SELECT A.case_exe_user AS user_real_name,COUNT(1) AS tc_total FROM regress_case_info A WHERE A.case_exe_type='2' GROUP BY A.case_exe_user) Q ON Q.user_real_name=M.user_real_name LEFT JOIN (SELECT A.case_executor AS user_real_name,COUNT(1) AS tc_total FROM regress_case_result A INNER JOIN regress_case_info B ON B.case_id=A.case_id WHERE B.case_exe_type='2' AND A.case_result='3' GROUP BY A.case_executor) R ON R.user_real_name=M.user_real_name WHERE  M.user_partment='测试部' "+sql_doc
        test_lists = getJsonFromDatabase(test_sql)
        at_data = dict()
        stat_lists = []
        if test_lists:

            for i in test_lists:
                stat_lists.append(i)
        else:
            stat_lists = []
        at_data['stat_list'] = stat_lists
        at_data["counts"] = ['', "", '', '', '', "", "", '']
        result = respdata().sucessMessage(at_data, "查询成功")
        return json.dumps(result, ensure_ascii=False)
    def pl_data(self):
        test_sql = "SELECT M.code,M.group_desc,IFNULL(N.total,0) AS total_api,IFNULL(O.total,0) AS total_dbc,IFNULL(P.total,0) AS total_shell FROM p_group_info M LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM api_case_info A INNER JOIN p_group_info B ON B.code=A.group_id GROUP BY LEFT(B.code,3)) N ON N.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM dbc_case_info A INNER JOIN p_group_info B ON B.code=A.group_id GROUP BY LEFT(B.code,3)) O ON O.group_code=M.code LEFT JOIN (SELECT LEFT(B.code,3) AS group_code,COUNT(1) AS total FROM shell_case_info A INNER JOIN p_group_info B ON B.code=A.group_id GROUP BY LEFT(B.code,3)) P ON P.group_code=M.code WHERE LENGTH(M.code)='3' ORDER BY M.code"
        test_lists = getJsonFromDatabase(test_sql)
        at_data = dict()
        stat_lists = []
        if test_lists:

            for i in test_lists:
                stat_lists.append(i)
        else:
            stat_lists = []
        at_data['stat_list'] = stat_lists
        at_data["counts"] = ['', "", '', '', '', "", "", '']
        result = respdata().sucessMessage(at_data, "查询成功")
        return json.dumps(result, ensure_ascii=False)
