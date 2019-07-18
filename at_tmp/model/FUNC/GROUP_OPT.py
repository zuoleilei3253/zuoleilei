#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 10:23
# @Author  : bxf
# @File    : GROUP_OPT.py
# @Software: PyCharm
'''
需求：
对新增数据进行权限控制，通过数据增加group_id


'''
from model.util.TMP_DB_OPT import *
from model.util.PUB_DATABASEOPT import *
from model.util.PUB_RESP import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from model.FUNC.USERINFO.LOG_IN import *
CSRF_ENABLED = True
# 密钥
SECRET_KEY = 'ATest'


class GROP_OPT:
    def __init__(self, token):
        self.user_name = getUserid(token)

    def getGroupidsFromUser(self):
        '''
        获取用户下的数据GROUP_IDS
        :param user_name:
        :return:
        '''
        group_id_sql = "select * from p_role_info_data where id = (SELECT data_role from p_user_info where user_name ='" + self.user_name + "')"
        group_ids = getJsonFromDatabase(group_id_sql)
        if group_ids:
            return group_ids[0]['group_ids']
        else:
            a = []
            return a

    def save_group_id(self):
        return

    def judge_group_id(self, group_id):
        '''
        判断数据是否在用户的权限内
        是  返回ID
        否  返回 False
        :param group_id:
        :return:
        '''
        group_ids = self.getGroupidsFromUser()
        if group_id in group_ids:
            return group_id
        else:
            return False

    def getGroupID(self):
        '''
        获取一级菜单权限ID
        :return: 一级菜单权限ID
        '''
        group_id_sql = 'select group_role from p_user_info where user_name="' + self.user_name + '"'
        group_id = getJsonFromDatabase(group_id_sql)
        if group_id:
            return group_id[0]['group_role']
        else:
            return False


def getLists(data):
    '''
    递归分组菜单--递归方法
    :param data: 菜单数据
    :return:
    '''
    sql = 'select * from p_group_info where parent_id ="' + str(data["id"]) + '"'
    children_data = get_JSON(sql)
    lists = []
    for i in children_data:
        idv = i["id"]
        label = i['group_desc']
        list = dict()
        list['id'] = idv
        list['label'] = label
        lists.append(list)
        getLists(list)
    if lists != []:
        data['children'] = lists
    return data


def getGroup(token):
    '''
    分组菜单数据
    :return:
    '''
    try:
        # code =GROP_OPT(token).getGroupID()\
        code = GROP_OPT(token).getGroupID()
        if code:
            if code != '999':
                sql = 'select id,group_desc label from p_group_info where id="' + str(code) + '"'
            else:
                sql = 'select id,group_desc label from p_group_info where parent_id=1'
            db = getJsonFromDatabase(sql)
            navlists = []
            for i in db:
                # print(i)
                nav_list = getLists(i)
                navlists.append(nav_list)
        else:
            navlists = []
        return json.dumps(respdata().sucessMessage(navlists, ''), ensure_ascii=False)
    except Exception as e:
        return json.dumps(respdata().exceptionResp(e), ensure_ascii=False)


def groupDel(data):
    '''
    分组信息的删除
    :param data: 要删除的id 信息
    :return:
    '''
    try:
        getdata = json.loads(data)
        id = getdata['id']
        dba = DB_CONN()
        sql = 'select code from p_group_info where id =' + str(id)
        code = getJsonFromDatabase(sql)[0]['code']
        sqla = 'delete  from p_group_info where code like "' + str(code) + '%"'
        dba.db_Update(sqla)
        return json.dumps(respdata().sucessResp(''), ensure_ascii=False)
    except Exception as e:
        return json.dumps(respdata().exceptionResp(e), ensure_ascii=False)


def groupInsert(data):
    '''
    分组信息新增
    :param data:
    :return:
    '''
    try:
        getdata = json.loads(data)

        dba = getJsonMysql()
        id = getdata['parent_id']

        sqla = 'select code ,level from p_group_info where id=' + str(id) + ' order by code DESC'
        c = get_JSON(sqla)
        sqlb = 'select code ,level from p_group_info where parent_id=' + str(id) + ' order by code DESC'
        childrn_num = get_JSON(sqlb)

        if childrn_num != ():
            code = childrn_num[0]['code'] + 1
        else:
            code = str(int(c[0]['code'] * 100) + 1)
        level = str(c[0]['level'] + 1)
        group_desc = getdata['label']

        insertsql = 'insert into p_group_info (parent_id,group_desc,code,level) VALUE (%s,%s,%s,%s)'
        params = (id, group_desc, code, level)
        # print(insertsql,params)
        dba.exeUpdateByParamJson(insertsql, params)
        return json.dumps(respdata().sucessResp(''), ensure_ascii=False)
    except Exception as e:
        return json.dumps(respdata().exceptionResp(e), ensure_ascii=False)


def groupUpdate(data):
    '''
    分组信息更新
    :param data:
    :return:
    '''
    try:
        getdata = json.loads(data)
        id = getdata['id']
        desc = getdata['label']
        dba = DB_CONN()
        sql = 'update p_group_info set group_desc= "' + desc + '" where id= ' + str(id)
        # print(sql)
        a = dba.db_Update(sql)
        return json.dumps(respdata().sucessResp(''), ensure_ascii=False)
    except Exception as e:
        return json.dumps(respdata().exceptionResp(e), ensure_ascii=False)





def getCode(id):
    if id:
        if id ==0:
            cd=1
        else:
            code_sql = 'select code from p_group_info where id =' + str(id)
            code = getJsonFromDatabase(code_sql)
            if code:
                cd=code[0]['code']
            else:
                cd =False
        return cd
    else:
        return False

def getGroupName(id):
    if id:
        code_sql = 'select group_desc from p_group_info where code =' + str(id)
        code = getJsonFromDatabase(code_sql)
        return code[0]['group_desc']
    else:
        return False

