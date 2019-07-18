#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 9:16
# @Author  : bxf
# @File    : DBC_OPT.py
# @Software: PyCharm
from model.util.TMP_DB_OPT import *
from model.util.TMP_PAGINATOR import *
from model.util.newID import *
from model.util.GET_PARAM import *
from model.FUNC.PARAMS_OPT import *
'''
数据检查基本信息维护
'''

class DBC_OPT:
    def __init__(self,token):
        self.token=token
    def getLists(self,data,**kwargs):
        '''
        获取信息列表
        :param data:
        :param kwargs:
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')
            dbc_sql='select * from dbc_case_info   WHERE '
            dbc_lists=GET_RECORDS(dbc_sql,page,records,group_id=group_id,token=self.token)
            return_data=respdata().sucessResp(dbc_lists)
            return json.dumps(return_data,cls=MyEncoder,ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def getListsForSuite(self, data, **kwargs):
        '''
        获取信息列表
        :param data:
        :param kwargs:
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')
            get_data = data.to_dict()
            del get_data['_page']
            del get_data['_limit']
            del get_data['group_id']
            sql_doc = searchToDatabase('api_case_info', get_data)
            dbc_sql = 'select dbc_id info_id,dbc_desc info_desc,dbc_status info_status,dbc_type info_type,init_data  from dbc_case_info    where init_data is not NULL   and '+sql_doc
            dbc_lists = GET_RECORDS_SQL(dbc_sql, page, records,group_id=group_id,token=self.token)
            data = dbc_lists[0]
            case_list = dbc_lists[2]#getJsonFromDatabase(dbc_lists[1])
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

    def dbcDetail(self,dbc_id):
        '''
        获取明细
        :param data:
        :return:
        '''
        try:
            sql="SELECT t.*,t2.env_id FROM dbc_case_info t LEFT JOIN t_env_detail t2 ON t2.env_d_id=t.env_d_id WHERE t.dbc_id='"+str(dbc_id)+"'"
            dbc_detail=getJsonFromDatabase(sql)


            if dbc_detail:
                dbc_detail=dbc_detail[0]
                # 获取参数 增加判断参数表中是否存在分支
                if dbc_detail["init_data"] != None:
                    if PARAMS_OPT(self.token, dbc_id).getData():
                        init_data = toDict(PARAMS_OPT(self.token, dbc_id).getData()[0]["init_data"])
                    else:
                        init_data = toDict(dbc_detail["init_data"])
                else:
                    init_data = []
                dbc_detail["init_data"] = init_data
                return_data = respdata().sucessResp(dbc_detail)
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
            else:
                return_data = respdata().failMessage('', '不存在该接口信息！')
                return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def dbcInsert(self,data):
        '''
        插入基本信息DBC
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)

            group_id = getCode(get_data['group_id'])
            get_data['group_id'] = group_id
            insert_result = insertToDatabase('dbc_case_info', get_data)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def dbcUpdate(self,data):
        '''
        更新信息
        :return:
        '''
        try:
            get_data = json.loads(data)
            dbc_id=get_data["dbc_id"]
            if "env_id" in get_data:
                del get_data['env_id']
            # 【修改】 增加保存参数到参数表中分支操作
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
                if PARAMS_OPT(self.token, dbc_id).getData():
                    PARAMS_OPT(self.token, dbc_id).updateData(init_data_b)  # 更新操作
                else:
                    PARAMS_OPT(self.token, dbc_id).insertData(init_data_b)  # 插入操作
            update_result = updateToDatabase('dbc_case_info', get_data, dbc_id=dbc_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
    def dbcDelete(self,data):
        '''
        删除信息
        :param data:
        :return:
        '''
        try:
            dba = getJsonMysql()
            dbc_id = data
            delsql = 'delete from dbc_case_info where dbc_id="' + str(dbc_id) + '"'
            DB_CONN().db_Update(delsql)
            return_data = json.dumps(respdata().sucessMessage('', '删除成功！~'))
            return return_data
        except Exception as e:
            return_data = json.dumps(respdata().otherResp(e, '删除失败！~'))
            return return_data
    def dbcSearch(self,data):
        try:
            page = data.get('_page')
            records = data.get('_limit')
            group_id = data.get('group_id')

            del data['_page']
            del data['_limit']
            del data['group_id']
            if data:
                search_sql=searchToDatabase('dbc_case_info',data)
            else:
                search_sql="SELECT * FROM dbc_case_info   WHERE"
            result=GET_RECORDS(search_sql,page,records,group_id=group_id,token=self.token)
            return_data = respdata().sucessResp(result)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
    def dbcParams(self,data):
        dbc_id = json.loads(data)["dbc_id"]
        init_dataa = toDict(PARAMS_OPT(self.token, dbc_id).getData()[0]["init_data"])
        return_data= self.dbcInit( data, init_dataa)
        return return_data

    def dbcInit(self, data,init_data):
        param_data = json.loads(data)["params"]
        params_init1 = []
        for i in param_data:
            params_init = GET_Variable(i)
            params_init1.extend(params_init)
        params = list(set(params_init1))
        dbc_id = json.loads(data)["dbc_id"]

        person_params = PARAMS_OPT(self.token, dbc_id).getData()
        if person_params:
            params_list = self.intiChange(params, init_data)
            return_data = respdata().sucessMessage(params_list, '')
            return json.dumps(return_data, ensure_ascii=False)
        else:
            sql = "select * from dbc_case_info WHERE  dbc_id ='" + dbc_id + "'"
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
            info_id = data["dbc_id"]
            init_data = data["init_data"]
            result = PARAMS_OPT(self.token, info_id).saveParams("dbc_case_info", "dbc_id", init_data)
            return_data = respdata().sucessResp('')
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)