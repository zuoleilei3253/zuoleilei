#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/28 16:12
# @Author  : bxf
# @File    : ENV_OPT.py
# @Software: PyCharm
from model.util.PUB_RESP import *
from model.util.TMP_PAGINATOR import *
from model.util.newID import *


class ENV_OPT():
    def __init__(self, table):
        self.table = table

    def get_lists(self, data, **kwargs):
        '''
        获取环境列表
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql_doc = ''
            for i in kwargs:
                col = i
                val = kwargs[i]
                sql_doc = ' WHERE ' + col + '="' + str(val) + '" And '
            sql = 'SELECT * FROM ' + self.table + '     ' + sql_doc
            # print(sql)
            case_lists = GET_RECORDS(sql, page, records)
            return_data = respdata().sucessResp(case_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def insert(self, data, **kwargs):
        '''
        添加环境组信息
        :return:
        '''
        try:
            get_data = json.loads(data)
            env_id = newID().envID()
            get_data.update(kwargs)
            insert_result = insertToDatabase(self.table, get_data, env_id=env_id)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def update(self, data):
        '''
        修改
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)
            env_id = get_data['env_id']
            update_result = updateToDatabase(self.table, get_data, env_id=env_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def delete(self, **kwargs):
        '''
        删除
        :param data:
        :return:
        '''
        sql_doc = ''
        for i in kwargs:
            col = i
            val = kwargs[i]
            sql_doc = ' WHERE ' + col + '="' + str(val) + '"'
        sql = 'DELETE FROM ' + self.table + sql_doc
        DB_CONN().db_Update(sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def get_env_lists(self, data, **kwargs):
        '''
                获取环境列表
                :return:
                '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql_doc = ''
            for i in kwargs:
                col = i
                val = kwargs[i]
                sql_doc = ' WHERE ' + col + '="' + str(val) + '" And '
            sql = 'SELECT * FROM ' + self.table + '     ' + sql_doc
            env_lists_sql = GET_RECORDS_SQL(sql, page, records)
            tb_data=[]
            env_lists=env_lists_sql[2]#getJsonFromDatabase(env_lists_sql[1])
            if env_lists:
                for i in env_lists:
                    i ['env_d_params']=json.loads(i['env_d_params'])
                    tb_data.append(i)
            else:
                tb_data=[]
            result=env_lists_sql[0]
            result['tb_data']=tb_data
            return_data = respdata().sucessResp(result)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def env_insert(self, data, **kwargs):
        '''
                获取环境列表
                :return:
                '''
        try:
            get_data = json.loads(data)
            env_d_id = newID().ENV_ID_D()
            env_d_params=json.dumps(get_data['env_d_params'])
            del  get_data['env_d_params']
            get_data.update(kwargs)
            insert_result = insertToDatabase(self.table, get_data, env_d_id=env_d_id,env_d_params=env_d_params)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def env_update(self, data, **kwargs):
        '''
                修改
                :param data:
                :return:
                '''
        try:
            get_data = json.loads(data)
            env_d_id = get_data['env_d_id']
            env_d_params = json.dumps(get_data['env_d_params'])
            del get_data['env_d_params']
            get_data['env_d_params']=env_d_params
            update_result = updateToDatabase(self.table, get_data, env_d_id=env_d_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def env_delete(self, **kwargs):
        '''
                删除
                :param data:
                :return:
                '''
        sql_doc = ''
        for i in kwargs:
            col = i
            val = kwargs[i]
            sql_doc = ' WHERE ' + col + '="' + str(val) + '"'
        sql = 'DELETE FROM ' + self.table + sql_doc
        DB_CONN().db_Update(sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def getEnvLists(self):
        '''
        获取环境清单
        包括 环境ID 和环境描述
        :return:
        '''
        try:

            list_sql="select env_id,env_desc from t_env_info "
            lists=getJsonFromDatabase(list_sql)
            if lists:
                lists=lists[0]
            else:
                lists=[]
            return json.dumps(lists, cls=MyEncoder, ensure_ascii=False)

        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
    def getEnvDetail(self,data):
        '''
        获取环境明细内容
        :param env_id:
        :return:
        '''
        try:
            env_id=data.get('env_id')
            env_type = data.get('env_d_type')
            list_sql="select env_d_id,env_d_desc from t_env_detail WHERE env_id='"+env_id+"'  and env_d_type ='"+str(env_type)+"'"
            lists=getJsonFromDatabase(list_sql)
            if lists:
                lists=lists
            else:
                lists=[]
            return json.dumps(lists, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)





