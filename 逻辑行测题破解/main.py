#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Lin Xin'
'''
0 for A
1 for B
2 for C
3 for D
'''

import math

global puzzle, answer
answer = ['x']
dict10 = {0: 3, 1: 2, 2: 4, 3: 1}


def trueorfalse(num):
    if num == 3:
        if answer[3] == 0 and answer[2] == 0:
            return False
        if answer[3] == 1 and answer[2] != 1:
            return False
        if answer[3] == 2 and answer[2] == 2:
            return False
        if answer[3] == 3 and answer[2] != 3:
            return False
        return True
    if num == 4:
        if answer[3] == 0 and answer[2] != answer[4]:
            return False
        if answer[3] == 1 and answer[4] != 1:
            return False
        if answer[3] == 2 and answer[4] != 2:
            return False
        if answer[3] == 3 and answer[4] == 3:
            return False
        if answer[4] == 0 and answer[1] != answer[5]:
            return False
        return True
    if num == 5:
        if answer[5] == 1 and answer[4] != 1:
            return False
        return True
    if num == 6:
        if answer[6] == 0 and answer[3] != 1:
            return False
        if answer[6] == 1 and answer[0] != 1:
            return False
        return True
    if num == 7:
        if answer[4] == 1 and answer[7] != answer[2]:
            return False
        if answer[5] == 3 and answer[7] != 3:
            return False
        return True
    if num == 8:
        if answer[5] == 0 and answer[8] != 0:
            return False
        if answer[6] == 0 and answer[2] != answer[8]:
            return False
        if answer[6] == 1 and answer[1] != answer[8]:
            return False
        if answer[6] == 2 and answer[3] != answer[8]:
            return False
        if answer[6] == 3 and answer[5] != answer[8]:
            return False
        if answer[8] == 0 and math.fabs(answer[7] - answer[1]) < 2:
            return False
        if answer[8] == 1 and math.fabs(answer[5] - answer[1]) < 2:
            return False
        if answer[8] == 2 and math.fabs(answer[2] - answer[1]) < 2:
            return False
        return True
    if num == 9:
        if answer[4] == 2 and answer[9] != answer[1]:
            return False
        if answer[5] == 2 and answer[9] != 2:
            return False
        if answer[6] == 3 and answer[9] != answer[5]:
            return False
        if answer[1] == answer[6]:
            if answer[9] == 0 and answer[5] == answer[6]:
                return False
            if answer[9] == 3 and answer[5] == 1:
                return False
        if answer[1] != answer[6]:
            if answer[9] == 0 and answer[5] != answer[6]:
                return False
            if answer[9] == 3 and answer[5] != 3:
                return False
            if answer[9] == 2:
                return False
        return True
    if num == 10:
        if answer[4] == 3 and answer[6] != answer[10]:
            return False
        if answer[6] == 2 and answer[3] != answer[10]:
            return False
        if answer[8] == 3 and math.fabs(answer[1] - answer[10]) < 2:
            return False
        if answer[9] == 1:
            if answer[1] == answer[6] and answer[5] == answer[10]:
                return False
            if answer[1] != answer[6] and answer[5] != answer[10]:
                return False
        counts = [answer.count(i) for i in range(4)]
        cha = max(counts) - min(counts)
        if dict10[answer[10]] != cha:
            return False
        return True
    return True


def command(answer, num=1):
    for i in range(4):
        answer.append(i)
        if len(answer) >= 6:
            answer[5] = int(math.fmod(answer[2] + 2, 4))
        if trueorfalse(num):
            if num != 10:
                print(answer)
                if not command(answer, num + 1):
                    answer.pop()
                else:
                    return True
            else:
                return True
        else:
            answer.pop()
    else:
        return False


def main():
    command(answer, 0)
    answer.pop(0)
    answer.pop(-1)
    final_answer = [chr(65 + i) for i in answer]
    print('the final answer is {}'.format(final_answer))


if __name__ == '__main__':
    main()
