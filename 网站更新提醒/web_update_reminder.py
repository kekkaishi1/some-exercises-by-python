#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Lin Xin'

import requests, time, win32api, win32con, os

url = 'http://changjiang.chinadevelopment.com.cn/'

while True:
    web = requests.get(url)
    web.encoding = 'utf-8'
    with open('web.txt', encoding='utf-8') as web_old:
        web_old_text = web_old.read()
    with open('web_new.txt', 'w+',encoding='utf-8') as web_new:
        web_new.write(web.text)
    with open('web_new.txt',encoding='utf-8') as web_new:
        web_new_text = web_new.read()
    if web_old_text != web_new_text:
        with open('web.txt','w',encoding='utf-8') as web_old:
            web_old.write(web.text)
        t = win32api.MessageBox(0, "发展网更新了", '发展网更新监控', win32con.MB_OKCANCEL)
        if t == 1:
            os.system('explorer ' + url)
    else:

        print(time.ctime()[11:20], '没有更新')

    time.sleep(600)
