#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
test module
"""

__author__ = 'Lin Xin'

from gevent import monkey

monkey.patch_all()
import gevent
import requests
from bs4 import BeautifulSoup
from config import link_table, headers2, cur, db
import time

COMPLETE = []


def handle_html_one(web, id):
    soup = BeautifulSoup(web, 'lxml')
    career = soup.select(
        '#stu_style > div.stu_info > div > div.left_content > div > div.second_title')
    company = soup.find_all('td', {'class': 'td_content'})
    carrer_info = soup.select(
        '#stu_style > div.stu_info > div > div.left_content > div > div.div_info > div.child_title > div:nth-of-type(2) > table > tr > td')
    career_des = soup.select(
        '#stu_style > div.stu_info > div > div.left_content > div > div.div_info > div:nth-of-type(2) > div.retirement_desc_style')
    career_need = soup.select(
        '#stu_style > div.stu_info > div > div.left_content > div > div.div_info > div:nth-of-type(3) > div.retirement_desc_style')
    company_des = soup.select(
        '#stu_style > div.stu_info > div > div.left_content > div > div.div_info > div:nth-of-type(4) > div.unit_content')

    t = carrer_info[-1].get_text().strip()
    if not t:
        t = '1970-01-01'

    sql = "insert into career values ({id},'{career_name}','{}','{}','{}','{}','{}','{}','{}',{},'{}',date('{}'),'{career_des}','{career_need}','{company_des}');".format(
        *tuple([item.get_text().strip() for item in company][:-3]), carrer_info[-5].get_text().strip(), t, id=id,

        career_name=
        career[
            0].get_text().split()[0].strip(),
        career_des=
        career_des[
            0].get_text(),
        career_need=
        career_need[
            0].get_text(),
        company_des=
        company_des[
            0].get_text())
    cur.execute(sql)
    db.commit()
    print('id {} complete'.format(id))
    COMPLETE.append(id)


def main(url, id):
    while True:
        try:
            web = requests.get(url, headers=headers2)
        except ConnectionError:
            time.sleep(0.5)
            continue
        else:
            if web.status_code == 200:
                handle_html_one(web.text, id)
                break
            else:
                print(url, web.status_code)


if __name__ == '__main__':
    urls = ((info['link'], info['id']) for info in link_table.find())
    g_list = []
    while True:
        while True:
            for i in range(100):
                try:
                    g = gevent.spawn(main, *next(urls))
                    g_list.append(g)
                except StopIteration:
                    break
            else:
                gevent.joinall(g_list)
                continue
            gevent.joinall(g_list)
            break
        urls = ((info['link'], info['id']) for info in link_table.find() if info['id'] not in COMPLETE)
        if not urls:
            break
    print('all completed')
    cur.close()
    db.close()
