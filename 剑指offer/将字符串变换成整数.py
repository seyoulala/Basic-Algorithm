#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-09 21:08:01
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
将字符串变成整数,要求不能使用库函数
输入一个字符串,包括数字字母符号,可以为空
如果是合法的数值表达则返回该数字，否则返回0
"""


class Solution:
    def StrToInt(self, s):
        if not s:
            return 0
        # 将字符映射为整数
        dict_ = {str(k): v for k, v in zip(range(10), range(10))}
        num = []
        for i in s:
            if i in dict_.keys():
                num.app end(dict_[i])
            elif i == '+' or i == '-':
                continue
            else:
                return 0
        ans = 0
        for i in num:
            ans = ans * 10 + i
        if s[0] == '-':
            return 0 - ans
        else:
            return ans
