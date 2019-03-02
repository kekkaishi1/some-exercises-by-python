#!/usr/bin/env python3
# -*- coding:utf-8 -*-


__author__ = 'Lin Xin'

import sys
import os
import pymongo
from pymongo import errors
import re
from socket import socket
from multiprocessing import Process
# from signal import signal, SIGINT, SIGCHLD, SIG_IGN
from threading import Thread
import json
from time import ctime, sleep


class DictServer(socket):
    """
    请将dict.txt文件和服务器脚本放于同路径下
    save值用于初始化数据库
    """

    def __init__(self, addr=('0.0.0.0', 20000), save=False):
        super().__init__()
        # signal(SIGINT, self._quit)
        # signal(SIGCHLD, SIG_IGN)
        self.mongodb = pymongo.MongoClient('localhost', 27017)
        self.dictdb = self.mongodb['dict']['dict']
        self.userdb = self.mongodb['dict']['user']
        if save:
            self._save()
        self.bind(addr)
        self.listen(100)
        self.login_user = []
        print('waiting for connect')

    def run(self):
        while 1:
            client, c_addr = self.accept()
            print(c_addr, '连接并尝试登陆')
            t = Thread(target=self._client_handle, args=(client,))
            t = Process(target=self._client_handle, args=(client,))
            t.start()

    def _client_handle(self, client):
        try:
            client_name = self._login_in(client)
            if not client_name:
                return
            print("用户{}成功登入".format(client_name))
            self._lookup(client, client_name)
            client.close()
            sys.exit(0)
        except ConnectionResetError:
            print('客户端{}强迫关闭了连接'.format(client.getpeername()))

    def _lookup(self, client, name):
        while 1:
            msg = client.recv(1024).decode()
            if msg == '':
                print('{} ：退出登录'.format(name))
                client.close()
                return 0
            elif msg == '-h':
                print(name, ' ：进行了历史查询')
                t = 'history'
                try:
                    content = self.userdb.find({'name': name}).next()['history']
                except KeyError:
                    content = []
            else:
                print(name, '：查询了单词', msg)
                t = 'word'
                cursor = self.dictdb.find({'word': msg})
                try:
                    content = cursor.next()['content']
                except StopIteration as e:
                    print(e)
                    content = '如果你一定要查这个词，那我只能告诉你，无可奉告'
                self.userdb.update_one({'name': name}, {'$push': {'history': {'time': ctime(), 'check_word': msg}}})
            send_msg = json.dumps((t, content)).encode()
            client.send(send_msg)

    def _login_in(self, client):
        while 1:
            login_msg = client.recv(1024).decode()
            choice, user, password = json.loads(login_msg)
            if choice == 'l':
                login_result = self._login(user, password)
                client.send(login_result.encode())
                if login_result == "登陆成功":
                    return user
                else:
                    continue

            elif choice == 's':
                sign_up_result = self._sign_up(user, password)
                client.send(sign_up_result.encode())
                if sign_up_result == "注册成功":
                    return user
                else:
                    continue
            else:
                print(client.getpeername(), '放弃登陆')
                client.close()
                return False

    def _login(self, user, password):
        if user in self.login_user:
            return "该用户已登陆，请确认账号安全性"
        user_data = self.userdb.find({'name': user})
        if user_data.count():
            if user_data.next()['password'] == password:
                self.login_user.append(user)
                return "登陆成功"
            else:
                return "密码错误"
        else:
            return '用户不存在'

    def _sign_up(self, user, password):
        try:
            self.userdb.insert_one({'name': user, 'password': password})
            self.login_user.append(user)
            return "注册成功"
        except errors.DuplicateKeyError:
            return "已存在用户名"

    def _save(self):
        self.userdb.ensure_index('name', unique=True)
        r1 = re.compile(r'([-\w]+\s)*[-\w]+\s{2,}')  # 正常单词及词组
        r2 = re.compile(r'\w{16,}')
        with open('dict.txt') as d:
            for line in d.readlines():
                try:
                    word = {'word': r1.match(line).group().strip(), 'content': line[17:-1]}
                except AttributeError:
                    try:
                        word = {'word': r2.match(line).group(), 'content': line.split(maxsplit=1)[-1]}
                    except AttributeError:
                        print(line)
                        while 1:
                            p = input('请输入单词长度，无单词解释则输入p\n')
                            x = input("请确认输入是否正确  [y]/n")
                            if x != 'n':
                                break
                        if p != 'p':
                            word = {'word': line[:int(p)], 'content': line[int(p):-1].split()}
                        else:
                            word = {'word': line[:-1], 'content': '无可奉告'}
                finally:
                    self.dictdb.insert_one(word)
            else:
                print('录入完成')

    def _quit(self, sig, frame):
        if sig == SIGINT:
            self.mongodb.close()
            self.close()
            print('服务器即将关闭')
            self.mongodb.close()
            for i in range(3):
                sleep(1)
                print(3 - i, end='\r')
            os._exit(0)


def main():
    server = DictServer()
    server.run()


if __name__ == '__main__':
    main()
