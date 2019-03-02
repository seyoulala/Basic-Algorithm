#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-14 20:36:51
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$


"""
给定一个非负整数数组 A， A 中一半整数是奇数，一半整数是偶数。
对数组进行排序，以便当 A[i] 为奇数时，i 也是奇数；当 A[i] 为偶数时， i 也是偶数。
你可以返回任何满足上述条件的数组作为答案。


输入：[4,2,5,7]
输出：[4,5,2,7]
解释：[4,7,2,5]，[2,5,4,7]，[2,7,4,5] 也会被接受
"""


class Solution:
    def sortArrayByParityII(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        single = []
        double = []
        tmp = []
        for i in A:
            if i & 1 == 1:
                single.append(i)
            if i & 1 == 0:
                double.append(i)
        i, j = 0, 0
        while i < len(double):
            tmp.append(double[i])
            i += 1
            while j < len(single):
                tmp.append(single[j])
                j += 1
                break
        return tmp

    def sortArrayByParityII1(self, A):
        """
        时间复杂度o(n)
        """
        i, j = 0, 1
        tmp = len(A) * [0]
        for num in A:
            if num & 1 == 0:
                tmp[i] = num
                i += 2
            else:
                tmp[j] = num
                j += 2
        return tmp
