#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-09 20:06:50
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


class ListNode:
    def __init__(self, x=None):
        self.val = x
        self.next = None


class Solution:
    def PrintListNode(self, ListNode):
        if ListNode == None:
            return []
        stack = []
        pNode = ListNode
        while pNode:
            stack.append(pNode.val)
            pNode = pNode.next
        return stack


s = Solution()
node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node4 = ListNode(4)
node5 = ListNode(5)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5

print(s.PrintListNode(node1))
