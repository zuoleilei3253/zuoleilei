#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/16 11:33
# @Author  : bxf
# @File    : ATM_run.py
# @Software: PyCharm
import sys

sys.path.append("/opt/ATEST")

from flask import Flask, make_response, send_file, current_app
from flask_cors import *
from model.FUNC.RQMT_OPT import *
from model.FUNC.PUB_RULE_OPT import *
from model.FUNC.TASKT_INFO_OPT import *
from model.FUNC.RULE_TO_CASE import *
from model.FUNC.REGRESS_TO_CASE import *
from model.FUNC.TRANSFORM_OPT import *
from model.FUNC.ENV_OPT import *
from model.FUNC.PLUGIN_OPT import *
from model.FUNC.CASE_FILE_OPT import *
from model.FUNC.USER_INFO import *
from model.FUNC.CASE_RESULT_OPT import *
from model.FUNC.FRAME_OPT import *
from model.FUNC.STATISTICS_OPT import *
from model.FUNC.email_opt.EMAIL_OPT import *
from model.FUNC.WARNING.WARNING_OPT import *
from model.FUNC.API.API_OPT import *
from model.FUNC.WARNING.CHECK_DB import *
from model.FUNC.DBC.DBC_OPT import *
from model.FUNC.SUITE.SUITE_OPT import *
from model.FUNC.DBC.DBC_EXE import *
from model.FUNC.SEACH.SEARCH_OPT import *
from model.FUNC.SHELL.SHELL_OPT import *
from model.FUNC.INDEX.index_data import *
from model.FUNC.USERINFO.OPT_INFO import *
from model.FUNC.To_Excel import *
from model.FUNC.TAPD.GET_TAPD import *
from model.FUNC.TIME_TASK.TIME_TASK_OPT import *
from model.FUNC.API.API_IMP_OPT import *
from model.FUNC.TASK.TASK_OPT import *
from model.FUNC.GET_INIT_PARAMS import *
from model.FUNC.REDIS.REDIS_OPT import *

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 跨域访问

'''
需求操作接口
GET：获取列表
POST：插入数据
PATCH：更新数据
DELETE：删除数据
'''


@app.route('/requirements', methods=['GET', 'POST', 'PATCH'])
@userOpt()
def rqmt_opt():
    # print(current_app.name)
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        return SEARCH_OPT(token,'t_requirements_info').searchOpt(request.args)
    elif method == 'POST':
        return RQMT_OPT().insert(request.get_data().decode())
    elif method == 'PATCH':
        return RQMT_OPT().update(request.get_data().decode())


