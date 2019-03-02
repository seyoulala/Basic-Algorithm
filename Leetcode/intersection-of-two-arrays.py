#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-04 21:36:49
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
给定两个数组，编写一个函数来计算它们的交集
输入: nums1 = [4,9,5], nums2 = [9,4,9,8,4]
输出: [9,4]
"""

"""
思路:
对num1建立一个hash表。遍历nums2，判断nums2中数字是否出现在nums1中。同时更新nums中key对应的valaus
"""


class Solution:
    def intersect(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        from collections import Counter
        count = Counter(nums1)
        intersect_ = []
        for i in nums2:
            if i in count.keys():
                if count[i] > 0:
                    intersect_.append(i)
                    count[i] -= 1

        return intersect_
