#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-8 上午10:19
# @Author  : bxf
# @File    : Email_Send.py
# @Software: PyCharm
from model.util.PUB_DATABASEOPT import *
from model.util.PUB_RESP import *

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


SENDER='技术中心-测试部'
class Email_send():
    def __init__(self,email_id):
        self.server = 'smtp.exmail.qq.com'
        self.username = 'Testing@tuandai.com'
        self.passwd = 'Test123'
        self.sender = 'Testing@tuandai.com'
        self.email_id=email_id

    def get_mail_info(self):
        sql = 'select * from p_env_email_confg where email_id = "' + self.email_id + '"'
        info = get_JSON(sql)
        return info[0]
    def send_html(self,data):
        try:
            email_ini = self.get_mail_info()
            message=MIMEMultipart()
            message['Subject']=email_ini['email_title']
            message['From']= Header(SENDER,'utf-8').encode()
            if email_ini['email_cc'] !='':
                message['Cc']=str(email_ini['email_cc']).replace(";",",")
            message['To']=str(email_ini['email_mainrecv']).replace(";",",")
            text_html=MIMEText(data,'html','utf-8')
            text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
            message.attach(text_html)
            smtp = smtplib.SMTP()
            smtp.connect(self.server)
            # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
            smtp.set_debuglevel(1)
            # print(self.username, self.passwd)
            smtp.login(self.username, self.passwd)
            # print(self.get_mainrecv()+self.get_cc())
            smtp.sendmail(self.sender, str(email_ini['email_cc']).replace(";",",").split(",")+ str(email_ini['email_mainrecv']).replace(";",",").split(","), message.as_string())
            return respdata().sucessResp('success')
        except Exception as e:
            return respdata().exceptionResp(e)
    def send_text(self,data):
        try:
            email_ini=self.get_mail_info()
            message = MIMEMultipart()
            message['Subject'] = email_ini['email_title']
            message['From'] = Header(SENDER, 'utf-8').encode()
            if email_ini['email_cc'] != '':
                message['Cc'] = str(email_ini['email_cc']).replace(";",",")
                message['To'] = str(email_ini['email_mainrecv']).replace(";",",")
                text=data
                text_plain = MIMEText(text, 'html', 'utf-8')

                message.attach(text_plain)
                smtp = smtplib.SMTP()
                smtp.connect(self.server)
                # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
                smtp.set_debuglevel(1)

                smtp.login(self.username, self.passwd)
                # print(self.get_mainrecv()+self.get_cc())

                smtp.sendmail(self.sender, str(email_ini['email_cc']).replace(";",",").split(",")+ str(email_ini['email_mainrecv']).replace(";",",").split(","), message.as_string())
                smtp.quit()
            else:
                message['To'] = str(email_ini['email_mainrecv']).replace(";",",")
                text = data
                text_plain = MIMEText(text, 'html', 'utf-8')

                message.attach(text_plain)
                smtp = smtplib.SMTP()
                smtp.connect(self.server)
                # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
                smtp.set_debuglevel(1)

                smtp.login(self.username, self.passwd)
                # print(self.get_mainrecv() + self.get_cc())

                smtp.sendmail(self.sender, str(email_ini['email_mainrecv']).replace(";",",").split(","), message.as_string())
                smtp.quit()

            return True
        except Exception as e:
            print(e)
            return False



if __name__ == '__main__':
    print(Email_send('41628').send_text('02813'))
