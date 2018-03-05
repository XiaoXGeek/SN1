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
def follow(users, follows, follows_new):
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


if __name__ == '__main__':
    users = "../resource/20180305/init/users.txt"
    follows = "../resource/20180305/init/follows.txt"
    follows_new = "../resource/20180305/users.txt"
    follow(users, follows, follows_new)