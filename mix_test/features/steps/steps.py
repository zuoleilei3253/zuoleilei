# -*- coding: utf-8 -*-

from behave import *
import json
import time

from assertpy import assert_that
from features.utils.operation_db import *
from features.utils.req import *
from features.utils.check_data import *
from features.steps.config import *
from features.utils.logger import logger

# ------------------------------------------------------------------------
# STEPS with Parse Matcher ("parse")
# ------------------------------------------------------------------------
use_step_matcher("parse")


@given(u'执行删除sql')
def delete_sql(context):
    sql = eval(context.text)
    my_db2(sql)


@given(u'获取验证码')
def select_sql(context):
    sql = json.dumps(context.text, encoding="UTF-8", ensure_ascii=False).strip('"')
    code = my_db1(sql)
    context.code = code


@given(u'令验证码失效')
def invalid_code(context):
    # 根据需求文档，验证码失效期为10分钟
    time.sleep(60 * 10)


@given(u'使用"{user}"注册，发送请求')
def send_request_with_register(context, user):
    request_info = json.loads(context.text)
    # 调试
    # logger.info(request_info)
    request_info['data']['code'] = context.code[0][0]
    logger.info(request_info)
    my_request = Request(request_info, user)
    context.response = my_request.send_request()


@given(u'发送请求')
def send_request(context):
    request_info = json.loads(context.text)
    # 调试
    # logger.info('request_info is:' + `request_info`)
    # logger.info(request_info)
    my_request = Request(request_info)
    context.response = my_request.send_request()


@given(u'发送请求,传递验证码给接口')
def send_request(context):
    request_info = json.loads(context.text)
    request_info['data']['code'] = context.code[0][0]
    my_request = Request(request_info)
    context.response = my_request.send_request()


@given(u'使用"{user}"登陆,发送请求')
def send_request_with_login(context, user):
    request_info = json.loads(context.text)
    # 调试
    # logger.info(`request_info`)
    my_request = Request(request_info, user)
    context.response = my_request.send_request()


@then(u'验证返回数据,返回等于期望')
def checkout_response_equal(context):
    # 去掉了响应头信息
    # context.response.pop('headers')
    actual_response = context.response['body']
    expected_response = json.loads(context.text)
    # log,报错放开
    logger.info(actual_response)
    assert_that(expected_response).is_equal_to(actual_response)


# 特殊情况下使用,返回中包含不太好验证的字段时使用,如：timestamp等，
@then(u'验证返回数据,返回包含期望')
def checkout_response_contain(context):
    actual_response = context.response['body']
    expected_response = json.loads(context.text)
    # log,报错放开
    # logger.info(actual_response)
    # logger.info(expected_response)
    CheckData().json_contain(actual_response, expected_response)
