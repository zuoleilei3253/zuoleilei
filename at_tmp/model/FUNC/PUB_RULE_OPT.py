#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/16 21:21
# @Author  : bxf
# @File    : PUB_RULE_OPT.py
# @Software: PyCharm
from model.util.TMP_PAGINATOR import *
from model.util.PUB_RESP import *
from model.util.newID import *


class PUB_RULE_OPT:
    def get_lists(self, data):
        '''
        获取规则列表
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql = 'SELECT * FROM t_rule_info     '
            rule_lists = GET_RECORDS_SQL(sql, page, records)
            tb_data = []
            rule_list = rule_lists[2]#getJsonFromDatabase(rule_lists[1])
            if rule_list:
                for i in rule_list:
                    i['rule_import_desc'] = json.loads(i['rule_import_desc'])
                    i['rule_import_project'] = json.loads(i['rule_import_project'])
                    tb_data.append(i)
            else:
                tb_data=[]
            result = rule_lists[0]
            result['tb_data'] = tb_data
            return_data = respdata().sucessResp(result)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def get_lists_by_check(self, data):
        '''
        获取规则列表
        :return:
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql = 'SELECT * FROM t_rule_info  WHERE rule_checked=1     '
            rule_lists = GET_RECORDS_SQL(sql, page, records)
            tb_data = []
            rule_list =rule_lists[2] #getJsonFromDatabase(rule_lists[1])
            if rule_list:
                for i in rule_list:
                    i['rule_import_desc'] = json.loads(i['rule_import_desc'])
                    i['rule_import_project'] = json.loads(i['rule_import_project'])
                    tb_data.append(i)
            else:
                tb_data=[]
            result = rule_lists[0]
            result['tb_data'] = tb_data
            return_data = respdata().sucessResp(result)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def insert(self, data):
        '''
        新增
        :param data: 新增数据
        :return:
        '''
        try:
            get_data = json.loads(data)
            rule_id = newID().RULE_ID()
            rule_import_desc = json.dumps(get_data['rule_import_desc'])
            rule_import_project=get_data['rule_import_project']
            # rule_import_project_a = dict()
            # for i in get_data['rule_import_desc']:
            #     rule_import_project_a[i] = ''
            # rule_import_project.append(rule_import_project_a)
            rule_import_project=json.dumps(rule_import_project)
            rule_checked=get_data['rule_checked']
            del get_data['rule_checked']
            del get_data['rule_import_desc']
            insert_result = insertToDatabase('t_rule_info', get_data, rule_id=rule_id,group_id=0,
                                             rule_import_desc=rule_import_desc, rule_import_project=rule_import_project,rule_checked=rule_checked)
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
            get_data=json.loads(data)
            rule_id = get_data['rule_id']
            update_result = updateToDatabase('t_rule_info', get_data, rule_id=rule_id)
            return_data = respdata().sucessMessage('', '更新成功,更新条数为：' + str(update_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def delete(self, data):
        '''
        删除
        :param data:
        :return:
        '''
        rule_id = data
        sql = 'DELETE FROM t_rule_info WHERE rule_id ="' + rule_id + '"'
        DB_CONN().db_Update(sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    # 规则的用例模板配置

    def case_rule_list(self, id, data):
        '''
        公共规则用例模板获取
        :param data: 规则ID
        :return: 用例模板列表
        '''
        try:
            page = data.get('_page')
            records = data.get('_limit')
            sql = 'SELECT * FROM rule_case_info WHERE rule_id="' + id + '"' + ' AND '
            rule_lists = GET_RECORDS(sql, page, records)
            return_data = respdata().sucessResp(rule_lists)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().exceptionResp(e)
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def case_rule_insert(self, data):
        '''
        用例模板新增
        :param data: 新增数据
        :return:
        '''
        try:
            get_data = json.loads(data)
            rule_case_id = newID().RULE_CASE_ID()
            insert_result = insertToDatabase('rule_case_info', get_data, rule_case_id=rule_case_id)
            return_data = respdata().sucessMessage('', '新增成功，新增记录数为： ' + str(insert_result))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '新增失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def case_rule_update(self, data):
        '''
        用例模板更新
        :param data:
        :return:
        '''
        try:
            get_data=json.loads(data)
            rule_case_id = get_data['rule_case_id']

            del get_data['adddate']
            del get_data['c_id']
            update_result = updateToDatabase('rule_case_info', get_data,rule_case_id=rule_case_id)
            return_data = respdata().sucessMessage('', '更新成功')
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
        except Exception as e:
            return_data = respdata().failMessage('', '更新失败，请检查！错误信息为：' + str(e))
            return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)

    def case_rule_delete(self, data):
        '''
        用例模板删除
        :param data: 用例模板ID
        :return:
        '''
        rule_case_id = data
        sql = 'DELETE FROM rule_case_info WHERE rule_case_id ="' + rule_case_id + '"'
        DB_CONN().db_Update(sql)
        return_data = respdata().sucessMessage('', '删除成功！')
        return json.dumps(return_data, cls=MyEncoder, ensure_ascii=False)
