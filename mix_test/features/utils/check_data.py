# -*- coding: utf-8 -*-from assertpy import assert_thatclass CheckData(object):    def __init__(self):        pass    # 递归检查json数据,以期望数据为基准,实际数据包含期望数据    # 例如：{'a' : {'a1': 1,'a2' : 2} ,'b' : 1} 包含 {'a' : {'a1': 1} }    def json_contain(self, actual_value, expected_value):        # 格式化数据        # if not isinstance(actual_value, dict):        #     actual_value = json.loads(actual_value)        # if not isinstance(expected_value, dict):        #     expected_value = json.loads(expected_value)        for key in expected_value:            if key in actual_value:                if isinstance(expected_value[key], dict):                    self.json_contain(actual_value[key], expected_value[key])                else:                    if key in actual_value:                        assert_that(actual_value[key]).is_equal_to(expected_value[key])            else:                raise Exception("返回中不存在key为" + key + "的数据")    # 递归检查json数据,以期望数据为基准,实际数据包含期望数据(特殊：结果中有数组且数组中内容包含)    # 例如：{'a' : [{'a1': 1,'a11':11},{'a2': 2}] ,'b' : 1} 包含 {'a' : [{'a1': 1}] }    def json_contain_having_list(self, actual_value, expected_value):        for key in expected_value:            if key in actual_value:                if isinstance(expected_value[key], dict):                    self.json_contain_having_list(actual_value[key], expected_value[key])                elif isinstance(expected_value[key], list):                    if len(expected_value[key]) <= len(actual_value[key]):                        for i in range(len(expected_value[key])):                            self.json_contain_having_list(actual_value[key][i], expected_value[key][i])                    else:                        raise Exception(                            "返回的数组比期望的数据元素少,返回的数组长度为" + str(len(actual_value[key])) + ",期望的数组长度为" + str(len(                                expected_value[key])))                else:                    assert_that(actual_value[key]).is_equal_to(expected_value[key])            else:                raise Exception("返回中不存在key为" + key + "的数据")