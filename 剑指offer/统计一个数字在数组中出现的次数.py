#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-17 16:39:21
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
统计一个数字在排序数组中出现的次数
"""
"""
看到数组是有序的首先要想到二分查找。找到数字在数组中的位置，然后前后搜索
"""


class Solution:
    def GetNumberOfK(self, data, k):
        # write code here
        if not data:
            return 0
        end = len(data)
        index = self.BinarySearch(data, k)
        if index == -1:
            return 0
        count = 1
        if index > 0:
            for i in range(index)[::-1]:
                if data[i] == k:
                    count += 1
            for i in range(index + 1, end):
                if data[i] == k:
                    count += 1
        return count

    def BinarySearch(self, data, k):
        start = 0
        end = len(data) - 1
        while start <= end:
            middle = (start + end) // 2
            if data[middle] > k:
                end = middle - 1
            elif data[middle] < k:
                start = middle + 1
            else:
                return middle
        return -1


if __name__ == '__main__':
    s = Solution()
    data = [1, 3, 3, 3, 3, 4, 5]
    print(s.GetNumberOfK(data, 3))
