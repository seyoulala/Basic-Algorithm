#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-17 15:48:51
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
输入两个链表，找出它们的第一个公共结点。
"""
"""
思路:有公共节点的两个链表呈Y形,首先遍历两个链表，记录其长度为m,n
假设m>n，那么先让长的链表走m-n步。然后同时走
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def FindFirstCommonNode(self, phead1, phead2):
        if phead1 is None and phead2 is None:
            return None
        if phead1 is None or phead2 is None:
            return None
        tmphead1 = phead1
        tmphead2 = phead2
        m = 0
        n = 0
        while tmphead1:
            tmphead1 = tmphead1.next
            n += 1
        while tmphead2:
            tmphead2 = tmphead2.next
            m += 1
        if m > n:
            for i in range(m - n):
                phead2 = phead2.next
            while phead1 and phead2:
                if phead1 is phead2:
                    return phead1
                phead1 = phead1.next
                phead2 = phead2.next
        else:
            for i in range(n - m):
                phead1 = phead1.next
            while phead1 and phead2:
                if phead1 is phead2:
                    return phead1
                phead1 = phead1.next
                phead2 = phead2.next
        return None

    def FindFirstCommonNode2(self, phead1, phead2):
        if phead1 is None or phead2 is None:
            return None

        stack1 = []
        stack2 = []

        while phead1:
            stack1.append(phead1)
            phead1 = phead1.next
        while phead2:
            stack2.append(phead2)
            phead2 = phead2.next
        # 记录共同元素
        first = None

        while len(stack1)>0 and len(stack2)>0:
            p1 = stack1.pop()
            p2 = stack2.pop()
            if p1 is p2:
                first = p1
            else:
                break
        return first
