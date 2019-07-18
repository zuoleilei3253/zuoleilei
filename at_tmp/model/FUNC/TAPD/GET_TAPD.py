#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/31 10:02
# @Author  : kimmy-pan
# @File    : GET_TAPD.py

import requests
import tablib
from io import BytesIO
from requests.auth import HTTPBasicAuth
from model.util.PUB_DATABASEOPT import *
from model.util.PUB_LOG import *
from model.FUNC.ENUM_OPT import *
from model.util.newID import *
from model.FUNC.GROUP_OPT import *
import random
# from model.FUNC.CASE_FILE_OPT import *


def build_xls(headers, param):
    '''
    生成导出方法
    :param headers:
    :param table:
    :return:parambook
    '''

    # if param:
    #     param = list(param)
    # else:
    #     param = [()]
    data_set = tablib.Dataset(*param, headers=headers)
    data_book = tablib.Databook()
    data_book.add_sheet(data_set)
    return data_book

def tapd_to_excel(param):
    headers = ('用例ID','用例目录','用例名称','需求ID','前置条件','用例步骤','预期结果','用例类型','用例状态','用例等级','创建人','环境类型','执行类型','执行插件')
    parambook = build_xls(headers, param)
    output = BytesIO()
    output.write(parambook.xls)
    return_param = output.getvalue()
    return return_param

class GET_TAPD():
    def __init__(self,category_id):
        user = md_Config.getConfig("TAPD", "user")
        pwd = md_Config.getConfig("TAPD", "pwd")
        self.auth = HTTPBasicAuth(user, pwd)
        self.url = md_Config.getConfig("TAPD", "url")
        self.session = requests.Session()
        self.session.trust_env = False
        self.category_id = category_id

    def get_count(self):
        r = self.session.get(self.url + "/tcases/count?workspace_id=21840291&category_id={}".format(self.category_id),
                    auth=self.auth)
        if r.json()["data"] != [] :
            count = r.json()["data"]["count"]
            return count
        else:
            return 0

    def get_case_category(self):
        r = self.session.get(self.url + "/tcase_categories?workspace_id=21840291&id={}".
                             format(str(self.category_id).split("&_=")[0]),
                    auth=self.auth)
        # print("============================================")
        # print(str(self.category_id))
        # print(r.json()["data"])
        category_name = r.json()["data"]["TcaseCategory"]["name"]
        return category_name

    def get_case(self):
        """
        如果测试用例数量大于200，要进行分页获取
        :return: list
        """
        all_count = int(self.get_count())
        if all_count != 0:
            name = self.get_case_category()
            category_name = {}
            if all_count < 200 or all_count == 200:
                r = self.session.get(self.url + "/tcases?workspace_id=21840291&category_id={}&limit=200".format(self.category_id),
                        auth=self.auth)
                case = r.json()["data"]
                category_name["category_name"] = self.get_case_category()
                case.append(category_name)
                return case,all_count
            else:
                all_case = []
                loop_time = all_count/200
                if isinstance(loop_time,float):
                    for i in range(1,int(loop_time)+2):
                        r = self.session.get(
                            self.url + "/tcases?workspace_id=21840291&category_id={}&limit=200&page={}".format(self.category_id,i),
                            auth=self.auth)
                        case = r.json()["data"]
                        category_name["category_name"] = name
                        case.append(category_name)
                        all_case.append(case)
                elif isinstance(loop_time,int):
                    for i in range(1,int(loop_time)+1):
                        r = self.session.get(
                            self.url + "/tcases?workspace_id=21840291&category_id={}&limit=200&page={}".format(self.category_id,i),
                            auth=self.auth)
                        case = r.json()["data"]
                        category_name["category_name"] = name
                        case.append(category_name)
                        all_case.append(case)
            return all_case,all_count
        else:
            return [],0,'{}不存在或者{}不存在测试用例，请检查！'.format(self.category_id,self.category_id)


