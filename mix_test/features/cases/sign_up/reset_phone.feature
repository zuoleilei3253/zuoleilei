# Created by ray at 2019-06-12
Feature:XMP忘记密码-phone
  # Enter feature description here
#  Scenario:[1]手机为空
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-phone",
#        "method":"post",
#        "data":{
#                "phone":""
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "msg": "缺少phone参数",
#          "code": 1
#      }
#    '''
#  Scenario:[2]验证手机不存在
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-phone",
#        "method":"post",
#        "data":{
#                "phone":"17711221122"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "msg": "此手机号未注册",
#          "code": 3004
#      }
#    '''
#
#  Scenario:[3]手机字段错误
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-phone",
#        "method":"post",
#        "data":{
#                "phone":"ray-zuo@.cm"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "msg": "请输入正确的手机号",
#          "code": 3000
#      }
#    '''
#
#  Scenario:[4]手机号存在，验证码为空
#    Given 执行删除sql
#    '''
#      "delete from mix.sys_verify_code where type_name='17611377222' and ip=234597550"
#    '''
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-phone",
#        "method":"post",
#        "data":{
#                "phone":"17611377222"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#        "data": {},
#        "code": 0,
#        "msg": "Success"
#      }
#    '''
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/verify-password-code",
#        "method":"post",
#        "data":{
#                "phone":"17611377222",
#                "code":""
#              }
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
#
#  Scenario:[5]手机号存在，验证码错误
#    Given 执行删除sql
#    '''
#      "delete from mix.sys_verify_code where type_name='17611377222' and ip=234597550"
#    '''
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-phone",
#        "method":"post",
#        "data":{
#                "phone":"17611377222"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#        "data": {},
#        "code": 0,
#        "msg": "Success"
#      }
#    '''
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/verify-password-code",
#        "method":"post",
#        "data":{
#                "phone":"17611377222",
#                "code":"1234"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "msg": "验证码错误",
#          "code": 4000
#      }
#    '''

#  Scenario:[6]手机号存在，验证码正确
#    Given 执行删除sql
#    '''
#      "delete from mix.sys_verify_code where type_name='17700001234' and ip=234597550"
#    '''
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-phone",
#        "method":"post",
#        "data":{
#                "phone":"17700001234"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#        "data": {},
#        "code": 0,
#        "msg": "Success"
#      }
#    '''
#    Given 获取验证码
#    '''
#      select code from mix.sys_verify_code where type_name='17700001234' order by id desc limit 1
#    '''
#    Given 发送请求,传递验证码给接口
#    '''
#      {
#        "url":"sys/user/passport/verify-password-code",
#        "method":"post",
#        "data":{
#                "phone":"17700001234"
#              }
#      }
#    '''
#    Then 验证返回数据,返回包含期望
#    '''
#      {
#          "data": {},
#          "code": 0,
#          "msg": "Success"
#      }
#    '''

#  Scenario:[7]手机号存在，验证码失效
#    Given 执行删除sql
#    '''
#      "delete from mix.sys_verify_code where type_name='17700001234' and ip=234597550"
#    '''
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-phone",
#        "method":"post",
#        "data":{
#                "phone":"17700001234"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#        "data": {},
#        "code": 0,
#        "msg": "Success"
#      }
#    '''
#    Given 令验证码失效
#    '''
#    '''
#    Given 获取验证码
#    '''
#      select code from mix.sys_verify_code where type_name='17700001234' order by id desc limit 1
#    '''
#    Given 发送请求,传递验证码给接口
#    '''
#      {
#        "url":"sys/user/passport/verify-password-code",
#        "method":"post",
#        "data":{
#                "phone":"17700001234"
#              }
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


#  Scenario:[8]最终请求手机号为空
#    Given 执行删除sql
#    '''
#      "delete from mix.sys_verify_code where type_name='17700001234' and ip=234597550"
#    '''
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-phone",
#        "method":"post",
#        "data":{
#                "phone":"17700001234"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#        "data": {},
#        "code": 0,
#        "msg": "Success"
#      }
#    '''
#    Given 获取验证码
#    '''
#      select code from mix.sys_verify_code where type_name='17700001234' order by id desc limit 1
#    '''
#    Given 发送请求,传递验证码给接口
#    '''
#      {
#        "url":"sys/user/passport/verify-password-code",
#        "method":"post",
#        "data":{
#                "phone":""
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "msg": "缺少phone参数",
#          "code": 1
#      }
#    '''
#
#  Scenario:[9]最终请求手机号错误
#    Given 执行删除sql
#    '''
#      "delete from mix.sys_verify_code where type_name='17700001234' and ip=234597550"
#    '''
#    Given 发送请求
#    '''
#      {
#        "url":"sys/user/passport/send-reset-password-phone",
#        "method":"post",
#        "data":{
#                "phone":"17700001234"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#        "data": {},
#        "code": 0,
#        "msg": "Success"
#      }
#    '''
#    Given 获取验证码
#    '''
#      select code from mix.sys_verify_code where type_name='17700001234' order by id desc limit 1
#    '''
#    Given 发送请求,传递验证码给接口
#    '''
#      {
#        "url":"sys/user/passport/verify-password-code",
#        "method":"post",
#        "data":{
#                "phone":"123456"
#              }
#      }
#    '''
#    Then 验证返回数据,返回等于期望
#    '''
#      {
#          "data": {},
#          "msg": "请输入正确的手机号",
#          "code": 3000
#      }
#    '''

  Scenario:[10]最终请求手机号不存在
    Given 执行删除sql
    '''
      "delete from mix.sys_verify_code where type_name='17700001234' and ip=234597550"
    '''
    Given 发送请求
    '''
      {
        "url":"sys/user/passport/send-reset-password-phone",
        "method":"post",
        "data":{
                "phone":"17700001234"
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
      select code from mix.sys_verify_code where type_name='17700001234' order by id desc limit 1
    '''
    Given 发送请求,传递验证码给接口
    '''
      {
        "url":"sys/user/passport/verify-password-code",
        "method":"post",
        "data":{
                "phone":"13311001100"
              }
      }
    '''
    Then 验证返回数据,返回等于期望
    '''
      {
          "data": {},
          "msg": "此手机号未注册",
          "code": 3004
      }
    '''

