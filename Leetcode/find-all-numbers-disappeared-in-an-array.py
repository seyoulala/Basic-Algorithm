#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-07 21:40:03
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
给定一个范围在  1 ≤ a[i] ≤ n ( n = 数组大小 ) 的 整型数组，数组中的元素一些出现了两次，另一些只出现一次。
找到所有在 [1, n] 范围之间没有出现在数组中的数字。
您能在不使用额外空间且时间复杂度为O(n)的情况下完成这个任务吗? 你可以假定返回的数组不算在额外空间内。
输入:
[4,3,2,7,8,2,3,1]

输出:
[5,6]
"""
"""
方法1.利用集合去重，然后遍历1~n,找出不在集合中的数字

方法2.因为数的范围在【1，n】，将数组中数字作为索引，将索引处的数字取相反数,
然后遍历数组，出现正数的位置为数组中没有出现过的数字

"""


class Solution:
    def findDisappearedNumbers1(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        result = []
        length = len(nums)
        nums = set(nums)
        for i in range(1, length + 1):
            if i not in nums:
                result.append(i)
        return result

    def findDisappearedNumbers2(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        length = len(nums)
        for i in range(length):
            index = nums[i] - 1
            if nums[index] > 0:
                nums[index] = -nums[index]
        return [i + 1 for i in range(length) if nums[i] > 0]
