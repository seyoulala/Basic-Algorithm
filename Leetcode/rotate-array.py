#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-04 21:49:44
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
给定一个数组，将数组中的元素向右移动 k 个位置，其中 k 是非负数。
输入: [1,2,3,4,5,6,7] 和 k = 3
输出: [5,6,7,1,2,3,4]
解释:
向右旋转 1 步: [7,1,2,3,4,5,6]
向右旋转 2 步: [6,7,1,2,3,4,5]
向右旋转 3 步: [5,6,7,1,2,3,4]

"""


class Solution:
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: void Do not return anything, modify nums in-place instead.
        """

        length = len(nums)
        k %= length

        for i in range(k):
            tmp = nums[length - 1]
            for j in range(length)[::-1]:
                nums[j] = nums[j - 1]
            nums[0] = tmp

    def rotate1(self, nums, k):
        length = len(nums)
        k %= length

        while k:
            pop_num = nums.pop()
            nums.insert(0, pop_num)
            k -= 1

    def rotate2(self, nums, k):
        length = len(nums)
        k %= length
        nums[0:length] = nums[-k:] + nums[:-k]
