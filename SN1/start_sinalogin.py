import sys
import os
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "sinaLogin"])
# 不是按照名字启动爬虫，而是按照文件启动，并且目录也要正确
execute(["scrapy", "runspider", "spiders/sina.py"])

