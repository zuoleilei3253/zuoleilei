# coding=utf-8


import sys

sys.path.append("/opt/ATEST")

import time
from model.util.REPORT_DATA import *
from model.util.PUB_FILE_OPT import *


class template():
    HTML_HEADER = r'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<head lang="en">
    <meta charset="UTF-8">
    <title>接口测试报告</title>
    <!-- CSS goes in the document HEAD or added to your external stylesheet -->


</head>
  %(body)s
  </html>'''

    # desc
    # taskID
    # time
    # testtype
    # exetime
    # counts
    # pass
    # fail
    # report

    HTML_BODY = r'''<body>
    <style type="text/css">

table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size:11px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
}
table.gridtable th {
	border-width: 1px;
	border-style: solid;
	border-color: #666666;
	background-color: #aaccf6;
	white-space: pre-line;
}
table.gridtable td {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
	white-space: pre-line;
}

        .content{
            color: black;
            font-weight: bold ;
        }
        #count{
           color: deepskyblue;
        }
        #suCount{
            color: green;
        }
        #failCount{
            color: red;
        }
    </style>
    <h1 ><span>%(desc)s</span>-测试报告</h1> <div id="summary"><p>批&nbsp;&nbsp;次&nbsp;&nbsp;号：<span class="content">%(taskID)s</span></p><p>测试日期：<span class="content">%(time)s</span></p><p>测试时间：<span class="content">2017.11.21 11:52:20</span>--<span class="content">2017.11.21 15:30:29</span></p><p>任务类型：<span class="content">%(testtype)s</span></p><p>执行结果：<span class="content">本批次共执行<span id="count"> %(counts)s</span>条案例，其中：通过：<span id="suCount">%(passcount)s</span>条，不通过： <span id="failCount">%(failcount)s</span>条</span></p> </div> <div id="detailTable"  style=""><p>具体测试明细如下:</p> %(report)s </div>
</body> '''
    HTML_REPORT = '''<table width="100%%" class="gridtable">
  <thead>
    <tr >
      <th width="14%%" >用例ID</th>
      <th width="20%%">用例名称</th>
      <th width="12%%">用例描述</th>
      <th width="5%%">用例类型</th>
      
      <th width="22%%">实际结果</th>
      
      <th width="22%%">预期结果</th>
      <th width="5%%">验证结果</th>
    </tr>
  </thead>
  <tbody id="reports">
  %(reportlist)s
  </tbody>
</table>'''
    REPORT = '''<tr>
                    <td>%(caseID)s</td>
                    <td>%(casename)s</td>
                    <td>%(casedesc)s</td>
                    <td>%(casetype)s</td>
                    <td>%(real)s</td>
                   
                    <td>%(remark)s</td>
                     %(result)s
                </tr>'''
    ENDING_TMPL = ''' '''


class getHTML(template):
    def __init__(self, batchNO, des):
        # self.path=path
        self.batchNO = batchNO
        self.des = des

    def getDate(self):
        result = getReport(self.batchNO)
        # print(result)
        return result

    def passorfail(self, res):
        if res == "Pass":
            htl = ' <td style="color: #31C135">PASS</td>'
        elif res == "Fail":
            htl = ' <td style="color: #F80C11">FAIL</td>'
        else:
            htl = ' <td style="background-color:#dcb67f;color: #F80C11">ERROR</td>'
        return htl

    def getReports(self, result):
        rows = []
        # print(result)
        for i in range(0, len(result['records'])):
            row = self.REPORT % dict(
                caseID=result['records'][i]['case_id'],
                casename=result['records'][i]['case_title'],
                casedesc=result['records'][i]['case_desc'],
                casetype=result['records'][i]['case_type'],
                # uri=result['records'][i][3],
                # method=result['records'][i][4],
                # casetype=result['records'][i]['exe_type'],
                # prev=result['records'][i][5],
                real=result['records'][i]['response_data'],
                result=self.passorfail(result['records'][i]['diff_result']),
                remark=result['records'][i]['remark'],
            )
            rows.append(row)
        reports = self.HTML_REPORT % dict(reportlist=''.join(rows))
        return reports

    # desc
    # taskID
    # time
    # testtype
    # exetime
    # counts
    # passcount
    # failcount
    # report
    def HTMLBODY(self, result):
        htmlbody = self.HTML_BODY % dict(
            desc=self.des,
            taskID=self.batchNO,
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            testtype=result['records'][0]['exe_type'],
            # exetime=datetime.datetime.now(),
            counts=result['counts'],
            passcount=result['passcounts'],
            failcount=result['failcounts'],
            report=self.getReports(result))
        return htmlbody

    def getHTML(self, result):
        HTML = self.HTML_HEADER % dict(
            body=self.HTMLBODY(result)
        )
        return HTML

    def run(self, task_id):
        file_OPT().newFolder(task_id)
        path = '/opt/AT/model/output/report/' + task_id + "/"
        filename = path + self.batchNO + '.html'
        data = self.getDate()
        if data:
            data = self.getDate()
            text = self.getHTML(data)
        else:
            tex = " <h1 ><span>%(desc)s</span>该任务未执行或有问题无法显示，请联系管理员</h1>" % dict(desc=self.batchNO)
            text = self.getHTML(tex)
        fp = open(filename, 'wb')
        fp.write(text.encode('utf-8'))
        fp.close()


if __name__ == '__main__':
    a = getHTML('BATCH-20180323-20816', '测试').run('TASK-20180328160604')
