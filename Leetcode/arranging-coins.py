#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-05 22:20:14
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
你总共有 n 枚硬币，你需要将它们摆成一个阶梯形状，第 k 行就必须正好有 k 枚硬币。
给定一个数字 n，找出可形成完整阶梯行的总行数。
n 是一个非负整数，并且在32位有符号整型的范围内

n = 5
硬币可排列成以下几行:
¤
¤ ¤
¤ ¤

因为第三行不完整，所以返回2
"""

import math


class Solution:
    def arrangeCoins(self, n):
        """
        :type n: int
        :rtype: int
        """
        result = math.sqrt(2 * n + 0.25) - 0.5
        return int(result)

    def arrangeCoins1(self, n):
        sum_ = 0
        for i in range(1, n):
            sum_ += i
            if sum_ > n:
                return i - 1
            else:
                continue


s = Solution()
print(s.arrangeCoins1(10))
