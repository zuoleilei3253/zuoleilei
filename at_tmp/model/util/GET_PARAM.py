#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/14 11:03
# @Author  : kimmy-pan
# @File    : GET_PARAM.py
import json
import re

# from model.util.PUB_LOG import exeLog


class GET_PARAM(object):
    def __init__(self,isparam,replaceValue):
        self.replaceValue = replaceValue
        self.isparam = isparam

    def GET_INIT_DATA(self):
        adict = self.isparam
        text = self.replaceValue
        return self.multiple_replace(text, adict)

        # if self.isparam['data'] == "":
        #     return self.replaceValue
        # elif self.isparam['data'] != "":
        #     adict = self.isparam['data']
        #     text = self.replaceValue
        #     # for k,v in adict.items():
        #     #     if v not in text:
        #     #         return "参数值：{}，不存在{}".format(k,text)
        #     return self.multiple_replace(text,adict)

    def multiple_replace(self,text, adict):
        """
        :param text: 是需要被替换的
        :param adict: 是模板,dict格式
        :return:
        """
        #
        # exeLog("text：" + str(text))
        # exeLog("adict：" + str(adict))
        if isinstance(text, dict):
            for key, value in list(text.items()):
                changevalue=value
                if '${' in str(changevalue):
                    # adictkey="\${"+key+".*?}"
                    for adictkey ,adictvalue in adict.items():
                        if isinstance(changevalue,dict)or isinstance(changevalue,list):
                            #print(self.multiple_replace(changevalue,adict))
                            text[key]= json.loads(json.dumps(eval(self.multiple_replace(changevalue,adict)),ensure_ascii=False))
                        else:
                            if adictkey in str(changevalue):
                                if 'integer' in str(changevalue) or 'long' in str(changevalue):
                                    text[key] = int(adictvalue)
                                elif 'boolean' in str(changevalue):
                                    text[key] = 'true' ==adictvalue.lower()
                                elif 'float' in str(changevalue):
                                    text[key] = float(adictvalue)
                                elif 'array' in str(changevalue):
                                    text[key] = adictvalue
                                elif 'json' in str(changevalue):
                                    if isinstance(adictvalue,dict):
                                        text[key] = adictvalue
                                    else:
                                        text[key]=json.loads(adictvalue)
                                else:
                                    adictkey = "\${" + adictkey + ".*?}"
                                    changevalue=re.sub(adictkey,str(adictvalue),str(changevalue))
                                    text[key]=changevalue
                        # print(key)
                        # if 'integer' in value or 'long' in value:
                        #     text[key] = int(adict.get(key))
                        # elif 'boolean' in value:
                        #     text[key] = 'true' == adict.get(key).lower()
                        # elif 'float' in value:
                        #     text[key] = float(adict.get(key))
                        # elif 'json' in value:
                        #     text[key] = json.loads(adict.get(key))
                        # else:
                        #     text[key] = adict.get(key)
                else:
                    text[key] = value
            return str(text)
        else:
            for key, value in adict.items():
                key = "\${" + key + ".*?}"
                text = re.sub(key, str(value), str(text))
            return text

        # rx = re.compile('|'.join(map(re.escape, adict)))
        #
        # def one_xlat(match):
        #     return adict[match.group(0)]
        #
        # # RECORD BY [panshuhua]: 返回数据类型为：dict,list,tuple
        # try:
        #     replaceText = rx.sub(one_xlat, str(text))
        #     # if "$" in replaceText:
        #     #     return '参数值替换错误',eval(replaceText),text
        #     # else:
        #     #     return eval(replaceText)
        #     exeLog("replaceText：" + replaceText)
        #     return eval(replaceText)
        # # RECORD BY [panshuhua]: 返回数据类型为：string
        # except SyntaxError:
        #     # replaceText = rx.sub(one_xlat, str(text))
        #     # if "$" in replaceText:
        #     #     return '参数值替换错误', replaceText,text
        #     # else:
        #     #     return rx.sub(one_xlat, str(text))
        #     return rx.sub(one_xlat, str(text))


# 获取带${}的参数
def GET_Variable(param):
    """
    获取带${}的参数
    :param param: {'Data': {"userId":"${userId}","bankId":"${bankId}"},'Token': ""}
    :return: 返回list；['${userId}', '${bankId}']
    """
    a = re.compile(r'\${(.*?)}')
    list = a.findall(str(param))
    returnList = []
    for i in list:
        text = i.replace("${","").replace("}","")
        text = text.split('.')[0]
        returnList.append(text)

    return returnList


if __name__ == "__main__":
    # isparam = {"data":{"{content-type}": "xxxxxx"}}
    # replaceValue = '{"content-type": "{content-type}"}'
    # replaceValue = {'Data': {"userId":"${userId}","bankId":"${bankId}"},'Token': ""}
    # param = {"${userId}":"test","${bankId}":"test"}
    a={'methodName': 'string', 'token': '${t1.string}', 'systemName': '${test.string}', 'machineCode': 'string', 'fromType': 0, 'ip': 'string', 'cdn': 'string', 'version': 'string', 'userId': 'string', 'requestTime': 'string', 'data': {'salary': 'string', 'marriage': 'string', 'nickName': 'string', 'university': 'string', 'graduation': 'string', 'isHaveHouse': True, 'isHaveCar': True, 'contactTelNo': 'string', 'officeScale': 'string', 'position': 'string', 'officeDomain': 'string', 'contactRelationShip': 0, 'contactName': 'string', 'address': 'string'}, 'channel': 'string'}


    b={'test': '18107139826', 't1': 'e12e'}
    print(type(a),type(b))
    print(GET_PARAM(b,a).GET_INIT_DATA())

