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


def user_tweet(users_all, follows_all, users_all_new):
    users_all = open(users_all, 'r')
    follows_all = open(follows_all, 'r')
    users_all_new = open(users_all_new, 'w')
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
    for ele in other:
        print(ele+"\n")
    users_all.close()
    follows_all.close()
    users_all_new.close()


if __name__ == '__main__':
    users = "../resource/20180305/init/users.txt"
    follows = "../resource/20180305/init/follows.txt"
    users_init_new = "../resource/20180305/users_init.txt"
    users_all = "../resource/20180305/all/users.txt"
    follows_all = "../resource/20180305/all/follows.txt"
    users_all_new = "../resource/20180305/users_all.txt"
    # user_init(users, follows, users_init_new)
    user_tweet(users_all, follows_all, users_all_new)