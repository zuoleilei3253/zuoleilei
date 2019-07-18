# Created by ray at 2019/5/28
Feature: XMP登陆接口-邮箱登陆

  Scenario:[1]校验正常登陆场景
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "ray-zuo@qq.com",
            "password": "0c779a4e7ddffaf842f8d316039909ec",
            "code": "YFX5",
            "remember": 0
          }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
      {
          "data": {
              "user_name": "RayZuo",
              "email": "ray-zuo@qq.com",
              "phone": "0"
          },
          "code": 0,
          "msg": "Success"
      }
    '''

  Scenario:[2]邮箱为空
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "",
            "password": "0c779a4e7ddffaf842f8d316039909ec",
            "code": "YFX5",
            "remember": 0
          }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "缺少login_name参数",
          "code": 1
      }
    '''

  Scenario:[3]密码为空
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "ray-zuo@qq.com",
            "password": "",
            "code": "YFX5",
            "remember": 0
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


#  Scenario:[4]验证码为空
#    Given 发送请求
#    '''
#      {
#	    "url": "sys/user/passport/login",
#	    "method": "post",
#	    "data": {
#            "login_name": "ray-zuo@qq.com",
#            "password": "0c779a4e7ddffaf842f8d316039909ec",
#            "code": "",
#            "remember": 0
#          }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "msg": "缺少code参数",
#          "code": 1
#      }
#    '''

#  Scenario:[5]记住密码为空
#    Given 发送请求
#    '''
#      {
#	    "url": "sys/user/passport/login",
#	    "method": "post",
#	    "data": {
#            "login_name": "ray-zuo@qq.com",
#            "password": "0c779a4e7ddffaf842f8d316039909ec",
#            "code": "YFX5",
#            "remember": ""
#          }
#      }
#    '''
#    Then 验证返回数据,返回包含期望
#    '''
#      {
#          "data": {},
#          "msg": "缺少remember参数",
#          "code": 1
#      }
#    '''

#  Scenario:[6]邮箱不存在
#    Given 发送请求
#    '''
#      {
#	    "url": "sys/user/passport/login",
#	    "method": "post",
#	    "data": {
#            "login_name": "ray-z@qq.com",
#            "password": "0c779a4e7ddffaf842f8d316039909ec",
#            "code": "YFX5",
#            "remember": "0"
#          }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "msg": "邮箱/手机号不存在",
#          "code": 4001
#      }
#    '''

  Scenario:[7]邮箱错误
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "ray-z@.com",
            "password": "0c779a4e7ddffaf842f8d316039909ec",
            "code": "YFX5",
            "remember": "0"
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

  Scenario:[8]密码错误
    Given 发送请求
    '''
      {
	    "url": "sys/user/passport/login",
	    "method": "post",
	    "data": {
            "login_name": "ray-zuo@qq.com",
            "password": "0c779a4e7ddffaf842f8d316039909e",
            "code": "YFX5",
            "remember": "0"
          }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "密码错误",
          "code": 4002
      }
    '''

