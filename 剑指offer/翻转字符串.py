#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-03 21:12:03
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
例如，字符序列S=”abcXYZdef”,要求输出循环左移3位后的结果，即“XYZdefabc”

"""
class Solution:
    def LeftRotateString(self, s, n):
        # write code here
        if n == 0:
            return s
        if len(s)<n:
            return ""
        n = n % len(s)
        s = s[n:] + s[:n]
        return s


s = Solution()
print(s.LeftRotateString(',6', 10))
