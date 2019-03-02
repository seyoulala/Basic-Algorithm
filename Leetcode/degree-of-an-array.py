#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-13 21:28:01
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
给定一个非空且只包含非负数的整数数组 nums, 数组的度的定义是指数组里任一元素出现频数的最大值。
你的任务是找到与 nums 拥有相同大小的度的最短连续子数组，返回其长度。

示例 1:
输入: [1, 2, 2, 3, 1]
输出: 2
解释: 
输入数组的度是2，因为元素1和2的出现频数最大，均为2.
连续子数组里面拥有相同度的有如下所示:
[1, 2, 2, 3, 1], [1, 2, 2, 3], [2, 2, 3, 1], [1, 2, 2], [2, 2, 3], [2, 2]
最短连续子数组[2, 2]的长度为2，所以返回2.

"""
"""
思路:
1.建立hash表确定数组的度
2.确定度所对应的数字，确定其在nums中最左索引以及最右索引
3.输出长度最小的子数组
"""


class Solution:

    def findShortestSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        from collections import Counter
        count = Counter(nums)
        max_values = max(count.values())
        if max_values == 1:
            return 1

        degree = []
        length_of_array = []

        for key, values in count.items():
            if values == max_values:
                degree.append(key)
        for key in degree:
            tmp = []
            for i in range(len(nums)):
                if nums[i] == key:
                    tmp.append(i)
                if len(tmp) == max_values:
                    length_of_array.append(len(nums[tmp[0]:tmp[-1] + 1]))
                    # 在这个key中已经是最短的了，结束loop
                    break
        return min(length_of_array)


s = Solution()
print(s.findShortestSubArray([1, 2, 2, 3, 1, 4, 2]))
