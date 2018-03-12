#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: test_progress_bar.py

@time: 2018/3/9 13:59
"""
import sys, time
import progressbar


bar = progressbar.ProgressBar()
bar.start(0)
for i in range(5):
    bar.update(i)
    time.sleep(2)
bar.finish()