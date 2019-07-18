# Created by ray at 2019/5/28
Feature: XMP登陆接口-邮箱登陆

  Scenario:[1]校验正常登陆场景-手机号登陆
    # Enter steps here
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "17611377222",
            "password": "9cbf8a4dcb8e30682b927f352d6559a0",
            "code": "YFX5",
            "remember": 0
          }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
      {
          "data": {
              "user_name": "222s",
              "email": "",
              "phone": "17611377222",
              "auth_list": []
          },
          "code": 0,
          "msg": "Success"
      }
    '''

  Scenario:[2]手机号为空
    # Enter steps here
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "",
            "password": "9cbf8a4dcb8e30682b927f352d6559a0",
            "code": "YFX5",
            "remember": 0
          }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
      {
          "data": {},
          "msg": "缺少login_name参数",
          "code": 1
      }
    '''
  Scenario:[3]手机号不存在
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "17611001100,
            "password": "9cbf8a4dcb8e30682b927f352d6559a0",
            "code": "YFX5",
            "remember": 0
          }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
      {
          "data": {},
          "msg": "邮箱/手机号不存在",
          "code": 4001
      }
    '''
  Scenario:[4]手机号错误
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "17611000,
            "password": "9cbf8a4dcb8e30682b927f352d6559a0",
            "code": "YFX5",
            "remember": 0
          }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
      {
          "data": {},
          "msg": "账号错误",
          "code": 4003
      }
    '''
  Scenario:[5]密码为空
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "17611377222",
            "password": "",
            "code": "YFX5",
            "remember": 0
          }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
      {
          "data": {},
          "msg": "缺少password参数",
          "code": 1
      }
    '''
  Scenario:[5]密码错误
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "17611377222",
            "password": "xwmiwmiw",
            "code": "YFX5",
            "remember": 0
          }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
      {
          "data": {},
          "msg": "密码错误",
          "code": 4002
      }
    '''
  Scenario:[6]验证码为空
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "17611377222",
            "password": "xwmiwmiw",
            "code": "YFX5",
            "remember": 0
          }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
      {
          "data": {},
          "msg": "密码错误",
          "code": 4002
      }
    '''