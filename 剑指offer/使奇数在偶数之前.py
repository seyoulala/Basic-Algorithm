#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-20 17:01:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


class Solution:
    def reOrderArray(self, array):
        if len(array) < 0 or len(array) == []:
            return None
        left = []
        right = []
        for i in range(len(array)):
            if array[i] & 1 != 0:
                left.append(array[i])
            if array[i] & 1 == 0:
                right.append(array[i])
        return left + right


s = Solution()
array = [1, 2, 3, 4, 5, 6, 7, 8]
print(s.reOrderArray(array))
