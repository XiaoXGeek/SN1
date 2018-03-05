#!/usr/bin/env python

# encoding: utf-8

"""
@author: xiaox

@contact: xiaoxgeek@163.com

@file: EnterEvery5min.py

@time: 2018/1/11 16:39

每5分钟按下回车
"""
import win32gui
import win32api
import win32con
import time
# # 获得前置窗口
# hwnd = win32gui.GetForegroundWindow()
# # 获取窗口类名
# cls = win32gui.GetClassName(win32gui.GetForegroundWindow())
while True:
    print("按下回车 %s" % time.strftime("%H:%M", time.localtime()))
    # 获取句柄的文本标题内容
    hwnd = win32gui.FindWindow("ConsoleWindowClass", "cmd - scrapy  crawl sinaLogin")
    # 设置成前台
    win32gui.SetForegroundWindow(hwnd)
    # 按下回车
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(60 * 5)

