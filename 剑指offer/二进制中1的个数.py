#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-16 20:51:54
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


class Solution:
    def Numberofone(self, number):
        if number < 0:
            number = number & 0xffffffff  # python中负数用补码表示，通过与oxffffffff相与 消除负数影响。
        count = 0
        while number:
            count += 1
            number = number & (number - 1)
        return count

    def Numberofone2(self, number):
        if number < 0:
            number = number & 0xffffffff
        s = bin(number)
        return s.count('1')


s = Solution()
print(s.Numberofone2(3))
print(s.Numberofone(3))
