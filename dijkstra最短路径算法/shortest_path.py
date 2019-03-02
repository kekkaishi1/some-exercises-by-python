#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
find shortest path with method dijkstra
"""

__author__ = 'Lin Xin'

import sys
import re


class Dijkstra:
    def __init__(self, data):
        self.data = self.data_handle(data)
        self.spots = set(self.data.keys())
        self.length = len(self.spots)
        self.not_handle_spots = self.spots
        self.longest_dis = sum(dis for v in self.data.values() for dis in v.values()) / 2 + 1
        self.flag = 0


    @staticmethod
    def data_handle(data):
        result = {}
        for d in data:
            for i in (0, 1):
                if result.get(d[i]):
                    result[d[i]].update({d[1 - i]: float(d[2])})
                else:
                    result[d[i]] = {d[1 - i]: float(d[2])}
        return result

    def __run_once_init(self,start):
        self.result = {spot: {'path': None, 'dis': self.longest_dis} for spot in self.spots}  # 最短路径中上一级节点
        if not start:
            start=input("please input start spot:")
        self.result[start]['dis'] = 0
        self.start_spot = start
        self.last_handle_spot = start
        self.not_handle_spots = self.spots - set(self.last_handle_spot)
        self.flag += 1

    def run(self,start=None):
        if not self.flag:
            self.__run_once_init(start)
        if not self.not_handle_spots:
            self.flag = 0
            self.not_handle_spots = self.spots
            print('compute complete')
            return
        for spot in self.data[self.last_handle_spot]:
            if spot in self.not_handle_spots:  # spot是当前处理的非源点
                new_dis = self.result[self.last_handle_spot]['dis'] + self.data[spot][self.last_handle_spot]
                old_dis = self.result[spot]['dis']
                self.result[spot]['dis'] = new_dis < old_dis and new_dis or old_dis
                self.result[spot]['path'] = self.last_handle_spot
        self.last_handle_spot = [s for s in self.find_key_via_value(self.result, min(
            self.result[spot]['dis'] for spot in self.not_handle_spots)) if s in self.not_handle_spots][0]
        self.not_handle_spots.discard(self.last_handle_spot)
        self.run()

    def find_path(self, end_spot, path=None):
        if not path:
            path = list()
        path.append(end_spot)
        last_path = self.result[end_spot]['path']
        if not last_path:
            return ' ---> '.join(reversed(path))
        return self.find_path(last_path, path)

    def show_path_all(self):
        print('start spot:', self.start_spot)
        print('spot\t', 'PATH'.ljust((self.length - 1) * 7 + 1), 'distance')
        for spot in sorted(self.result.keys(), key=lambda r: r):
            if not self.result[spot]['path']:
                continue
            print('{0}\t {1} (distance={2})'.format(spot, self.find_path(spot), self.result[spot]['dis']))

    def show_path(self, end_spot,show=True):
        dis = self.result[end_spot]['dis']
        if show:
            print('The shortest path to {0} is {1} (distance={2})'.format(end_spot, self.find_path(end_spot), dis))
        return dis,self.find_path(end_spot)

    @staticmethod
    def find_key_via_value(d, value):
        result = []
        for k, v in d.items():
            if v['dis'] == value:
                result.append(k)
        return result


def __data_handle(data, terminated=re.compile(r'[\s,，、/\\]')):
    result = []
    with open(data) as f:
        for line in f.readlines():
            result.append(tuple(terminated.split(line)))
    return result


def data_input(terminated=re.compile(r'[\s,，、/\\]')):
    readme = '''
    please input 'start_spot', 'end_spot', 'length' with usual separator, enter 2 enters to end
    e.g. 1 4 12 ---->spot 1 to spot 4 with distance=12\n     3,5,6 ---->spot 3 to spot 5 with distance=6
    use "\d -num" to delete input, default num is last one
    use \s to show current data
    use \h to show help
    '''
    print(readme)
    data = []
    while 1:
        temp = input(">>>").strip()
        if temp == '\s':
            for i, d in enumerate(data):
                print(i, '\t', d)
        elif temp.startswith('\d'):
            t = temp.split('-')
            num = len(t) > 1 and t[-1] or len(t) - 1
            print('delete data:{}'.format(data.pop(num)))
        elif temp == '':
            print('data input complete')
            return data
        elif temp == '\h':
            print(readme)
        else:
            t = terminated.split(temp)
            if len(t) == 3:
                try:
                    t[-1] = float(t[-1])
                except ValueError:
                    print('input error. Last input should be num')
                else:
                    data.append(t)


def __main():
    if len(sys.argv) == 2:
        data = __data_handle(sys.argv[1])
    elif len(sys.argv) == 1:
        data = data_input()
    else:
        print('data input error')
        return
    dijkstra = Dijkstra(data)
    dijkstra.run()
    dijkstra.show_path_all()


if __name__ == '__main__':
    __main()
