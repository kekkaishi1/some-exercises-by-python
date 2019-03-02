#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Lin Xin'


import os,time,win32api, win32con


def main(process_name):
    # print('开始检测')
    count=0
    while count<2:
        process_list = os.popen('wmic process list brief').read()
        if process_name in process_list:
            # print('检测到游戏运行，即将关闭')
            os.system('ipconfig /release')
            time.sleep(10)
            os.system('taskkill /im '+process_name+'.exe')
            time.sleep(3)
            win32api.MessageBox(0,
                                "Failed to load the engine2 DLL.\n\nPath:\"D:hyxd\\Launcher.exe\"\n\nError: (0x0000007e) 找不到指定的模块",
                                "Launcher Error", win32con.MB_ICONERROR)
            count += 1
        # print('循环中')
        time.sleep(17)



while True:
    main('hyxd')
    # print('即将等待10min')
    time.sleep(586)
