#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-05 21:55:08
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$


"""
如果数组是单调递增或单调递减的，那么它是单调的。

如果对于所有 i <= j，A[i] <= A[j]，那么数组 A 是单调递增的。 如果对于所有 i <= j，A[i]> = A[j]，那么数组 A 是单调递减的。

当给定的数组 A 是单调数组时返回 true，否则返回 false
"""
"""
法一：时间复杂度O(n),空间复杂度O(1)。两次遍历
"""


class Solution:
    def isMonotonic(self, A):
        """
        :type A: List[int]
        :rtype: bool
        """
        ascending = True
        length = len(A)
        for i in range(length - 1):
            if A[i] > A[i + 1]:
                ascending = False

        desascending = True
        for i in range(length - 1):
            if A[i] < A[i + 1]:
                desascending = False

        result = ascending or desascending
        return result
