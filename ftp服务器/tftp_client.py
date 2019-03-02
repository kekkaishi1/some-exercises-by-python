# -*- coding:utf-8 -*-

from socket import socket
import os
import sys
from signal import signal, SIGCHLD, SIG_IGN
import struct
from time import sleep


class Client(socket):
    def __init__(self, server_host=('127.0.0.1', 11000)):
        super(Client, self).__init__()
        self.connect(server_host)

        while 1:
            self.name = input('>>>请输入姓名作为资源唯一标识符\n').encode()
            self.send(self.name)
            login_msg = self.recv(100).decode()
            print(login_msg)
            if login_msg == '欢迎登入':
                break

    def run(self):
        readme = \
            '''
            ***********************************************
            help                                 获取帮助指令 
            showlist                             列出文件列表 
            download 文件名1[,文件名2,...]         下载文件    
            upload 路径/文件名1[,路径/文件名2,...]  上传文件     
            exit                                 退出客户端   
            ***********************************************
            '''
        print(readme)
        while 1:
            key = input('>>>')
            if key.strip() == 'help':
                print(readme)
            elif key.startswith('download'):
                self.download(key)
            elif key.startswith('upload'):
                self.upload(key)
            elif key.strip() == 'showlist':
                self.show()
            elif key.strip() == 'exit':
                self.close()
                print('客户端已退出')
                break
            else:
                print('输入指令有误,请参阅help帮助')

    def download(self, key):
        self.send(key.encode())
        success = []
        while 1:
            name_len = self.recv(4)
            l = struct.unpack('i', name_len)[0]  # 名字长度
            if l == 31415926:
                break
            header = self.recv(8+ceil(l/4)*4)
            file_name, data_size = struct.unpack(str(l) + 's' + 'i', header)
            data = b''
            while 1:
                for i in range(data_size // 1024):
                    data += self.recv(1024)
                    block = round((i + 1) * 102400 / data_size,2)
                    print(str(block)[:5] + '% ' + '▇' * int(block * 0.5),end='\r')

                else:
                    data += self.recv(data_size % 1024)
                    print('100%', '▇' * 50)
                    break
            with open(file_name.decode(), 'wb') as f:
                f.write(data)
                success.append(file_name.decode())
        print('共下载{}项文件,其中成功{}项'.format(key.count(',') + 1, len(success)))
        fail = set(key[9:].split(',')) - set(success)
        fail and print('失败列表:\n{}'.format(fail))

    def upload(self, key):
        name_list = set(key[7:].split())
        self.send(key.encode())
        self.recv(1024)
        for file in name_list:
            try:
                with open(file, 'rb') as f:
                    data = f.read()
            except:
                print(file, '不存在')
                continue
            file_name = os.path.split(file)[1]
            name_len = len(file_name)
            self.send(struct.pack('i', name_len))
            header = struct.pack(str(name_len) + 's' + 'i', file_name.encode(), len(data))
            self.send(header)
            up_ok = self.recv(1024)
            if up_ok == b'ok':
                self.send(data)
            elif up_ok[-1] == b'?':
                print(up_ok.decode())
                while 1:
                    respon = input('[y]/n')
                    if respon in ('y', ''):
                        self.send(b'y')
                        self.send(data)
                        break
                    elif respon == 'n':
                        self.send(b'n')
                        break
                    else:
                        print("请重新输入")
            else:
                print(up_ok.decode())
        self.send(struct.pack('i', 31415926))
        print(self.recv(1024).decode())

    def show(self):
        self.send(b'showlist')
        file_list = self.receive()
        print(file_list.decode())

    def receive(self):
        data = b''
        while 1:
            data += self.recv(1024)
            if len(data) < 1024:
                break
        return data


def main():
    client = Client()
    client.run()


if __name__ == '__main__':
    main()
