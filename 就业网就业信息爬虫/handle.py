#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
test module
"""

__author__ = 'Lin Xin'

from config import *


def main():
    id_list = [i['id'] for i in link_table.find().sort('id')]
    id_rest =[id for id in range(1,18032) if id not in id_list]
    print([int(i/20) for i in id_rest[19::20]])


if __name__ == '__main__':
    main()
    
