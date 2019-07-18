# coding:utf-8


import sys

sys.path.append("/opt/ATEST")

import string
import random
import datetime
import uuid

"""
函数实现随机生成满足格式的手机号码
参数repeat为True，获取重复的的手机号码，参数repeat为False，获取不重复的的手机号码,参数num获取具体数量的手机号码
"""
'''
1.获取随机手机号
2.获取身份证号
3.获取UUID
4.获取工行卡号
5.获取int数值
6.获取随机名字
7.获取随机邮箱

'''


def getcdata(num):
    if num == "1":
        return get_phone_num(False, 1)[0]
    elif num == "2":
        return get_ident(1)[0]
    elif num == "3":
        return get_uuid(1)[0]
    elif num == "4":
        return get_bankNo("62220238")[0]
    elif num == "5":
        return data_generation()
    elif num == "6":
        return get_name()
    elif num =='7':
        return get_email()
    else:
        redata = ["暂无 '" + num + "'  参数的常量！"]
        return redata


def get_phone_num(repeat, num):
    """根据输入的参数，获取不同类型的手机号码,repeat为True,
    获取重复的手机号码,Flase获取不重复的手机号码，num为获取具体数量的手机号码"""

    try:
        # 创建一个空列表
        all_phone_nums = []

        # 开头手机号码
        num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187',
                     '188',
                     '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189', '181', '183',
                     '184',
                     '176', '177', '153', '199']

        # 如果参数为True，获取对应数量重复的手机号码
        if repeat == True:
            start = random.choice(num_start)
            end = ''.join(random.sample(string.digits, 8))
            res = start + end + ' '
            re = (res * num).split(' ')
            re.pop()
            return re

        # 如果参数为False，获取对应数量不重复的手机号码
        elif repeat == False:
            for i in range(num):
                start = random.choice(num_start)
                end = ''.join(random.sample(string.digits, 8))
                res = start + end
                all_phone_nums.append(res)

            # 判断是否存在重复的手机号码
            if len(all_phone_nums) == len(set(all_phone_nums)):
                print("没有重复的手机号码")
            else:
                print("存在重复的手机号码")
            return all_phone_nums
        else:
            print("输入错误")
    except BaseException as msg:
        print(msg)


"""
函数实现随机生成满足身份证格式的身份证号码
参数num为获取具体数量的身份证号码
"""


def get_ident(num):
    try:
        all_id = []
        # 身份证号的前两位，省份代号
        sheng = (
            '11', '12', '13', '14', '15', '21', '22', '23', '31', '32', '33', '34', '35', '36', '37', '41', '42', '43',
            '44',
            '45', '46', '50', '51', '52', '53', '54', '61', '62', '63', '64', '65', '66')
        for i in range(num):
            # 随机选择距离今天在5000到25000的日期作为出生日期（没有特殊要求我就随便设置的，有特殊要求的此处可以完善下）
            birthdate = (datetime.date.today() - datetime.timedelta(days=random.randint(6800, 25000)))

            # 拼接出身份证号的前17位（第3-第6位为市和区的代码；第15-第17位为出生的顺序码，随机在100到199中选择）
            ident = sheng[random.randint(0, 31)] + str(random.randint(1000, 2000)) + birthdate.strftime("%Y%m%d") + str(
                random.randint(100, 199))

            # 前17位每位需要乘上的系数，用字典表示，比如第一位需要乘上7，最后一位需要乘上2
            coe = {1: 7, 2: 9, 3: 10, 4: 5, 5: 8, 6: 4, 7: 2, 8: 1, 9: 6, 10: 3, 11: 7, 12: 9, 13: 10, 14: 5, 15: 8,
                   16: 4,
                   17: 2}
            summation = 0

            # for循环计算前17位每位乘上系数之后的和
            for i in range(17):
                summation = summation + int(ident[i:i + 1]) * coe[i + 1]  # ident[i:i+1]使用的是python的切片获得每位数字

            # 前17位每位乘上系数之后的和除以11得到的余数对照表，比如余数是0，那第18位就是1
            key = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}

            # 拼接得到完整的18位身份证号
            id = ident + key[summation % 11]
            all_id.append(id)

        # 判断是否存在重复的手机号码
        if len(all_id) == len(set(all_id)):
            print("没有重复的身份证号码")
        else:
            print("存在重复的身份证号码")
        return all_id

    except BaseException as msg:
        print(msg)


"""
函数实现生成相对应的类型数据
参数d_type为数据的类型，目前支持'str'，'int','float',参数max_value为获取的最长度值,min_value为最小长度值
"""


def boundary_value(d_type, max_value, min_value):
    try:
        all_data = []
        if d_type == "str":
            str_max = ''
            str_min = ''
            chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
            lenth = len(chars) - 1
            for i in range(max_value):
                str_max += chars[random.randint(0, lenth)]

            for i in range(min_value):
                str_min += chars[random.randint(0, lenth)]
            all_data.append(str_max)
            all_data.append(str_min)
            return all_data

        elif d_type == "int":
            str_max = ''
            str_min = ''
            chars = '0123456789'
            lenth = len(chars) - 1
            for i in range(max_value):
                str_max += chars[random.randint(0, lenth)]

            for i in range(min_value):
                str_min += chars[random.randint(0, lenth)]
            str_min = int(str_min)
            str_max = int(str_max)
            all_data.append(str_max)
            all_data.append(str_min)
            return all_data

        elif d_type == "float":
            re = random.randint(3, 9)
            r = random.uniform(2, re)
            # 获取小数点后面的长度
            str_r = str(r)
            str_r_s = str_r[:2]
            str_r_m = str_r[2:max_value + 1]
            str_r_max = str_r_s + str_r_m
            str_r_n = str_r[2:min_value + 1]
            str_r_min = str_r_s + str_r_n
            f_max = float(str_r_max)
            f_min = float(str_r_min)
            all_data.append(f_max)
            all_data.append(f_min)
            return all_data
        else:
            print("暂不支持其他数据类型")
    except BaseException as msg:
        print(msg)


