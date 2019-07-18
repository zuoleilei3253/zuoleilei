# Created by ray at 2019/5/28
Feature: XMP注册接口--邮箱
  # Enter feature description here
  Scenario:[1]验证XMP注册接口-校验使用邮箱正确注册
    Given 执行删除sql
    '''
      "delete from mix.sys_user where email='prettysxq@163.com'"
    '''

    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='prettysxq@163.com' and ip=234597550"
    '''

    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-email",
        "method":"post",
        "data":{
                "email":"prettysxq@163.com"
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
      select code from mix.sys_verify_code where type_name='prettysxq@163.com' order by id desc limit 1
    '''

    Given 发送请求,传递验证码给接口
    '''
      {
        "url": "sys/user/passport/register",
        "method": "post",
        "data": {
          "user_name":"Wee",
          "password":"9cbf8a4dcb8e30682b927f352d6559a0",
          "email":"prettysxq@163.com"
          }
      }
    '''

    Then 验证返回数据,返回包含期望
    '''
        {
            "data": {
                "email": "prettysxq@163.com",
                "phone": "0",
                "user_name": "Wee",
                "auth_list": []
            },
            "code": 0,
            "msg": "Success"
        }
    '''

  Scenario:[2]验证邮箱已存在
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='prettysxq@163.com' and ip=234597550"
    '''

    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-email",
        "method":"post",
        "data":{
                "email":"prettysxq@163.com"
              }
      }
    '''

    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "邮箱已经被注册",
          "code": 2001
      }
    '''

  Scenario:[3]验证姓名为空
    Given 执行删除sql
    '''
      "delete from mix.sys_user where email='prettysxq@163.com'"
    '''

    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='prettysxq@163.com' and ip=234597550"
    '''

    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-email",
        "method":"post",
        "data":{
                "email":"prettysxq@163.com"
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
      select code from mix.sys_verify_code where type_name='prettysxq@163.com' order by id desc limit 1
    '''

    Given 发送请求,传递验证码给接口
    '''
      {
        "url": "sys/user/passport/register",
        "method": "post",
        "data": {
          "user_name":"",
          "password":"9cbf8a4dcb8e30682b927f352d6559a0",
          "email":"prettysxq@163.com"
          }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "code": 1,
          "msg": "缺少user_name参数"
      }
    '''

  Scenario: [4]验证邮箱为空
    Given 执行删除sql
    '''
      "delete from mix.sys_user where email='prettysxq@163.com'"
    '''
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='prettysxq@163.com' and ip=234597550"
    '''
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-email",
        "method":"post",
        "data":{
                "email":"prettysxq@163.com"
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
      select code from mix.sys_verify_code where type_name='prettysxq@163.com' order by id desc limit 1
    '''
    Given 发送请求,传递验证码给接口
    '''
      {
        "url": "sys/user/passport/register",
        "method": "post",
        "data": {
          "user_name":"Wee",
          "password":"9cbf8a4dcb8e30682b927f352d6559a0",
          "email":""
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

  Scenario: [5]验证码为空
    Given 执行删除sql
    '''
      "delete from mix.sys_user where email='prettysxq@163.com'"
    '''
    Given 发送请求
    '''
      {
        "url": "sys/user/passport/register",
        "method": "post",
        "data": {
          "user_name":"Wee",
          "password":"9cbf8a4dcb8e30682b927f352d6559a0",
          "email":"prettysxq@163.com",
          "code":""
          }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "缺少code参数",
          "code": 1
      }
    '''

  Scenario: [6]验证码错误
    Given 执行删除sql
    '''
      "delete from mix.sys_user where email='prettysxq@163.com'"
    '''
    Given 发送请求
    '''
      {
        "url": "sys/user/passport/register",
        "method": "post",
        "data": {
          "user_name":"Wee",
          "password":"9cbf8a4dcb8e30682b927f352d6559a0",
          "email":"prettysxq@163.com",
          "code":"1234"
          }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "验证码错误",
          "code": 4000
      }
    '''


#  Scenario: [7]验证码失效
#    Given 执行删除sql
#    '''
#      "delete from mix.sys_user where email='prettysxq@163.com'"
#    '''
#    Given 执行删除sql
#    '''
#      "delete from mix.sys_verify_code where type_name='prettysxq@163.com' and ip=234597550"
#    '''
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reg-email",
#        "method":"post",
#        "data":{
#                "email":"prettysxq@163.com"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#      "data": {},
#      "code": 0,
#      "msg": "Success"
#      }
#    '''
#    Given 令验证码失效
#    '''
#    '''
#    Given 获取验证码
#    '''
#      select code from mix.sys_verify_code where type_name='prettysxq@163.com' order by id desc limit 1
#    '''
#    Given 发送请求,传递验证码给接口
#    '''
#      {
#        "url": "sys/user/passport/register",
#        "method": "post",
#        "data": {
#          "user_name":"Wee",
#          "password":"9cbf8a4dcb8e30682b927f352d6559a0",
#          "email":"prettysxq@163.com"
#          }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "msg": "验证码已过期",
#          "code": 4001
#      }
#    '''

  Scenario: [8]密码为空
    Given 执行删除sql
    '''
      "delete from mix.sys_user where email='prettysxq@163.com'"
    '''
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='prettysxq@163.com' and ip=234597550"
    '''
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reg-email",
        "method":"post",
        "data":{
                "email":"prettysxq@163.com"
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
      select code from mix.sys_verify_code where type_name='prettysxq@163.com' order by id desc limit 1
    '''
    Given 发送请求,传递验证码给接口
    '''
      {
        "url": "sys/user/passport/register",
        "method": "post",
        "data": {
          "user_name":"Wee",
          "password":"",
          "email":"prettysxq@163.com"
          }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
        "data": {},
        "msg": "缺少password参数",
        "code": 1
      }
    '''

