#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: testRe.py

@time: 2018/3/5 13:38
"""
import re

arr = ["123", '123a', 'abcd', '321', 'a123']
for ele in arr:
    if re.match(r"^[0-9]*$", ele) is not None:
        print("合法")
    else:
        print("不合法")