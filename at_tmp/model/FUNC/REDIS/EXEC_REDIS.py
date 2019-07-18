#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 14:06
# @Author  : kimmy-pan
# @File    : EXEC_REDIS.py
import redis


class RedisQueue(object):
    """读取redis"""
    def __init__(self, redis_data):
        """
        host ：redis地址
        port: redis 端口
        db: redis的数据库
        key: redis的键
        pwd：redis的密码
        type: value的类型：1.string 2.list 3.set 4.hash 5.zset
        :param redis_data: {host:'',port:'',db:'',key:'',pwd:'','type':''}
        """
        # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
        if redis_data["pwd"] == "":
            pwd = None
        else:
            pwd = redis_data["pwd"]
        self.db = redis_data["db"]
        self.__db = redis.Redis(host=redis_data["host"],port=int(redis_data["port"]),db=int(self.db),password=pwd)
        self.key = redis_data["key"]
        self.type = str(redis_data["type"])


    def get_value(self):
        """
        获取value值
        :return: 返回 str
        """
        try:
            if self.type == "2":
                """返回list，默认获取最后一个值"""
                value = self.__db.lindex(self.key,0)
                all_value = self.__db.llen(self.key)
                if value != None and all_value !=0:
                    return str(value.decode())
                # elif value == None and all_value !=0:
                #     return False,'key对应的值只有{}个'.format(0)
                elif value == None and all_value == 0:
                    return False,'{}不存在redis(db:{})'.format(self.key,self.db)
            elif self.type == "4":
                value = self.__db.hgetall(self.key)
                if value != {}:
                    return str(value).replace("b","")
                else:
                    return False, '{}不存在redis(db:{})'.format(self.key,self.db)
            elif self.type == "1":
                value = self.__db.get(self.key)
                if value != None:
                    return value.decode()
                else:
                    return False, '{}不存在redis(db:{})'.format(self.key,self.db)
            elif self.type == "3":
                s = []
                value = self.__db.smembers(self.key)
                if value != set():
                    for i in value:
                        s.append(i.decode())
                    return s
                else:
                    return False, '{}不存在redis(db:{})'.format(self.key,self.db)
            elif self.type == "5":
                s = {}
                value = self.__db.zrangebyscore(self.key,0,1000000000)
                if len(value) != 0:
                    for i in value:
                        i.decode()
                        s[i.decode()] = self.__db.zscore(self.key,i)
                    return s
                else:
                    return False, '{}不存在redis(db:{})'.format(self.key, self.db)
        except Exception as e:
            return False,'连接redis失败，失败原因：{}'.format(str(e))


if __name__ == "__main__":
    # data = {"host": "127.0.0.1", "port": 6379, "db": 0,
    #         "key": "22", "pwd": "123456","type":"3"}
    data = {"host":"node.td-k8s.com","port":1379,"db":5,"key":"aqs:commission:userscore","pwd":"mWRK6joVy5No","type":"5"}
    print(RedisQueue(data).get_value())


