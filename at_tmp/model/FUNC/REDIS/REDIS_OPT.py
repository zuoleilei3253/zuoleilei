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

class REDIS_OPT:
    def __init__(self,token):
        self.token=token
    def redisInsert(self,data):
        try:
            get_data=json.loads(data)
            group_id = getCode(get_data['group_id'])
            get_data['group_id'] = group_id
            del get_data['group_id_arr']
            result = insertToDatabase('redis_case_info', get_data)
            return_data = respdata().sucessMessage('', "保存成功")
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', "保存失敗！~~c错误为："+str(e))
            return json.dumps(return_data, ensure_ascii=False)

    def redisDelete(self,data):
        try:
            rd_id = data
            delsql = 'delete from redis_case_info where rd_id="' + str(rd_id) + '"'
            DB_CONN().db_Update(delsql)
            return_data = json.dumps(respdata().sucessMessage('', '删除成功！~'))
            return return_data
        except Exception as e:
            return_data = json.dumps(respdata().otherResp(e, '删除失败！~'))
            return return_data
    def redisUpdate(self,data):
        try:
            get_data = json.loads(data)
            rd_id = get_data["rd_id"]
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
                if PARAMS_OPT(self.token, rd_id).getData():
                    PARAMS_OPT(self.token, rd_id).updateData(init_data_b)  # 更新操作
                else:
                    PARAMS_OPT(self.token, rd_id).insertData(init_data_b)  # 插入操作
            update_result = updateToDatabase('redis_case_info', get_data, rd_id=rd_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def redisDetail(self,redis_id):
        try:
            sql="SELECT t.*,t2.env_id FROM redis_case_info t LEFT JOIN t_env_detail t2 ON t2.env_d_id=t.env_d_id WHERE t.rd_id='"+str(redis_id)+"'"
            redis_detail=getJsonFromDatabase(sql)
            if redis_detail:
                redis_detail=redis_detail[0]
                if redis_detail["init_data"] != None:
                    if PARAMS_OPT(self.token, redis_id).getData():
                        init_data = toDict(PARAMS_OPT(self.token, redis_id).getData()[0]["init_data"])
                    else:
                        init_data = toDict(redis_detail["init_data"])
                else:
                    init_data = []
                redis_detail["init_data"] = init_data
                return_data = respdata().sucessResp(redis_detail)
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
            else:
                return_data = respdata().failMessage('', '不存在该接口信息！')
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)


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

    def redisExe(self,data):
        t = time.time()
        response = dict()
        get_data=json.loads(data)
        request_data=get_data['rd_cmd']
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
    def redisParams(self,data):
        shell_id = json.loads(data)["rd_id"]
        init_dd =PARAMS_OPT(self.token, shell_id).getData()
        if init_dd:
            init_dataa = toDict(init_dd[0]["init_data"])
        else:
            init_dataa = toDict([])
        return_data= self.redisInit( data, init_dataa)
        return return_data

    def redisInit(self, data,init_data):
        param_data = json.loads(data)["params"]
        params_init1 = []
        for i in param_data:
            params_init = GET_Variable(i)
            params_init1.extend(params_init)
        params = list(set(params_init1))
        shell_id = json.loads(data)["rd_id"]

        person_params = PARAMS_OPT(self.token, shell_id).getData()
        if person_params:

            params_list = self.intiChange(params, init_data)
            return_data = respdata().sucessMessage(params_list, '')
            return json.dumps(return_data, ensure_ascii=False)
        else:
            sql = "select * from redis_case_info WHERE  rd_id ='" + shell_id + "'"
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
            info_id = data["rd_id"]
            init_data = data["init_data"]
            result = PARAMS_OPT(self.token, info_id).saveParams("redis_case_info", "rd_id", init_data)
            return_data = respdata().sucessResp('')
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)




if __name__ == '__main__':
    params=[{"ip": "${333.string}"},{"ip": "${33.string}"}]
    init_data=[['33',1],['333',777]]
    # print(SHELL_OPT().intiChange(params,init_data))
