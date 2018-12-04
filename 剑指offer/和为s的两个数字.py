#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-03 21:11:28
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$
"""
输入一个递增排序的数组和一个数字S，在数组中查找两个数,使得他们的和正好是S，
如果有多对数字的和等于S，输出两个数乘积的最小
"""


class Solution:
    def FindNumbersWithSum(self, array, num):
        if len(array) <= 0 or (array[-1] + array[-2]) < num:
            return []
        start = 0
        end = len(array) - 1
        tmp = []
        while start < end:
            sum_ = array[start] + array[end]
            if sum_ > num:
                end -= 1
            elif sum_ < num:
                start += 1
            else:
                tmp.append([array[start], array[end]])
                # 防止时循环
                start += 1
        return tmp


test = []
s = Solution()
print(s.FindNumbersWithSum(test, 0))
