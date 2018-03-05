#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: flush_db.py

@time: 2018/1/8 19:43
"""
from SinaLogin.utils.redis_conn import rconn_db_dup

rconn_db_dup.execute_command("flushdb")