#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
test module
"""

__author__ = 'Lin Xin'

from gevent import monkey

monkey.patch_all()
import gevent
import sys
import requests
from bs4 import BeautifulSoup
from config import link_table, headers, url_root, urls
import time

COMPLETE_PAGE = []


def handle_html_one(web, page):
    soup = BeautifulSoup(web, 'lxml')
    links = soup.select(
        '#stu_style > div.stu_info > div > div.calender_style > div.div_info > div > div.article_title_style > a')
    companies = soup.select(
        '#stu_style > div.stu_info > div > div.calender_style > div.div_info > div > div.org_name_style')
    for id, link, company in zip(range(1, 21), links, companies):
        data = {'id': id + 20 * (int(page) - 1), 'company': company.get_text().strip(),
                'career': link.get_text().strip(),
                'link': url_root + link.get('href')}
        link_table.insert_one(data)
    print('page {} complete'.format(page))
    COMPLETE_PAGE.append(page)


def main(url):
    while True:
        try:
            web = requests.get(url, headers=headers)
        except ConnectionError:
            time.sleep(0.5)
            continue
        else:
            if web.status_code == 200:
                handle_html_one(web.text, url[-3:].split('=')[-1])
                break
            else:
                print(url, web.status_code)


if __name__ == '__main__':
    while True:
        g_list = [gevent.spawn(main, url) for url in urls]
        gevent.joinall(g_list)
        urls = [url for url in urls if url[-3:].split('=')[-1] not in COMPLETE_PAGE]
        if not urls:
            break
    print('all completed')
