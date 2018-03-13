#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: results.py

@time: 2018/3/10 11:13
"""
from SN1.utils.utils import myutils


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


# simrank的结果分析，综合follows和fans，存储中间结果
def simrank_analysis_phase_1(file_path, result_tmp, inner):
    file_path = open(file_path, 'r')
    result_tmp = open(result_tmp, 'w')
    inner = open(inner, 'r')
    inners = set()
    for line in inner:
        inners.add(line.strip())
    sim_init = {}
    for line in file_path:
        arr = line.strip().split()
        for ele in arr[1:]:
            arr_ = ele.split(":")
            if arr[0] in inners or arr_[0] in inners:
                sim_init[(arr[0], arr_[0])] = arr_[1]
    sim_init_inner = set()
    for key in sim_init.keys():
        sim_init_inner.add(key[0])
        result_tmp.write("%s\t%s\t%s\n" % (key[0], key[1], sim_init.get(key)))
    print("结果集中inners用户留存数量%d" % len(inners.intersection(sim_init_inner)))
    file_path.close()
    result_tmp.close()
    inner.close()


# 变换lambda_的值
def simrank_analysis_phase_2(result_tmp, inner, result, lambda_=0.75):
    result_tmp = open(result_tmp, 'r')
    result = open(result, 'w')
    inner = open(inner, 'r')
    inners = set()
    for line in inner:
        inners.add(line.strip())
    sim_init = {}
    for line in result_tmp:
        arr = line.strip().split()
        sim_init[(arr[0], arr[1])] = float(arr[2])
    sim = {}
    solved = set()
    for key in sim_init.keys():
        if key not in solved:
            if key[0] in inners:
                sim[key] = lambda_ * sim_init.get(key, 0) + (1 - lambda_) * sim_init.get((key[1], key[0]), 0)
            else:
                sim[(key[1], key[0])] = (1 - lambda_) * sim_init.get(key, 0) + lambda_ * sim_init.get((key[1], key[0]), 0)
            solved.add(key)
            solved.add((key[1], key[0]))
    sim_inner = set()
    for key in sim.keys():
        sim_inner.add(key[0])
        result.write("%s\t%s\t%s\n" % (key[0], key[1], sim.get(key)))
    print("结果集中inners用户留存数量%d" % len(inners.intersection(sim_inner)))
    inner.close()
    result_tmp.close()
    result.close()


# 根据值进行相似度排序
def simrank_analysis_phase_3(result_last, inner, result):
    result_last = open(result_last, 'r')
    sim = {}
    for line in result_last:
        arr = line.strip().split()
        sim[(arr[0], arr[1])] = float(arr[2])
    result_last.close()

    inner = open(inner, 'r')
    inners = set()
    for line in inner:
        inners.add(line.strip())
    inner.close()

    user = {}
    for key in sim.keys():
        neighbour = []
        if key[0] in user.keys():
            neighbour = user.get(key[0])
        neighbour.append((key[1], sim.get(key)))
        user[key[0]] = neighbour
    result = open(result, 'w')
    left_inner = set()
    for keys in user.keys():
        neighbour = sorted(user[keys], key=lambda x: x[1], reverse=True)
        line = keys + '\t'
        left_inner.add(keys)
        for ele in neighbour:
            line = line + ele[0] + ":" + str(ele[1]) + "\t"
        result.write(line+'\n')
    print("结果集中inners用户留存数量%d" % len(inners.intersection(left_inner)))
    result.close()


def simrank_analysis_phase_4(result_last, result, user_choose_left, user_choose, recommand_num):
    user_choose = open(user_choose, 'r')
    user_chooses = {}
    for line in user_choose:
        arr = line.strip().split()
        user_set = set()
        for i in range(1, len(arr)):
            user_set.add(arr[i])
        user_chooses[arr[0]] = user_set
    user_choose.close()

    user_choose_left = open(user_choose_left, 'r')
    user_choose_lefts = {}
    for line in user_choose_left:
        arr = line.strip().split()
        user_set = set()
        for i in range(1, len(arr)):
            user_set.add(arr[i])
        user_choose_lefts[arr[0]] = user_set
    user_choose_left.close()

    result_last = open(result_last, 'r')
    sim_result = {}
    for line in result_last:
        arr = line.strip().split()
        if arr[0] in user_chooses.keys():
            user_set = set()
            user_choose_left_set = user_choose_lefts[arr[0]]
            j = recommand_num
            for i in range(1, len(arr)):
                arr_ = arr[i].split(':')
                if arr_[0] not in user_choose_left_set and j > 0:
                    j = j - 1
                    user_set.add(arr_[0])
                sim_result[arr[0]] = user_set
    result_last.close()

    result_file = open(result, 'w')
    right = 0
    wrong = 0
    need = 0
    all = 0
    recommand_num = 100
    for ele in sim_result.keys():
        result = sim_result[ele]
        choose = user_chooses[ele]
        result_file.write("%s\t%d\t%d\t%d\n" % (ele, len(result), len(choose.intersection(result)), len(result-choose)))
        print("总预测数:%d\t需要预测数:%d\t预测正确数:%d\t预测错误数:%d\t" % (len(result), len(choose),len(choose.intersection(result)), len(result-choose)))
        need = need + len(choose)
        right = right + len(choose.intersection(result))
        wrong = wrong + (recommand_num - right)
        all = all + recommand_num
    precision = right / all
    recall = right / need
    F1 = 2*precision*recall/(precision+recall)
    print("准确率：%f\t召回率:%f\tF1:%f" % (precision, recall, F1))
    result_file.close()
