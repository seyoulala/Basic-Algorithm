#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-10 19:59:13
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

"""
思路：
队列是先进先出，所以就一个栈只负责进，另外一个负责pop。
"""

class Solution:
    def __init__(self):
        self.stack1 = []
        self.stack2 = []

    def push(self, node):
        self.stack1.append(node)

    def pop(self):
        if self.stack1 == [] and self.stack2 == []:
            return None
        elif self.stack2 == []:
            while self.stack1 != []:
                self.stack2.append(self.stack1.pop())
        return self.stack2.pop()


P = Solution()
P.push(10)
P.push(11)
P.push(12)
print(P.pop())
P.push(13)
print(P.pop())
print(P.pop())
print(P.pop())
print(P.pop())
