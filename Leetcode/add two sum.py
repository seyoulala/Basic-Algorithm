# -*- coding: utf-8 -*-
# author='XuYingHao'

class ListNode:
    def __init__(self,x):
        self.val = x
        self.next = None


class Solution:
    def addTwoNumbers(self,L1,L2):
        preHead = ListNode(0)
        pNode = preHead
        carry = 0
        while L1 or L2:
            if L1 is not None:
                x = L1.val
            else:
                x= 0
            if L2 is not None:
                y = L2.val
            else:
                y = 0
            sum = x+y+carry
            carry = sum//10
            pNode.next = ListNode(sum%10)
            pNode = pNode.next
            if L1 is not None:
                L1 = L1.next
            if L2 is not None:
                L2 = L2.next
        if carry>0:
            pNode.next = ListNode(1)
        return  preHead.next






node1 = ListNode(2)
node2 = ListNode(4)
node3 = ListNode(3)

node4 = ListNode(5)
node5 = ListNode(6)
node6 = ListNode(4)

node1.next = node2
node2.next = node3

node4.next = node5
node5.next = node6
s = Solution()
print(s.addTwoNumbers(node1,node4))
