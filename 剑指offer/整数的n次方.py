#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-17 22:18:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


class Solution:
    def Power(self, number, exponent):
        if exponent == 0:
            return 1
        if exponent == 1:
            return number
        if exponent = -1:
            return 1.0 / number

        result = self.Power(number, exponent >> 1)
        result *= result
        if exponent & (0x1) == 1:
            result *= number
        return result
