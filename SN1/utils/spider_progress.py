#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: spider_progress.py

@time: 2018/3/12 10:43
"""
import pymysql.cursors
from SN1.weiboID import inners


# 查看爬虫进度
def mysql_utils(mysql, para):
    # Connect to the database
    connection = pymysql.connect(host='10.18.57.110',
                                 user='root',
                                 password='root_123a',
                                 db='db_sn2',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = mysql
            if para is not None:
                cursor.execute(sql, para)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


def not_scraw():
    bathpath = "F:\社交网络\微博\论文\实验\实验数据\\resource\\20180309"
    follow_inner_fan = bathpath + "/simrank/pre/follow_inner_fan.txt"
    new_crawl = bathpath + "/new_crawl.txt"
    inners = set()
    follow_inner_fan = open(follow_inner_fan, 'r')
    for line in follow_inner_fan:
        inners.add(line.strip())
    mysql_tweet_uid = "SELECT DISTINCT tweet_uid FROM tweets;"
    tweet_uid_map = mysql_utils(mysql_tweet_uid, None)
    tweet_uid = []
    crawl = []
    for ele in tweet_uid_map:
        tweet_uid.append(ele['tweet_uid'])
    for ele in inners:
        if ele not in tweet_uid:
            crawl.append(ele)
    print(len(inners))
    new_crawl = open(new_crawl, 'w')
    new_crawl.write(str(list(inners)))
    new_crawl.close()
    follow_inner_fan.close()


if __name__ == '__main__':
    # 获取当前爬取的微博的uid
    mysql_tweet_uid = "SELECT DISTINCT tweet_uid FROM tweets;"
    tweet_uid_map = mysql_utils(mysql_tweet_uid, None)
    tweet_uid = []
    for ele in tweet_uid_map:
        tweet_uid.append(ele['tweet_uid'])
    inners = list(inners)
    for ele in tweet_uid:
        for i in range(len(inners)):
            if ele == inners[i]:
                print(i)
                break