#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-15 20:47:02
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

"""
HZ偶尔会拿些专业问题来忽悠那些非计算机专业的同学。今天测试组开完会后,他又发话了:在古老的一维模式识别中,
常常需要计算连续子向量的最大和,当向量全为正数的时候,问题很好解决。但是,如果向量中包含负数,是否应该包含某个负数,
并期望旁边的正数会弥补它呢？例如:{6,-3,-2,7,-15,1,2,2},连续子向量的最大和为8(从第0个开始,到第3个为止)。给一个数组，
返回它的最大连续子序列的和，你会不会被他忽悠住？(子向量的长度至少是1)

"""
"""
思路：
1. 若当前和小于0，将下一个值赋值为当前和。
2. 用一个列表来记录当前最大值
"""


class Solution:
    def FindGreatestSumOfSubArray(self, Array):
        if not Array:
            return -1
        # nlargenumber
        largenumber = Array[0]
        ncum = 0
        for i in range(len(Array)):
            if ncum < 0:
                ncum = Array[i]
            else:
                ncum += Array[i]
            if ncum > largenumber:
                largenumber = ncum
        return largenumber



if __name__ == "__main__":
    alist = [1, -2, 3, 10, -4, 7, 2, -5]
    s = Solution()
    print(s.FindGreatestSumOfSubArray(alist))
