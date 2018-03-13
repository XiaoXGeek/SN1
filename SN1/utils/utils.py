#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: utils.py

@time: 2018/3/13 8:49
"""
# 一些基本的工具
import os


class myutils(object):
    @classmethod
    def mkdirs_by_file(self, file_path):
        if not os.path.exists('/'.join((file_path.split("/" or "\\")[:-1]))):
            os.makedirs('/'.join((file_path.split("/" or "\\")[:-1])))


if __name__ == '__main__':
    pass