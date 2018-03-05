# -*- coding: utf-8 -*-
import scrapy
from SN1.weiboID import weiboID
import re
from scrapy.http import Request
from SN1.items import WeiboItemLoader, UsersItem, TweetsItem, LikesItem, RetweetsItem, CommentsItem
from urllib import parse


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['weibo.cn']
    redis_key = "sinaLogin:start_urls"
    start_urls = list(weiboID)

    def start_requests(self):
        for uid in self.start_urls:
            # 用户微博
            yield Request(url="https://weibo.cn/u/%s" % uid, callback=self.parse_tweets, meta={'uid': uid})

    # 处理非字母uid
    def parse_charuid(self, response):
        char_uid = response.meta["uid"]
        uid_ = response.xpath("//div[@class='ut']/a[contains(@href,'info')]/@href").extract_first()
        if uid_ is not None:
            uid = uid_.split("/")[-2]
            if uid is not None:
                item_loader = WeiboItemLoader(item=UsersItem(), response=response)
                item_loader.add_value("user_uid", uid)
                item_loader.add_value("char_uid", char_uid)
                weibo_item = item_loader.load_item()
                yield weibo_item

    # 微博
    def parse_tweets(self, response):
        uid = response.meta["uid"]
        """
        1. 解析微博页面，获取全部微博
        2. 将微博存入数据库
        """
        for div in response.xpath("//div[@id and not(contains(@id,'pagelist'))]"):
            item_loader = WeiboItemLoader(item=TweetsItem(), response=response)
            tweet_id_real = "无"
            tweet_like_real = 0
            tweet_comment_real = 0
            tweet_id_real_ = div.xpath("string(.//@id)").extract_first()[2:]
            if tweet_id_real_ is not None:
                tweet_id_real = tweet_id_real_
            tweet_like_real_ = div.xpath("string(.//a[contains(@href,'attitude')])").extract_first()
            if tweet_like_real_ is not None:
                tweet_like_real = re.findall("\d+", tweet_like_real_)
            tweet_comment_real_ = div.xpath("string(./div[last()]/a[contains(@href,'comment')])").extract_first()
            if tweet_comment_real_ is not None:
                tweet_comment_real = re.findall("\d+", tweet_comment_real_)
            tweet_rt_real_ = div.xpath("string(.//a[contains(@href,'repost')])").extract_first()
            if tweet_rt_real_ is not None:
                tweet_rt_real = re.findall("\d+", tweet_rt_real_)
            item_loader.add_value("tweet_uid", uid)
            item_loader.add_value("tweet_id_real", tweet_id_real)
            item_loader.add_value("tweet_like_real", tweet_like_real)
            item_loader.add_value("tweet_comment_real", tweet_comment_real)
            item_loader.add_value("tweet_rt_real", tweet_rt_real)
            # 微博是否为转发微博，1是转发，0表示未转发
            tweet_is_rt = 0
            if len(div.xpath(".//span[@class='cmt']//a[contains(@href,'https://weibo.cn/')]").extract()) != 0:
                tweet_is_rt = 1
            item_loader.add_value("tweet_is_rt", tweet_is_rt)
            weibo_item = item_loader.load_item()
            yield weibo_item
            # 微博的点赞
            yield Request(url="https://weibo.cn/attitude/%s?#attitude" % tweet_id_real, callback=self.parse_likes,
                          meta={'tweet_id_real': tweet_id_real})
            # 微博的评论
            yield Request(url="https://weibo.cn/comment/%s?#cmtfrm" % tweet_id_real, callback=self.parse_comments,
                          meta={'tweet_id_real': tweet_id_real})
            # 微博的转发
            yield Request(url="https://weibo.cn/repost/%s?#rt" % tweet_id_real, callback=self.parse_retweets,
                          meta={'tweet_id_real': tweet_id_real})
        # 转发的微博提取出来，放入请求队列
        for rep in response.xpath("//span[@class='cmt']//a[contains(@href,'https://weibo.cn/')]"):
            rt_uid = rep.xpath("./@href").extract_first().split("/")[-1]
            if re.match(r"^[0-9]*$", rt_uid) is not None:
                yield Request(url="https://weibo.cn/%s/info" % rt_uid, callback=self.parse_info, meta={'uid': rt_uid})
            else:
                yield Request(url="https://weibo.cn/%s" % rt_uid, callback=self.parse_charuid, meta={'uid': rt_uid})
        page_num_ = response.css("#pagelist").extract_first()
        if page_num_ is not None:
            page_num = re.findall('(\d+)/(\d+)', page_num_)
            # 只有在有下一页的情况下才要去处理下一页
            if page_num[0][0] <= page_num[0][1]:
                url = response.css("#pagelist a::attr(href)").extract_first()
                yield Request(url=parse.urljoin(response.url, url), callback=self.parse_tweets, meta={'uid': uid})

    # 点赞
    def parse_likes(self, response):
        tweet_id_real = response.meta["tweet_id_real"]
        for rep in response.xpath("//div[@class='c' and ./span[contains(@class,'ct')]]"):
            like_uid = "无"
            like_time = "无"
            like_tweet_id_real = "无"
            like_uid_ = rep.xpath("./a/@href").extract_first()
            if like_uid_ is not None:
                like_uid = like_uid_.split("/")[-1]
            like_time_ = rep.xpath("./span/text()").extract_first()
            if like_time_ is not None:
                like_time = like_time_
            if tweet_id_real is not None:
                like_tweet_id_real = tweet_id_real
            item_loader = WeiboItemLoader(item=LikesItem(), response=response)
            item_loader.add_value("like_uid", like_uid)
            item_loader.add_value("like_time", like_time)
            item_loader.add_value("like_tweet_id_real", like_tweet_id_real)
            weibo_item = item_loader.load_item()
            yield weibo_item
            if re.match(r"^[0-9]*$", like_uid) is None:
                yield Request(url="https://weibo.cn/%s" % like_uid, callback=self.parse_charuid,
                              meta={'uid': like_uid})

        page_num_ = response.css("#pagelist").extract_first()
        if page_num_ is not None:
            page_num = re.findall('(\d+)/(\d+)', page_num_)
            # 只有在有下一页的情况下才要去处理下一页
            if page_num[0][0] <= page_num[0][1]:
                url = response.css("#pagelist a::attr(href)").extract_first()
                yield Request(url=parse.urljoin(response.url, url), callback=self.parse_likes,
                              meta={'tweet_id_real': tweet_id_real})

    # 评论
    def parse_comments(self, response):
        tweet_id_real = response.meta["tweet_id_real"]
        for rep in response.xpath("//div[contains(@id,'C_')]"):
            item_loader = WeiboItemLoader(item=CommentsItem(), response=response)
            comment_tweet_id_real = "无"
            comment_uid = "无"
            if tweet_id_real is not None:
                comment_tweet_id_real = tweet_id_real
            comment_uid_ = rep.xpath("./a/@href").extract_first()
            if comment_uid_ is not None:
                comment_uid = comment_uid_.split("/")[-1]
            item_loader.add_value("comment_tweet_id_real", comment_tweet_id_real)
            item_loader.add_value("comment_uid", comment_uid)
            weibo_item = item_loader.load_item()
            yield weibo_item
            if re.match(r"^[0-9]*$", comment_uid) is None:
                yield Request(url="https://weibo.cn/%s" % comment_uid, callback=self.parse_charuid,
                              meta={'uid': comment_uid})
        page_num_ = response.css("#pagelist").extract_first()
        if page_num_ is not None:
            page_num = re.findall('(\d+)/(\d+)', page_num_)
            # 只有在有下一页的情况下才要去处理下一页
            if page_num[0][0] <= page_num[0][1]:
                url = response.css("#pagelist a::attr(href)").extract_first()
                if url is not None:
                    yield Request(url=parse.urljoin(response.url, url), callback=self.parse_comments,
                                  meta={'tweet_id_real': tweet_id_real})

    # 转发
    def parse_retweets(self, response):
        tweet_id_real = response.meta["tweet_id_real"]
        for rep in response.xpath("//div[@class='c' and .//span[@class='cc']]"):
            item_loader = WeiboItemLoader(item=RetweetsItem(), response=response)
            retweet_tweet_id_real = "无"
            retweet_uid = "无"
            if tweet_id_real is not None:
                retweet_tweet_id_real = tweet_id_real
            retweet_uid_ = rep.xpath("./a[1]/@href").extract_first()
            if retweet_uid_ is not None:
                retweet_uid = retweet_uid_.split("/")[-1]
            item_loader.add_value("retweet_tweet_id_real", retweet_tweet_id_real)
            item_loader.add_value("retweet_uid", retweet_uid)
            weibo_item = item_loader.load_item()
            yield weibo_item
            if re.match(r"^[0-9]*$", retweet_uid) is None:
                yield Request(url="https://weibo.cn/%s" % retweet_uid, callback=self.parse_charuid,
                              meta={'uid': retweet_uid})
        page_num_ = response.css("#pagelist").extract_first()
        if page_num_ is not None:
            page_num = re.findall('(\d+)/(\d+)', page_num_)
            # 只有在有下一页的情况下才要去处理下一页
            if page_num[0][0] <= page_num[0][1]:
                url = response.css("#pagelist a::attr(href)").extract_first()
                if url is not None:
                    yield Request(url=parse.urljoin(response.url, url), callback=self.parse_retweets,
                                  meta={'tweet_id_real': tweet_id_real})