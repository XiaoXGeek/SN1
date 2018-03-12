#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: data_pre.py

@time: 2018/3/8 13:12
"""
import scipy.io as sio
import numpy as np
import sys
import progressbar


def write_file_mat(data_file, mat_file):
    bar = progressbar.ProgressBar()
    c_nodes = []
    r_nodes = []
    c_nodes_map = {}
    r_nodes_map = {}
    data = ''
    # 为所有节点编号
    f = open(data_file, 'r')
    j = 0
    bar.start(351)
    for line in f:
        arr = line.strip().split()
        j = j + 1
        bar.update(j)
        if arr[0] not in c_nodes:
            c_nodes_map[arr[0]] = len(c_nodes)
            c_nodes.append(arr[0])
        for i in range(1, len(arr)):
            arr_ = arr[i].split(':')
            if arr_[0] not in r_nodes:
                r_nodes_map[arr_[0]] = len(r_nodes)
                r_nodes.append(arr_[0])
    f.close()
    bar.finish()
    j = 0
    bar.start()
    f = open(data_file, 'r')
    data = np.mat(np.zeros((len(c_nodes), len(r_nodes))))
    for line in f:
        arr = line.strip().split()
        j = j + 1
        bar.update(j)
        sys.stdout.write("当前正在写入第%d个节点编号\r" % j)
        sys.stdout.flush()
        for i in range(1, len(arr)):
            arr_ = arr[i].split(':')
            data[c_nodes_map[arr[0]], r_nodes_map[arr_[0]]] = arr_[1]
    data_column = np.mat(np.zeros((1, len(c_nodes))))
    bar.finish()
    for i in range(0, len(c_nodes)):
        data_column[0, i] = int(c_nodes[i])
    data_row = np.mat(np.zeros((1, len(r_nodes))))
    for i in range(0, len(r_nodes)):
        data_row[0, i] = int(r_nodes[i])
    sio.savemat(mat_file, {'data_row': data_row, 'data_column': data_column, 'data': data})
    f.close()


if __name__ == '__main__':
    data_file = "../../resource/20180305/simrank/result/i%d/follow_nodesim_naive_after_all"
    mat_file = "../../resource/20180305/simrank/result/i%d/follow_nodesim_naive_after_all_mat"
    write_file_mat(data_file % 10, mat_file % 10)

