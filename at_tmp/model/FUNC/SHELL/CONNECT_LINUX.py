#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 10:49
# @Author  : kimmy-pan
# @File    : CONNECT_LINUX.py


import paramiko
from model.util.PUB_LOG import *
from model.util.PUB_RESP import *
import json


class Connect(object):
    #方法复用,连接客户端通过不同id进来即可
    #这个方法是进行非实时的连接返回,例如ls这样的cmd命令，或者grep这样的命令。。
    # def link_server_cmd(slef):
    #     exeLog('------------开始连接服务器(%s)-----------' % serverip)
    #     client = paramiko.SSHClient()
    #     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     exeLog('------------开始认证......-----------')
    #     client.connect(serverip, 22, username=user, password=pwd, timeout=4)
    #     exeLog('------------认证成功!.....-----------')
    #     while 1:
    #         cmd = input('(输入linux命令)~:')
    #         stdin, stdout, stderr = client.exec_command(cmd)
    #         #enumerate这个写法可遍历迭代对象以及对应索引
    #         for i, line in enumerate(stdout):
    #             exeLog(line.strip("\n"))
    #         break
    #     client.close()
    
    #此方法是进行实时返回，例如tail -f这样的命令，本次监控就用的是此方法。
    #将实时返回的日志返回到本地
    def link_server_IM(self,config, cmd,**kwargs):
        """
        :param config: {"ip":"","user":"","pwd":"","port":""}
        """
        try:
            ip = config["url"]
            user = config["user"]
            pwd = config["pwd"]
            port = int(config["port"])
            # 进行连接
            exeLog('------------开始连接服务器(%s)-----------' % ip)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            exeLog('------------开始认证......-----------')

            client.connect(ip, port, username=user, password=pwd, timeout=4, **kwargs)
            exeLog('------------认证成功!.....-----------')
            stdin, stdout, stderr = client.exec_command(cmd)
            errmessage = stderr.read().decode()
            outmessage = stdout.read().decode()
            if errmessage:
                raise Exception("请输入正确的shell语句,错误详情:"+errmessage)
            else:
                result = outmessage
            client.close()
            return result
            # # 实例化Transport，并建立会话Session
            # transport = client.get_transport()
            # channel = transport.open_session()
            # if channel.active:
            #     # 将命令传入管道中
            #     # cmd = "tail -f /root/redis6388.log"
            #     channel.exec_command(cmd)
            #     exeLog(">>>>>>>>>>>>{} ，执行成功！----------".format(cmd))
            #     while True:
            #         # 判断退出的准备状态
            #         if channel.exit_status_ready():
            #             break
            #         try:
            #             # 获取返回的数据,5M的数据
            #             recv = channel.recv(5242880)
            #             if recv:
            #                 # 将获取的数据解码成gbk的存入本地日志
            #                 exeLog(recv.decode('gbk', 'ignore'))
            #                 result = recv.decode('utf-8', 'ignore')
            #                 return result
            #                 # return_data=respdata().sucessMessage(result,'返回数据成功！~')
            #                 # return json.dumps(return_data,ensure_ascii=False)
            #         # 键盘终端异常
            #         except KeyboardInterrupt:
            #             exeLog("Caught control-C")
            #             channel.send("\x03")  # 发送 ctrl+c
            #             channel.close()
            #             raise Exception("请输入正确的SQL语句")
            #         time.sleep(1)
            #     client.close()
        except Exception as e:
            exeLog("认证失败：{}".format(str(e)))
            return str(e)
            # return_data = respdata().failMessage('','返回失败，请检查数据，错误信息为：' +str(e))
            # return json.dumps(return_data,ensure_ascii=False)


if __name__ == "__main__":
    config = {"ip":"","user":"","pwd":"","cmd":""}
    Connect().link_server_IM(config)