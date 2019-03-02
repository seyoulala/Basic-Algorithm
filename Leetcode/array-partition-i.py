#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-07 21:57:31
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
给定长度为 2n 的数组, 你的任务是将这些数分成 n 对, 例如 (a1, b1), (a2, b2), ..., (an, bn) ，使得从1 到 n 的 min(ai, bi) 总和最大。
"""
"""
因为要求min(ai, bi) 总和最大，因此元组内的值应该是越近越好，这样累积和才会最大.
所以先将原数组排序,然后累加奇数项
"""


class Solution:
    def arrayPairSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums = sorted(nums, reverse=False)
        length = len(nums)
        tuple_nums = []
        for i in range(length - 1):
            if i & 1 != 0:
                continue
            tuple_nums.append(nums[i:i + 2])
        min_sum = sum(map(lambda x: x[0], tuple_nums))
        return min_sum
