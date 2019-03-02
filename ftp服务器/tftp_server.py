# -*- coding:utf-8 -*-
from socket import socket, SOL_SOCKET, SO_REUSEADDR
import os
import sys
from signal import signal, SIGINT
import struct
from threading import Thread
from time import sleep
from math import ceil


class MyThread(Thread):
    def __init__(self, target, *args):
        super().__init__()
        self.func = target
        self.args = args
        self.result = '1'

    def run(self):
        self.result = self.func(*self.args)
        print(self.result)

    def get_value(self):
        return self.result


class Server(socket):
    def __init__(self, host=('0.0.0.0', 11000), path='/home/tarena/lx/tftpbase/'):
        super(self.__class__, self).__init__()
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.bind(host)
        self.path = path
        self.listen(100)
        self.filelist = {'1.jpg': 'asfd', 'newuser': []}
        print('waiting for connect')
        signal(SIGINT, self.server_close)

    def server_close(self, sig, frame):
        if sig == SIGINT:
            print('服务器即将关闭')
            for i in range(3):
                print(3 - i, end='\r')
                sleep(0.5)
            os._exit(0)

    def client_init(self, client):
        client_name = self.login(client)
        self.jieke(client, client_name)

    def login(self, client):
        while 1:
            client_name = client.recv(100).decode()
            if client_name in self.filelist.values() or client_name in self.filelist['newuser']:
                client.send('该名字有人使用,请重新输入'.encode())
                continue
            else:
                self.filelist['newuser'].append(client_name)
                client.send('欢迎登入'.encode())
                return client_name

    def run(self):
        while 1:
            client, attr = self.accept()
            t = MyThread(self.client_init, (client,))
            t.daemon = True
            t.start()
            print('connect from {}({})'.format(client.getpeername(), attr))

    def jieke(self, client, name):
        while 1:
            key = client.recv(1024).decode()
            if key == '':
                client.close()
                print('客户端{}退出'.format(name))
                sys.exit()
            elif key == 'showlist':
                self.showlist(client)
            elif key.startswith('download'):
                self.download(client, key)
            elif key.startswith('upload'):
                self.upload(client, name, key)

    def showlist(self, client):
        try:
            filelist = sorted([f for f in os.listdir(self.path) if os.path.isfile(self.path + f)])
            flist = '\n'.join(filelist)
            client.send(flist.encode())
        except FileNotFoundError:
            client.send(b'No file')
            os.mkdir(self.path)

    def download(self, client, key):
        name_list = set(key[9:].split(','))
        print(client.getpeername(), '请求文件下载', name_list)
        for file in name_list:
            try:
                with open(os.path.join(self.path, file), 'rb') as f:
                    data = f.read()
            except:
                print(file, '不存在')
                continue
            name_len = len(file)
            client.send(struct.pack('i', name_len))
            header = struct.pack(str(name_len) + 's' + 'i', file.encode(), len(data))
            client.send(header)
            client.send(data)
        print('{}下载完成'.format(client.getpeername()))
        client.send(struct.pack('i', 31415926))

    def upload(self, client, name, key):
        name_list = set(key[7:].split(','))
        print(client.getpeername(), '请求文件上传', name_list)
        all_list = set([f for f in os.listdir(self.path) if os.path.isfile(self.path + f)])
        newfile_list = name_list - all_list
        already_list = name_list & all_list
        client.send('准备完毕'.encode())
        success = []
        jump = []
        while 1:
            name_len = client.recv(4)
            l = struct.unpack('i', name_len)[0]  # 名字长度
            if l == 31415926:
                break
            header = client.recv(8 + ceil(l / 4) * 4)
            file_name, data_size = struct.unpack(str(l) + 's' + 'i', header)
            file_name = file_name.decode()
            if file_name in newfile_list:
                client.send(b'ok')
                data = b''
                while 1:
                    for i in range(data_size // 1024):
                        data += client.recv(1024)
                    else:
                        data += client.recv(data_size % 1024)
                        break
                with open(self.path + file_name, 'wb') as f:
                    f.write(data)
                    success.append(file_name)
                    self.filelist[file_name] = name
            elif file_name in already_list:
                if self.filelist[file_name] != name:
                    client.send('{}在FTP文件库中已存在,文件上传者为{},你没有权限覆盖'.format(file_name, self.filelist[file_name]).encode())
                    jump.append(file_name)
                    continue
                else:
                    client.send('您已经上传过{},是否覆盖源文件?'.format(file_name).encode())
                    overwrite_or_not = client.recv(1)
                    if overwrite_or_not == b'n':
                        jump.append(file_name)
                        continue
                    else:
                        data = b''
                        while 1:
                            for i in range(data_size // 1024):
                                data += client.recv(1024)
                            else:
                                data += client.recv(data_size % 1024)
                                break
                        with open(self.path + file_name, 'wb') as f:
                            success.append(file_name)
        print('{}上传完成'.format(client.getpeername()))
        end_send = '共上传{}项文件,其中成功{}项'.format(key.count(',') + 1, len(success))
        if jump:
            end_send += '跳过列表:\n{}'.format(set(jump))
        fail = set(key[7:].split(',')) - set(success) - set(jump)
        if fail:
            end_send += '失败列表:\n{}'.format(fail)
        client.send(end_send.encode())


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
