# -*- coding: utf-8 -*-
import scrapy
from SN1.weiboID import weiboID
import re
from scrapy.http import Request
from SN1.items import WeiboItemLoader, UsersItem, FollowsItem
from urllib import parse
import time


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['weibo.cn']
    redis_key = "sinaLogin:start_urls"
    start_urls = list(weiboID)

    def start_requests(self):
        for uid in self.start_urls:
            # 用户微博
            yield Request(url="https://weibo.cn/%s/follow" % uid, callback=self.parse_follow, meta={'uid': uid})

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

    # 关注
    def parse_follow(self, response):
        """
        1. 解析follow页面，获取uid，发起获取info请求
        2. 请求下一页关注列表
        3. 请求fans页面首页
        """
        uid = response.meta["uid"]
        for rep in response.xpath("//table"):
            # todo 这段代码硬编码，得改
            follow_uid_ = rep.xpath(".//td[.//a[contains(@href,'attention')]]//a[1]/@href").extract_first()
            if follow_uid_ is not None:
                follow_uid = follow_uid_.split("/")[-1]
                item_loader = WeiboItemLoader(item=FollowsItem(), response=response)
                item_loader.add_value("follow_from_id", uid)
                item_loader.add_value("follow_to_id", follow_uid)
                # todo 时间类型的编码格式可以修改成可配置
                item_loader.add_value("follow_time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                weibo_follow_item = item_loader.load_item()
                yield weibo_follow_item
                if re.match(r"^[0-9]*$", uid) is not None:
                    weibo_item_loader = WeiboItemLoader(item=UsersItem(), response=response)
                    weibo_item_loader.add_value("user_uid", uid)
                    weibo_item_loader.add_value("char_uid", "0")
                    weibo_item = weibo_item_loader.load_item()
                    yield weibo_item
                else:
                    yield Request(url="https://weibo.cn/%s" % uid, callback=self.parse_charuid,
                                  meta={'uid': uid})
                if re.match(r"^[0-9]*$", follow_uid) is not None:
                    weibo_item_loader = WeiboItemLoader(item=UsersItem(), response=response)
                    weibo_item_loader.add_value("user_uid", follow_uid)
                    weibo_item_loader.add_value("char_uid", "0")
                    weibo_item = weibo_item_loader.load_item()
                    yield weibo_item
                else:
                    yield Request(url="https://weibo.cn/%s" % follow_uid, callback=self.parse_charuid,
                                  meta={'uid': follow_uid})
        # 只有在有下一页的情况下才要去处理下一页
        page_num_ = response.css("#pagelist").extract_first()
        if page_num_ is not None:
            page_num = re.findall('(\d+)/(\d+)', page_num_)
            if page_num[0][0] < page_num[0][1]:
                url = response.css("#pagelist a::attr(href)").extract_first()
                yield Request(url=parse.urljoin(response.url, url), callback=self.parse_follow, meta={'uid': uid})
        yield Request(url="https://weibo.cn/%s/fans" % uid, callback=self.parse_fans, meta={'uid': uid})

    # 粉丝
    def parse_fans(self, response):
        """
        1. 解析fans页面，获取uid，发起获取info请求
        2. 请求下一页fans页面
        3. 请求tags标签页面
        """
        uid = response.meta["uid"]
        for rep in response.xpath("//table"):
            # todo 为空的判断
            fan_ = rep.xpath(".//td[.//a[contains(@href,'attention')]]//a[1]/@href").extract_first()
            if fan_ is not None:
                fans_uid = fan_.split("/")[-1]
                item_loader = WeiboItemLoader(item=FollowsItem(), response=response)
                item_loader.add_value("follow_to_id", uid)
                item_loader.add_value("follow_from_id", fans_uid)
                # todo 时间类型的编码格式可以修改成可配置
                item_loader.add_value("follow_time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                weibo_follow_item = item_loader.load_item()
                yield weibo_follow_item
                if re.match(r"^[0-9]*$", uid) is not None:
                    weibo_item_loader = WeiboItemLoader(item=UsersItem(), response=response)
                    weibo_item_loader.add_value("user_uid", uid)
                    weibo_item_loader.add_value("char_uid", "0")
                    weibo_item = weibo_item_loader.load_item()
                    yield weibo_item
                else:
                    yield Request(url="https://weibo.cn/%s" % uid, callback=self.parse_charuid,
                                  meta={'uid': uid})
                if re.match(r"^[0-9]*$", fans_uid) is not None:
                    weibo_item_loader = WeiboItemLoader(item=UsersItem(), response=response)
                    weibo_item_loader.add_value("user_uid", fans_uid)
                    weibo_item_loader.add_value("char_uid", "0")
                    weibo_item = weibo_item_loader.load_item()
                    yield weibo_item
                else:
                    yield Request(url="https://weibo.cn/%s" % fans_uid, callback=self.parse_charuid,
                                  meta={'uid': fans_uid})
        page_num_ = response.css("#pagelist").extract_first()
        if page_num_ is not None:
            page_num = re.findall('(\d+)/(\d+)', page_num_)
            # 只有在有下一页的情况下才要去处理下一页
            if page_num[0][0] < page_num[0][1]:
                url = response.css("#pagelist a::attr(href)").extract_first()
                yield Request(url=parse.urljoin(response.url, url), callback=self.parse_fans, meta={'uid': uid})