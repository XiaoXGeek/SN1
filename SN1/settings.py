# -*- coding: utf-8 -*-

# Scrapy settings for SN1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import sys
import os

BOT_NAME = 'SN1'

SPIDER_MODULES = ['SN1.spiders']
NEWSPIDER_MODULE = 'SN1.spiders'

# scrapy_redis设置
SCHEDULER = "SN1.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
DUPEFILTER_CLASS = "SN1.scrapy_redis.dupefilter.RFPDupeFilter"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# 1. 设置随机的useragent，必须设置scrapy原本的useragent为None
# 2. 自定义的useragent
# 3. cookie的操作
DOWNLOADER_MIDDLEWARES = {
   'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
   'SN1.middlewares.RandomUserAgentMiddlware': 401,
   'SN1.middlewares.CookieMiddleware': 402,
}

# 数据存储到数据库
ITEM_PIPELINES = {
   'SN1.pipelines.MysqlTwistedPipline': 500
}

# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'SN1'))

# 间隔时间
DOWNLOAD_DELAY = 1  # 间隔时间

# 设置日志级别
LOG_LEVEL = 'DEBUG'
LOG_FILE = BASE_DIR + "/log"
# 设置scrapy_redis去重队列和请求队列
# 关系爬取用1，微博爬取用3
REDIS_PARAMS = {
   'host': "10.18.51.54",
   'port': 6379,
   'db': 3
}

# cookie的redis连接配置
# 关系爬取用2，微博爬取用4
COOKIE_REDIS_HOST = "10.18.51.54"
COOKIE_REDIS_PORT = 6379
COOKIE_REDIS_DB = 4

# MySQL数据库连接配置
MYSQL_HOST = "10.18.57.110"
MYSQL_DBNAME = "db_sn1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root_123a"

print(BASE_DIR)