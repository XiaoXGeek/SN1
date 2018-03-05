#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: RandomUID.py

@time: 2018/1/10 13:50
"""
import pymysql.cursors
import random

# file = open("F:\\数据\\weibodata\\解压后\\uidlist.txt")
# lines = []
# while 1:
#     line = file.readline()
#     if not line:
#         break
#     lines.append(int(line))
# print(len(lines))
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'db_sina',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}
# Connect to the database
connection = pymysql.connect(**config)
weiboId = []
with connection.cursor() as cursor:
    # 执行sql语句，插入记录
    sql = 'select user_uid from users'
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        weiboId.append(result[i]['user_uid'])
# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
connection.commit()
fo = open("D:\\code\\idea_python\\SinaLogin\\SinaLogin\\weiboId.txt", "w")
fo.write(str(weiboId))
# 关闭打开的文件
fo.close()
connection.close()

