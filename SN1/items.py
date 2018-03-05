# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class WeiboItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class UsersItem(scrapy.Item):
    # 微博的item
    user_uid = scrapy.Field()   # 微博中uid
    char_uid = scrapy.Field()

    def get_insert_sql(self):
        # 插入weibouser表的sql语句，在uid存在时更新表
        insert_sql = "insert ignore into users(user_uid, char_uid) VALUES(%s, %s)"
        params = (
            self["user_uid"], self["char_uid"]
        )
        return insert_sql, params


class FollowsItem(scrapy.Item):
    follow_from_id = scrapy.Field()
    follow_to_id = scrapy.Field()
    follow_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入weibouser表的sql语句，在uer_id重复时不插入
        insert_sql = "insert ignore into follows(follow_from_id, follow_to_id, follow_time) VALUES (%s, %s, %s)"
        params = (
            self["follow_from_id"], self["follow_to_id"], self["follow_time"]
        )
        return insert_sql, params


class TweetsItem(scrapy.Item):
    tweet_id_real = scrapy.Field()
    tweet_uid = scrapy.Field()
    tweet_like_real = scrapy.Field()
    tweet_comment_real = scrapy.Field()
    tweet_rt_real = scrapy.Field()
    tweet_is_rt = scrapy.Field()

    def get_insert_sql(self):
        # 插入weibouser表的sql语句，在uer_id重复时不插入
        insert_sql = "insert ignore into tweets(" \
                     "tweet_id_real, tweet_uid, tweet_like_real, tweet_comment_real, " \
                     "tweet_rt_real, tweet_is_rt)" \
                     " VALUES (%s, %s, %s, %s, %s, %s)"
        params = (
            self["tweet_id_real"], self["tweet_uid"], self["tweet_like_real"], self["tweet_comment_real"],
            self["tweet_rt_real"], self["tweet_is_rt"]
        )
        return insert_sql, params


class LikesItem(scrapy.Item):
    like_tweet_id_real = scrapy.Field()
    like_uid = scrapy.Field()
    like_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入weibouser表的sql语句，在uer_id重复时不插入
        insert_sql = "insert ignore into likes(" \
                     "like_tweet_id_real, like_uid, like_time" \
                     ")VALUES (%s, %s, %s)"
        params = (
            self["like_tweet_id_real"], self["like_uid"], self["like_time"]
        )
        return insert_sql, params


class CommentsItem(scrapy.Item):
    comment_tweet_id_real = scrapy.Field()
    comment_uid = scrapy.Field()

    def get_insert_sql(self):
        # 插入weibouser表的sql语句，在uer_id重复时不插入
        insert_sql = "insert ignore into comments(comment_tweet_id_real, comment_uid)VALUES (%s, %s)"
        params = (
            self["comment_tweet_id_real"], self["comment_uid"]
        )
        return insert_sql, params


class RetweetsItem(scrapy.Item):
    retweet_tweet_id_real = scrapy.Field()
    retweet_uid = scrapy.Field()

    def get_insert_sql(self):
        # 插入weibouser表的sql语句，在uer_id重复时不插入
        insert_sql = "insert ignore into retweets(retweet_tweet_id_real, retweet_uid)VALUES (%s, %s)"
        params = (
            self["retweet_tweet_id_real"], self["retweet_uid"]
        )
        return insert_sql, params


