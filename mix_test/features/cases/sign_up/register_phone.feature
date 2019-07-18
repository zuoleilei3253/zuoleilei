# Created by ray at 2019-06-12
Feature: XMP注册接口--手机
  # Enter feature description here
  Scenario:[1]XMP注册接口-校验使用手机正确注册
    Given 执行删除sql
    '''
      "delete from mix.sys_user where phone='17611377226'"
    '''
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='17611377226' and ip=234597550"
    '''
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-phone",
        "method":"post",
        "data":{
                "phone":"17611377226"
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
        "data": {},
        "code": 0,
        "msg": "Success"
      }
    '''
    Given 获取验证码
    '''
      select code from mix.sys_verify_code where type_name='17611377226' order by id desc limit 1
    '''
    Given 发送请求,传递验证码给接口
    '''
      {
        "url": "sys/user/passport/register",
        "method": "post",
        "data": {
          "user_name":"Wee",
          "password":"9cbf8a4dcb8e30682b927f352d6559a0",
          "phone":"17611377226"
          }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
       {
          "data": {
              "user_name": "Wee",
              "email": "",
              "phone": "17611377226",
              "auth_list": []
          },
          "code": 0,
          "msg": "Success"
        }
    '''

  Scenario:[2]手机已存在
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='17611377226' and ip=234597550"
    '''
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-phone",
        "method":"post",
        "data":{
                "phone":"17611377226"
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "手机号已经被注册",
          "code": 3001
      }
    '''

  Scenario: [3]获取验证码时手机为空
    Given 执行删除sql
    '''
      "delete from mix.sys_user where phone='17611377226'"
    '''
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='17611377226' and ip=234597550"
    '''
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-phone",
        "method":"post",
        "data":{
                "phone":""
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
        "data": {},
        "code": 0,
        "msg": "Success"
      }
    '''


  Scenario: [4]获取验证码时手机号多次请求(运营商限制1小时只能发送5次验证码)
    Given 执行删除sql
    '''
      "delete from mix.sys_user where phone='17611377226'"
    '''
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='17611377226' and ip=234597550"
    '''
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-phone",
        "method":"post",
        "data":{
                "phone":"17611377226"
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "发送失败，请重试",
          "code": 3003
      }
    '''

  Scenario: [5]验证注册请求时手机为空
    Given 执行删除sql
    '''
      "delete from mix.sys_user where phone='17611377226'"
    '''
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='17611377226' and ip=234597550"
    '''
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-phone",
        "method":"post",
        "data":{
                "phone":"17611377226"
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
        "data": {},
        "code": 0,
        "msg": "Success"
      }
    '''
    Given 获取验证码
    '''
      select code from mix.sys_verify_code where type_name='17611377226' order by id desc limit 1
    '''
    Given 发送请求,传递验证码给接口
    '''
      {
        "url": "sys/user/passport/register",
        "method": "post",
        "data": {
          "user_name":"Wee",
          "password":"9cbf8a4dcb8e30682b927f352d6559a0",
          "phone":""
          }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
        "data": {},
        "msg": "手机号或邮箱不能为空",
        "code": 1
      }
    '''
