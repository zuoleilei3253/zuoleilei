#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 10:21
# @Author  : bxf
# @File    : SHELL_OPT.py
# @Software: PyCharm

from model.FUNC.ENUM_OPT import ENUM_OPT
from model.util.TMP_PAGINATOR import *
from model.util.newID import *
from model.FUNC.SHELL.CONNECT_LINUX import *
from model.util.GET_PARAM import *
from model.FUNC.PARAMS_OPT import *
from model.util.PUB_initParams import *
import pandas as pd

class SHELL_OPT:
    def __init__(self,token):
        self.token=token
    def shellInsert(self,data):
        try:
            get_data=json.loads(data)
            group_id = getCode(get_data['group_id'])
            get_data['group_id'] = group_id
            result = insertToDatabase('shell_case_info', get_data)
            return_data = respdata().sucessMessage('', "保存成功")
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', "保存失敗！~~c错误为："+str(e))
            return json.dumps(return_data, ensure_ascii=False)

    def shellDelete(self,data):
        try:
            shell_id = data
            delsql = 'delete from shell_case_info where shell_id="' + str(shell_id) + '"'
            DB_CONN().db_Update(delsql)
            return_data = json.dumps(respdata().sucessMessage('', '删除成功！~'))
            return return_data
        except Exception as e:
            return_data = json.dumps(respdata().otherResp(e, '删除失败！~'))
            return return_data
    def shellUpdate(self,data):
        try:
            get_data = json.loads(data)
            shell_id = get_data["shell_id"]
            if "env_id" in get_data:
                del get_data['env_id']
            if "init_data" in get_data:
                init_data_b = json.dumps(get_data['init_data'])
                if get_data['init_data'] is None or get_data['init_data'] == []:
                    get_data['init_data'] = json.dumps([])
                else:
                    init_data_a = get_data['init_data']
                    init_data_list = []
                    for i in init_data_a:
                        key = i[0]
                        param_list = [key, None, {}]
                        init_data_list.append(param_list)
                    get_data['init_data'] = json.dumps(init_data_list, ensure_ascii=False)
                # 判断参数表里的数据是否存在
                if PARAMS_OPT(self.token, shell_id).getData():
                    PARAMS_OPT(self.token, shell_id).updateData(init_data_b)  # 更新操作
                else:
                    PARAMS_OPT(self.token, shell_id).insertData(init_data_b)  # 插入操作
            update_result = updateToDatabase('shell_case_info', get_data, shell_id=shell_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def shellDetail(self,shell_id):
        try:
            sql="SELECT t.*,t2.env_id FROM shell_case_info t LEFT JOIN t_env_detail t2 ON t2.env_d_id=t.env_d_id WHERE t.shell_id='"+str(shell_id)+"'"
            shell_detail=getJsonFromDatabase(sql)
            if shell_detail:
                shell_detail=shell_detail[0]
                if shell_detail["init_data"] != None:
                    if PARAMS_OPT(self.token, shell_id).getData():
                        init_data = toDict(PARAMS_OPT(self.token, shell_id).getData()[0]["init_data"])
                    else:
                        init_data = toDict(shell_detail["init_data"])
                else:
                    init_data = []
                shell_detail["init_data"] = init_data
                return_data = respdata().sucessResp(shell_detail)
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
            else:
                return_data = respdata().failMessage('', '不存在该接口信息！')
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def readExcelShell(self,file,group_id):
        '''

        :param file: excel文件或io流
        :param group_id:  group_id
        :return:
        有效是1
        无效是2
        '''
        try:
            exceldata = pd.read_excel(file, header=2, sheet_name=0)
            dataToDict=exceldata.to_dict()
            shell_id=ENUM_OPT('shell_excel').get_val('shell_id')
            shell_desc = ENUM_OPT('shell_excel').get_val('shell_desc')
            shell_cmd=ENUM_OPT('shell_excel').get_val('shell_cmd')
            shell_status = ENUM_OPT('shell_excel').get_val('shell_status')
            iddata=dataToDict.get(shell_id)
            descdata=dataToDict.get(shell_desc)
            cmddata=dataToDict.get(shell_cmd)
            statusdata=dataToDict.get(shell_status)
            for i in range(len(iddata)):
                shelldict={}
                shelldict['group_id']=group_id
                id=iddata.get(i)
                if str(id) == "nan":
                    id=newID().SHELL_ID()

                shelldict[shell_id]=id
                shelldict[shell_desc]=descdata.get(i)
                shelldict[shell_cmd]=cmddata.get(i)
                status=statusdata.get(i)
                if status=='有效':
                    status=1
                else:
                    status=2
                shelldict['shell_status']=status
                if shelldict:
                    self.shellInsert(json.dumps(shelldict))
                return_data = respdata().sucessMessage('', '导入成功')
        except Exception as e:
            return_data = respdata().failMessage('错误详情：'+str(e), '导入失败，请检查导入文件类型！')
        return json.dumps(return_data, ensure_ascii=False)
    def writeExcelShell(self,filename,group_id):
        '''

        :param filename: 保存的文件名
        :param group_id: group_id
        :return:
        1 指有效
        2 指无效
        '''
        try:
            sql="SELECT shell_id,shell_desc,shell_cmd,shell_status FROM shell_case_info WHERE group_id='%s'" %group_id
            shelldata=getTupleFromDatabase(sql)
            headers = []
            headers.append(('shell信息录入模板',))
            headers.append(('shell编号', 'shell操作描述', 'shell操作内容', '状态(有效、无效)'))
            headers.append(('shell_id', 'shell_desc', 'shell_cmd', 'shell_status'))
            data = []
            if shelldata:
                for shell in shelldata:
                    status = shell[3]
                    if str(status) == str(1):
                        shell = shell[:3] + ('有效',)
                    else:
                        shell = shell[:3] + ('无效',)
                    data.append(shell)
                #data = list(shelldata)
            headers.extend(data)
            df = pd.DataFrame(headers)
            writer = pd.ExcelWriter(filename)
            df.to_excel(writer, sheet_name='shell', header=False, encoding='utf-8', index=False)
            writer.save()
            writer.close()
        except Exception as e:
            exeLog("导出shell到excel失败，错误详情："+str(e))
            #return_data = respdata().failMessage('错误详情：' + str(e), '导出失败')

    def getListsForSuite(self,data):
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')
            get_data = data.to_dict()
            del get_data['_page']
            del get_data['_limit']
            del get_data['group_id']
            sql_doc = searchToDatabase('shell_case_info', get_data)
            shell_sql = 'select shell_id info_id,shell_desc info_desc,shell_status info_status,shell_type info_type,init_data  from shell_case_info    where init_data is not NULL   and '+sql_doc
            shell_lists = GET_RECORDS_SQL(shell_sql, page, records,group_id=group_id,token=self.token)
            data = shell_lists[0]
            case_list =shell_lists[2] #getJsonFromDatabase(shell_lists[1])
            tb_data = []
            if case_list:
                for i in case_list:
                    init_data = i['init_data']
                    del i['init_data']
                    if init_data !=None:
                        i['init_data'] = json.loads(init_data)
                    else:
                        i['init_data']=None
                    tb_data.append(i)
            else:
                tb_data = []
            data['tb_data'] = tb_data
            return_data = respdata().sucessResp(data)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def shellExe(self,data):
        t = time.time()
        response = dict()
        get_data=json.loads(data)
        request_data=get_data['shell_cmd']
        init_data=get_data['init_data']
        if init_data!=None and init_data !=[]:
            giveParam = json.loads(getParams(init_data))
            response['request'] = GET_PARAM(giveParam,request_data).GET_INIT_DATA()
            env_d_id =get_data['env_d_id']
            env_sql="select * from t_env_detail WHERE env_d_id ='"+env_d_id+"'"
            env_data=getJsonFromDatabase(env_sql)
            linux_env = dict()
            if env_data:
                env_params=json.loads(env_data[0]["env_d_params"])
                linux_env["地址"]=env_params["url"]
                linux_env["端口"]=env_params["port"]
                linux_env["用戶"]=env_params["user"]
                response['response'] = Connect().link_server_IM(env_params,response['request'])
                response['status'] = 200
                response['exetime'] = str(time.time() - t) + "s"
                return_data = respdata().sucessMessage(response,'发送成功！')
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
            else:
                linux_env["錯誤"]="該 "+env_d_id+" 環境地址不存在,或有誤，請查看數據是否正確！~"
                response['response'] = '地址錯誤'
                response['status']=201
                response['env']=linux_env
                response['exetime'] = str(time.time() - t) + "s"
                return_data = respdata().failMessage(response, '发送失败！地址錯誤,{}'.format(env_d_id))
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        elif init_data == []:
            env_d_id = get_data['env_d_id']
            env_sql = "select * from t_env_detail WHERE env_d_id ='" + env_d_id + "'"
            env_data = getJsonFromDatabase(env_sql)
            linux_env = dict()
            if env_data:
                env_params=json.loads(env_data[0]["env_d_params"])
                linux_env["地址"]=env_params["url"]
                linux_env["端口"]=env_params["port"]
                linux_env["用戶"]=env_params["user"]
                response['request'] = request_data
                response['response'] = Connect().link_server_IM(env_params,request_data)
                response['status'] = 200
                response['exetime'] = str(time.time() - t) + "s"
                return_data = respdata().sucessMessage(response,'发送成功！')
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
            else:
                linux_env["錯誤"]="該 "+env_d_id+" 環境地址不存在,或有誤，請查看數據是否正確！~"
                response['response'] = '地址錯誤'
                response['status']=201
                response['env']=linux_env
                response['exetime'] = str(time.time() - t) + "s"
                return_data = respdata().failMessage(response, '发送失败！地址錯誤,{}'.format(env_d_id))
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
    def shellParams(self,data):
        shell_id = json.loads(data)["shell_id"]
        init_dataa = toDict(PARAMS_OPT(self.token, shell_id).getData()[0]["init_data"])
        return_data= self.shellInit( data, init_dataa)
        return return_data

    def shellInit(self, data,init_data):
        param_data = json.loads(data)["params"]
        params_init1 = []
        for i in param_data:
            params_init = GET_Variable(i)
            params_init1.extend(params_init)
        params = list(set(params_init1))
        shell_id = json.loads(data)["shell_id"]

        person_params = PARAMS_OPT(self.token, shell_id).getData()
        if person_params:

            params_list = self.intiChange(params, init_data)
            return_data = respdata().sucessMessage(params_list, '')
            return json.dumps(return_data, ensure_ascii=False)
        else:
            sql = "select * from shell_case_info WHERE  shell_id ='" + shell_id + "'"
            shell_info = getJsonFromDatabase(sql)
            if shell_info:
                init_data = json.loads(shell_info[0]["init_data"])
                if init_data == None:
                    params_list = []
                    for i in params:
                        param = [i, None, {}]
                        params_list.append(param)
                        return_data = respdata().sucessMessage(params_list, '')
                        return json.dumps(return_data, ensure_ascii=False)
                else:
                    params_list = self.intiChange(params, init_data)
                    return_data = respdata().sucessMessage(params_list, '')
                    return json.dumps(return_data, ensure_ascii=False)
            else:
                return_data = respdata().failMessage('', '獲取參數錯誤，請檢查！~~')
                return json.dumps(return_data, ensure_ascii=False)

    def intiChange(self, param_list, init_data):
        init_data_new = []
        for n in param_list:
            init_list = []
            for i in init_data:
                init_list.append(i[0])
            if n in init_list:
                index = init_list.index(n)
                init_data_new.append(init_data[index])
            else:
                param = [n, None, {}]
                init_data_new.append(param)
        return init_data_new
    def paramSave(self, data):
        try:
            data = toDict(data)
            info_id = data["shell_id"]
            init_data = data["init_data"]
            result = PARAMS_OPT(self.token, info_id).saveParams("shell_case_info", "shell_id", init_data)
            return_data = respdata().sucessResp('')
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)




if __name__ == '__main__':
    params=[{"ip": "${333.string}"},{"ip": "${33.string}"}]
    init_data=[['33',1],['333',777]]
    # print(SHELL_OPT().intiChange(params,init_data))
    print(SHELL_OPT().shellParams(params))