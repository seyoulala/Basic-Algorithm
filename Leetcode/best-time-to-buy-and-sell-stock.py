#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-28 19:48:18
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
如果你最多只允许完成一笔交易（即买入和卖出一支股票），设计一个算法来计算你所能获取的最大利润。
注意你不能在买入股票前卖出股票。

输入: [7,1,5,3,6,4]
输出: 5
解释: 在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
     注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格。
"""
"""
思路（动态规划问题）
目标是找到两个数i，j使得j-i的差值最大.
保持两个变量，当前最大收益，以及前i-1天的最低买入价格。通过第i天卖出价格减去前i-1天最低买入价格来更新
当前最大收益
"""


class Solution:
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        if len(prices) == 0:
            return 0
        # 当前最大收益
        max_profit = 0
        # 最低价格
        min_prices = max(prices)
        for num in prices:
            if num < min_prices:
                min_prices = num
            # 更新maxprofit
            elif num - min_prices > max_profit:
                max_profit = num - min_prices
        return max_profit
