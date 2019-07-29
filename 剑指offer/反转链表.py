#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-20 17:25:05
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def ReversedList(self, pHead):
        if not pHead or pHead.next == None:
            return pHead
        preHead = None
        while pHead:
            tmp = pHead.next  # 当前节点的下一个节点
            pHead.next = preHead  # 当前节点指向前一个节点
            preHead = pHead  # 前一节点移动
            pHead = tmp  # 当前节点更新
        return preHead
    def ReversedList2(self,pHead):
        #将当前链表中值保存在一个栈中，栈是先进后出的，因此可以达到逆序的效果
        if pHead is None or pHead.next is None:
            return pHead
        nodes =[]
        while pHead:
            nodes.append(pHead.val)
            pHead=pHead.next
        dumpy=ListNode(0)
        prehead =dumpy
        while nodes:
            prehead.next=ListNode(nodes.pop())
            prehead = prehead.next
        return dumpy.next



node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node4 = ListNode(4)

node1.next = node2
node2.next = node3
node3.next = node4
if __name__ == "__main__":
    S = Solution().ReversedList2(node1)
    while S:
        print(S.val)
        S = S.next
