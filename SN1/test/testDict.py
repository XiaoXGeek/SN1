#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: testDict.py

@time: 2018/3/12 10:33
"""
# dict的key是否可以是一个元组
map_1 = {('a', 'b'): 1, ('a', 'c'): 2}
tuple_1 = 'a', 'c'
for key in map_1:
    print(key[0])
print(map_1.get(tuple_1))