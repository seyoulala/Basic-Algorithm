#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-03 21:45:28
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

'''
找出所有和为S的连续正数序列
输出所有和为S的连续正数序列。序列内按照从小至大的顺序，序列间按照开始数字从小到大的顺序
'''

"""
思路:用两个指针begin,end分别表示序列的最小值和最大值，
首先将begin,end初始化为1,2.
如果begin到end的和大于s那么去掉较小的值(增大begin)
想反只需要增加end.

终止条件，begin<(s+1)/2,并且end< s
"""


class Solution:
    def FindContinuousSequence(self, tsum):
        # write code here
        res = []
        for i in range(1, tsum // 2 + 1):
            sumRes = i
            for j in range(i + 1, tsum // 2 + 2):
                sumRes += j
                if sumRes == tsum:
                    res.append(list(range(i, j + 1)))
                    break
                elif sumRes > tsum:
                    break
        return res


s = Solution()
print(s.FindContinuousSequence(100))