class cloud_to_TAPD():
    """
    云盾平台测试用例同步到TAPD
    先判断目录是否存在于TAPD
    否：返回False，目录不存在TAPD，请创建！
    是：同步测试
    """
    def __init__(self,gourp_id,tapd_id):
        user = md_Config.getConfig("TAPD", "user")
        pwd = md_Config.getConfig("TAPD", "pwd")
        self.auth = HTTPBasicAuth(user, pwd)
        self.url = md_Config.getConfig("TAPD", "url")
        self.session = requests.Session()
        self.session.trust_env = False
        self.gourp_id = gourp_id
        self.tapd_id = tapd_id
        self.n = 0

    def get_cloud_category(self,gourp_id):
        """
        获取云盾平台的用例目录
        :return:
        """
        sql = "SELECT group_desc FROM `p_group_info` where code = '{}'".format(gourp_id)
        cloud_category = get_JSON(sql)[0]["group_desc"]
        return cloud_category

    def get_cloud_case(self):
        """
        获取云盾平台的测试用例
        :return:
        """
        sql = "SELECT case_id,case_desc,case_init,case_step,case_prev_data,case_builder,case_type,case_level,case_exe_status,adddate FROM `regress_case_info` where group_id = '{}'".format(self.gourp_id)
        case = get_JSON(sql)
        return case
    def getRqmtCase(self):
        sql = "SELECT case_id,case_desc,case_init,case_step,case_prev_data,case_builder,case_type,case_level,case_exe_status,adddate FROM `rqmt_case_info` where rqmt_id = '{}'".format(
            self.gourp_id)
        case = get_JSON(sql)
        return case

    def get_case_category(self,gourp_id):
        """
        获取TAPD平台的用例目录
        :return:
        """
        r = self.session.get(self.url + "/tcase_categories?workspace_id=21840291&name={}".
                             format(str(self.get_cloud_category(gourp_id))),
                    auth=self.auth)
        name = r.json()["data"]
        # exeLog("TAPD目录：" + name["TcaseCategory"]["name"])
        return name

    def get_TAPD_category(self):
        """
        判断获取TAPD的用例目录返回是否唯一，且TAPD的父目录是否与云盾平台的父目录一致
        否：继续递归，找到对应的父目录，返回唯一值的子目录
        :return:
        """
        if self.n == 0:
            name = self.get_case_category(self.gourp_id)
            if len(name) == 1:
                if name[0]["TcaseCategory"]["name"] == self.get_cloud_category(self.gourp_id) and \
                                GET_TAPD(name[0]["TcaseCategory"]["parent_id"]).get_case_category() == self.get_cloud_category(self.gourp_id[:-2]):

                    return name
                else:
                    return False,self.get_cloud_category(self.gourp_id[:-2])
            elif len(name) == 0:
                return name
            elif len(name) >1:
                for i in name:
                    if i["TcaseCategory"]["name"] == self.get_cloud_category(self.gourp_id):
                        self.n = self.n + 2
                        return self.get_TAPD_category()
                    else:
                        return False,self.get_cloud_category(self.gourp_id)

        else:
            name = self.get_case_category(self.gourp_id[:-self.n])
            # exeLog("TAPD平台目录：" + str(name))
            if len(name) == 1:
                if name[0]["TcaseCategory"]["name"] == self.get_cloud_category(self.gourp_id[:-2]):

                    r = self.session.get(self.url + "/tcase_categories?workspace_id=21840291&parent_id={}".
                                         format(name[0]["TcaseCategory"]["id"]),auth=self.auth)
                    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    # print(r.json()["data"])
                    return r.json()["data"]
                else:
                    return False,self.get_cloud_category(self.gourp_id[:-2])
            elif len(name) >1:
                self.n = self.n + 2
                return self.get_TAPD_category()

        return

    def gettapd(self):
        """通过id获取tapd的目录"""
        r = self.session.get(self.url + "/tcase_categories?workspace_id=21840291&id={}".
                             format(self.tapd_id),
                    auth=self.auth)
        name = r.json()["data"]
        # exeLog("TAPD目录：" + name["TcaseCategory"]["name"])
        return name


    def sync_case(self,type=None):
        '''
        从APT导入用例到TAPD
        :return:
        '''
        # print("*********************************")
        # print(self.n)
        # category = self.get_TAPD_category()
        category = self.gettapd()
        # if type(category) is list and category != [] and category != None:
        if category :
            errorList = []
            exeLog("获取TAPD目录成功！~")
            param= {}
            if type == 1:
                case = self.getRqmtCase()
            else:
                case = self.get_cloud_case()
            exeLog("导入用例数量：{}".format(len(case)))
            for i in case:
                leveldict = {"1": "高", "2": "中", "3": "低"}
                statusDict = {"1": "normal", "2": "updating", "3": "abandon"}
                typeDict = {"1": "功能测试", "2": "安全测试", "3": "安全测试", "4": "接口测试", "5": "压力测试", "6": "其他"}
                # for i in case:
                for k, v in leveldict.items():
                    if k == str(i["case_level"]):
                        param["priority"] = v
                for k, v in statusDict.items():
                    if k == str(i["case_exe_status"]):
                        param["status"] = v
                for k, v in typeDict.items():
                    if k == str(i["case_type"]):
                        param["type"] = v
                param["steps_S"] = i["case_step"]
                param["precondition"] = i["case_init"]
                param["created"] = str(i["adddate"])
                param["expectation"] = i["case_prev_data"]
                param["creator"] = i["case_builder"]
                param["workspace_id"] = "21840291"
                # for j in category:
                #     if j["TcaseCategory"]["name"] == self.get_cloud_category(self.gourp_id):
                #         param["category_id"] = j["TcaseCategory"]["id"]
                param["category_id"] = category["TcaseCategory"]["id"]
                param["name"] = i["case_desc"]
                print(param)
                r = self.session.post(self.url + "/tcases",data=param,
                                     auth=self.auth)
                time.sleep(1)
                if r.json()["status"] != 1:
                    errorList.append((i["case_id"],r.json()["info"]))
                # print(r.json())
            if errorList == []:
                exeLog("TAPD导入完成！")
                return_data = respdata().sucessMessage('', '导入完成，请检查数据，如有问题请联系管理！')
                return json.dumps(return_data, ensure_ascii=False)
            else:
                exeLog("{}导入失败".format(errorList))
                # print(r.json())
                # print("导入成功！")
                return_data=respdata().failMessage('','导入失败！{}'.format(errorList))
                return json.dumps(return_data,ensure_ascii=False)
        else:
            return_data = respdata().failMessage('', "TAPD不存在<{}>目录，请检查！".format(self.tapd_id))
            return json.dumps(return_data, ensure_ascii=False)
        # elif type(category) is tuple and category[0] == False:
        #     a = category[1]
        #     b = self.get_cloud_category(self.gourp_id[0:3])
        #     if a == b:
        #         c = a
        #         exeLog("TAPD导入失败，错误目录信息："+c)
        #         return_data=respdata().failMessage('',"TAPD不存在<{}>目录".format(c))
        #
        #     else:
        #         c = b + "/" + "..." + "/" +a
        #         exeLog("TAPD导入失败，错误目录信息：" + c)
        #         return_data = respdata().failMessage('', "TAPD不存在<{}>目录".format(c))
        #     return json.dumps(return_data,ensure_ascii=False)
        #
        # elif category == []:
        #     a = self.get_cloud_category(self.gourp_id[:-2])
        #     a1 = self.get_cloud_category(self.gourp_id)
        #     b = self.get_cloud_category(self.gourp_id[0:3])
        #     if a != b:
        #         c = b + "/" + "..." + "/" + a + "/" + a1
        #         exeLog("TAPD导入失败，错误目录信息：" + c)
        #         return_data = respdata().failMessage('', "TAPD不存在<{}>目录".format(c))
        #     else:
        #         c = b + "/" + "..." + "/" +a1
        #         return_data = respdata().failMessage('', "TAPD不存在<{}>目录".format(c))
        #     return json.dumps(return_data,ensure_ascii=False)




