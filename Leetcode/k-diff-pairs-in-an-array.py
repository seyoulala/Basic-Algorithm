#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-13 20:55:40
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
给定一个整数数组和一个整数 k, 你需要在数组里找到不同的 k-diff 数对。
这里将 k-diff 数对定义为一个整数对 (i, j), 其中 i 和 j 都是数组中的数字，且两数之差的绝对值是 k.

示例 1:
输入: [3, 1, 4, 1, 5], k = 2
输出: 2
解释: 数组中有两个 2-diff 数对, (1, 3) 和 (3, 5)。
尽管数组中有两个1，但我们只应返回不同的数对的数量。
"""

"""
建立hash表，统计整数数组中数字出现的次数。如果k=0的话，那么只能是与自身组成
k-diff对，假如其key对应的values大于1，数量加一，若k不为0，那么判断key+k是否
在hash表中，若在那么数量加1.
"""


class Solution:
    def findPairs(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        from collections import Counter
        if k < 0:
            return 0
        count = Counter(nums)
        result = 0
        for key, values in count.items():
            if k == 0:
                if values > 1:
                    result += 1
            else:
                if (key + k) in count.keys():
                    result += 1
        return result
