#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-16 19:26:20
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
在一个字符串(0<=字符串长度<=10000，全部由字母组成)中找到第一个只出现一次的字符,
并返回它的位置, 如果没有则返回 -1（需要区分大小写）.
"""


class Solution:
    def FirstNotRepeatingChar(self, s):
        # write code here
        if not s:
            return -1
        tmp = {}
        for i in s:
            if i not in tmp.keys():
                tmp[i] = 1
            else:
                tmp[i] += 1
        for k, v in tmp.items():
            if v == 1:
                return s.index(k)
        return -1


if __name__ == "__main__":
    s = Solution()
    print(s.FirstNotRepeatingChar('aasdfjee'))
