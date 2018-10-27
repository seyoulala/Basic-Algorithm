#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-20 17:11:07
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def FindKthToTail(self, phead, k):
        if phead == None:
            return None
        PreHead = phead
        aftHead = phead
        for i in range(k - 1):
            if PreHead.next == None:
                return None
            else:
                PreHead = PreHead.next
        while PreHead.next != None:
            PreHead = PreHead.next
            aftHead = aftHead.next
        return aftHead


node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node4 = ListNode(4)
node5 = ListNode(5)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5

s = Solution()
print(s.FindKthToTail(node1, 2).val)
