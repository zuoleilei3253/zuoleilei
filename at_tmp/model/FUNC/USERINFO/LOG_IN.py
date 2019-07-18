

#用户登陆模块


import json
import time
from model.util.PUB_DATABASEOPT import *
from model.util.TMP_DB_OPT import *
from model.util.PUB_RESP import *
from model.util.ENCRY import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
CSRF_ENABLED = True
# 密钥
SECRET_KEY = 'ATest'
USERTIME=18000
class QXToken(object):
    def __init__(self, user_name,ip):
        self.user_name = user_name
        self.ip=ip
#校验用户登录名及密码
    def loginConfirm(self, user_pwd):
        sql = 'select * from p_user_info WHERE user_name="'+self.user_name+'"'
        user_data=getJsonFromDatabase(sql)
        if user_data:
            user_pwds=(PrpCrypt().decrypt(user_data[0]['user_password']))
            if str(user_pwd) == str(user_pwds):
                if self.updateUserIp():
                    user_status=user_data[0]['user_status']
                    if user_status=='1':
                        ROLE_ID=user_data[0]['user_role_id']
                        USER_VERIFY = user_data[0]['user_verify']
                        AUTH_ID = json.loads(user_data[0]['auth_id_lists'])
                        role_sql='select role_desc from p_role_info WHERE id="'+str(ROLE_ID)+'"'
                        role_desc=get_JSON(role_sql)[0]['role_desc']
                        data = dict()
                        data['access_token'] = self.generate_auth_token(ROLE_ID,AUTH_ID,USER_VERIFY)
                        data['user_name'] = self.user_name
                        data['role_desc']=str(role_desc)
                        return_data = respdata().sucessResp(data)
                        return json.dumps(return_data, ensure_ascii=False)
                    else:
                        return_data=respdata().otherResp('','该用户状态不允许登录！～')
                        return json.dumps(return_data, ensure_ascii=False)
                else:
                    return_data = respdata().otherResp('', '用户登录失败，登录数据无法写入数据库，请联系管理员！')
                    return json.dumps(return_data, ensure_ascii=False)
            else:
                return_data = respdata().otherResp('','登陆失败，请检测用户名及密码！～～')
                return json.dumps(return_data, ensure_ascii=False)
        else:
            return_data = respdata().otherResp('', '该用户名不存在！～～')
            return json.dumps(return_data, ensure_ascii=False)
# 生成TOKEN
    def generate_auth_token(self,ROLE_ID,auth_id, USER_VERIFY,expiration = USERTIME):
        timestamp=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        s = Serializer(SECRET_KEY, expires_in = expiration)
        return s.dumps({'user_id': self.user_name,'ROLE_ID':ROLE_ID,'timestamp':timestamp,'USER_VERIFY':USER_VERIFY,'auth_id':auth_id}).decode()
    def updateUserIp(self):
        try:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            ip_sql="update p_user_info set usr_ipaddr = '" + str(self.ip) + "',login_time ='"+str(timestamp)+"' where user_name='"+self.user_name+"'"
            ip_update=getJsonMysql().exeUpdate(ip_sql)
            return True
        except:
            return False

# 验证TOKEN
def verify_auth_token( token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
        permissions=get_url(token)
    except SignatureExpired:
        return_data=respdata().otherResp(False,'登录过期请重新登录！～')
        return json.dumps(return_data, ensure_ascii=False) # valid token, but expired 过期TOKEN  203
    except BadSignature:
        return_data= respdata().otherResp(None,'登录账户无效！～')
        return json.dumps(return_data, ensure_ascii=False)# invalid token 无效TOKEN  203


    return_data= respdata().sucessResp(permissions)

    return json.dumps(return_data, ensure_ascii=False)
#解密token获取角色值
def encrypToken(token):
    s =Serializer(SECRET_KEY)
    try:
        data=s.loads(token)
        ROLE_ID=data['ROLE_ID']
        return ROLE_ID
    except Exception as e:
        print(str(e))
        return "获取 权限失败！31231231～～～"
# 获取用户验证代码
def getUSER_VERIFY(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
        auth_id = data['USER_VERIFY']
        return auth_id
    except Exception as e:

        return "获取 权限失败！～～1～"
##权限
###添加权限
###根据权限获取分组列表
def authCtrl(auth_id):
    group_sql='select * from p_user_auth where auth_id="'+auth_id+'"'
    # print(group_sql)
    group_listsa=get_JSON(group_sql)[0]['group_lists']
    group_lists = tuple(json.loads(group_listsa))
    # print("==================groups=======")
    # print(group_lists)
    return str(group_lists)
###保存分组信息到权限中
def saveAuth(auth_id,group_id):
    authsql='select group_lists from p_user_auth  WHERE  auth_id = "'+ auth_id+'"'
    group_listsa=get_JSON(authsql)
    group_lists=json.loads(group_listsa[0]['group_lists'])
    group_lists.append(group_id)
    group_list=json.dumps(group_lists)
    authInsert="update p_user_auth set group_lists = '" + group_list +"' where auth_id = '"+auth_id+"'"
    # print(authInsert)
    dba=getJsonMysql()
    dba.exeQuery(authInsert)
    return True


def logIn(data,ip):
    user_info=json.loads(data)
    user_id=user_info['user_name']
    user_pwd=user_info['user_password']

    return_data=QXToken(user_id,ip).loginConfirm(user_pwd)

    return return_data
def verify_token(data):
    token_info = json.loads(data)
    token=token_info['access_token']
    return_data=verify_auth_token(token)
    return return_data

def get_nav_permission(token):
    role_id=encrypToken(token)
    role_sql='SELECT role_permissions_ids FROM p_role_info WHERE  id = "'+str(role_id)+'"'
    permission_ids =json.loads(get_JSON(role_sql)[0]['role_permissions_ids'])
    return permission_ids

def get_url(token):
    ""
    sql = "select id,url from p_user_permission"
    navlists = get_JSON(sql)
    permission_ids=get_nav_permission(token)
    permissions=dict()
    permission=[]
    for i in permission_ids:
        for j in navlists:
            if j['id'] == i:
                url_list=j['url']
                permission.append(url_list)
    permissions['permissions_url']=permission

    return permissions

# 获取用户名称

def getUserid(token):
    s = Serializer(SECRET_KEY)
    # print(token)
    try:
        data = s.loads(token)
        # print(data)
        # print(data)
        user_name = data['user_id']
        return user_name
    except Exception as e:
        print(str(e))
        return False
# 获取用户ID
def getRealName(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
        user_name = data['user_id']
        name_sql = 'select * from p_user_info WHERE  user_name="' + user_name + '"'
        name = getJsonFromDatabase(name_sql)
        real_name = ''
        if name:
            print("*************登录用户实际名称*****************")
            real_name = name[0]['user_real_name']
            print(real_name)
        else:
            real_name = ''
        return real_name
    except Exception as e:
        exeLog("获取真实姓名失败，错误代码为" + str(e))
        return False


if __name__ == '__main__':

    encrypToken('eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNTA5NTAwMywiaWF0IjoxNTM0OTk1MDAzfQ.eyJ0aW1lc3RhbXAiOiIyMDE4MDgyMzExMzAwMyIsIlVTRVJfVkVSSUZZIjoiQURNSU4iLCJ1c2VyX2lkIjoiYWRtaW4iLCJhdXRoX2lkIjpbIjEyMzQiXSwiUk9MRV9JRCI6Mn0.PGWKPpNmP69R_2dG6ibUJWRnRwKAoQwtjQTyjVee_00')