def get_all_case(category_id,group_id):

    """
    将tapd数据转换成EXCEL文件
    :param category_id: tapdID
    :return:
    """
    param = []
    for i in category_id:
        result = GET_TAPD(i).get_case()
        case = result[0]
        count = result[1]
        if count != 0:
            exeLog("TAPD用例数量："+str(count))
            # print("TAPD用例数量：")
            # print(count)
            if count > 200 and count != 200:
                name = case[0][200]['category_name']
            elif count < 200 or count == 200:
                name = case[-1]['category_name']

            for j in case:
                if isinstance(j,list):
                    for D in j:
                        if 'Tcase' in D:
                            testcase = D['Tcase']
                            case_level=ENUM_OPT("case_level").get_val(testcase["priority"])
                            case_type = ENUM_OPT("case_type").get_val(testcase["type"])
                            if testcase["status"] == "normal":
                                case_exe_status = 1
                            elif testcase["status"] == "updating":
                                case_exe_status = 2
                            elif testcase["status"] =="abandon":
                                case_exe_status = 3
                            param.append((testcase["id"][12:],name,testcase["name"],"",testcase["precondition"],testcase["steps_S"],testcase["expectation"],case_type,
                                          case_exe_status,case_level,testcase["creator"],group_id))
                            exeLog("写入数据库的用例数量：" + str(len(param)))
                elif isinstance(j,dict):
                    if 'Tcase' in j:
                        testcase = j['Tcase']
                        case_level = ENUM_OPT("case_level").get_val(testcase["priority"])
                        case_type = ENUM_OPT("case_type").get_val(testcase["type"])
                        if testcase["status"] == "normal":
                            case_exe_status = 1
                        elif testcase["status"] == "updating":
                            case_exe_status = 2
                        elif testcase["status"] == "abandon":
                            case_exe_status = 3
                        param.append(
                            (testcase["id"][12:], name, testcase["name"], "", testcase["precondition"], testcase["steps_S"],
                             testcase["expectation"], case_type,
                             case_exe_status, case_level, testcase["creator"],group_id))
                        exeLog("写入数据库的用例数量："+str(len(param)))
        # print("写入数据库的用例数量：")
        # print(len(param))
            print(param)
            # '用例ID'case_id,'用例目录'case_path,'用例名称'case_desc,'需求ID','前置条件'case_init,'用例步骤'case_step,'预期结果'case_prev_data,'用例类型case_type','用例状态'case_exe_status,'用例等级'case_level,'创建人'case_builder,'环境类型','执行类型','执行插件',缺少case_exe_env,case_exe_type,case_exe_plugin
            sql = "INSERT INTO regress_case_info ( case_id,case_path,case_desc,rqmt_id,case_init,case_step,case_prev_data,case_type,case_exe_status,case_level,case_builder,group_id) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            result = DB_CONN().db_Batch(sql, param)
            if type(result) is tuple and result[0] == False:
                return_data = respdata().failMessage('', '操作失败，错误信息：{}'.format(result[1]))
                return json.dumps(return_data, ensure_ascii=False)
            # tapd_to_excel(param)

            else:
                return_data = respdata().sucessMessage('', '操作完成，请检查导入情况')
                return json.dumps(return_data, ensure_ascii=False)
        else:
            return_data = respdata().failMessage('', '操作失败，错误信息：{}'.format(result[3]))
            return json.dumps(return_data, ensure_ascii=False)


