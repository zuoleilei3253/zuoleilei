#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 10:20
# @Author  : kimmy-pan
# @File    : CHECK_DB.py
from model.util.TMP_DB_OPT import *
from model.FUNC.email_opt.EMAIL_SEND import *
from model.FUNC.REPORT_HTML_OPT import *


class CHECK_DB(object):
    def __init__(self,task_ids):
        self.task_ids = task_ids

    def Get_DB_Keyword(self,task_id):
        # RECORD BY [panshuhua]: 获取task_id的case_result
        caselevel_sql = "SELECT warning_info FROM `w_warning_info`"
        get_caselevel = str(eval(getJsonFromDatabase(caselevel_sql)[0]["warning_info"])["case_type"])
        # RECORD BY [panshuhua]: case_result != 1都告警
        sql = "SELECT t.task_id,c.case_result,d.case_level FROM t_task_to_case t INNER JOIN ((SELECT *,'core' AS case_table FROM core_case_result) UNION ALL (SELECT *,'regress' AS case_table FROM regress_case_result)) c ON c.case_id=t.case_id  LEFT JOIN ((SELECT *,'core' AS case_table FROM core_case_info) UNION ALL (SELECT *,'regress' AS case_table FROM regress_case_info)) d ON d.case_id=c.case_id    WHERE" \
              " t.task_id='{}' and case_level in ({}) and case_result != 1".format(task_id,
                                                                                   get_caselevel.replace("[",
                                                                                                         "").replace(
                                                                                       "]", ""))
        result = getJsonFromDatabase(sql)
        return result



    def Send_result(self,task_id):
        try:
            global email_id
            DB_result = self.Get_DB_Keyword(task_id)
            # RECORD BY [panshuhua]: 获取发送的email_id
            sql = "SELECT warning_email_id FROM `w_warning_info`"
            result = getJsonFromDatabase(sql)
            if result != False:
                email_id = eval(result[0]["warning_email_id"])
            # RECORD BY [panshuhua]: 如果查询结果不为空，则发送警告
            if DB_result !=False:
                for i in email_id:
                    try:
                        report_data=getHTML().getHtmlByTask(task_id)
                        Email_send(i).send_text(report_data)
                        exeLog("========告警邮件id:{}发送成功".format(i))
                        exeLog("******+++++++++++++++ 告警信息发送完成+++++++++++++=========")
                    except Exception as e:
                        errorLog("========告警邮件id:{}发送失败，失败原因：{}".format(i,e))
                        exeLog("******+++++++++++++++ 告警信息发送失败+++++++++++++=========")
            else:
                exeLog("========未查找到case_result!=1数据")
        except Exception as e:
            errorLog(e)

    def CHECK(self):
        exeLog("******+++++++++++++++ 启动告警信息+++++++++++++=========")
        for i in self.task_ids:
            self.Send_result(i)


if __name__ == "__main__":
    CHECK_DB(["TASK_201808201944370022"]).CHECK()