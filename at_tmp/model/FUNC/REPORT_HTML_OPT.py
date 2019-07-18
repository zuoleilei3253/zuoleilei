#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 17:39
# @Author  : bxf
# @File    : REPORT_HTML_OPT.py
# @Software: PyCharm

import time
from model.FUNC.REPORT_DATA import *


class template():
    HTML_HEADER = r'''<div id="mailContentContainer" style="font-size: 14px; padding: 0px;">                
  <div style="height:20px;"></div>
  <div align="center" ><strong style="font-size:32px">功能回归测试报告</strong><h4>%(desc)s</h4></div>
  <div style="height:30px;"></div>
  <div><strong>1.概要信息</strong></div>
  <div style="height:3px;"></div>
  <table width="100%%" cellpadding="0" cellspacing="1" style="background:#000; font-size:12px; border:1px solid; border-spacing: 1px; border-collapse: separate;">
	<tbody>
		<tr>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>报告日期</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>报告人</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>环境类型</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>执行起止时间</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>执行总数</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>通过数</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>失败数</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>测试结论</strong></td>
		</tr>
		<tr>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(report_date)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(report_er)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(report_env_type)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;"><p>%(report_start_time)s</p><p>%(report_end_time)s</p></td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(report_exe_counts)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(report_exe_pass)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(report_exe_fail)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(report_test_result)s</td>
		</tr>
	</tbody>
  </table>
   <div style="height:20px;"></div>
     <div><strong>2.测试信息</strong></div>
  <div style="height:3px;"></div>
 <div >%(report_info)s</div>
 <div style="height:20px;"></div>
  <div><strong>3.执行失败汇总</strong></div>
  <div >%(reports_fail)s</div>
  <div style="height:20px;"></div>
  <details>
  <summary style="color:blue;cursor:pointer;"><strong>附：所有执行明细(点击展开)</strong></summary>
  <div style="height:10px;"></div>
  <div >%(reports)s</div>
  '''
    REPORT_INFO = r''' <table width="100%%" cellpadding="0" cellspacing="1" style="background:#000; font-size:12px; border:1px solid; border-spacing: 1px; border-collapse: separate;">
	<tbody>
		<tr>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>测试项目</strong></td>
            <td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>总接口数</strong></td>
            <td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>接口覆盖数</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>总用例数</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>自动化用例数</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>接口自动化覆盖率</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>用例自动化覆盖率</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>自动化执行率</strong></td>
            <td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>自动化通过率</strong></td>
		</tr>
		<tr>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(group_desc)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(total_api)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(auto_api)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(total_regress)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(total_auto)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(rate_api)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(rate_cover)s</td>
            <td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(rate_exec)s</td>
            <td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(rate_pass)s</td>
	</tbody>
  </table>
    '''
    HTML_REPORT = r'''
  <table width="100%%" align="center" cellpadding="0" cellspacing="1" style="background:#000; font-size:12px; border:1px solid; border-collapse: separate; border-spacing: 1px;">
	<thead>
		<tr>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>用例ID</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>用例路径</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>用例描述</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>类型</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>执行次数</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>预期结果</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>执行结果</strong></td>
			<td height="35" bgcolor="#CCCCCC" style="padding:3px;"><strong>执行结论</strong></td>
		</tr>		
	</thead>
	<tbody id="reports">
  %(reportlist)s
  </tbody>
  </table>
  </details>
</div>'''
    REPORT = '''
    <tr>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(case_id)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(case_path)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(case_desc)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(case_exe_type)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(case_exe_num)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(case_prev_data)s</td>
			<td height="35" bgcolor="#FFFFFF" style="padding:3px;">%(case_exe_realresult)s</td>
			%(case_result)s

		</tr>
    '''