class requiretotapd:
    def __init__(self, group_id, tapd_id=None ,rmid=None):
        user = md_Config.getConfig("TAPD", "user")
        pwd = md_Config.getConfig("TAPD", "pwd")
        self.auth = HTTPBasicAuth(user, pwd)
        self.url = md_Config.getConfig("TAPD", "url")
        self.session = requests.Session()
        self.session.trust_env = False
        self.group_id = getCode(group_id)
        self.tapd_id = tapd_id
        self.rmid = rmid

    def sync_tapd(self):
        """同步tapd平台的需求(目录id)"""
        rmList = []
        i = 1
        while True:
            param = {"workspace_id": "21840291", "category_id": self.tapd_id,"page":i}
            r = self.session.get(self.url + "/stories", params=param, auth=self.auth)
            if r.json()["data"] != []:
                rmList.append(r.json()["data"])
                i = i + 1
                time.sleep(1)
            else:
                return rmList

    def sync_tapd_rmid(self):
        """同步tapd平台的需求(需求id)"""

        param = {"workspace_id": "21840291", "id": self.rmid}
        r = self.session.get(self.url + "/stories", params=param, auth=self.auth)
        return r.json()["data"]

    def write_db(self):
        """把需求写进数据库"""
        statusdict = {"planning": 1, "resolved": 2, "rejected": 3, "status_2": 4, "new": 5, "status_3": 6,
                      "suspended": 7, "status_5": 8, "status_7": 9, "status_4": 10, "status_1": 11}
        param = []
        idlist = []
        if self.tapd_id != None and self.tapd_id != "":
            data = self.sync_tapd()
            print("$%#$%#########################################$")
            print(len(data))
            if data != []:
                alldata = []
                for j in data:
                    for k in j:
                        alldata.append(k)
                for i in alldata:
                    id = i["Story"]["id"][-9:]
                    statuskey=i["Story"]["status"]
                    status=statusdict.get(statuskey)
                    param.append((id, i["Story"]["name"], i["Story"]["creator"], i["Story"]["owner"], i["Story"]["due"],
                                  status, self.group_id, i["Story"]["begin"]))
                    idlist.append((id,))
            else:
                return_data = respdata().failMessage('',
                                                     '操作失败，错误信息：{}不存在或者{}不存在需求，请检查！'.format(self.tapd_id, self.tapd_id))
                return json.dumps(return_data, ensure_ascii=False)

        elif self.rmid !=None and self.rmid != "":
            data = self.sync_tapd_rmid()
            for i in data:
                if data != []:
                    id = i["Story"]["id"][-9:]
                    statuskey = i["Story"]["status"]
                    status = statusdict.get(statuskey)
                    param.append(
                        (id, i["Story"]["name"], i["Story"]["creator"], i["Story"]["owner"], i["Story"]["due"],
                         status, self.group_id, i["Story"]["begin"]))
                    idlist.append((id,))
                else:
                    return_data = respdata().failMessage('',
                                                         '操作失败，错误信息：{}不存在或者{}不存在需求，请检查！'.format(self.tapd_id,
                                                                                                self.tapd_id))
                    return json.dumps(return_data, ensure_ascii=False)
        if len(idlist)>0:
            deletesql="DELETE FROM t_requirements_info WHERE rqmt_id= %s"
            DB_CONN().db_Batch(deletesql,idlist)
            sql = "INSERT INTO t_requirements_info (rqmt_id, rqmt_desc, rqmt_dever, rqmt_tester, rqmt_end_date, rqmt_status, group_id, rqmt_begin_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            print("22222222222222222222222222222222222222222222222222222222222222")
            print(len(param))
            result = DB_CONN().db_Batch(sql, param)
            if type(result) is tuple and result[0] == False:
                return_data = respdata().failMessage('', '操作失败，错误信息：{}'.format(result[1]))
                return json.dumps(return_data, ensure_ascii=False)
            else:
                return_data = respdata().sucessMessage('', '操作完成，请检查导入情况')
                return json.dumps(return_data, ensure_ascii=False)
        else:
            return_data = respdata().sucessMessage('', '无数据可插入')
            return json.dumps(return_data, ensure_ascii=False)



