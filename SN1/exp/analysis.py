#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: results.py

@time: 2018/3/10 11:13
"""


def simrank_analysis(sim_result, sim_result_anysis, relation_graphFile_after, user_choose, recommand_num):
    relation_graphFile_after = open(relation_graphFile_after, 'r')
    sim_result_anysis = open(sim_result_anysis, 'w')
    user_choose = open(user_choose, 'r')
    sim_result = open(sim_result, 'r')
    user_chooses = {}
    user_choose_after = {}
    sim_result_map = {}
    for line in user_choose:
        arr = line.strip().split()
        user_set = set()
        for i in range(1, len(arr)):
            user_set.add(arr[i])
        user_chooses[arr[0]] = user_set
    for line in relation_graphFile_after:
        arr = line.strip().split()
        user_set = set()
        for i in range(1, len(arr)):
            user_set.add(arr[i])
        user_choose_after[arr[0]] = user_set
    for line in sim_result:
        arr = line.strip().split()
        if arr[0] in user_chooses.keys():
            user_set = set()
            user_choose_set = user_choose_after[arr[0]]
            j = recommand_num
            for i in range(1, len(arr)):
                arr_ = arr[i].split(':')
                if arr_[0] not in user_choose_set and j > 0:
                    j = j - 1
                    user_set.add(arr_[0])
            sim_result_map[arr[0]] = user_set
    for ele in sim_result_map.keys():
        result = sim_result_map[ele]
        choose = user_chooses[ele]
        sim_result_anysis.write("%s\t%d\t%d\t%d\n" % (ele, len(result), len(choose.intersection(result)), len(result-choose)))
        print("总预测数:%d\t预测正确数:%d\t预测错误数:%d\t" % (len(result), len(choose.intersection(result)), len(result-choose)))
    user_choose.close()
    relation_graphFile_after.close()
    sim_result_anysis.close()

