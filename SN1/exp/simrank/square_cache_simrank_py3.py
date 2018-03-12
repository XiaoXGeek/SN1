#!/usr/bin/env python
# -*-coding:utf-8-*-

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: SimRankv02.py

@time: 2018/1/18 9:41
"""
import numpy as np

nodes = []  # 所有节点存入数组
nodesnum = 0    # 所有节点的数目
nodes_index = {}    # <节点名， 节点在nodes数组中的编号>
damp = 0.8  # 阻尼系数
trans_matrix = np.matrix(0)     # 转移概率矩阵
sim_matrix = np.matrix(0)   # 节点相似度矩阵


def initParam(graphFile):
    # 构建nodes、nodes_indes、trans_matrix和第0代的sim_matrix
    # 输入文件格式要求：node \t outneighbor \t outneighbotor
    global nodes
    global nodes_index
    global trans_matrix
    global sim_matrix
    global damp
    global nodesnum

    link_in = {}
    for line in open(graphFile, "r", 1024):
        arr = line.strip("\n").split()
        node = arr[0]
        nodeid = -1
        if node in nodes_index:
            nodeid = nodes_index[node]
        else:
            nodeid = len(nodes)
            nodes_index[node] = nodeid
            nodes.append(node)
        for ele in arr[1:]:
            outneighbor = ele
            outneighborid = -1
            if outneighbor in nodes_index:
                outneighborid = nodes_index[outneighbor]
            else:
                outneighborid = len(nodes)
                nodes_index[outneighbor] = outneighborid
                nodes.append(outneighbor)
            inneighbors = []
            if outneighborid in link_in:
                inneighbors = link_in[outneighborid]
            inneighbors.append(nodeid)
            link_in[outneighborid] = inneighbors

    nodesnum = len(nodes)
    trans_matrix = np.zeros((nodesnum, nodesnum))   # 生成一个nodesum阶的矩阵，元素是0
    # 转移矩阵的初始值是入度节点数目的倒数
    for node, inneighbors in link_in.items():
        num = len(inneighbors)
        prob = 1.0 / num
        for neighbor in inneighbors:
            trans_matrix[node, neighbor] = prob
    sim_matrix = np.identity(nodesnum) * (1 - damp)  # 生成一个nodesnum阶矩阵，主对角线元素是(1 - damp)


def iterate():
    global trans_matrix
    global sim_matrix
    global damp
    global nodesnum

    damp = damp ** 2    # damp的平方
    # 矩阵的积
    trans_matrix = np.dot(trans_matrix, trans_matrix)
    # transpose是矩阵的转置
    sim_matrix = damp * np.dot(np.dot(trans_matrix,
                                      sim_matrix), trans_matrix.transpose()) + sim_matrix


# 输出结果到文件
def printResult(sim_node_file):
    global sim_matrix
    global link_out
    global link_in
    global nodes
    global nodesnum

    f_out_user = open(sim_node_file, "w")
    for i in range(nodesnum):
        f_out_user.write(nodes[i] + "\t")
        neighbour = []
        for j in range(nodesnum):
            if i != j:
                sim = sim_matrix[i, j]
                if sim == None:
                    sim = 0
                if sim > 0:
                    neighbour.append((j, sim))
        neighbour = sorted(
            neighbour, key=lambda x: x[1], reverse=True)
        for (u, sim) in neighbour:
            f_out_user.write(nodes[u] + ":" + str(sim) + "\t")
        f_out_user.write("\n")
    f_out_user.close()


# 筛选结果数据
def simrank_result_filter(follows, follows_new, inner):
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


#
def simrank(graphFile, maxIteration):
    # global nodes_index
    # global trans_matrix
    # global sim_matrix

    initParam(graphFile)
    # print("nodes:")
    # print(nodes_index)
    # print("trans ratio:")
    # print(trans_matrix)
    for i in range(maxIteration):
        print("第%d次迭代" % (i + 1))
        iterate()
        # print(sim_matrix)


if __name__ == '__main__':
    # graphFile = "../../../data/weibo/20180304/user_matrix_follow.txt"
    # graphFile = "../../../data/linkgraph"
    follow_graphFile = "../../resource/20180305/simrank/follow_link%s"
    follow_sim_node_file = "../../resource/20180305/simrank/result/i%d/follow_nodesim_naive%s"
    fan_graphFile = "../../resource/20180305/simrank/follow_link.txt"
    fan_sim_node_file = "../../resource/20180305/simrank/result/fan_nodesim_naive"
    maxIteration = 10
    simrank(follow_graphFile % "_all", maxIteration)
    printResult(follow_sim_node_file % (maxIteration, "_all"))


