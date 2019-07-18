#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-7 下午2:41
# @Author  : bxf
# @File    : EMAIL_OPT.py
# @Software: PyCharm
from model.util.newID import *
from model.util.TMP_PAGINATOR import *
import json


class Email_opt():

    def email_save(self,data):
        getdata = json.loads(data)
        email_id = newID().groupID()
        email_groupname=getdata['email_groupname']
        email_mainrecv=getdata['email_mainrecv']
        email_cc=getdata['email_cc']
        email_title=getdata['email_title']
        group_id= getCode(getdata['group_id'])
        group_id_arr=json.dumps(getdata['group_id_arr'])
        sql = 'insert into p_env_email_confg (email_id,email_groupname,email_mainrecv,email_cc,email_title,group_id,group_id_arr) VALUE (%s,%s,%s,%s,%s,%s,%s)'
        params = (email_id,email_groupname,email_mainrecv,email_cc,email_title,group_id,group_id_arr)
        try:
            dba=getJsonMysql()
            dba.exeUpdateByParamJson(sql, params)
            return_data = resp(200, '成功', '')
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            a = dict()
            a['response'] = '请求错误，错误信息为： ' + str(e)
            return json.dumps(resp(201, '请求失败', a), ensure_ascii=False)
    def email_list(self,data,token):
        groupId = data.get('group_id')
        page = int(data.get('_page'))
        records = int(data.get('_limit'))

        sql = 'select email_id,email_groupname,email_mainrecv,email_cc,email_sender,email_title,group_id,group_id_arr from p_env_email_confg  where '
        try:

            paging = GET_RECORDS_SQL(sql, page, records, groupId,token)
            data = paging[0]

            env_lists =paging[2] #getJsonFromDatabase(paging[1])
            tb_data = []
            if env_lists:
                for i in env_lists:
                    group_id_arr = i['group_id_arr']
                    del i['group_id_arr']
                    i['group_id_arr'] = json.loads(group_id_arr)
                    tb_data.append(i)
            else:
                tb_data = []
            data['tb_data'] = tb_data
            return_data = resp(200, 'success', data)
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            a = dict()
            a['response'] = '请求错误，错误信息为： ' + str(e)
            return json.dumps(resp(202, '请求失败', a), ensure_ascii=False)
    def email_delete(self,data):
        getdata = json.loads(data)
        email_id=getdata['email_id']
        sql = 'delete from p_env_email_confg WHERE email_id =' + str(email_id)
        try:
            dba=getJsonMysql()
            dba.exeUpdate(sql)
            return_data = resp(200, 'success', '')
            return json.dumps(return_data, ensure_ascii=False)
        except Exception as e:
            a = dict()
            a['response'] = '请求错误，错误信息为： ' + str(e)
            return json.dumps(resp(201, '请求失败', a), ensure_ascii=False)

    def update(self, data):
        '''
        修改
        :param data:
        :return:方法
        '''
        try:
            get_data = json.loads(data)
            group_id_arr=get_data['group_id_arr']
            get_data['group_id_arr']=json.dumps(group_id_arr)
            group_id=get_data['group_id']
            get_data['group_id']=getCode(group_id)
            case_id = get_data['email_id']
            update_result = updateToDatabase("p_env_email_confg", get_data, email_id=case_id)
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
        sql = 'DELETE FROM ' + "p_env_email_confg" + sql_doc
        DB_CONN().db_Update(sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)


    def email_send(self,email_id,data):

        return