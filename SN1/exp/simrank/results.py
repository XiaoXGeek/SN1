#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: results.py

@time: 2018/3/7 8:59
"""


# 筛选结果数据
def follow_result(follows, follows_new, inner):
    follows = open(follows, 'r')
    follows_new = open(follows_new, 'w')
    inner = open(inner, 'r')
    linner = []
    for line in inner:
        linner.append(line.strip())
    i = 0
    for line in follows:
        arr = line.strip().split()
        if arr[0] in linner and len(arr) > 1:
            i = i + 1
            follows_new.write(line)
    print("交集大小：%d,结果中数据大小：%d" % (len(linner), i))
    inner.close()
    follows.close()
    follows_new.close()


if __name__ == '__main__':
    # 全集
    follows_all = "../../resource/20180305/simrank/result/i%d/follow_nodesim_naive_all"
    follows_new_all = "../../resource/20180305/simrank/result/i%d/follow_nodesim_naive_after_all"
    inner = "../../resource/20180305/simrank/inner.txt"
    # 筛选结果数据
    follow_result(follows_all % 10, follows_new_all % 10, inner)
    # 部分集
    follows = "../../resource/20180305/simrank/result/follow_nodesim_naive"
    follows_new = "../../resource/20180305/simrank/result/follow_nodesim_naive_after"
    # follow_result(follows, follows_new, inner)

