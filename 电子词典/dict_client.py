#!/usr/bin/env python3
# -*- coding:utf-8 -*-


__author__ = 'Lin Xin'

from socket import socket
import json
import sys


class Client(socket):
    def __init__(self, host=('127.0.0.1', 20000)):
        super().__init__()
        self.connect(host)

    def run(self):
        try:
            self._login()
            self._lookup()
        except ConnectionResetError:
            print('服务器已断开连接')

    def _lookup(self):
        panel = '''
                **********************************
                *        电子词典使用说明         *
                *--------------------------------*
                *  查询单词解释  |  输入任意单词  *
                *  查看历史纪录  |     输入-h     *
                *  退出电子词典  |     输入-q     *
                **********************************
'''
        print(panel)
        while 1:
            word = input(">>>").strip()
            if word == '-q':
                print('期待下次再见')
                self.close()
                sys.exit(0)
            else:
                self.send(word.encode())
                recv_msg = self.recv(1024)
                t, content = json.loads(recv_msg.decode())
                if t == 'history':
                    print('您的搜索历史纪录：\nid\tword\ttime')
                    for index, w in enumerate(content):
                        print('{}\t{}\t{}'.format(index, w['check_word'], w['time']))
                else:
                    print(word, '：\n', content.strip())

    def _login(self):
        panel = '''
        **********************************
        *      欢迎登陆电子词典服务器     *
        *--------------------------------*
        *     登录       |        l      *
        *     注册       |        s      *
        *     退出       |        q      *
        **********************************
>>>'''

        while 1:
            choice = input(panel)
            if choice == 'l':
                print('欢迎登录')
                while 1:
                    user = input("请输入用户名\n>>>")
                    if user:
                        break
                    else:
                        print("用户名不可为空，请重新输入")
                while 1:
                    password = input("请输入密码\n>>>")
                    if password:
                        break
                    else:
                        print("密码不可为空，请重新输入")
                self.send(json.dumps(('l', user, password)).encode())
                return_msg = self.recv(1024).decode()
                print(return_msg)
                if return_msg == '登陆成功':
                    break

            elif choice == 's':
                print('欢迎注册')
                user = input("请输入用户名\n>>>")
                password = input("请输入密码\n>>>")
                self.send(json.dumps(('s', user, password)).encode())
                return_msg = self.recv(1024).decode()
                print(return_msg)
                if return_msg == '注册成功':
                    print('请牢记账号密码，欢迎登入')
                    break
            elif choice == 'q':
                self.send(json.dumps(('q', 1, 1)).encode())
                print("期待下次再见")
                self.close()
                sys.exit(0)
            else:
                print("输入有误\n")


def main():
    client = Client()
    client.run()


if __name__ == '__main__':
    main()
