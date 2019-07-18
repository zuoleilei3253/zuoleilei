#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 14:21
# @Author  : bxf
# @File    : USER_INFO.py
# @Software: PyCharm
from model.util.TMP_PAGINATOR import *
from model.util.PUB_RESP import *
from model.util.newID import *
from model.util.ENCRY import *


class USER_INFO():
    def __init__(self, table):
        self.table = table

    def get_lists(self, data, **kwargs):
        '''
        获取用户信息
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql = 'SELECT * FROM ' + self.table + '     '
            case_lists = GET_RECORDS_SQL(sql, page, records)
            data = case_lists[0]
            case_list =case_lists[2] #getJsonFromDatabase(case_lists[1])
            tb_data = []
            if case_list:
                for i in case_list:
                    group_role_arr = i['group_role_arr']
                    del i['group_role_arr']
                    i['group_role_arr'] = json.loads(group_role_arr)
                    tb_data.append(i)
            else:
                tb_data = []
            data['tb_data'] = tb_data
            return_data = respdata().sucessResp(data)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            exeLog("***ERROR****获取用户列表失败，请检查数据***")
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
        exeLog("*********用户信息删除成功*******")
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def insert(self, data, **kwargs):
        '''
        新增
        :param data: 新增数据
        :return:
        '''
        try:
            get_data = json.loads(data)
            pwd = get_data['user_password']
            del get_data['user_password']
            user_password = str(PrpCrypt().encrypt(pwd))
            group_role_arr=get_data['group_role_arr']
            del get_data['group_role_arr']
            group_role_arr=json.dumps(group_role_arr)
            get_data.update(kwargs)
            insert_result = insertToDatabase(self.table, get_data, user_password=user_password,group_role_arr=group_role_arr)
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
            id = get_data['id']
            pwd = get_data['user_password']
            del get_data['user_password']
            user_password = str(PrpCrypt().encrypt(pwd))
            get_data['user_password'] = user_password
            update_result = updateToDatabase(self.table, get_data, id=id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)


    def get_lists_p(self, data, **kwargs):
        '''
        获取权限清单
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql = 'SELECT * FROM ' + self.table + ' WHERE id !=1       '
            case_lists = GET_RECORDS_SQL(sql, page, records)
            data = case_lists[0]
            case_list =case_lists[2] #getJsonFromDatabase(case_lists[1])
            tb_data = []
            if case_list:
                for i in case_list:
                    parent_id_arr = i['parent_id_arr']
                    del i['parent_id_arr']
                    i['parent_id_arr'] = json.loads(parent_id_arr)
                    tb_data.append(i)
            else:
                tb_data = []
            data['tb_data'] = tb_data
            return_data = respdata().sucessResp(data)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def permission_update(self, data):
        '''
        更新权限列表
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)
            id = get_data['id']
            update_result = updateToDatabase(self.table, get_data, id=id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    # 获取权限列表
    def permission_get_lists(self):
        '''
        获取权限列表
        :return:
        '''
        try:
            sql = 'select id, label from p_user_permission where parent_id=0'
            db = getJsonFromDatabase(sql)
            if db:
                navlists = []
                for i in db:
                    nav_list = self.getLists(i)
                    navlists.append(nav_list)

            else:
                navlists = []
            exeLog("********权限列表生成******")
            return json.dumps(respdata().sucessResp(navlists), ensure_ascii=False)

        except Exception as e:
            return json.dumps(respdata().exceptionResp(e), ensure_ascii=False)

    def getLists(self, data):
        '''
        递归权限清单树
        :param data:
        :return:
        '''
        sql = 'select * from p_user_permission where parent_id ="' + str(data["id"]) + '"'
        children_data = getJsonFromDatabase(sql)
        if children_data:
            #num = DB_CONN().db_Query_tuple(sql).rowcount
            lists = []
            for i in children_data:
                idv = i["id"]
                label = i['label']
                list = dict()
                list['id'] = idv
                list['label'] = label
                lists.append(list)
                self.getLists(list)
            if lists != []:
                data['children'] = lists
            return data
        else:
            return data

    def permission_insert(self, data):
        '''
        权限新增模块
        :param data:
        :return:
        '''
        try:
            getdata = json.loads(data)
            id = getdata['parent_id']
            sqla = 'select level from p_user_permission where id=' + str(id) + ' order by id DESC'
            c = getJsonFromDatabase(sqla)
            if c:
                level = str(c[0]['level'] + 1)
            else:
                level = '1'
            getdata['level'] = level
            parent_id_arr = getdata['parent_id_arr']
            del getdata['parent_id_arr']
            parent_id_arr = json.dumps(parent_id_arr)
            getdata['parent_id_arr'] = parent_id_arr
            insert_result = insertToDatabase(self.table, getdata)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    # 角色模块
    def role_insert(self, data):
        '''
        角色新增
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)
            role_permissions_ids = get_data['role_permissions_ids']
            del get_data['role_permissions_ids']
            get_data['role_permissions_ids'] = json.dumps(role_permissions_ids)
            insert_result = insertToDatabase(self.table, get_data)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def role_get_lists(self, data):
        '''
        角色清单
        :param data:
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql = 'SELECT * FROM ' + self.table + '       '
            case_lists = GET_RECORDS_SQL(sql, page, records)
            data = case_lists[0]
            case_list =case_lists[2] #getJsonFromDatabase(case_lists[1])
            tb_data = []
            if case_list:
                for i in case_list:
                    role_permissions_ids = i['role_permissions_ids']
                    del i['role_permissions_ids']
                    i['role_permissions_ids'] = json.loads(role_permissions_ids)
                    tb_data.append(i)
            else:
                tb_data = []
            data['tb_data'] = tb_data
            return_data = respdata().sucessResp(data)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def role_update(self, data):
        '''
        角色清单
        :param data:
        :return:
        '''
        try:
            get_data = json.loads(data)
            id = get_data['id']
            role_permissions_ids = get_data['role_permissions_ids']
            del get_data['role_permissions_ids']
            get_data['role_permissions_ids'] = json.dumps(role_permissions_ids)

            update_result = updateToDatabase(self.table, get_data, id=id)
            return_data = respdata().sucessMessage('', '更新成功,更新记录：' + str(update_result) + ' 条')
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    # 获取菜单列表
    def nav_lists(self):
        '''
        获取菜单列表
        :return:
        '''
        try:
            sql = 'select id, label,url,icon from p_user_permission where parent_id=1'
            db = getJsonFromDatabase(sql)
            # print(db)
            if db:
                navlists = []
                for i in db:
                    nav_list = self.navLists(i)
                    navlists.append(nav_list)
            else:
                navlists = []
            exeLog("********菜单列表列表生成******")
            return json.dumps(respdata().sucessResp(navlists), ensure_ascii=False)

        except Exception as e:
            return json.dumps(respdata().exceptionResp(e), ensure_ascii=False)

    def navLists(self, data):
        '''
        递归权限清单树
        :param data:
        :return:
        '''
        sql = 'select * from p_user_permission where parent_id ="' + str(data["id"]) + '"  And is_menu=1 '
        children_data = getJsonFromDatabase(sql)
        # print(children_data)
        if children_data:
            #num = DB_CONN().db_Query_tuple(sql).rowcount
            lists = []
            for i in children_data:
                idv = i["id"]
                label = i['label']
                url = i['url']
                icon = i['icon']
                list = dict()
                list['id'] = idv
                list['label'] = label
                list['url'] = url
                list['icon'] = icon
                lists.append(list)
                self.getLists(list)
            if lists != []:
                data['children'] = lists
            return data
        else:
            return data

    def get_menu(self, data):
        menu_lists = []
        user_name = data.get('user_name')
        get_role_sql = 'select user_role_id from p_user_info where user_name="' + user_name + '"'
        role_id = getJsonFromDatabase(get_role_sql)[0]['user_role_id']
        role_ids_sql = 'select * from p_role_info where  id = "' + str(role_id) + '"'
        menu_ids = json.loads(getJsonFromDatabase(role_ids_sql)[0]['role_permissions_ids'])
        menu_1_list_sql = 'select id,label,url,icon,level from p_user_permission WHERE level= 1'
        menu_1_list = getJsonFromDatabase(menu_1_list_sql)
        menu_1_lists = []
        menu_2_list_sql = 'select id,label,url,icon,level,parent_id from p_user_permission WHERE level= 2'
        menu_2_list = getJsonFromDatabase(menu_2_list_sql)
        for i in menu_ids:
            for j in menu_1_list:
                if i == j['id']:
                    menu_i = j
                    menu_1_lists.append(menu_i)
                else:
                    pass
        for i in menu_1_lists:
            menu = self.get_menu_2(i, menu_2_list, menu_ids)
            menu_lists.append(menu)
        return json.dumps(respdata().sucessResp(menu_lists), ensure_ascii=False)

    def get_menu_2(self, data, menu_2_list, menu_ids):
        id = data['id']
        menu_2_lists = []
        for i in menu_ids:
            for j in menu_2_list:
                if i == j['id'] and j['parent_id'] == id:
                    menu_2_lists.append(j)
                else:
                    pass
        data['children'] = menu_2_lists
        return data

    def changPassord(self,data):
        try:
            get_data=json.loads(data)
            password=get_data['user_password']
            user_name=get_data['user_name']
            user_password = str(PrpCrypt().encrypt(password))
            password_sql="update p_user_info set user_password = '" + user_password + "' where user_name='"+user_name+"'"
            DB_CONN().db_Update(password_sql)
            return_data=respdata().sucessMessage('','密码更新成功！~请重新登录！~~')
            return json.dumps(return_data,ensure_ascii=False)
        except:
            return_data = respdata().failMessage('', '密码更新失败，请检查！~')
            return json.dumps(return_data, ensure_ascii=False)
