#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  :

"""
定义栈的数据结构，请在该类型中实现一个能够得到栈中所含最小元素的min函数（时间复杂度应为O（1））

思路：
    利用一个数据栈和一个辅助栈，数据都往数据栈压入，当辅助栈为空或者当前压入数小于辅助栈中数时入
    辅助栈，否则辅助栈栈顶元素入栈。

    如： stakck = [3,2,1,5,6]
        minstack = [3,2,1,1,1]
        z这样保证了辅助栈栈顶元素为最小值，且栈长度一致
"""

class Solution:
    def __init__(self):
        self.stack = []
        self.minstack = []

    def push(self, node):
        self.stack.append(node)
        if self.minstack == [] or node < self.min():
            self.minstack.append(node)
        else:
            tmp = self.min()
            self.minstack.append(tmp)

    def pop(self):
        if self.stack == [] or self.minstack == []:
            return None
        self.minstack.pop()
        self.stack.pop()

    def top(self):
        return self.stack[-1]

    def min(self):
        return self.minstack[-1]
