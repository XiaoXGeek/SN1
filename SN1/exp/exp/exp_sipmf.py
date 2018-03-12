#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: exp001.py

@time: 2018/3/9 9:35
"""
import os
import SN1.data.simrank.square_cache_simrank_py3 as simr
import SN1.data.nmf.data_pre as nmf
import SN1.data.users as user
import SN1.data.analysis as analysis


bathpath="F:\社交网络\微博\论文\实验\实验数据\\resource\\20180309"


# 数据预处理
def data_pre():
    print("step 1: 预处理开始...")
    # 0.1: 替换字符用户，生成新的follows
    users_init = bathpath + "/init/users_init.txt"
    relation_init = bathpath + "/init/relation_init.txt"
    relation_rp_char = bathpath + "/data_pre/relation_rp_char.txt"
    print("1.1 替换字符用户...")
    user.replace_by_user(users_init, relation_init, relation_rp_char)
    # 0.2: 生成fans和follows的详细的关注列表
    follows_detail = bathpath + "/data_pre/follows_detail.txt"
    fans_detail = bathpath + "/data_pre/fans_detail.txt"
    follow_filter_num = 10
    fan_filter_num = 10
    print("1.2.1 生成follow的详细信息...")
    user.follow(relation_rp_char, follows_detail, follow_filter_num)
    print("1.2.2 生成fan的详细信息...")
    user.fan(relation_rp_char, fans_detail, fan_filter_num)
    # 0.3: 生成fan和follows的simrank预处理数据
    follows_simrank_pre = bathpath + "/simrank/pre/follows_simrank_pre.txt"
    fans_simrank_pre = bathpath + "/simrank/pre/fans_simrank_pre.txt"
    print("1.3.1 将follow处理成simrank可处理格式...")
    user.simrank_link(follows_detail, follows_simrank_pre)
    print("1.3.2 将fan处理成simrank可处理格式...")
    user.simrank_link(fans_detail, fans_simrank_pre)
    # 0.4: follow和fan的交集
    follow_inner_fan = bathpath + "/simrank/pre/follow_inner_fan.txt"
    print("1.4 生成follow和fan的交集...")
    user.follows_inner_fans(follows_simrank_pre, fans_simrank_pre, follow_inner_fan)
    print("数据预处理完成")


# 选择要去除的用户
def chose_user(relation, num=3):
    print("选择用户开始...")
    inner = bathpath + "/simrank/pre/follow_inner_fan.txt"
    relation_graphFile_before = bathpath + "/simrank/pre/%s_simrank_pre.txt" % relation
    relation_graphFile_after = bathpath + "/simrank/pre/%s_simrank_pre_after_chose.txt" % relation
    user_choose = bathpath + "/simrank/pre/%s_simrank_pre_choose.txt" % relation
    user.chose_user(relation_graphFile_before, relation_graphFile_after, inner, user_choose, num)
    print("选择用户结束...")


def simrank(relation, maxIteration = 10):
    print("step 2: simrank开始...")
    # 2.1 执行simrank
    print("2.1 执行%s simrank" % relation)
    relation_graphFile = bathpath + "/simrank/pre/%s_simrank_pre_after_chose.txt"
    relation_sim_node_file = bathpath + "/simrank/result/iterator_%d/%s_simrank_result.txt"
    if not os.path.exists('/'.join((relation_sim_node_file % (maxIteration, relation)).split("/" or "\\")[:-1])):
        os.makedirs('/'.join((relation_sim_node_file % (maxIteration, relation)).split("/" or "\\")[:-1]))
    simr.simrank(relation_graphFile % relation, maxIteration)
    simr.printResult(relation_sim_node_file % (maxIteration, relation))
    # 2.2 筛选结果数据
    print("2.2 筛选结果")
    inner = bathpath + "/simrank/pre/follow_inner_fan.txt"
    relation_sim_node_file_filter = bathpath + "/simrank/result/iterator_%d/%s_simrank_result_filter.txt"
    simr.simrank_result_filter(relation_sim_node_file % (maxIteration, relation), relation_sim_node_file_filter % (maxIteration, relation), inner)
    print("%s simrank结束..." % relation)


# nmf数据预处理
def nmf_pre(maxIteration, relation):
    print("step 3: 运行nmf")
    print("step 3.1: 生成nmf初始文件")
    nmf_init = bathpath + "/simrank/result/iterator_%d/%s_simrank_result.txt"
    nmf_init_mat = bathpath + "/nmf/init/%s_simrank_init_mat_iterator_%d.mat"
    if not os.path.exists('/'.join((nmf_init_mat % (relation, maxIteration)).split("/" or "\\")[:-1])):
        os.makedirs('/'.join((nmf_init_mat % (relation, maxIteration)).split("/" or "\\")[:-1]))
    nmf.write_file_mat(nmf_init % (maxIteration, relation), nmf_init_mat % (relation, maxIteration))
    print("进入matlab执行")


def simrank_anysis(relation, maxIteration = 10, recommand_num=5):
    print("simrank结果分析：")
    sim_result = bathpath + "/simrank/result/iterator_%d/%s_simrank_result_filter.txt" % (maxIteration, relation)
    sim_result_anysis = bathpath + "/simrank/result/iterator_%d/%s_simrank_result_analysis.txt" % (maxIteration, relation)
    relation_graphFile_after = bathpath + "/simrank/pre/%s_simrank_pre_after_chose.txt" % relation
    user_choose = bathpath + "/simrank/pre/%s_simrank_pre_choose.txt" % relation
    analysis.simrank_analysis(sim_result, sim_result_anysis, relation_graphFile_after, user_choose, recommand_num)


if __name__ == '__main__':
    maxIteration = 3
    relation = "follows"
    # 随机选取的用户数
    choose_user_num = 0
    # 推荐的用户数
    recommand_num = 1000

    # step 0:数据预处理
    # data_pre()

    # step 1: 随机去掉几个用户
    # chose_user(relation, choose_user_num)

    # step 2: simRank
    # # step 2.1: 执行follows simrank
    # simrank(relation, maxIteration)
    # step 2.2: 执行fans simrank
    # simrank(relation, maxIteration)
    # step 3: 运行nmf
    # nmf_pre(maxIteration, relation)

    # step 4: 数据分析
    simrank_anysis(relation, maxIteration, recommand_num)
