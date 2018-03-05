#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: pageRedisManager.py

@time: 2017/10/19 15:18

@func: 管理下载页面
"""
import re
import time
from scrapy.utils.serialize import ScrapyJSONEncoder, ScrapyJSONDecoder
from SinaLogin.utils.redis_conn import rconn_db_page
from SinaLogin.settings import PAGE_REDIS_CHANNEL, PAGE_REDIS_CHANNEL_MESSAGE, PAGE_REDIS_NUM, PAGE_REDIS_LIST_NAME, \
    PAGE_REDIS_SAVE_PATH


class PageManger(object):
    def __init__(self):
        self.rconn = rconn_db_page
        self.channel = PAGE_REDIS_CHANNEL
        self.message = PAGE_REDIS_CHANNEL_MESSAGE
        self.page_num = PAGE_REDIS_NUM
        self.page_list = PAGE_REDIS_LIST_NAME
        self.basepath = PAGE_REDIS_SAVE_PATH
        self.ser = ScrapyJSONEncoder().encode
        self.deser = ScrapyJSONDecoder().decode

    def publish_task(self):
        self.rconn.publish(channel=self.channel, message=self.message)

    def add_to_redis(self, response):
        group = re.findall(".*/(\d+)/(info|follow|fans)", response.url)[0]
        if group is not None:
            filename = group[0] + "_" + group[1] + "_" + str(int(time.time() * 1000)) + ".html"
            content = self.ser(filename + "#$$#" + response.text)
            pipe = self.rconn.pipeline(transaction=True)
            pipe.incr(self.page_num)
            pipe.lpush(self.page_list, content)
            pipe.publish(channel=self.channel, message=self.message)
            pipe.execute()

    def get_from_redis(self):
        page = self.rconn.lpop(self.page_list)
        if page is not None:
            page_str = self.deser(str(page, encoding="utf-8"))
            page = page_str.split("#$$#")
            self.write_to_local(page[0], page[1])

    def write_to_local(self, filename, page_content):
        group = re.findall("(\d+)_(.*?)_(\d+).*", str(filename))[0]
        path = self.basepath + "/" + group[1] + "/" + filename
        with open(path, 'w', encoding='utf-8') as f:
            f.write(page_content)
        print("下载页面 %s" % filename)


class Client(object):
    def __init__(self):
        self.page_manager = PageManger()
        self.rconn = rconn_db_page
        self.channel = PAGE_REDIS_CHANNEL
        self.message = PAGE_REDIS_CHANNEL_MESSAGE
        self.page_num = PAGE_REDIS_NUM
        self.page_list = PAGE_REDIS_LIST_NAME
        self.ps = self.rconn.pubsub()
        self.ps.subscribe(self.channel)

    def listen_task(self):
        for msg in self.ps.listen():
            if msg['type'] == 'message':
                message = str(msg['data'], encoding='utf8')
                if message is "Q":
                    self.ps.unsubscribe(self.channel)
                    print('%s 关闭！' % self.channel)
                else:
                    self.rconn.decr(self.page_num)
                    print("开始下载页面----->")
                    self.page_manager.get_from_redis()


if __name__ == '__main__':
    print('开始接收消息消息：')
    client = Client()
    client.listen_task()

