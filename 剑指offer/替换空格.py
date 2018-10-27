#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-09 19:36:06
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

"""
指针思路：首先遍历一遍字符串，得到字符串长度以及空格的数目，将字符串长度扩充空格数*2。
设置指针P1指向原字符串尾部，p2指向新字符串尾部，同时向前走，p1遇到空格时，将空格替换为%20，然后P2向前走3布，P1走一步，直到P1与p2重合。

python append()思路
由于list的append是O(1)的时间复杂度，除了扩容所导致的时间损耗，该算法复杂度为O(n)
"""


class Solution:

    def replaceSpaceByAppend(self, s):
        string = list(s)
        repalceString = []
        for i in string:
            if i == ' ':
                repalceString.append("%")
                repalceString.append("2")
                repalceString.append("0")
            else:
                repalceString.append(i)

        return "".join(repalceString)

    def repalceSpaceByanother(self, s):
        if len(s) == None:
            return None
        return s.replace(' ', '%20')


test_string = 'hello world this is a python script'
s = Solution()
print(s.replaceSpaceByAppend(test_string))
print(s.repalceSpaceByanother(test_string))
