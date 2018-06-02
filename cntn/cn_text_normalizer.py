#!/usr/bin/env python3
#-*- coding: utf8 -*-
"""
Author: 2018 Meixu Song <meixu.asr@gmail.com>
Date: 2018-06-01
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import re
from functools import partial

from cntn import pycnnum

# todo:
# - 几分之几

cn_key = [u"[\u4e00-\u9fff]+"]
en_key = ['[A-Z]+']
num_key = ['\d+\.\d+', '\d+']

PRE_UNITS = {
    "%": "百分之"
}

POST_UNITS = {
    # 科学符号
    "CM": "厘米",
    "KM": "公里",
    "M": "米",
    "KG": "公斤",
    "G": "克",
    # 货币符号
    # "$" : "美元",
    # "\$" : "美元", # for regex happy
    # "￥" : "人民币",
}

units_key = list(PRE_UNITS.keys()) + list(POST_UNITS.keys())
split_str = '('+"|".join(cn_key + en_key + num_key+units_key)+')'
# print(split_str)
split_pat = re.compile(split_str)


def full2half(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ss


def w2s(in_str, numbering_type="low", big=False, traditional=False, alt_zero=False,
        alt_two=False, use_zeros=True, use_units=True):
    num2cn = partial(pycnnum.num2cn, numbering_type=numbering_type, big=big, traditional=traditional,
                        alt_zero=alt_zero, alt_two=alt_two, use_zeros=use_zeros, use_units=use_units)

    in_str = in_str.upper()

    results = []
    i = 0

    strings = split_pat.split(in_str)
    strings = list(filter(None, strings))

    # print(strings)

    while i < len(strings):
        # 处理数字串
        if strings[i].replace('.', '', 1).isdecimal():
            # 处理其后有符号情况
            if i+1 < len(strings):
                # 处理发音前置符号：
                if strings[i+1] in PRE_UNITS:
                    results.append(PRE_UNITS[strings[i+1]])
                    results.append(num2cn(strings[i]))
                    i += 2
                    continue
                # 处理发音后置符号：
                elif strings[i+1] in POST_UNITS:
                    results.append(num2cn(strings[i]))
                    results.append(POST_UNITS[strings[i+1]])
                    i += 2
                    continue

            # 整数：以“年”结尾或长度大于等于8，则拼读
            if strings[i].isdecimal() and \
                ((i+1 < len(strings) and strings[i+1].startswith("年"))
                    or len(strings[i]) >= 8):
                results.append(num2cn(strings[i], use_units=False))
            else:
                results.append(num2cn(strings[i]))
        else:
            results.append(strings[i])
        i += 1

    return "".join(results)


if __name__ == '__main__':
    print(w2s("小王的身高是153.5cm,梦想是打篮球!我觉得有0.1%的可能性。"))
    print(w2s("小王的钱包有1116$，可以买个iphone7s。"))
