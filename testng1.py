#!/usr/bin/python
# coding:utf-8
__Author__ = 'Adair.l'
import requests
import bs4
import http.cookiejar as cookiejar

headers = {
                'Host': 'manhua1032-101-69-161-98.cdndm5.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'http://cnc.dm5.com/m575919/',
                'Connection': 'keep-alive',
            }
for x in headers:
    print(x, headers[x])
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True) # 如果已经有 cookie信息的话 直接用于登录
except:
    print("Cookie 未能加载")


r0=session.get('http://cnc.dm5.com/m575919/')
print(r0)
r1=session.get('http://manhua1032-101-69-161-98.cdndm5.com/41/40586/575919/1_5252.jpg?cid=575919&key=e98e2016acb7167394dbc062a7161755&type=1',headers=headers,)
print(r1)
print(session.cookies)
open('1.jpg','wb').write(r1.content)











