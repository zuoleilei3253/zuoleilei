#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/11 10:18
# @Author  : bxf
# @File    : API_OPT.py
# @Software: PyCharm


from model.util.TMP_PAGINATOR import *
from model.util.newID import *
from model.util.GET_PARAM import *
from model.FUNC.PARAMS_OPT import *
import time


class API_OPT:
    def __init__(self, token):
        self.token = token

    def getLists(self, data, **kwargs):
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')

            sql = 'select api_id case_id,title case_desc,method,uri,adddate,api_type,api_is_remold,api_need_login,api_status from api_case_info  where'
            case_lists = GET_RECORDS(sql, page, records, group_id=group_id, token=self.token)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def getListsForSuite(self, data, **kwargs):
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')
            get_data = data.to_dict()
            del get_data['_page']
            del get_data['_limit']
            del get_data['group_id']
            sql_doc = searchToDatabase('api_case_info', get_data)
            sql = 'select api_id info_id,title info_desc,method,uri,api_type,api_status,init_data from api_case_info  where uri is NOT NULL    AND  ' + sql_doc

            case_lists = GET_RECORDS_SQL(sql, page, records, group_id=group_id, token=self.token)
            data = case_lists[0]
            #case_list = getJsonFromDatabase(case_lists[1])
            case_list=case_lists[2]
            tb_data = []
            if case_list:
                for i in case_list:
                    init_data = i['init_data']
                    if init_data != None:
                        i['init_data'] = json.loads(init_data)
                    else:
                        i['init_data'] = None
                    tb_data.append(i)
            data['tb_data'] = tb_data
            return_data = respdata().sucessResp(data)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def apiDelete(self,id, **kwargs):
        '''
        删除
        :param data:
        :return:
        '''
        resultData=self.apiDel(id)
        if resultData:
            return_data = respdata().sucessMessage('', '删除成功！')
        else:
            return_data = respdata().failMessage('', '该接口已关联用例，不允许删除！~~')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)


    def apiDel(self,id):
        sql = 'select info_id from case_suite_info'
        sql_data = DB_CONN().db_Query_tuple(sql)
        api_ids = loop_api(sql_data.fetchall())
        if id in api_ids:
            return_data = False
        else:
            sql = 'DELETE FROM api_case_info  WHERE api_id="' + str(id) + '"'
            DB_CONN().db_Update(sql)
            return_data = True
        return return_data

    def apisDelete(self,data):
        get_data=json.loads(data)
        api_ids=get_data['api_ids']
        apiFail_ids=[]
        try:
            for i in api_ids:
                if self.apiDel(i) is not True:
                    apiFail_ids.append(i)
            if apiFail_ids:
                msg='其中接口【'+str(apiFail_ids)+'】已关联用例，不允许删除！~~'
            else:
                msg = '所选用例全部删除！～'
            return_data = respdata().sucessMessage('', msg)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def paramSave(self,data):
        try:
            data=toDict(data)
            info_id=data["api_id"]
            init_data=data["init_data"]
            result=PARAMS_OPT(self.token,info_id).saveParams("api_case_info","api_id",init_data)
            return_data = respdata().sucessResp('')
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)



    def apiUpdate(self, data):
        try:
            savedata = json.loads(data)
            api_id = savedata['api_id']
            uri = savedata['uri']
            del savedata['id']
            del savedata['group_id']
            del savedata['adddate']
            if uri is None:
                del savedata['uri']
            method = savedata['method']
            if method is None:
                savedata['method'] = ''
            desc = savedata['title']
            head = savedata['headers']
            if head is None or head == "" or head == "{}":
                savedata['headers'] = json.dumps({})
            else:
                savedata['headers'] = json.dumps(head)
            if savedata['params'] is None or savedata['params'] == "" or savedata['params'] == "{}":
                savedata['params'] = json.dumps({})
            else:
                savedata['params'] = json.dumps(savedata['params'], ensure_ascii=False)
            if "env_d_desc" in savedata:
                del savedata['env_d_desc']
            if "env_id" in savedata:
                del savedata['env_id']
            #【修改】 增加保存参数到参数表中分支操作
            if "init_data" in savedata:
                init_data_b=json.dumps(savedata['init_data'],ensure_ascii=False)

                # if savedata['init_data'] is None or savedata['init_data'] == []:
                #     savedata['init_data'] = json.dumps([])
                # else:
                #     init_data_a=savedata['init_data']
                #     init_data_list=[]
                #     for i in init_data_a:
                #         key=i[0]
                #         param_list=[key, None, {}]
                #         init_data_list.append(param_list)
                #     savedata['init_data'] = json.dumps(init_data_list, ensure_ascii=False)
                #判断参数表里的数据是否存在
                if PARAMS_OPT(self.token,api_id).getData():
                    PARAMS_OPT(self.token, api_id).updateData(init_data_b) #更新操作
                else:
                    PARAMS_OPT(self.token, api_id).insertData(init_data_b)# 插入操作
                del savedata['init_data']  #删除，不在主表中保存，用另一个函数单独保存
            if savedata['env_d_id'] is None or savedata['env_d_id'] == "":
                savedata['env_d_id'] = ''
            else:
                savedata['env_d_id'] = savedata['env_d_id']

            time.sleep(0.1)
            updateToDatabase("api_case_info", savedata, api_id=api_id)

            return_data = respdata().sucessResp('')
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def apiSearch(self, data):
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')
            del data['_page']
            del data['_limit']
            if data:
                search_sql = searchToDatabase('api_case_info', data)
            else:
                search_sql = "SELECT * FROM api_case_info   WHERE"
            result = GET_RECORDS(search_sql, page, records, group_id=group_id, token=self.token)
            return_data = respdata().sucessResp(result)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def apiDetail(self, api_id):
        try:
            detail_sql = "SELECT t.*,t2.env_id FROM api_case_info t LEFT JOIN t_env_detail t2 ON t2.env_d_id=t.env_d_id WHERE t.api_id='" + api_id + "'"
            detail = getJsonFromDatabase(detail_sql)
            if detail:
                detail = detail[0]
                if detail["headers"] != None:
                    header = json.loads(detail["headers"])
                    del detail["headers"]
                else:
                    header = {}
                if detail["params"] != None:
                    params = json.loads(detail["params"])
                    del detail["params"]
                else:
                    params = {}
                # 获取参数 增加判断参数表中是否存在分支
                if detail["init_data"] != None:
                    if PARAMS_OPT(self.token, api_id).getData():
                        print("ddddddd*****************************************")
                        init_data = toDict(PARAMS_OPT(self.token, api_id).getData()[0]["init_data"])
                    else:
                        init_data=toDict(detail["init_data"])
                else:
                    init_data = []
                detail["params"] = params
                detail["headers"] = header
                detail["init_data"] = init_data
                del detail["tail_data"]
                # del detail["return_1"]
                # del detail["return_2"]
                return_data = respdata().sucessResp(detail)
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
            else:
                return_data = respdata().failMessage('', '不存在该接口信息！')
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def apiInsert(self, data):
        try:
            get_data = json.loads(data)
            group_id = getCode(get_data['group_id'])
            get_data['group_id'] = group_id
            result = insertToDatabase('api_case_info', get_data)
            return_data = respdata().sucessMessage('', "保存成功")
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            a = dict()
            a['response'] = '请求错误，错误信息为： ' + str(e)
            return json.dumps(resp(202, '请求失败', a), ensure_ascii=False)

    def apiCopy(self, data):
        try:
            get_data = json.loads(data)
            api_id = get_data['api_id']
            sql = "select * from api_case_info where api_id = '{}'".format(api_id)
            result = getJsonFromDatabase(sql)[0]
            for k,v in result.items():
                if k == 'api_id':
                    result[k] = newID().apiId()
                if k == 'title':
                    result[k] = v + "___（复制）"
            del result['adddate']
            insertToDatabase('api_case_info', result)
            return_data = respdata().sucessMessage('', "复制成功!~")
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            a = dict()
            a['response'] = '请求错误，错误信息为： ' + str(e)
            return json.dumps(resp(202, '请求失败', a), ensure_ascii=False)
    def apiParams(self,data):
        api_id = json.loads(data)["api_id"]
        init_dataa = toDict(PARAMS_OPT(self.token, api_id).getData()[0]["init_data"])
        return_data= self.apiInit( data, init_dataa)
        return return_data

    def apiInit(self, data,init_data):
        param_data = json.loads(data)["params"]
        params_init1 = []
        for i in param_data:
            params_init = GET_Variable(i)
            params_init1.extend(params_init)
        params = list(set(params_init1))
        api_id = json.loads(data)["api_id"]
        person_params = PARAMS_OPT(self.token, api_id).getData()
        if person_params:
            params_list = self.intiChange(params, init_data)
            return_data = respdata().sucessMessage(params_list, '')
            return json.dumps(return_data, ensure_ascii=False)
        else:
            sql = "select * from api_case_info WHERE  api_id ='" + api_id + "'"
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
def loop_api(api_t):
    api_l = []
    for i in range(len(api_t)):
        api_l.append(api_t[i][0])
    return api_l

if __name__ == '__main__':
    init_data=[["32p", None, {"key": "32p", "arr_index": 0, "custom_val": "侧hi他hi", "assign_type": "custom"}]]
    params=['32p']


    print(API_OPT('').intiChange(params,init_data))

