#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

class ListNode:
    def __init__(self,x):
        self.val = x
        self.next = None

class Solution:

    def Merge(self,pHead1,pHead2):
        if pHead1 == None:
            return pHead2
        if pHead2 == None:
            return  pHead1
        pMergeHead = None
        if pHead1.val < pHead2.val:
            pMergeHead = pHead1
            pMergeHead.next = self.Merge(pHead1.next,pHead2)
        else:
            pMergeHead = pHead2
            pMergeHead.next = self.Merge(pHead1,pHead2.next)

        return pMergeHead

if __name__ =='__main__':
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node5 = ListNode(5)

    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5

    node11 = ListNode(3)
    node22 = ListNode(6)
    node33 = ListNode(7)
    node44 = ListNode(8)
    node55 = ListNode(9)

    node11.next = node22
    node22.next = node33
    node33.next = node44
    node44.next = node55

    s = Solution().Merge(node1,node11)
    while s:
        print(s.val)
        s = s.next
