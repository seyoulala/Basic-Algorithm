#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-21 16:01:23
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


class Solution:
    def test(self, string):
        res = string.split(' ')
        res = res[::-1]
        return ' '.join(res)


s = Solution()
print(s.test('I am a Student.'))
