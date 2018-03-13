#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: exp001.py

@time: 2018/3/9 9:35
"""
import os
import SN1.exp.simrank.square_cache_simrank_py3 as simr
import SN1.exp.nmf.data_pre as nmf
import SN1.exp.users as user
import SN1.exp.analysis as analysis
from SN1.utils.utils import myutils


bathpath = "F:\社交网络\微博\论文\实验\实验数据\\resource\\20180309"
# bathpath="/home/xiaox/data/weibo/20180313/"


# 数据预处理
def data_pre():
    print("step 1: 预处理开始...")
    # 0.1: 替换字符用户，生成新的follows
    users_init = bathpath + "/init/users_init.txt"
    relation_init = bathpath + "/init/relation_init.txt"
    relation_rp_char = bathpath + "/data_pre/relation_rp_char.txt"
    myutils.mkdirs_by_file(users_init)
    myutils.mkdirs_by_file(relation_init)
    myutils.mkdirs_by_file(relation_rp_char)
    print("1.1 替换字符用户...")
    user.replace_by_user(users_init, relation_init, relation_rp_char)
    # 0.2: 生成fans和follows的详细的关注列表
    follows_detail = bathpath + "/data_pre/follows_detail.txt"
    fans_detail = bathpath + "/data_pre/fans_detail.txt"
    myutils.mkdirs_by_file(follows_detail)
    myutils.mkdirs_by_file(fans_detail)
    follow_filter_num = 0
    fan_filter_num = 10
    print("1.2.1 生成follow的详细信息...")
    user.follow(relation_rp_char, follows_detail, follow_filter_num)
    print("1.2.2 生成fan的详细信息...")
    user.fan(relation_rp_char, fans_detail, fan_filter_num)
    # 0.3: 生成fan和follows的simrank预处理数据
    follows_simrank_pre = bathpath + "/simrank/pre/follows_simrank_pre.txt"
    fans_simrank_pre = bathpath + "/simrank/pre/fans_simrank_pre.txt"
    myutils.mkdirs_by_file(follows_simrank_pre)
    myutils.mkdirs_by_file(fans_simrank_pre)
    print("1.3.1 将follow处理成simrank可处理格式...")
    user.simrank_link(follows_detail, follows_simrank_pre)
    print("1.3.2 将fan处理成simrank可处理格式...")
    user.simrank_link(fans_detail, fans_simrank_pre)
    # 0.4: follow和fan的交集
    follow_inner_fan = bathpath + "/simrank/pre/follow_inner_fan.txt"
    follows_simrank_pre_all = bathpath + "/simrank/pre/follows_simrank_pre_all.txt"
    myutils.mkdirs_by_file(follow_inner_fan)
    myutils.mkdirs_by_file(follows_simrank_pre_all)
    user.simrank_link2(follows_simrank_pre, follows_simrank_pre_all, follow_inner_fan)
    print("1.4 生成follow和fan的交集...")
    # user.follows_inner_fans(follows_simrank_pre, fans_simrank_pre, follow_inner_fan)
    print("数据预处理完成")


# 随机选择要去除的用户
def chose_user(relation, choose_rate=0.2):
    print("选择用户开始...")
    inner = bathpath + "/simrank/pre/follow_inner_fan.txt"
    relation_graphFile_before = bathpath + "/simrank/pre/%s_simrank_pre_all.txt" % relation
    simrank_choose_left = bathpath + "/simrank/pre/%s_simrank_choose_left.txt" % relation
    simrank_choose = bathpath + "/simrank/pre/%s_simrank_choose.txt" % relation
    myutils.mkdirs_by_file(inner)
    myutils.mkdirs_by_file(relation_graphFile_before)
    myutils.mkdirs_by_file(simrank_choose_left)
    choose_num = 5
    # user.choose_user(relation_graphFile_before, simrank_choose_left, inner, simrank_choose, choose_num)
    user.chose_user_random(relation_graphFile_before, simrank_choose_left, inner, simrank_choose, choose_rate)
    print("选择用户结束...")


def simrank(relation, maxIteration = 10):
    print("step 2: simrank开始...")
    # 2.1 执行simrank
    print("2.1 执行%s simrank" % relation)
    relation_graphFile = bathpath + "/simrank/pre/%s_simrank_choose_left.txt" % relation
    relation_sim_node_file = bathpath + "/simrank/result/iterator_%d/%s_simrank_result.txt"
    if not os.path.exists('/'.join((relation_sim_node_file % (maxIteration, relation)).split("/" or "\\")[:-1])):
        os.makedirs('/'.join((relation_sim_node_file % (maxIteration, relation)).split("/" or "\\")[:-1]))
    simr.simrank(relation_graphFile, maxIteration)
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
    # sim_result = bathpath + "/simrank/result/iterator_%d/%s_simrank_result_filter.txt" % (maxIteration, relation)
    # sim_result_anysis = bathpath + "/simrank/result/iterator_%d/%s_simrank_result_analysis.txt" % (maxIteration, relation)
    # relation_graphFile_after = bathpath + "/simrank/pre/%s_simrank_pre_after_chose.txt" % relation
    # user_choose = bathpath + "/simrank/pre/%s_simrank_pre_choose.txt" % relation
    # myutils.mkdirs_by_file(sim_result)
    # myutils.mkdirs_by_file(sim_result_anysis)
    # myutils.mkdirs_by_file(relation_graphFile_after)
    # myutils.mkdirs_by_file(user_choose)
    # analysis.simrank_analysis(sim_result, sim_result_anysis, relation_graphFile_after, user_choose, recommand_num)

    print("phase 1:")
    sim_result_all = bathpath + "/simrank/result/iterator_%d/%s_simrank_result.txt" % (maxIteration, relation)
    follow_inner_fan = bathpath + "/simrank/pre/follow_inner_fan.txt"
    simrank_result_analysis_phase_1 = bathpath + "/simrank/result/iterator_%d/%s_simrank_result_analysis_phase_1.txt" % (maxIteration, relation)
    # analysis.simrank_analysis_phase_1(sim_result_all, simrank_result_analysis_phase_1, follow_inner_fan)
    print("phase 2:")
    simrank_result_analysis_phase_2 = bathpath + "/simrank/result/iterator_%d/%s_simrank_result_analysis_phase_2.txt" % (maxIteration, relation)
    # analysis.simrank_analysis_phase_2(simrank_result_analysis_phase_1, follow_inner_fan, simrank_result_analysis_phase_2, lambda_=1)

    print("phase 3:")
    simrank_result_analysis_phase_3 = bathpath + "/simrank/result/iterator_%d/%s_simrank_result_analysis_phase_3.txt" % (maxIteration, relation)
    # analysis.simrank_analysis_phase_3(simrank_result_analysis_phase_2, follow_inner_fan, simrank_result_analysis_phase_3)

    print("phase 4:")
    simrank_result_analysis_phase_4 = bathpath + "/simrank/result/iterator_%d/%s_simrank_result_analysis_phase_4.txt" % (maxIteration, relation)
    user_choose_left = bathpath + "/simrank/pre/%s_simrank_choose_left.txt" % relation
    user_choose = bathpath + "/simrank/pre/%s_simrank_choose.txt" % relation
    analysis.simrank_analysis_phase_4(simrank_result_analysis_phase_3, simrank_result_analysis_phase_4, user_choose_left, user_choose, recommand_num)


if __name__ == '__main__':
    maxIteration = 3
    relation = "follows"
    # 随机选取的用户数
    choose_rate = 0.2
    # 推荐的用户数
    recommand_num = 10000
    # # step 0:数据预处理
    data_pre()
    # step 1: 随机去掉几个用户
    chose_user(relation, choose_rate)

    # step 2: simRank
    # # step 2.1: 执行follows simrank
    simrank(relation, maxIteration)
    # step 2.2: 执行fans simrank
    simrank(relation, maxIteration)
    # step 3: 运行nmf
    nmf_pre(maxIteration, relation)

    # step 4: 数据分析
    simrank_anysis(relation, maxIteration, recommand_num)

