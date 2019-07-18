## 迭代五接口说明文档



### 1.数据库检查接口

##### 1）查询接口

接口地址：/dbc?group_id=0 &_page=1&_limit=20

请求方法：GET

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：

```json
null
```

成功返回：

```json
{
    "data":
    {"page": 1,
     "tb_data": [
     {
     "dbc_id": "ID", 
     "adddate": "2018-09-25 16:40:02", 
     "dbc_desc": "描述", 
     "dbc_type": "执行类型", 
     "dbc_sql": "执行SQL",
      "group_id": "999", 
      "dbc_status": "状态"
       },
       {
     "dbc_id": "ID", 
     "adddate": "2018-09-25 16:40:02", 
     "dbc_desc": "描述", 
     "dbc_type": "执行类型", 
     "dbc_sql": "执行SQL",
      "group_id": "999", 
      "dbc_status": "状态"
       }
      ],
      "total": 2, 
      "group_id": 0, 
      "pages": 1}, 
      "code": 200, 
      "message": "操作成功!"
      }


```

异常返回：

```json
{
    "code":"401-异常",
    "data":"",
    "message":"异常信息！～"
}
```
##### 2）明细接口

接口地址：/dbc/DBC_00001(dbcID)

请求方法：GET

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：

```json
null
```

成功返回：

```json
{
    "data":   
     {
     "dbc_id": "ID", 
     "adddate": "2018-09-25 16:40:02", 
     "dbc_desc": "描述", 
     "dbc_type": "执行类型", 
     "dbc_sql": "执行SQL",
      "group_id": "999", 
      "dbc_status": "状态"
       },
      "code": 200, 
      "message": "操作成功!"
      }


```

异常返回：

```json
{
    "code":"401-异常",
    "data":"",
    "message":"异常信息！～"
}
```

##### 3）新增

接口地址：/dbc

请求方法：POST

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：

```json
  {
     "dbc_desc": "描述", 
     "dbc_type": "数据类型1-查询，2-变更", 
      "group_id": "", 
      "dbc_status": "状态 0-无效，1-有效"
       }
```

成功返回：

```json
{
    "code":200,
    "data":"",
    "message":"新增成功"
}


```

异常返回：

```json
{
    "code":"401-异常",
    "data":"",
    "message":"异常信息！～"
}
```



##### 4）更新明細

接口地址：/dbc/detail

请求方法：POST

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：

```json
  {
  
     "dbc_desc": "描述", 
     "dbc_type": "执行类型", 
      "group_id": "", 
      "dbc_status": "状态",
      "dbc_id":"ID",
      "dbc_sql":"執行sql",
      "init_data":[["11",null,{}],["11",null,{}]]
       }
```

成功返回：

```json
{
    "code":200,
    "data":"",
    "message":"新增成功"
}


```

异常返回：

```json
{
    "code":"401-异常",
    "data":"",
    "message":"异常信息！～"
}
```


##### 5）删除

接口地址：/dbc/DBC_00001(dbcID)

请求方法：POST

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：

```json
null
```

成功返回：

```json
{
    "code":200,
    "data":"",
    "message":"删除成功"
}


```

异常返回：

```json
{
    "code":"401-异常",
    "data":"",
    "message":"异常信息！～"
}
```
##### 4）修改

接口地址：/dbc

请求方法：PATCH

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：

```json
 {
     "dbc_desc": "描述", 
     "dbc_type": "执行类型", 
     "dbc_sql": "执行SQL",
      "dbc_status": "状态",
      "group_id":""
       }
```

成功返回：

```json
{
    "code":200,
    "data":"",
    "message":"删除成功"
}


```

异常返回：

```json
{
    "code":"401-异常",
    "data":"",
    "message":"异常信息！～"
}
```
##### 5）执行

接口地址：/dbc/exe

请求方法：POST

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：

```json
 {

     "dbc_sql": "执行SQL",
     "dbc_env_id":"数据库环境ID"

       }
```

成功返回：

```json
{
    "code":200,
    "data":[
    {
    "数据库数据":"数据库数据"
    }
    ],
    "message":""
}


```

异常返回：

```json
{
    "code":"401-异常",
    "data":"",
    "message":"异常信息！～"
}
```


### 2.API检查接口

##### 1）新增

接口地址：/api/detail

请求方法：post

请求头：

