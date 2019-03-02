#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
test module
"""

__author__ = 'Lin Xin'

import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)
data = client['career']
link_table = data['link']

# 访问参数
url_root = 'http://career.buaa.edu.cn'
url_page = '/gotoRecruitmentInfoListByKetWordAction.dhtml?selectedItem=recruit&selectedNavigationName=RecruitmentInfoMain&positionInfoKeyWord=&orgNameKeyWord=&workAddressKeyWord=&pageIndex='
urls = (url_root+url_page + str(i) for i in range(1, 903))

raw_headers = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8
Connection: keep-alive
Cookie: CASTGC=TGT-166685-m2gEXd2PYaHNcNngQFbLqSzuOIdtJyxc97vWwdziMAyVQkh405-cas; JSESSIONID=4ed0588305df7b78a83836f91ec0
Host: career.buaa.edu.cn
Referer: http://career.buaa.edu.cn/gotoAllRecruitmentInfosAction.dhtml?selectedNavigationName=RecruitmentInfoMain&selectedItem=recruit&more=all
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'''

headers = {item[0]: item[1].strip() for item in [item.split(':', 1) for item in raw_headers.split('\n')[1:-1]]}

raw_headers2='''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Cookie: JSESSIONID=5af7fed49a9e4852f07679098e19; CASTGC=TGT-169145-15mZuEExHq1s0Ks1LbRdriXUXyMSKyoDIvCCu3AJrabmuCXADg-cas
Host: career.buaa.edu.cn
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'''
headers2 = {item[0]: item[1].strip() for item in [item.split(':', 1) for item in raw_headers2.split('\n')[1:-1]]}
import pymysql
db = pymysql.Connect(host='localhost',port=3306,user='root',password='xiaoji0909',database='career')
cur = db.cursor()