"""
函数实现生成相应数据类型的数据
参数d_type目前只支持生成'str'，'int','float'三种类型数据,参数le为获取数据类型的长度，float参数le，获取的是小数点后面的参数,
float参数lx，lx参数的值必须比le大 获取float总的的长度,每个参数都有默认值，可以不传参 
"""


def data_generation(d_type='int', le=3, lx=5, b="True"):
    try:
        if d_type == "str":
            str_s = ''
            chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
            length = len(chars) - 1
            for i in range(le):
                str_s += chars[random.randint(0, length)]
            return str_s

        elif d_type == "int":
            str_i = ''
            chars = '0123456789'
            length = len(chars) - 1
            for i in range(le):
                str_i += chars[random.randint(0, length)]

            str_i = int(str_i)
            return str_i

        elif d_type == "float":

            # re = random.randint(2, 9)
            # r = random.uniform(1, re)
            # # 获取小数点后面的长度
            # str_f = round(r, le)
            # str_r = str(r)
            # str_r_s = str_r[:2]
            # str_r_e = str_r[2:lx+1]
            # str_r_re = str_r_s+str_r_e
            # f_re = float(str_r_re)
            # return str_f, f_re
            c = lx - le
            if c >= 1:
                if c == 1:
                    r = random.uniform(1, 9)
                    ru = str(r)
                    ru_s = ru[:2]
                    ru_e = ru[2:le + 2]
                    rul = ru_s + ru_e
                    rult = float(rul)
                    return rult
                elif c == 2:
                    r = random.uniform(10, 99)
                    ru = str(r)
                    ru_s = ru[:2]
                    ru_e = ru[2:le + 3]
                    rul = ru_s + ru_e
                    rult = float(rul)
                    return rult
                elif c == 3:
                    r = random.uniform(100, 999)
                    ru = str(r)
                    ru_s = ru[:2]
                    ru_e = ru[2:le + 4]
                    rul = ru_s + ru_e
                    rult = float(rul)
                    return rult
                elif c == 4:
                    r = random.uniform(1000, 9999)
                    ru = str(r)
                    ru_s = ru[:2]
                    ru_e = ru[2:le + 5]
                    rul = ru_s + ru_e
                    rult = float(rul)
                    return rult
                elif c == 5:
                    r = random.uniform(10000, 99999)
                    ru = str(r)
                    ru_s = ru[:2]
                    ru_e = ru[2:le + 6]
                    rul = ru_s + ru_e
                    rult = float(rul)
                    return rult
                elif c == 6:
                    r = random.uniform(100000, 999999)
                    ru = str(r)
                    ru_s = ru[:2]
                    ru_e = ru[2:le + 7]
                    rul = ru_s + ru_e
                    rult = float(rul)
                    return rult

                elif c == 7:
                    r = random.uniform(1000000, 9999999)
                    ru = str(r)
                    ru_s = ru[:2]
                    ru_e = ru[2:le + 8]
                    rul = ru_s + ru_e
                    rult = float(rul)
                    return rult
                elif c == 8:
                    r = random.uniform(10000000, 99999999)
                    ru = str(r)
                    ru_s = ru[:2]
                    ru_e = ru[2:le + 9]
                    rul = ru_s + ru_e
                    rult = float(rul)
                    return rult
            else:
                print("lx必须大于le")

        elif d_type == "bool":
            if b == "True":
                return True
            elif b == "False":
                return False
            else:
                print("输入错误")

        else:
            print("暂不支持其他数据类型生成")

    except BaseException as msg:
        print(msg)


"""
函数实现生成uuid
参数num为生成多少数量的uuid
"""


def get_uuid(num):
    try:
        all_uuid = []
        for i in range(num):
            u_id = uuid.uuid1()
            all_uuid.append(u_id.__str__())

        # 判断是否存在重复的uuid
        if len(all_uuid) == len(set(all_uuid)):
            print("没有重复的UUID")
        else:
            print("存在重复的UUID")
        return all_uuid
    except BaseException as msg:
        print(msg)


'''
生成银行卡号：num为卡bin  8位
'''


def get_bankNo(num):
    a = 6222023803013297860
    bank = []
    bank_no = int(str(num) + str(data_generation(d_type="int", le=11, lx=12)))
    bank.append(bank_no)
    return bank


# 获取随机名字
def get_name():
    a1 = ['ZDH']

    a2 = ['玉', '明', '龙', '芳', '军', '玲', '晓', '张', '金', '李', '王', '赵', '孙', '伍', '白', '杨', '覃', '吴', '陈', '许', '廖', '江',
          '林', '马', '黄', '梁', '温', '夏', '周']

    a3 = ['乐', '立', '玲', '伟', '国', '蓝', '锋']
    name = random.choice(a1) + random.choice(a2) + random.choice(a3)
    return name


# 获取随机邮箱
def get_email():
    str_s = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    length = len(chars) - 1
    for i in range(10):
        str_s += chars[random.randint(0, length)]

    emai_end = ['@126.com', '@163.com', '@sina.com', '@sohu.com', '@qq.com', '@sogou.com', '@56.com', '@citiz.com',
                '@tuandai.com']
    email = str_s + random.choice(emai_end)
    return email


if __name__ == '__main__':
    # print(get_phone_num(True, 2))
    # print(get_ident(2))
    # print(boundary_value("float", 1, 2))
    # print()
    # print(get_bankNo('62220238'))

    print(get_email())
    print(getcdata('5'))