```json
{
"Token":"密钥YYYY"
}
```
请求参数：

```json
 {

     "uri": "接口地址",
     "method":"接口方法",
     "title": "接口名称",
     "headers":"请求头",
     "params": "请求参数",
     "group_id":"分组ID",
     "api_type": "1-查询，2-新增，3-修改，4-删除",
     "api_is_remold":"0-否，1-是",
     "api_need_login": "0-否，1-是",
     "api_status":"0-否，1-是",
     "api_id":"api编号"

       }
```

成功返回：

```json
{
    "code":200,
    "data":"",
    "message":""
}


```

异常返回：

```json
{
    "code":"401-异常",
    "data":"",
    "message":"异常信息！～"
}
```
DBUG参数：

```json
{
    "uri":"接口地址",
    "url":"主机地址",
    "method":"请求方法",
    "headers":"请求头",
    "params":"请求参数",
    "init_data":"入参参数！～"
}
```

获取环境列表：
/env_opt?group_id=0&_page=1&_limit=10
获取环境明细
/env_opt/detail?env_id=111&env_d_type=111

env_d_type:1-接口地址  2- 数据库地址


地址：/dbc/exe
请求方法：post
参数
{"dbc_sql":"sql语句","env_d_id":"环境服务ID"}

接口返回格式：
```json
[{
    "字段1":"返回值1",
    "字段2":"返回值1",
    "字段3":"返回值1"
},
{
    "字段1":"返回值1",
    "字段2":"返回值1",
    "字段3":"返回值1"
},{
    "字段1":"返回值1",
    "字段2":"返回值1",
    "字段3":"返回值1"
},{
    "字段1":"返回值1",
    "字段2":"返回值1",
    "字段3":"返回值1"
}
]
```


日志執行格式

<<************测试套件执行开始**********>>
**


接口加解密新增字段
测试环境：
解密地址
http://10.100.13.76:9998/interface/cryptography/decrypt
加密地址：
http://10.100.13.76:9998/interface/cryptography/encrypt

请求头：
{'Content-Type':'Application/Json','env':'1'}

isncry :0-否，1-是





##shell检查接口

##### 1）新增列表接口


接口地址：/shell

请求方法：POST

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：

```json
  {
     "shell_desc": "描述", 
      "group_id": "", 
      "shell_status": "状态 0-无效，1-有效",
       }
```

成功返回：

```json
{
    "code":200,
    "data":"",
    "message":"新增成功"
}


```

异常返回：

```json
{
    "code":"201-异常",
    "data":"",
    "message":"异常信息！～"
}
```

##### 1）新增接口信息


接口地址：/shell

请求方法：PATCH

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：

```json
  {
  "shell_id": "shell_id", 
     "shell_desc": "描述", 
     "shell_type": "数据类型1-查询，2-变更", 
      "group_id": "", 
      "shell_status": "状态 0-无效，1-有效",
      "shell_cmd":"",
      "env_d_id":"环境ID"
       }
```

成功返回：

```json
{
    "code":200,
    "data":"",
    "message":"更新成功"
}


```

异常返回：

```json
{
    "code":"201-异常",
    "data":"",
    "message":"异常信息！～"
}
```



##### 3）shell信息列表


接口地址：/shell?group_id=0 &_page=1&_limit=20 

请求方法：GET

请求头：

```json
{
"Token":"密钥YYYY"
}
```

请求参数：


成功返回：

```json
{
    "code":200,
    "data":  {"page": 1,
     "tb_data": [
     {
  "shell_id": "shell_id", 
     "shell_desc": "描述", 
     "shell_type": "数据类型1-查询，2-变更", 
      "group_id": "", 
      "shell_status": "状态 0-无效，1-有效",
      "shell_cmd":"",
      "env_d_id":"环境ID"
       },
       {
  "shell_id": "shell_id", 
     "shell_desc": "描述", 
     "shell_type": "数据类型1-查询，2-变更", 
      "group_id": "", 
      "shell_status": "状态 0-无效，1-有效",
      "shell_cmd":"",
      "env_d_id":"环境ID"
       }
      ],
      "total": 2, 
      "group_id": 0, 
      "pages": 1},
    "message":"更新成功"
}


```

异常返回：

```json
{
    "code":"201-异常",
    "data":"",
    "message":"异常信息！～"
}
```