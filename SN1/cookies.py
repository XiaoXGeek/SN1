"""
1. 处理cookie
"""
import os
import requests
from SN1.weiboID import myWeiBo
import redis
import SN1.settings
import logging

base_path = os.path.dirname(os.path.abspath(__file__))
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
headers = {
    "Host": "passport.weibo.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Referer": "https://passport.weibo.cn/signin/login",
}
post_data = {
    "username": "",
    "password": "",
    "savestate": "1",
    "r": "http%3A%2F%2Fweibo.cn",
    "ec": "0",
    "pagerefer": "",
    "entry": "",
    "wentry": "",
    "loginfrom": "",
    "client_id": "",
    "code": "",
    "mainpageflag": "1",
    "hff": "",
    "hfp": ""
}
post_url = "https://passport.weibo.cn/sso/login"


# 使用账号密码获取cookie
def get_cookie(account, password):
    post_data["username"] = account
    post_data["password"] = password
    response = requests.post(post_url, data=post_data, headers=headers)
    cookie = {}
    # 如果登录成功，存储cookie
    if response.status_code == 200:
        logging.log(logging.DEBUG, "%s登录成功。" % account)
        print("%s登录成功。\n" % account)
        for c in response.cookies:
            cookie[c.name] = c.value
    else:
        logging.log(logging.DEBUG, "%s登录失败。" % account)
        print("%s登录失败。\n" % account)
    return cookie


def init_cookie(rconn, spider_name):
    """ 获取所有账号的Cookies，存入Redis。如果Redis已有该账号的Cookie，则不再获取。 """
    # 'SinaSpider:Cookies:账号--密码'，为None即不存在。
    try:
        for weibo in myWeiBo:
            if rconn.get("%s:Cookies:%s--%s" % (spider_name, weibo["account"], weibo["password"])) is None:
                cookie = get_cookie(weibo["account"], weibo["password"])
                if len(cookie) > 0:
                    rconn.set("%s:Cookies:%s--%s" % (spider_name, weibo["account"], weibo["password"]), cookie)
        # fixme 提示"sequence item 0: expected str instance, bytes found"
        cookie_num = "".join(str(rconn.keys())).count("%s:Cookies" % spider_name)
        if cookie_num == 0:
            os.system("pause")
    except Exception as e:
        print(e)


def update_cookie(account_text, rconn, spider_name):
    """ 更新一个账号的Cookie """
    account = account_text.split("--")[0]
    password = account_text.split("--")[1]
    cookie = get_cookie(account, password)
    if len(cookie) > 0:
        rconn.set("%s:Cookies:%s" % (spider_name, account_text), cookie)
    else:
        # 登录不成功，删除cookie
        logging.log(logging.DEBUG, "删除了%s的cookie" % account_text)
        print("删除了%s的cookie" % account_text)
        remove_cookie(account_text, rconn, spider_name)


def remove_cookie(account_text, rconn, spider_name):
    """ 删除某个账号的Cookie """
    rconn.delete("%s:Cookies:%s" % (spider_name, account_text))
    cookie_num = "".join(rconn.keys()).count("%s:Cookies", spider_name)
    if cookie_num == 0:
        # cookie全部失效重新初始化cookie
        logging.log(logging.DEBUG, "cookie全部失效。")
        print("cookie全部失效。\n")
        init_cookie(rconn, spider_name)


# 获取所有账号的全部cookie
rconn = redis.Redis(SN1.settings.COOKIE_REDIS_HOST, SN1.settings.COOKIE_REDIS_PORT, SN1.settings.COOKIE_REDIS_DB)
spider_name = "SN1"

if __name__ == '__main__':
    get_cookie("xiaoxiongyouxiang0@163.com", "xiaox123789456")
