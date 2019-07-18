# Created by ray at 2019-06-12
Feature:XMP忘记密码-email
  # Enter feature description here
  Scenario:[1]验证邮箱为空
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reset-password-email",
        "method":"post",
        "data":{
                "email":"",
                "url":"reset?type=reset_email"
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "缺少email参数",
          "code": 1
      }
    '''
  Scenario:[2]验证邮箱不存在
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reset-password-email",
        "method":"post",
        "data":{
                "email":"prett@163.com",
                "url":"reset?type=reset_email"
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "此邮箱未注册",
          "code": 2004
      }
    '''


  Scenario:[3]邮箱字段错误
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reset-password-email",
        "method":"post",
        "data":{
                "email":"ray-zuo@.cm",
                "url":"reset?type=reset_email"
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "code": 2000,
          "msg": "请填写正确的邮箱"
      }
    '''

  Scenario:[4]url字段为空
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reset-password-email",
        "method":"post",
        "data":{
                "email":"ray-zuo@qq.com",
                "url":""
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "缺少url参数",
          "code": 1
      }
    '''

# Scenario:[5]url字段错误
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-email",
#        "method":"post",
#        "data":{
#                "email":"ray-zuo@qq.com",
#                "url":"mxn"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "code": 2000,
#          "msg": "请填写正确的url"
#      }
#    '''

  Scenario:[6]验证邮箱存在
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='ray-zuo@qq.com' and ip=234597550"
    '''
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reset-password-email",
        "method":"post",
        "data":{
                "email":"ray-zuo@qq.com",
                "url":"reset?type=reset_email"
              }
      }
    '''
    Then 验证返回数据,返回包含期望
    '''
      {
          "data": {},
          "code": 0,
          "msg": "Success"
      }
    '''


