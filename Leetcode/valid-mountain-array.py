#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-09 21:40:11
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$


"""
给定一个整数数组 A，如果它是有效的山脉数组就返回 true，否则返回 false。
让我们回顾一下，如果 A 满足下述条件，那么它是一个山脉数组：

A.length >= 3
在 0 < i < A.length - 1 条件下，存在 i 使得：
A[0] < A[1] < ... A[i-1] < A[i]
A[i] > A[i+1] > ... > A[B.length - 1]

示例 2：

输入：[3,5,5]
输出：false
示例 3：

输入：[0,3,2,1]
输出：true

"""

"""
首先找到最大值的索引i，然后判断A[:i]是否递增A[i:]是否递减
"""


class Solution:
    def validMountainArray(self, A):
        """
        :type A: List[int]
        :rtype: bool
        """
        if len(A) < 3:
            return False
        length = len(A) - 1
        max_index = A.index(max(A))
        count = A.count(max(A))
        if count > 1:
            return False
        if max_index == 0 or max_index == length:
            return False
        for i in range(max_index):
            if A[i] >= A[i + 1]:
                return False
        for i in range(max_index, length):
            if A[i] <= A[i + 1]:
                return False
        return True
`

s = Solution()
result = s.validMountainArray([3, 5, 5])
print(result)
