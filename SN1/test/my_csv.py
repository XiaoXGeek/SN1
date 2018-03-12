#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: my_csv.py

@time: 2018/3/8 12:55
"""
import csv
import numpy  as np


# 加载文件
def load_file():
    pass


# 写入文件
def write_file(new_file):
    with open(new_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([11, 12, 13])
        writer.writerow([21, 22, 23])


if __name__ == '__main__':
    write_file("./data/csv.csv")