class getHTML(template):
    '''

    '''
    def __init__(self,token=None):
        self.token=token

    def get_report_data(self, type,group_id,search_id=None,task_id=None):
        if type==1:
            return REPORT_DATA(self.token).get_data_rqmt(search_id)
        elif type==2:
            return REPORT_DATA(self.token).getReportData(group_id,search_id,1,1) #回归测试报告 --上线时间
        elif type==3:
            return REPORT_DATA(self.token).getReportData(group_id,task_id,2,1)#回归测试报告 ---任务编号
        elif type==4:
            return REPORT_DATA(self.token).getReportData(group_id,search_id,1,2) #线上回归测试报告 --上线时间
        elif type==5:
            return REPORT_DATA(self.token).getReportData(group_id,task_id,2,2) #线上回归测试报告 --任务编号
        elif type ==6:
            return REPORT_DATA(self.token).getReportData(group_id,search_id,3,int(task_id))#核心定时任务---定时任务编号



    def case_result(self, case_result):
        if case_result == 1:
            htl = ' <td height="35" bgcolor="#FFFFFF" style="color: #31C135;padding:3px;">PASS</td>'
        elif case_result == 2:
            htl = ' <td height="35" bgcolor="#FFFFFF" style="color: #F80C11;padding:3px;">FAIL</td>'
        elif case_result == 3:
            htl = ' <td height="35" bgcolor="#FFFFFF" style="background-color:#dcb67f;color: #F80C11;padding:3px;">ERROR</td>'
        elif case_result == 4:
            htl = ' <td height="35" bgcolor="#FFFFFF" style="padding:3px;">不适用</td>'
        else:
            htl = ' <td height="35" bgcolor="#FFFFFF" style="color: #F80C11;padding:3px;">未执行</td>'
        return htl
  # 明细
    def Reports(self, data):
        rows = []
        if data:
            for i in range(len(data)):
                row = self.REPORT % dict(
                    case_id=data[i]['case_id'],
                    case_path=data[i]['case_path'],
                    case_desc=data[i]['case_desc'],
                    case_exe_type=data[i]['case_exe_type'],
                    case_exe_num=data[i]['case_exe_num'],
                    case_prev_data=data[i]['case_prev_data'],
                    case_exe_realresult=data[i]['case_exe_realresult'],
                    case_result=self.case_result(data[i]['case_exe_result']),
                )
                rows.append(row)
        else:
            row = self.REPORT % dict(
                case_id='无记录',
                case_path='',
                case_desc='',
                case_exe_type='',
                case_exe_num='',
                case_prev_data='',
                case_exe_realresult='',
                case_result=' <td height="35" bgcolor="#FFFFFF" style="color: #F80C11;padding:3px;"></td>',
            )
            rows.append(row)
        reports = self.HTML_REPORT % dict(reportlist=''.join(rows))
        return reports
    # 信息
    def ReportInfo(self,data):
        reports_info=self.REPORT_INFO % dict(
            group_desc=data['group_desc'],
            total_api=data['total_api'],
            auto_api=data['auto_api'],
            total_regress=data['total_regress'],
            total_auto=data['total_auto'],
            rate_api=data['rate_api'],
            rate_cover=data['rate_cover'],
            rate_exec=data['rate_exec'],
            rate_pass=data['rate_pass']
        )
        return reports_info
    # 汇总
    def get_HTML_BODY(self, reports_data):

        html_body = self.HTML_HEADER % dict(
            desc=reports_data['rqmt_desc'],
            report_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            report_er=reports_data['report_er'],  # reports_data['report_er']
            report_env_type=reports_data['report_env_type'],
            report_start_time=reports_data['report_start_time'],
            report_end_time=reports_data['report_end_time'],
            report_exe_counts=reports_data['report_exe_counts'],
            report_exe_pass=reports_data['report_exe_pass'],
            report_exe_fail=reports_data['report_exe_fail'],
            # report_exe_exception=reports_data['report_exe_exception'],
            # report_exe_not=reports_data['report_exe_not'],
            report_test_result=reports_data['report_test_result'],
            reports_fail =self.Reports(reports_data['records_fail']),
            reports=self.Reports(reports_data['records']),
            report_info=self.ReportInfo(reports_data['report_info'])
        )
        return html_body

    def get_html_rqmt(self,typea, group_id,search_id=None,task_id=None):
        data = self.get_report_data(typea,group_id,search_id,task_id)
        if data:
            reports_data = json.loads(data)
            if typea==1:
                reports_data['rqmt_desc']=reports_data['rqmt_desc']
            elif typea==2:
                reports_data['rqmt_desc'] = '上线日期：'+reports_data['online_time']
            elif typea ==3:
                reports_data['rqmt_desc'] = '任务编号为:'+task_id
            elif typea == 4:
                reports_data['rqmt_desc'] = '上线日期：' + reports_data['online_time']
            elif typea == 5:
                reports_data['rqmt_desc'] = '任务编号为:'+task_id
            elif typea==6:
                reports_data['rqmt_desc'] = '【定时任务执行】,批次号为:'+search_id
            html_txt = self.get_HTML_BODY(reports_data)
        else:
            html_txt = '<div align="center" ><strong style="font-size:20px;color:red">尚未有执行结果，如有问题请检查用例明细或日志,或联系管理员！~~</strong></div>'

        return html_txt

    def getHtmlByTask(self,taskId):
        data=REPORT_DATA(self.token).getReportDataByTaskid(taskId)
        if data:
            reports_data = json.loads(data)
            reports_data['rqmt_desc']='<strong style="font-size:15px;color:red">【告警】</strong>'+"   任务编号为："+taskId+""
            html_txt = self.get_HTML_BODY(reports_data)
        else:
            html_txt = '<div align="center" ><strong style="font-size:20px;color:red">尚未有执行结果，如有问题请检查用例明细或日志,或联系管理员！~~</strong></div>'
        return html_txt