@app.route('/requirements/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def rqmt_opt_params(id):
    method = request.method
    if method == 'GET':
        return
    elif method == 'DELETE':
        return RQMT_OPT().delete(id)


@app.route('/rqmt_case', methods=['GET', 'POST', 'PATCH'])
@userOpt()
def rqmt_case():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        result = CASE_INFO_OPT('rqmt_case_info', token).get_lists(request.args)  # 需求用例获取，全部
        return result
    elif method == "POST":
        return CASE_INFO_OPT('rqmt_case_info', token).insert(request.get_data().decode())  # 需求用例新增
    elif method == "PATCH":
        return CASE_INFO_OPT('rqmt_case_info', token).rqmtCaseUpdate(request.get_data().decode())  # 用例更新


@app.route('/rqmt_case/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def rqmt_case_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        result = CASE_INFO_OPT('rqmt_case_info', token).getRqmtCaseLists(request.args, rqmt_id=id)  # 需求用例获取，按照需求ID
        return result
    elif method == 'POST' and id == 'create_case_a':
        return RULE_TO_CASE(request.get_data().decode()).rule_to_case(token)  # 公共规则转换成用例
    elif method == 'POST' and id == 'create_case_b':
        return REGRESS_TO_CASE(request.get_data().decode()).regress_case(token)  # 回归用例添加
    elif method == 'DELETE':
        return CASE_INFO_OPT('rqmt_case_info', token).rqmtCaseDeleteOne(request.args, id)
    elif method == 'POST' and id == 'toregress':
        return RQMT_OPT().rqmtToregress(request.get_data().decode())
    elif method == 'POST' and id == "delete":
        return CASE_INFO_OPT('rqmt_case_info', token).rqmtCaseDelete(request.get_data().decode())


'''
公共规则库
'''


@app.route('/rule', methods=['GET', 'POST', 'PATCH'])
@userOpt()
def rule_opt():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        return PUB_RULE_OPT().get_lists(request.args)
    elif method == 'POST':
        return PUB_RULE_OPT().insert(request.get_data().decode())
    elif method == 'PATCH':
        return PUB_RULE_OPT().update(request.get_data().decode())


@app.route('/rule/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def rule_opt_params(id):
    method = request.method
    if method == 'GET' and id == 'bychecked':
        return PUB_RULE_OPT().get_lists_by_check(request.args)

    elif method == 'DELETE':
        return PUB_RULE_OPT().delete(id)


@app.route('/rule_design', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def rule_design():
    method = request.method
    if method == 'GET':
        return
    elif method == 'POST':
        return PUB_RULE_OPT().case_rule_insert(request.get_data().decode())
    elif method == 'PATCH':
        return PUB_RULE_OPT().case_rule_update(request.get_data().decode())


@app.route('/rule_design/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def rule_design_params(id):
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        return PUB_RULE_OPT().case_rule_list(id, request.args)
    elif method == 'DELETE':
        return PUB_RULE_OPT().case_rule_delete(id)

    elif method == 'POST':
        print("*****公共规则转换用例~~*******开始")
        return RULE_TO_CASE(request.get_data().decode()).rule_to_case(token)


# 回归用例
@app.route('/regress_case', methods=['GET', 'POST', 'PATCH'])
@userOpt()
def regress_case():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        # return_data = CASE_INFO_OPT('regress_case_info', token).get_regress_lists(request.args)
        return_data = SEARCH_OPT(token, 'regress_case_info').searchOpt(request.args)
        return return_data
    elif method == 'POST':
        return CASE_INFO_OPT('regress_case_info', token).regressInsert(request.get_data().decode(), case_sign_type=2)
    elif method == 'PATCH':
        return CASE_INFO_OPT('regress_case_info', token).update(request.get_data().decode())


@app.route('/regress_case/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def regress_case_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET' and id == "params":
        result = INIT_OPT(token).getInit(request.args)
        return result
    elif method == 'GET':
        result = CASE_INFO_OPT('regress_case_info', token).getDetail(request.args, case_id=id)
        return result
    elif method == 'DELETE':
        return CASE_INFO_OPT('regress_case_info', token).delete(1,case_id=id)
    elif method == 'POST' and id == "delete":
        return CASE_INFO_OPT('regress_case_info', token).regressDelete(request.get_data().decode())


# 回归用例任务处理
@app.route('/regress_task', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def regress_task_opt():
    method = request.method
    if method == 'GET':
        token = request.headers.get('Token')
        result = SEARCH_OPT(token,'regress_task_info').searchOpt(request.args)
        return result


@app.route('/regress_task/<path:id>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def regress_task_opt_params(id):
    '''
    回归用例的转换
    :param id: group_id
    :return:
    '''
    method = request.method
    token = request.headers.get('Token')
    if method == 'DELETE':
        return TASK_INFO_OPT('regress_task_info').delete_regress(id)
    elif method == 'POST' and id == "transform":
        data = request.get_data().decode()
        get_data = json.loads(data)
        token = request.headers.get('Token')
        online_time = get_data['regress_time']
        group_id = getCode(get_data['group_id'])
        return TRANSFORM_OPT(id, 'regress_case_info', token).insert_to_casetable(online_time, group_id)
    elif method == 'GET':
        return_data = SEARCH_OPT(token, 'regress_task').searchOpt(request.args, id)
        # result = CASE_INFO_OPT('', token).regress_case_lists(request.args, id=id)
        return return_data
    elif method == 'POST' and id =="status":
        result = CASE_RESULT_OPT('regress_case_result').insert_info(request.get_data().decode())
        return result
    elif method == 'POST':
        result = CASE_RESULT_OPT('regress_case_result').insert_info(request.get_data().decode())
        return result
    elif method == 'PATCH':
        result = CASE_RESULT_OPT('regress_case_result').result_update(request.get_data().decode())
        return result



# 核心用例
@app.route('/core_case', methods=['GET', 'POST', 'PATCH'])
@userOpt()
def core_case():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        token = request.headers.get('Token')
        # return_data = CASE_INFO_OPT('core_case_info', token).getCoreLists(request.args, token)
        return_data = SEARCH_OPT(token, 'core_case_info').searchOpt(request.args)
        return return_data
    elif method == 'POST':
        return CASE_INFO_OPT('core_case_info', token).coreInsert(request.get_data().decode(), case_sign_type=1)
    elif method == 'PATCH':
        return CASE_INFO_OPT('core_case_info', token).update(request.get_data().decode())


@app.route('/core_case/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def core_case_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == 'DELETE':
        result = CASE_INFO_OPT('core_case_info', token).delete(1,case_id=id)
        return result
    elif method == 'GET':
        return CASE_INFO_OPT('core_case_info', token).getDetail(request.args, case_id=id)
    elif method == 'POST' and id == "exe":
        return_data = respdata().sucessMessage('', '執行成功')
        return json.dumps(return_data, ensure_ascii=False)
    # 批量删除
    elif method == 'POST' and id == "delete":
        return CASE_INFO_OPT('core_case_info', token).regressDelete(request.get_data().decode())


# 线上用例任务处理
@app.route('/online_task', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def online_task_opt():
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        token = request.headers.get('Token')
        result = SEARCH_OPT(token, 'core_task_info').searchOpt(request.args)
        return result


@app.route('/online_task/<path:id>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def online_task_opt_params(id):
    '''
    回归用例的转换
    :param id: group_id
    :return:
    '''
    method = request.method
    token = request.headers.get('Token')
    if method == 'DELETE':
        return TASK_INFO_OPT('core_task_info').delete_core(id)
    elif method == 'POST' and id == "transform":
        data = request.get_data().decode()
        get_data = json.loads(data)
        online_time = get_data['regress_time']
        group_id = getCode(get_data['group_id'])
        return TRANSFORM_OPT(id, 'core_case_info', token).insert_to_casetable(online_time, group_id)
    elif method == 'GET':
        return_data=SEARCH_OPT(token,'core_task').searchOpt(request.args,id)
        # result = CASE_INFO_OPT('', token).core_case_lists(request.args, id=id)
        return return_data
    elif method == 'POST':
        result = CASE_RESULT_OPT('core_case_result').insert_info(request.get_data().decode())
        return result
    elif method == 'PATCH':
        result = CASE_RESULT_OPT('core_case_result').result_update(request.get_data().decode())
        return result


# 任务列表
##需求任务列表


@app.route('/requirements_task', methods=['GET', 'POST'])
@userOpt()
def requirements_task():
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        result = TASK_INFO_OPT('rqmt_task_info').get_lists(request.args)
        return result
    elif method == 'POST':
        return TASK_INFO_OPT('rqmt_task_info').insert(request.get_data().decode())


@app.route('/requirements_task/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def requirements_task_params(id):
    token = request.headers.get('Token')
    method = request.method
    if method == 'DELETE':
        result = TASK_INFO_OPT('rqmt_task_info').delete(id)
        return result
    elif method == 'GET':
        return TASK_INFO_OPT('rqmt_task_info').get_lists(request.args, rqmt_id=id)
    elif method == 'POST':
        token = request.headers.get('Token')
        print(token)
        return TRANSFORM_OPT(id, 'rqmt_case_info', token).insert_to_casetable('', '1')


# 用例执行
# 手工用例执行
@app.route('/case_v3', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def case_info_v3():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        result = CASE_INFO_OPT('t_case_info', token).get_lists(request.args, case_sign_type=1)
        return result
    return


@app.route('/case_v3/<path:id>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def case_info_v3_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        result = CASE_INFO_OPT('', token).rqmt_case_lists(request.args, id=id)
        return result
    elif method == 'POST':
        result = CASE_RESULT_OPT('rqmt_case_result').insert_info(request.get_data().decode())
        return result
    elif method == 'PATCH':
        result = CASE_RESULT_OPT('rqmt_case_result').result_update(request.get_data().decode())
        return result


# 导入导出案例
@app.route('/file_opt/<path:id>', methods=['POST', 'GET'])
def file_opt(id):
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET' and id == 'rqmt_case':
        rqmt_id = request.args.get('rqmt_id')
        time_id = newID().FILT_ID()
        filename = "{0}.xlsx".format(rqmt_id + '_' + str(time_id))
        # response=make_response(CASE_FILE_OPT().rqmt_case_export_opt(request.args))
        CASE_FILE_OPT().case_write(filename, 'rqmt_case_info',None, rqmt_id=rqmt_id)
        response = make_response(send_file(filename))
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename=" + filename
        return response
    elif method == 'POST' and id == 'rqmt_case':
        opt_files = request.files['file']
        rqmt_id = request.form['rqmt_id']
        result = CASE_FILE_OPT().imt_excel(opt_files, 'rqmt_case_info', rqmt_id, 1, None)
        return result

    elif method == 'GET' and id == 'regress':
        group_id = getCode(str(request.args.get('group_id')))
        time_id = newID().FILT_ID()
        filename = "{0}.xlsx".format(str(group_id) + '_' + str(time_id))
        # response=make_response(CASE_FILE_OPT().rqmt_case_export_opt(request.args))
        CASE_FILE_OPT().case_write(filename, 'regress_case_info', group_id=group_id, )
        response = make_response(send_file(filename))
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename=" + filename
        return response
    elif method == 'POST' and id == 'regress':
        opt_files = request.files['case_lists']
        group_id = getCode(request.form['group_id'])
        group_id_arr = request.form.getlist('group_id_arr[]')
        result = CASE_FILE_OPT().imt_excel(opt_files, 'regress_case_info', None, group_id, group_id_arr)
        return result


    elif method == 'GET' and id == 'statics':
        time_id = newID().FILT_ID()
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        filename = "{0}.xlsx".format(str(time_now) + '_' + str(time_id))
        CASE_FILE_OPT().rqmt_case_export_opt()
        response = make_response(CASE_FILE_OPT().rqmt_case_export_opt())
        response = make_response(send_file(filename))
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename=" + filename
        return response


    elif method == 'GET' and id == 'core':
        group_id = getCode(str(request.args.get('group_id')))
        time_id = newID().FILT_ID()
        filename = "{0}.xlsx".format(str(group_id) + '_' + str(time_id))
        # response=make_response(CASE_FILE_OPT().rqmt_case_export_opt(request.args))
        CASE_FILE_OPT().case_write(filename, 'core_case_info', group_id=group_id)
        response = make_response(send_file(filename))
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename=" + filename
        return response
    elif method == 'POST' and id == 'core':
        opt_files = request.files['case_lists']
        group_id = getCode(request.form['group_id'])
        result = CASE_FILE_OPT().imt_excel(opt_files, 'core_case_info', None, group_id, None)
        return result



    elif method == 'GET' and id == 'api':
        group_id = getCode(str(request.args.get('group_id')))
        time_id = newID().FILT_ID()
        filename = "{0}.xlsx".format(str(group_id) + '_' + str(time_id))
        # response=make_response(CASE_FILE_OPT().rqmt_case_export_opt(request.args))
        CASE_FILE_OPT().api_write(filename, group_id)
        response = make_response(send_file(filename))
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename=" + filename
        return response
    elif method == 'POST' and id == 'api':
        opt_files = request.files['excel']
        group_id = getCode(request.form['group_id'])
        result = apiIMP(opt_files,group_id)
        return result
    # shell导入
    elif method == 'GET' and id == 'shell':
        group_id = getCode(str(request.args.get('group_id')))
        time_id = newID().FILT_ID()
        filename = "{0}.xlsx".format(str(group_id) + '_' + str(time_id))
        # response=make_response(CASE_FILE_OPT().rqmt_case_export_opt(request.args))
        #CASE_FILE_OPT().api_write(filename, group_id)
        SHELL_OPT(token).writeExcelShell(filename,group_id)
        response = make_response(send_file(filename))
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename=" + filename
        return response
    elif method == 'POST' and id == 'shell':
        opt_files = request.files['file']
        group_id = request.form['group_id']
        # result = apiIMP(opt_files,group_id)
        result=SHELL_OPT(token).readExcelShell(opt_files,group_id)
        return result

    elif method == 'GET' and id == 'toxmind':
        group_id = getCode(str(request.args.get('group_id')))
        time_id = newID().FILT_ID()
        rqmt_id=request.args.get('rqmt_id')
        filename = "{0}.xlsx".format(str(group_id) + '_' + str(time_id))
        # response=make_response(CASE_FILE_OPT().rqmt_case_export_opt(request.args))
        CASE_FILE_OPT().case_write(filename, 'rqmt_case_info', None,rqmt_id=rqmt_id )
        folder = os.path.exists("./model/output/export_xmindfile")
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs("./model/output/export_xmindfile")
        OUTPUT = "./model/output/export_xmindfile/" + filename.split(".")[0] + ".xmind"
        translate_format(2, OUTPUT=OUTPUT, excel_path=filename,group_id=group_id)
        response = make_response(send_file("model/output/export_xmindfile/" + filename.split(".")[0] + ".xmind"))
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename=" + filename.split(".")[0] + ".xmind"
        return response

    elif method == 'POST' and id == 'xmindtoexcel':
        # time_id = newID().FILT_ID()
        # opt_files = request.files['xcase_lists']
        group_id = request.form['group_id']
        opt_files = request.files['file']
        rqmt_id = request.form['rqmt_id']
        xmind_file = CASE_FILE_OPT().imt_xmind(opt_files)
        result = translate_format(1, xmind_file=xmind_file, table="rqmt_case_info",group_id=group_id,rqmt_id=rqmt_id)
        return json.dumps(result,ensure_ascii=False)

@app.route('/import_test', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def imp():
    token = request.headers.get('Token')
    response = make_response(send_file(getCurruntpath() + "/model/output/importfile/api_info.xlsx"))
    response.headers["Content-Disposition"] = "attachment; filename=api_info.xlsx;"
    return response


# 环境操作
@app.route('/env_opt', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def env_opt():
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        result = ENV_OPT('t_env_info').get_lists(request.args)
        return result
    if method == 'POST':
        result = ENV_OPT('t_env_info').insert(request.get_data().decode())
        return result
    if method == 'PATCH':
        result = ENV_OPT('t_env_info').update(request.get_data().decode())
        return result


@app.route('/env_opt/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def env_opt_params(id):
    method = request.method
    if method == 'DELETE':
        result = ENV_OPT('t_env_info').delete(env_id=id)
        return result
    elif method == "GET" and id == "detail":
        return ENV_OPT('t_env_info').getEnvDetail(request.args)


# 环境明细操作
@app.route('/env_opt_d', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def env_opt_d():
    method = request.method
    token = request.headers.get('Token')
    if method == 'POST':
        result = ENV_OPT('t_env_detail').env_insert(request.get_data().decode())
        return result
    elif method == 'PATCH':
        result = ENV_OPT('t_env_detail').env_update(request.get_data().decode())
        return result


@app.route('/env_opt_d/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def env_opt_params_d(id):
    method = request.method
    token = request.headers.get('Token')
    if method == 'DELETE':
        result = ENV_OPT('t_env_detail').env_delete(env_d_id=id)
        return result
    elif method == 'GET':
        result = ENV_OPT('t_env_detail').get_env_lists(request.args, env_id=id)
        return result


# 插件操作
@app.route('/plugin', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def plugin_opt():
    method = request.method
    token = request.headers.get('Token')
    if method == 'POST':
        result = PLUGIN_OPT('t_plugin_info').insert(request.get_data().decode())
        return result
    elif method == 'PATCH':
        result = PLUGIN_OPT('t_plugin_info').update(request.get_data().decode())
        return result
    elif method == 'GET':
        result = PLUGIN_OPT('t_plugin_info').get_lists(request.args)
        return result


@app.route('/plugin/<path:id>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def plugin_opt_params(id):
    token = request.headers.get('Token')
    method = request.method
    if method == 'DELETE':
        result = PLUGIN_OPT('t_plugin_info').delete(plugin_id=id)
        return result
    elif method == 'POST' and id == 'send':
        return_data = plugin_run(request.get_data().decode(), token)
        return return_data
    elif method == 'GET' and id == 's':
        return_data = PLUGIN_OPT('t_plugin_info').get_lists_a(request.args)
        return return_data
    elif method == 'POST' and id == 's':
        data = request.get_data().decode()
        get_data = json.loads(data)
        plugin_id = get_data['plugin_id']
        plugin_status_opt(0, plugin_id)
        return_data = respdata().sucessMessage('', '初始化完成！~~')
        return json.dumps(return_data)


@app.route('/astatistics', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def stat():
    token = request.headers.get('Token')
    data = STATIC_OPT().test_statics()
    result = respdata().sucessMessage(data, "查询成功")
    return json.dumps(result, ensure_ascii=False)


@app.route('/astatistics/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def stat_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET' and id == 'download':
        response = make_response(send_file(getCurruntpath() + "/model/output/importfile/api_info.xlsx"))
        response.headers["Content-Disposition"] = "attachment; filename=api_info.xlsx;"
        return response
    elif method == "GET" and id == "iter":
        result = STATIC_OPT(token).iter_data()
        return result
    elif method == "GET" and id == "at":
        result = STATIC_OPT(token).at_data()

        return result
    elif method == "GET" and id == "te":
        result = STATIC_OPT(token).test_data(request.args)
        return result
    elif method == "GET" and id == "pl":
        result = STATIC_OPT(token).pl_data()
        return result
    elif method == "GET" and id == "ui":
        result = STATIC_OPT(token).UIdata()
        return result

# 权限管理模块
@app.route('/permission', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def permission_opt():
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        result = USER_INFO('p_user_permission').get_lists_p(request.args)
        return result
    if method == 'POST':
        result = USER_INFO('p_user_permission').permission_insert(request.get_data().decode())
        return result
    elif method == 'PATCH':
        result = USER_INFO('p_user_permission').permission_update(request.get_data().decode())
        return result


@app.route('/permission/<path:id>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def permission_op_params(id):
    token = request.headers.get('Token')
    method = request.method
    if method == 'DELETE':
        result = USER_INFO('p_user_permission').delete(id=id)
        return result
    elif method == 'GET' and id == 'tree':
        result = USER_INFO('p_user_permission').permission_get_lists()
        return result
    elif method == 'GET' and id == 'menu':
        result = USER_INFO('p_user_permission').get_menu(request.args)
        return result
    # 调试接口
    elif method == 'GET' and id == 'test':
        result = USER_INFO('p_user_permission').get_menu(request.args)
        return result


# 用户信息管理
@app.route('/userinfo', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def user_info():
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        result = USER_INFO('p_user_info').get_lists(request.args)
        return result
    elif method == 'POST':
        result = USER_INFO('p_user_info').insert(request.get_data().decode())
        return result
    elif method == 'PATCH':
        result = USER_INFO('p_user_info').update(request.get_data().decode())
        return result


@app.route('/userinfo/<path:id>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def user_info_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == 'DELETE':
        result = USER_INFO('p_user_info').delete(id=id)
        return result
    elif method == 'POST' and id == 'pwd':
        result = USER_INFO('p_user_info').changPassord(request.get_data().decode())
        return result


# 角色管理
@app.route('/role', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def role_opt():
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        result = USER_INFO('p_role_info').role_get_lists(request.args)
        return result
    elif method == 'POST':
        result = USER_INFO('p_role_info').role_insert(request.get_data().decode())
        return result
    elif method == 'PATCH':
        result = USER_INFO('p_role_info').role_update(request.get_data().decode())
        return result


@app.route('/role/<path:id>', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@userOpt()
def role_opt_params(id):
    token = request.headers.get('Token')
    method = request.method
    if method == 'DELETE':
        result = USER_INFO('p_role_info').delete(id=id)
        return result


@app.route('/group/<path:uri>', methods=['GET', 'POST'])
@userOpt()
def group(uri):
    if uri == 'get':
        token = request.headers.get('Token')
        return getGroup(token)
    elif uri == 'insert':
        return groupInsert(request.get_data().decode())
    elif uri == 'delete':
        return groupDel(request.get_data().decode())
    elif uri == 'update':
        return groupUpdate(request.get_data().decode())


@app.route('/getdata', methods=['GET', 'POST'])
#@userOpt()
def get_data():
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        return_data = "测试平台数据传输接口正常，请正常使用！~~"
        return return_data
    elif method == 'POST':
        requestFile=request.files.get('resultFile')
        if requestFile:
            fromdata=request.form.get('params')
            jsondata=analysicResultJson(requestFile,fromdata)
            return COLLECT_DATA(jsondata).save_result(fromdata)
        else:
            return COLLECT_DATA(request.get_data().decode()).save_result()


@app.route('/reporta/<path:uri>', methods=['GET', 'POST'])
@userOpt()
def report_opt(uri):
    token = request.headers.get('Token')
    get_data=request.args
    if uri == 'online_time':

        '''
        按照时间查询报告
        '''
        exe_type = get_data.get('type')
        group_id = get_data.get('group_id')
        if group_id == '0':
            return_data = {'code': 201, 'data': '请选择要生成报告的分组！~'}
            return json.dumps(return_data,ensure_ascii=False)
        else:
            group_id = getCode(group_id)
            rqmt_id = get_data['online_time']
            if exe_type =='1':
                return getHTML(token).get_html_rqmt(2, str(group_id), rqmt_id) #回归测试报告
            elif exe_type =='2':
                report_data = getHTML(token).get_html_rqmt(4, str(group_id), rqmt_id) #线上报告
                return report_data
            elif exe_type =='3':
                return getHTML(token).get_html_rqmt(1, group_id, rqmt_id) #需求报告，按照需求编号
    elif uri =='task':
        '''
        按照任务编号查询报告
        '''
        exe_type = get_data.get('type')
        task_id = get_data.get('task_id')
        if exe_type =='1':
            return getHTML(token).get_html_rqmt(3, None, None, task_id) #回归测试报告
        elif exe_type =='2':
            report_data = getHTML(token).get_html_rqmt(5, None, None, task_id)#线上报告
            return report_data
        elif exe_type ==3:
            return getHTML(token).get_html_rqmt(3, '', None, task_id) #需求报告，按照需求编号
    elif uri == 'timetask':
        '''
        定时报告
        '''
        batch_id = get_data.get('batch_id')
        task_type= get_data.get('taskType')
        group_id = get_data.get('group_id')
        report_data = getHTML(token).get_html_rqmt(6,group_id, batch_id,task_type)
        return report_data




@app.route('/sendmail/<path:uri>', methods=['GET', 'POST'])
@userOpt()
def send_mail_opt(uri):
    token = request.headers.get('Token')
    get_data = json.loads(request.get_data().decode())
    exe_type = get_data.get('type')
    group_id = get_data.get('group_id')
    email_id = get_data.get('email_id')
    if uri == 'online_time':
        '''
        按照时间查询报告
        '''
        if group_id == '0':
            return_data = {'code': 201, 'data': '请选择要生成报告的分组！~'}
            return json.dumps(return_data, ensure_ascii=False)
        else:
            group_id = getCode(group_id)
            rqmt_id = get_data['online_time']
            if exe_type == 1:
                report_data= getHTML(token).get_html_rqmt(2, str(group_id), rqmt_id)  # 回归测试报告
                if Email_send(email_id).send_text(report_data):
                    result = respdata().sucessMessage('', "发送成功")
                else:
                    result = respdata().failMessage('', '发送失败，请检查！')
                return json.dumps(result, ensure_ascii=False)
            elif exe_type == 2:
                report_data = getHTML(token).get_html_rqmt(4, str(group_id), rqmt_id)  # 线上报告
                if Email_send(email_id).send_text(report_data):
                    result = respdata().sucessMessage('', "发送成功")
                else:
                    result = respdata().failMessage('', '发送失败，请检查！')
                return json.dumps(result, ensure_ascii=False)
            elif exe_type == 3:
                report_data= getHTML(token).get_html_rqmt(1, group_id, rqmt_id)  # 需求报告，按照需求编号
                if Email_send(email_id).send_text(report_data):
                    result = respdata().sucessMessage('', "发送成功")
                else:
                    result = respdata().failMessage('', '发送失败，请检查！')
                return json.dumps(result, ensure_ascii=False)
    elif uri == 'task':
        '''
        按照任务编号查询报告
        '''
        task_id = get_data.get('task_id')
        if exe_type == 1:
            report_data= getHTML(token).get_html_rqmt(3, '', None, task_id)  # 回归测试报告
            if Email_send(email_id).send_text(report_data):
                result = respdata().sucessMessage('', "发送成功")
            else:
                result = respdata().failMessage('', '发送失败，请检查！')
            return json.dumps(result, ensure_ascii=False)
        elif exe_type == 2:
            report_data = getHTML(token).get_html_rqmt(5, '', None, task_id)  # 线上报告
            if Email_send(email_id).send_text(report_data):
                result = respdata().sucessMessage('', "发送成功")
            else:
                result = respdata().failMessage('', '发送失败，请检查！')
            return json.dumps(result, ensure_ascii=False)
        elif exe_type == 3:
            report_data= getHTML(token).get_html_rqmt(3, '', None, task_id)  # 需求报告，按照需求编号
            if Email_send(email_id).send_text(report_data):
                result = respdata().sucessMessage('', "发送成功")
            else:
                result = respdata().failMessage('', '发送失败，请检查！')
            return json.dumps(result, ensure_ascii=False)
    elif uri == 'timetask':
        '''
        定时报告
        '''
        batch_id = get_data.get('batch_id')
        task_type = get_data.get('taskType')
        group_id = get_data.get('group_id')
        report_data = getHTML(token).get_html_rqmt(6, group_id, batch_id, task_type)
        if Email_send(email_id).send_text(report_data):
            result = respdata().sucessMessage('', "发送成功")
        else:
            result = respdata().failMessage('', '发送失败，请检查！')
        return json.dumps(result, ensure_ascii=False)

# 告警配置

@app.route('/warn', methods=['GET', 'POST', 'PATCH'])
@userOpt()
def warning_data():
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        return WARNING_OPT('w_warning_info').get_lists(request.args)
    elif method == 'POST':
        return WARNING_OPT('w_warning_info').warningInsert(request.get_data().decode())
    elif method == 'PATCH':
        result = USER_INFO('w_warning_info').update(request.get_data().decode())
        return result


@app.route('/warn/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def warning_data_params(id):
    token = request.headers.get('Token')
    method = request.method
    if method == 'DELETE':
        result = USER_INFO('w_warning_info').delete(warning_id=id)
        return result


# 邮件配置
@app.route('/email', methods=['GET', 'POST', 'PATCH'])
@userOpt()
def email_opt():
    token = request.headers.get('Token')
    method = request.method
    if method == 'GET':
        token = request.headers.get('Token')
        return Email_opt().email_list(request.args, token)
    elif method == 'POST':
        return Email_opt().email_save(request.get_data().decode())
    elif method == 'PATCH':
        return Email_opt().update(request.get_data().decode())


@app.route('/email/<path:id>', methods=['GET', 'POST', 'DELETE'])
@userOpt()
def email_opt_params(id):
    token = request.headers.get('Token')
    method = request.method
    if method == 'DELETE':
        result = Email_opt().delete(email_id=id)
        return result


# 接口信息管理
@app.route('/api', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def api_opt():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        return_data = SEARCH_OPT(token, 'api_case_info').searchOpt(request.args)
        # return_data = API_OPT(token).getLists(request.args)
        return return_data
    elif method == 'POST':
        data = API_OPT(token).apiInsert(request.get_data().decode())
        return data


@app.route('/api/<path:id>', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def api_opt_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET' and id == 'get':
        return_data = API_OPT(token).getListsForSuite(request.args)
        return return_data
    elif method == 'POST' and id == "tocase":
        return_data = SUITE_OPT().suiteInsert(request.get_data().decode(), 3)
        return return_data
    elif method == 'POST' and id == "copy":
        return_data = API_OPT(token).apiCopy(request.get_data().decode())
        return return_data
    elif method == 'POST' and id == "params":
        return_data = API_OPT(token).apiParams(request.get_data().decode())
        return return_data
    elif method == "POST" and id == "param":
        return_data = API_OPT(token).paramSave(request.get_data().decode())
        return return_data
    elif method == "POST" and id == "delete":
        return_data = API_OPT(token).apisDelete(request.get_data().decode())
        return return_data
    elif method == 'GET':
        return_data = API_OPT(token).apiDetail(id)
        return return_data
    elif method == "POST" and id == "detail":
        data = API_OPT(token).apiUpdate(request.get_data().decode())
        return data
    elif method == "GET" and id == "search":
        data = SEARCH_OPT(token, 'api_case_info').searchOpt(request.args)
        return data
    elif method == 'DELETE':
        data = API_OPT(token).apiDelete(id)
        return data


# DBC信息管理
@app.route('/dbc', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def dbc_opt():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        # return_data = DBC_OPT(token).getLists(request.args)
        return_data = SEARCH_OPT(token, 'dbc_case_info').searchOpt(request.args)
        return return_data
    elif method == "POST":
        return DBC_OPT(token).dbcInsert(request.get_data().decode())
    elif method == "PATCH":
        return DBC_OPT(token).dbcUpdate(request.get_data().decode())


@app.route('/dbc/<path:id>', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def dbc_opt_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == "GET" and id == "get":
        return_data = DBC_OPT(token).getListsForSuite(request.args)
        return return_data
    elif method == 'POST' and id == "params":
        return_data = DBC_OPT(token).dbcParams(request.get_data().decode())
        return return_data
    elif method == "POST" and id == "param":
        return_data = DBC_OPT(token).paramSave(request.get_data().decode())
        return return_data
    elif method == "GET":
        return DBC_OPT(token).dbcDetail(id)
    elif method == "DELETE":
        return DBC_OPT(token).dbcDelete(id)
    elif method == "POST" and id == "detail":
        return DBC_OPT(token).dbcUpdate(request.get_data().decode())
    elif method == "POST" and id == "exe":
        return dbcDebug(request.get_data().decode())


# 测试套件管理

@app.route('/suite', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def suite_opt():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        return_data = DBC_OPT(token).getLists(request.args)
        return return_data
    elif method == "POST":
        return SUITE_OPT().suiteInsert(request.get_data().decode())
    elif method == "PATCH":
        return DBC_OPT(token).dbcUpdate(request.get_data().decode())


@app.route('/suite/<path:id>', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def suite_opt_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == "GET" and id == "get":
        return_data = DBC_OPT(token).getListsForSuite(request.args)
        return return_data
    elif method == "GET":
        return SUITE_OPT().getLists(id)
    elif method == "DELETE":
        return DBC_OPT(token).dbcDelete(id)
    elif method == "POST" and id == "core":
        return SUITE_OPT().suiteInsert(request.get_data().decode(), 1)
    elif method == "POST" and id == "regress":
        return SUITE_OPT().suiteInsert(request.get_data().decode(), 2)


# shell操作
@app.route('/shell', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def shell_opt():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        return_data = SEARCH_OPT(token, 'shell_case_info').searchOpt(request.args)
        return return_data
    elif method == "POST":
        return SHELL_OPT(token).shellInsert(request.get_data().decode())
    elif method == "PATCH":
        return SHELL_OPT(token).shellUpdate(request.get_data().decode())


@app.route('/shell/<path:id>', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def shell_opt_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == "GET" and id == "get":
        return_data = SHELL_OPT(token).getListsForSuite(request.args)
        return return_data
    elif method == 'POST' and id == "params":
        return_data = SHELL_OPT(token).shellParams(request.get_data().decode())
        return return_data
    elif method == "POST" and id == "param":
        return_data = SHELL_OPT(token).paramSave(request.get_data().decode())
        return return_data
    elif method == "GET":
        return SHELL_OPT(token).shellDetail(id)
    elif method == "DELETE":
        return SHELL_OPT(token).shellDelete(id)
    elif method == "POST" and id == "exe":
        return SHELL_OPT(token).shellExe(request.get_data().decode())


# redis操作
@app.route('/redis', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def redis_opt():
    method = request.method
    token = request.headers.get('Token')
    if method == 'GET':
        return_data = SEARCH_OPT(token, 'redis_case_info').searchOpt(request.args)
        return return_data
    elif method == "POST":
        return REDIS_OPT(token).redisInsert(request.get_data().decode())
    elif method == "PATCH":
        return REDIS_OPT(token).redisUpdate(request.get_data().decode())


@app.route('/redis/<path:id>', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def redis_opt_params(id):
    method = request.method
    token = request.headers.get('Token')
    if method == "GET" and id == "get":
        return_data = REDIS_OPT(token).getListsForSuite(request.args)
        return return_data
    elif method == 'POST' and id == "params":
        return_data = REDIS_OPT(token).redisParams(request.get_data().decode())
        return return_data
    elif method == "POST" and id == "param":
        return_data = REDIS_OPT(token).paramSave(request.get_data().decode())
        return return_data
    elif method == "GET":
        return REDIS_OPT(token).redisDetail(id)
    elif method == "DELETE":
        return REDIS_OPT(token).redisDelete(id)
    # elif method == "POST" and id == "exe":
    #     return REDIS_OPT(token).shellExe(request.get_data().decode())

# 调试口子，部署的时候记得删掉
@app.route('/test/<path:uri>', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
@userOpt()
def test(uri):
    method = request.method
    token = request.headers.get('Token')
    data = API_OPT(token).apiInsert(request.get_data().decode())
    return data


@app.route('/login', methods=['POST', 'GET'])
@userOpt()
def login():
    method = request.method
    token = request.headers.get('Token')
    if method == 'POST':
        try:
            ip = request.remote_addr
            return logIn(request.get_data().decode(), ip)
        except Exception as e:
            return json.dumps(respdata().exceptionResp(e), ensure_ascii=False)
    elif method == "GET":
        return INDEX_DATA(token).getData()


@app.route('/verify', methods=['POST'])
def verify_auth_token():
    try:
        return verify_token(request.get_data().decode())
    except Exception as e:
        return json.dumps(respdata().exceptionResp(e), ensure_ascii=False)


@app.route('/tapd/<path:uri>', methods=['POST'])
# @userOpt()
def tapd_opt(uri):
    method = request.method
    token = request.headers.get('Token')
    if uri == "totapd":
        return toTapd(request.get_data().decode())
    elif uri == "toatm":
        return toAtm(request.get_data().decode())
    elif uri == "casetotapd":
        return toTapd(request.get_data().decode(),1)
    elif uri == "requrietoatm":
        return requiretoAtm(request.get_data().decode())

@app.route('/timetask', methods=['POST','GET','PATCH'])
@userOpt()
def timetask_opt():
    method = request.method
    token = request.headers.get('Token')
    if method == "GET":
        return_data = SEARCH_OPT(token, 't_time_task').searchOpt(request.args)
        return return_data
    if method == "POST":
        result=TIME_TASK_OPT(token).timetaskInert(request.get_data().decode())
        return result
    elif method == "PATCH":
        return TIME_TASK_OPT(token).timetaskUpdate(request.get_data().decode())
@app.route('/timetask/<path:uri>', methods=['POST','DELETE','GET','PATCH'])
@userOpt()
def timetask_opt_params(uri):
    method = request.method
    token = request.headers.get('Token')
    if method == "DELETE":
        return TIME_TASK_OPT(token).timetaskDELETE(time_id=uri )
    elif method=="POST" and uri=="isrun":
        return TIME_TASK_OPT(token).timeTaskIsrun(request.get_data().decode())
    elif method=="POST" and uri=="exe":
        return plugin_run(request.get_data().decode(),token,1)
        # return json.dumps({"msg":"ok"},ensure_ascii=False)
    elif method=="GET" and uri=="batch":
        return TIME_TASK_OPT(token).timeTaskBatchNo(request.args)
    elif method=="GET":
        time_task= TIME_TASK_OPT(token).getTask_Info(uri, 1)
        return_data=respdata().sucessMessage(time_task,'')
        return json.dumps(return_data,ensure_ascii=False)
@app.route('/task', methods=['POST','GET'])
@userOpt()
def task_opt():
    method = request.method
    if method == 'GET':
        token = request.headers.get('Token')
        result = TASK_OPT(token).getTaskStatus(request.args)
        return result


@app.route('/getid', methods=['GET'])
@userOpt()
def get_id():
    method = request.method
    token =request.headers.get('Token')
    if method == 'GET':
        result = newID().getID(request.args)
        return result

@app.route('/getScenario', methods=['GET'])
def getCaseScenario():
    '''
    查询移动端ui场景接口
    :return:
    '''
    return PLUGIN_OPT('regress_case_info').getTestScenario()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7702, debug=True, threaded=True)

    # http_server = WSGIServer(('0.0.0.0', 7702), app)
    # http_server.serve_forever()
