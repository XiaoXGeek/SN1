#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: testDict.py

@time: 2018/3/12 10:33
"""
# dict的key是否可以是一个元组
map_1 = {('a', 'b'): 1, ('b', 'a'): 2}
tuple_1 = ('a', 'b')
print(map_1.get(tuple_1))
print(map_1.get(('b', 'a')))
print(map_1.get(('a', 'c'), -1))