# 导入到tapd
def toTapd(data,type=None):
    '''
    导入到tapd
    :param data:{"group_id":"11111"}
    :return:
    '''
    tapd_id = json.loads(data)['tapd_id']
    if type ==1:
        group_id=json.loads(data)['rqmt_id']
    else:
        group_id = json.loads(data)['group_id']
    result=cloud_to_TAPD(group_id,tapd_id).sync_case(type)
    return result
# 导入到平台
def toAtm(data):
    '''
    导入到平台
    :param data:{"tapd_id":["1000202020"],"group_id":"11111"}
    :return:
    '''
    tapd_id=json.loads(data)['tapd_id']
    # print(tapd_id)

    group_id = getCode(json.loads(data)['group_id'])
    # print(group_id)
    result=get_all_case(tapd_id,group_id)
    return result


def requiretoAtm(data):
    '''
    需求导入到平台
    :param data:{"tapd_id":"1000202020","group_id":"11111"}
    :return:
    '''
    tapd_id=json.loads(data).get('tapd_id')
    group_id = json.loads(data).get('group_id')
    rmid=json.loads(data).get('rmid')
    # print(group_id)
    result=requiretotapd(group_id, tapd_id=tapd_id,rmid=rmid).write_db()
    return result



if __name__ == "__main__":
    print(cloud_to_TAPD("1010601").sync_case())
    # print(get_all_case(['1121840291001000501']))
    # print(GET_TAPD("1121840291001001617").get_case())
    # print(get_all_case(["1121840291001000501&_=1540956463397"]))
    param = [('1078822', '回归测试', '测试tapd用例导入ATM平台', '', '<div>&nbsp;测试tapd用例导入ATM平台</div>', '', '', '2', 1, '1', '潘淑桦', '', '', '', '1010601')]

