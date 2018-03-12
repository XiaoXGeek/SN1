#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: users.py

@time: 2018/3/5 14:26
"""
import re


# 解析爬取列表，供follows和tweets使用
def user_init(users, follows, follows_new):
    users_id = ['1891502860', '1288739185', '1772191555', '1898495494', '2406523251', '5584871802', '5972903864','3191340984', '5087591810', '3195810885']
    users = open(users, 'r')
    follows = open(follows, 'r')
    follows_new = open(follows_new, 'w')
    user_map = {}
    user = set()
    for line in users:
        arr = line.strip().split(",")
        user_map[arr[1]] = arr[0]
    for line in follows:
        arr = line.strip().split(",")
        if re.match(r"^[0-9]*$", arr[0]) is None:
            user.add(user_map[arr[0]])
        else:
            user.add(arr[0])
        if re.match(r"^[0-9]*$", arr[1]) is None:
            user.add(user_map[arr[1]])
        else:
            user.add(arr[1])
    users_id = set(users_id)
    print("原长度：%d现长度%d\n" % (len(user), len(user-users_id)))
    user = list(user - users_id)
    follows_new.write(str(user))
    users.close()
    follows.close()
    follows_new.close()


# 提取出所有的用户，供爬取用户的微博及交互数据使用，同时为用户进行编号
def user_tweet(users_all, follows_all, users_all_new, users_id):
    users_all = open(users_all, 'r')
    follows_all = open(follows_all, 'r')
    users_all_new = open(users_all_new, 'w')
    users_id = open(users_id, 'w')
    user_map = {}
    user_1 = set()
    user_2 = set()
    for line in users_all:
        arr = line.strip().split(",")
        user_map[arr[2]] = arr[1]
    num = 0
    other = []
    for line in follows_all:
        arr = line.strip().split(",")
        if re.match(r"^[0-9]*$", arr[1]) is None:
            if arr[1] in user_map.keys():
                user_1.add(user_map[arr[1]])
            else:
                num = num + 1
                other.append(arr[1])
        else:
            user_2.add(arr[1])
        if re.match(r"^[0-9]*$", arr[2]) is None:
            if arr[2] in user_map.keys():
                user_1.add(user_map[arr[2]])
            else:
                num = num + 1
                other.append(arr[2])
        else:
            user_2.add(arr[2])
    print("%d" % num)
    print("总用户数：%d\nfollow中字符id用户数：%d\nfollow中数字id用户数：%d\nusers中用户数:%d\n" % (len(user_1.union(user_2)), len(user_1),len(user_2),len(user_map)))
    user = list(user_1.union(user_2))
    users_all_new.write(str(user))
    # for ele in other:
    #     print(ele+"\n")
    i = 0
    for ele in user:
        i = i + 1
        users_id.write("%d,%s\n" % (i, ele))
    users_all.close()
    follows_all.close()
    users_all_new.close()
    users_id.close()


# 替换字符用户
def replace_by_user(users_all, follows_all, follows_new):
    users_all = open(users_all, 'r')
    follows_all = open(follows_all, 'r')
    follows_new = open(follows_new, 'w')
    user_map = {}
    for line in users_all:
        arr = line.strip().split(",")
        user_map[arr[2]] = arr[1]
    i = 0
    for line in follows_all:
        arr = line.strip().split(",")
        follow_from = None
        follow_to = None
        if re.match(r"^[0-9]*$", arr[1]) is None:
            if arr[1] in user_map.keys():
                follow_from = user_map[arr[1]]
        else:
            follow_from = arr[1]
        if re.match(r"^[0-9]*$", arr[2]) is None:
            if arr[2] in user_map.keys():
                follow_to = user_map[arr[2]]
        else:
            follow_to = arr[2]
        if follow_from is not None and follow_to is not None:
            i = i + 1
            follows_new.write("%d,%s,%s\n" % (i, follow_from, follow_to))
    users_all.close()
    follows_all.close()
    follows_new.close()


# 用户微博id替换成用户id
def replace_by_id(users_id, follows, follows_new):
    users_id = open(users_id, 'r')
    follows = open(follows, 'r')
    follows_new = open(follows_new, 'w')
    user_map = {}
    for line in users_id:
        arr = line.strip().split(',')
        user_map[arr[1]] = arr[0]
    for line in follows:
        arr = line.strip().split(',')
        follows_new.write("%s,%s,%s\n" % (arr[0], user_map[arr[1]], user_map[arr[2]]))
    users_id.close()
    follows.close()
    follows_new.close()


# 将关注数据综合到一起
def follow(follows, follows_new, filter_num=10):
    follows = open(follows, 'r')
    follows_new = open(follows_new, 'w')
    link_out = {}
    for line in follows:
        arr = line.strip().split(',')
        neighbor = set()
        if arr[1] in link_out.keys():
            neighbor = link_out[arr[1]]
        neighbor.add(arr[2])
        link_out[arr[1]] = neighbor
    i = 0
    for ele in link_out.keys():
        if len(link_out[ele]) >= filter_num:
            i = i + 1
            line = ''
            for ngb in link_out[ele]:
                line = line + ',' + ngb
            follows_new.write("%d,%s,%d%s\n" % (i, ele, len(link_out[ele]), line))
    follows.close()
    follows_new.close()


# 将用户的粉丝数据综合到一起
def fan(fans, fans_new, filter_num=10):
    fans = open(fans, 'r')
    fans_new = open(fans_new, 'w')
    link_in = {}
    for line in fans:
        arr = line.strip().split(',')
        neighbor = set()
        if arr[2] in link_in.keys():
            neighbor = link_in[arr[2]]
        neighbor.add(arr[1])
        link_in[arr[2]] = neighbor
    i = 0
    for ele in link_in.keys():
        if len(link_in[ele]) >= filter_num:
            i = i + 1
            line = ''
            for ngb in link_in[ele]:
                line = line + ',' + ngb
            fans_new.write("%d,%s,%d%s\n" % (i, ele, len(link_in[ele]), line))
    fans.close()
    fans_new.close()


# 将follows, fans数据处理成simRank可以处理的数据
def simrank_link(follows, user_matrix_follow):
    follows = open(follows, 'r')
    user_matrix = open(user_matrix_follow, 'w')
    user = set()
    other = set()
    for line in follows:
        arr = line.strip().split(',')
        user.add(arr[1])
        user_matrix.write("%s\t%s\n" % (arr[1], '\t'.join(arr[3:])))
        for i in range(3, int(arr[2])+3):
            other.add(arr[i])
    for ele in other-user:
        user_matrix.write(ele + "\t\n")
    follows.close()
    user_matrix.close()


# 对fans和follows取交集
def follows_inner_fans(follows, fans, follows_in_fans, follow_length=10, fan_length=10):
    follows = open(follows, 'r')
    fans = open(fans, 'r')
    follows_in_fans = open(follows_in_fans, 'w')
    follow = {}
    fan = {}
    for line in follows:
        arr = line.strip().split()
        if len(arr) > follow_length:
            follow[arr[0]] = line
    for line in fans:
        arr = line.strip().split()
        if len(arr) > fan_length:
            fan[arr[0]] = line
    inner = set(follow.keys()).intersection(set(fan.keys()))
    for key in inner:
        follows_in_fans.write("%s\n" % key)
    follows.close()
    fans.close()
    follows_in_fans.close()


# 对fans和follows数据进行初步过滤
def pass_follow_fan(follows, follows_new, fans, fans_new, inter):
    follows = open(follows, 'r')
    follows_new = open(follows_new, 'w')
    fans = open(fans, 'r')
    fans_new = open(fans_new, 'w')
    inter = open(inter, 'w')
    follow_length = 10
    fan_length = 10
    follow = {}
    fan = {}
    for line in follows:
        arr = line.strip().split()
        if len(arr) >= follow_length:
            follow[arr[0]] = line
    for line in fans:
        arr = line.strip().split()
        if len(arr) >= fan_length:
            fan[arr[0]] = line
    inner = set(follow.keys()).intersection(set(fan.keys()))
    print("交集共有%d" % len(inner))
    for key in inner:
        inter.write("%s\n" % key)
        follows_new.write("%s" % follow[key])
        fans_new.write("%s" % fan[key])
    follows.close()
    follows_new.close()
    fans.close()
    fans_new.close()
    inter.close()


# 选择要预测用户
def chose_user(relations, relation_new, inner, user_choose, num):
    relations = open(relations, 'r')
    relation_new = open(relation_new, 'w')
    inner = open(inner, 'r')
    user_choose = open(user_choose, 'w')
    inners = []
    for line in inner:
        inners.append(line.strip())
    for line in relations:
        arr = line.strip().split()
        if arr[0] in inners:
            user_choose_line = arr[0]
            left_line = arr[0]
            for i in range(1, len(arr)):
                if i <= num:
                    user_choose_line = user_choose_line + '\t' + arr[i]
                else:
                    left_line = left_line + '\t' + arr[i]
            relation_new.write(left_line + '\n')
            user_choose.write(user_choose_line + '\n')
    user_choose.close()
    inner.close()
    relation_new.close()
    relations.close()


if __name__ == '__main__':
    users = "../resource/20180305/init/users.txt"
    follows = "../resource/20180305/init/follows.txt"
    users_init_new = "../resource/20180305/users_init.txt"
    users_all = "../resource/20180305/all/users.txt"
    follows_all = "../resource/20180305/all/follows.txt"
    users_all_new = "../resource/20180305/users_all.txt"
    users_id = "../resource/20180305/follow/users_id.txt"
    # user_init(users, follows, users_init_new)
    # user_tweet(users_all, follows_all, users_all_new, users_id)
    # 替换字符用户
    follows_rp_user = "../resource/20180305/follow/follow_replace_by_user/follows.txt"
    # replace_by_user(users_all, follows_all, follows_rp_user)
    # 用户微博id替换成用户id
    follows_rp_id = "../resource/20180305/follow/follow_replace_by_id/follows.txt"
    # replace_by_id(users_id, follows_rp_user, follows_rp_id)
    follows_neighbor = "../resource/20180305/follow/follows_neighbor.txt"
    # 将关注数据综合到一起
    # follow(follows_rp_id, follows_neighbor)
    fans_neighbor = "../resource/20180305/follow/fans_neighbor.txt"
    # 将用户的粉丝数据综合到一起
    # fan(follows_rp_id, fans_neighbor)
    follow_link = "../resource/20180305/follow/link_begin/follow_link.txt"
    # simrank_link(follows_neighbor, follow_link)
    fans_link = "../resource/20180305/follow/link_begin/fan_link.txt"
    # simrank_link(fans_neighbor, fans_link)
    follow_link_new = "../resource/20180305/follow/link_after/follow_link.txt"
    fans_link_new = "../resource/20180305/follow/link_after/fan_link.txt"
    inner = "../resource/20180305/follow/link_after/inner.txt"
    # 筛选关注和粉丝数据(按照关注和粉丝数量)
    pass_follow_fan(follow_link, follow_link_new, fans_link, fans_link_new, inner)