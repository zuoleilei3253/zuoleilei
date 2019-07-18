# coding=utf-8
import requests, json

hosts = {}


class BddService(object):
    def __init__(self, api, data={}, headers={}):

        """数据初始化"""

    def __before__(self, context, data, url):

        """处理数据，比如从测试用例中取参数，存放到context的requestData中，供后续的http请求使用"""

    def __after__(self, context, r, url):

        """从http request中获取数据，存放到context的responseData中，供后续的断言使用"""

    def get(self, context, url, data={}):
        pass
# 完成 http 调用