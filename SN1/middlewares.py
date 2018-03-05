# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from SN1.cookies import init_cookie, update_cookie, remove_cookie
from fake_useragent import UserAgent
import redis
import json
import os
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.response import response_status_message
import re
import logging


class Sn1SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 添加了一个RetryMiddleware，并不知道这是什么鬼
class CookieMiddleware(object):
    # 随机更换cookie
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        # 设置cookie的redis连接
        self.rconn = settings.get("RCONN", redis.Redis(settings.get('COOKIE_REDIS_HOST', 'localhsot'),
                                                       settings.get('COOKIE_REDIS_PORT', 6379),
                                                       settings.get('COOKIE_REDIS_DB', 2)))
        # 初始化所有cookie，将cookie放入redis
        init_cookie(self.rconn, crawler.spider.name)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        redis_keys = self.rconn.keys()
        while len(redis_keys) > 0:
            elem = random.choice(redis_keys).decode('utf-8')
            if "%s:Cookies" % spider.name in elem:
                # 因为从redis中取回的内容是bytes，所以先decode再转成str，又因为在json中引号是双引号所以又必须将str中单引号转成双引号
                # 我也很绝望！
                # todo 这段代码需要修改
                val = self.rconn.get(elem).decode("utf-8")
                val_encode = re.sub('\'', '\"', str(val))
                cookie = json.loads(val_encode)
                request.cookies = cookie
                request.meta["accountText"] = elem.split("Cookies:")[-1]
                break
            else:
                redis_keys.remove(elem)

    def process_response(self, request, response, spider):
        if response.status in [300, 301, 302, 303]:
            try:
                redirect_url = response.headers["location"]
                if "login.weibo" in redirect_url or "login.sina" in redirect_url:  # Cookie失效
                    print("%s的cookie失效" % request.meta['accountText'].split("--")[0])
                    logging.log(logging.DEBUG, "%s的cookie失效" % request.meta['accountText'].split("--")[0])
                    update_cookie(request.meta['accountText'], self.rconn, spider.name)
                elif "weibo.cn/security" in redirect_url:  # 账号被限
                    print("%s的账号失效" % request.meta['accountText'].split("--")[0])
                    logging.log(logging.DEBUG, "%s的账号失效" % request.meta['accountText'].split("--")[0])
                    remove_cookie(request.meta["accountText"], self.rconn, spider.name)
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response  # 重试
            except Exception as e:
                raise IgnoreRequest
        elif response.status in [403, 414]:
            print("+++++++++++++++++++++++++++++++++")
            print("出现%d错误。\n" % response.status)
            print(request.headers)
            print("+++++++++++++++++++++++++++++++++")
        else:
            return response


class RandomUserAgentMiddlware(object):
    # 随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())
