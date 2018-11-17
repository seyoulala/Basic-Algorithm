#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-15 21:17:50
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

"""
输入一个正整数数组，
把数组里所有数字拼接起来排成一个数，打印能拼接出的所有数字中最小的一个。例如输入数组{3，32，321}，
则打印出这三个数字能排成的最小数字为321323。
"""
"""
思路：
根据比较规则，若ab>ba ---> a>b,将数字变成字符串两两比较，将最小的放在最前。
"""


class Solution:
    def PrintMinNumber(self, numbers):
        if not numbers:
            return ""

        if min(numbers)<0:
            return ""

        strnum = list(map(str, numbers))
        # 两两比较
        for i in range(len(strnum)):
            for j in range(i + 1, len(strnum)):
                if strnum[i] + strnum[j] > strnum[j] + strnum[i]:
                    strnum[i], strnum[j] = strnum[j], strnum[i]
        return ''.join(strnum)


if __name__ == "__main__":
    s = Solution()
    numbers = [3, 321, 32]
    print(s.PrintMinNumber(numbers))
