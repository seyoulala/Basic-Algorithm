#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao


"""
题目:滑动窗口的最大值
"""
class Solution:
    def maxInWindows(self, num, size):
        if  not num or size <=0:
            return []

        i = 0
        length = len(num)
        max_list = []
        while (i+size)<= length:
            window_list = num[i:i+size]
            max_num = max(window_list)
            max_list.append(max_num)
            i+=1
        return max_list

s = Solution()
LIST = [10,14,12,11]
lis = s.maxInWindows(LIST,2)
print(lis)
