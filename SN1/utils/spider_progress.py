#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: spider_progress.py

@time: 2018/3/12 10:43
"""
import pymysql.cursors
import time
import sys


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


# 爬虫的进度
def progress():
    # tweet的爬取进度
    mysql_tweet_uid = "SELECT COUNT(DISTINCT tweet_uid) as crawl_num FROM tweets;"
    tweet_uid_map = mysql_utils(mysql_tweet_uid, None)
    return tweet_uid_map[0]['crawl_num']
    # print("tweet完成进度:%s/425" % (tweet_uid_map[0]['crawl_num']))


def lcr_progress(lcr):
    mysql_tweet_num = "SELECT COUNT(DISTINCT tweet_id_real) AS tweet_num FROM tweets;"
    mysql_tweet_num = mysql_utils(mysql_tweet_num, None)
    lcr_tweet_num = "SELECT COUNT(DISTINCT %s_tweet_id_real) AS crawl_tweet_num FROM %ss;" % (lcr, lcr)
    lcr_tweet_num = mysql_utils(lcr_tweet_num, None)
    return (lcr, lcr_tweet_num[0]['crawl_tweet_num'], mysql_tweet_num[0]['tweet_num'])
    # print("%s完成进度:%s/%s" % (lcr, lcr_tweet_num[0]['crawl_tweet_num'], mysql_tweet_num[0]['tweet_num']))


if __name__ == '__main__':
    tweet_old = 0
    like_old = ('0', '0', '0')
    comment_old = ('0', '0', '0')
    retweet_old = ('0', '0', '0')
    while True:
        tweet = progress()
        like = lcr_progress("like")
        comment = lcr_progress("comment")
        retweet = lcr_progress("retweet")
        tm = time.localtime(time.time())
        now_time = "%s年%s月%s日%s:%s" % (tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min)
        content = "\r%s\ttweet完成进度:%s/425-->%s/425\t" \
                  "%s完成进度:%s/%s-->%s/%s\t%s完成进度:%s/%s-->%s/%s\t" \
                  "%s完成进度:%s/%s-->%s/%s" \
                  % (now_time,
                     tweet_old, tweet,
                     like[0], like_old[1], like_old[2], like[1], like[2],
                     comment[0], comment_old[1], comment_old[2], comment[1], comment[2],
                     retweet[0], retweet_old[1], retweet_old[2], retweet[1], retweet[2])
        tweet_old = tweet
        like_old = like
        comment_old = comment
        retweet_old = retweet
        sys.stdout.write(content)
        sys.stdout.flush()
        time.sleep(5*60)
