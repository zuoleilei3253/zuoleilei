#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/17 15:22
# @Author  : kimmy-pan
# @File    : GET_DATA.py
from flask import Flask,request, jsonify
app = Flask(__name__)


@app.route('/getdata', methods=['POST','GET'])
def getdata():
    if request.method == 'POST':
        try:
            token = request.headers['Token']
        except Exception:
            return jsonify({'message': u'数据发送失败！没有传Token值',
                            'data':'',
                            'code': 201})
        params = ['task_id','result_lists']
        for i in params:
            if request.json[i] == "":
                return jsonify({'message': u'数据发送失败！{}不能为空'.format(i),
                                'data': '',
                                'code': 201})
        if type(request.json['result_lists']) is not list:
            return jsonify({'message': u'数据发送失败！result_lists数据格式错误',
                            'data': '',
                            'code': 201})
        params = ['case_id','case_result','case_time','case_executor','case_exetype']
        key = []
        for i in request.json['result_lists']:
            # print(i)
            for k,v in i.items():
                key.append(k)
            for j in params:
                if j not in key:
                    return jsonify({'message': 'case_id:'+str(i["case_id"])+'数据发送失败！没有传{}'.format(j),
                                    'data': '',
                                    'code': 201})

        return jsonify({'message': 'success','data': '','code': 200})
    elif request.method == 'GET':
        return jsonify({'message': '请求方式错误', 'data': '', 'code': 201})


if __name__ == '__main__':
    app.run(threaded=True,debug=True)