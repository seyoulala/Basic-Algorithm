#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

"""
题目描述:若链表中有环,则给出环的入口节点,若没有环,则给出null

"""
"""
思路:如果环中有n个节点,指针p1先在链表移动n步,然后两个指针以相同的速度移动,
两个指针相遇的地方就是链表中环的入口.所以首先需要知道环中节点的数目.
1.设置两个快慢指针,如果快慢指针相遇,那么相遇的地方一定在环中.比如p1走2x步,p2走x步
2.在相遇的地方设置一个指针,然后走,当回到原位置时,记录走过的步数k,步数就是环中的节点数,相当于快指针多走了一圈
3.然后将一个指针设置为头指针,其中一个指针不动,两个指针同时走,相遇的地方就是环的入口节点.
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def EntryNodeOfLoop(self, pHead):
        if pHead is None:
            return None
        Slow = pHead
        Fast = pHead
        while Fast.next:
            Fast = Fast.next.next
            Slow = Slow.next
            # 快慢指针相遇
            if Fast == Slow:
                # 设置一个指向头结点的指针
                Slow2 = pHead
                while Slow2 != Slow:
                    Slow = Slow.next
                    Slow2 = Slow2.next
                return Slow
        return None


node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node4 = ListNode(4)
node5 = ListNode(5)
node6 = ListNode(6)
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = node6
node6.next = node3

s = Solution()
print(s.EntryNodeOfLoop(node1).val)
