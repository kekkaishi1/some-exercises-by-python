#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Lin Xin'

import math

# 控制模块
tax_or_not = 0  # 计算税前值为0，税后为1

# 初始参数
annual_yield = 0.045  # 年化收益率
bonus_input_ori = 0.1  # 每月初始投入理财占比
bonus_input_increase = 0.03  # 理财投入增长比
bonus_input_increase_max = 0.25  # 理财投入极限比
monthly_wage_ori = 5000  # 初始月工资
wage_increase = 0.1  # 工资涨幅（每年）
wage_increase_year = 10  # 工资增长年限
work_start_year = 30  # 工作开始年龄
work_end_year = 65  # 工作结束年龄
tax_rate_china = [3500, (0, 3), (1500, 10), (4500, 20), (9000, 25), (35000, 30), (55000, 35),
                  (80000, 45)]  # 中国税率 第一项为个税起征点，后续为各级税率

# 中间参数
wage_ori = monthly_wage_ori * 12  # 基础年薪
monthly_yield = (1 + annual_yield) ** (1 / 12) - 1  # 月化收益率
work_year = work_end_year - work_start_year + 1  # 工作年限


def tax_monthly(wage_monthly, tax_rate=tax_rate_china):
    """
    :param wage_monthly: 月工资
    :param tax_rate: 税率模式
    :return: 当月缴税
    """
    # 是否计算个税
    if tax_or_not == 1:
        return 0

    # 处理税率，便于计算
    tax_rate_handle = [(tax_rate[i][0] - tax_rate[i - 1][0], tax_rate[i - 1][1]) for i in range(2, len(tax_rate))]
    tax_rate_handle.append(tax_rate[-1][-1])

    # 计算个税
    tax_wage = wage_monthly - tax_rate[0]  # 应纳税所得额
    tax = 0  # 初始化个税
    if tax_wage < 0:  # 未到起征点
        return tax
    for i in tax_rate_handle:
        try:
            if tax_wage > i[0]:
                tax += i[0] * i[1] / 100
                tax_wage -= i[0]
            else:
                tax += tax_wage * i[1] / 100
                return tax
        except TypeError:
            return tax + tax_wage*i/100


def wage():
    """
    :return: 每月工资列表
    """
    # 每年单月税前工资
    wage_pretax = [monthly_wage_ori * (1 + wage_increase) ** i for i in range(wage_increase_year)]  # 工资增长阶段
    wage_pretax += [monthly_wage_ori * (1 + wage_increase) ** wage_increase_year] * (
                work_year - wage_increase_year)  # 工资极大后稳定阶段

    # 每年单月税后工资
    wages_after_tax = [pretax - tax_monthly(pretax) for pretax in wage_pretax]

    return wages_after_tax


def bonus():
    """
    利息=本金*（（1+月化利率）^月份-1）
    :return:到退休时每份理财所得利息列表
    """
    # 各月理财的存储时间（月）
    time = [i for i in range(work_year * 12)]  # 工作年份*12为总工作月份
    time.reverse()  # 逆序排列

    # 理财投入工资占比
    bonus_input_increase_year = int(math.ceil((bonus_input_increase_max - bonus_input_ori) / bonus_input_increase))
    bonus_input_percent = [bonus_input_ori + bonus_input_increase * i for i in range(bonus_input_increase_year)]
    bonus_input_percent += [bonus_input_ori + bonus_input_increase * bonus_input_increase_year] * (work_year - bonus_input_increase_year)

    # 每月工资*投资比例，真正每月的投资本金
    bonus_input = [wage_monthly * bonus_input_percent_monthly for wage_monthly, bonus_input_percent_monthly in
                   zip(wage_list, bonus_input_percent)]

    # 本金扩展为每年12个月
    bonus_input *= 12
    bonus_input.sort()

    # 分别计算每个月存入所产生的复利
    bonus_all = [x * ((1 + monthly_yield) ** y - 1) for x, y in zip(bonus_input, time)]
    return bonus_all


wage_list = wage()  # 初始化工资
bonus_list = bonus()  # 初始化利息
wage_value = sum(wage_list) * 12  # 工资求和
bonus_value = sum(bonus_list)  # 利息求和
total = wage_value + bonus_value  # 财产求和

print('工资：{}\n利息：{}\n总计：{}'.format(wage_value, bonus_value, total))
