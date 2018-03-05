#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: conn.py

@time: 2017/10/19 15:27

@func: Redis的连接池配置
"""

import redis
from SinaLogin.settings import PAGE_REDIS_HOST, PAGE_REDIS_PORT, PAGE_REDIS_DB, COOKIE_REDIS_HOST, COOKIE_REDIS_PORT, \
    COOKIE_REDIS_DB, REDIS_PARAMS


pool_db0 = redis.ConnectionPool(host="10.18.51.57", port=6379, db=0)
pool_db_dup = redis.ConnectionPool(host=REDIS_PARAMS['host'], port=REDIS_PARAMS['port'], db=REDIS_PARAMS['db'])
pool_db_cookie = redis.ConnectionPool(host=COOKIE_REDIS_HOST, port=COOKIE_REDIS_PORT, db=COOKIE_REDIS_DB)
pool_db_page = redis.ConnectionPool(host=PAGE_REDIS_HOST, port=PAGE_REDIS_PORT, db=PAGE_REDIS_DB)

rconn_db0 = redis.Redis(connection_pool=pool_db0)
# 去重队列和请求队列的Redis连接
rconn_db_dup = redis.Redis(connection_pool=pool_db_dup)
# cookie的Redis连接
rconn_db_cookie = redis.Redis(connection_pool=pool_db_cookie)
# 下载页面的Redis连接
rconn_db_page = redis.Redis(connection_pool=pool_db_page)



