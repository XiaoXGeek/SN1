#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: exp_pmf.py

@time: 2018/3/12 9:32
"""
import os
import sys
from SN1 import utils


if __name__ == '__main__':
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    rootPath = '/'.join(rootPath.split("\\" or "/")[:-2])
    sys.path.append(rootPath)
    print('/'.join(rootPath.split("\\" or "/")[:-2]))