#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

class ListNode:
    def __init__(self,x):
        self.val = x
        self.next = None

class Solution:
    def deleteDuplication(self,pHead):
        if pHead is None:
            return  -1
        list_node = []
        while pHead:
            list_node.append(pHead.val)
            pHead = pHead.next
        list_node = list(filter(lambda x:list_node.count(x)==1,list_node))
        dumpy = ListNode(0)
        pre = dumpy
        for i in list_node:
            node = ListNode(i)
            pre.next = node
            pre = pre.next
        return  dumpy.next

    def deleteDuplication2(self,pHead):
        if pHead is None:
            return  -1
        preHead = None
        pNode = pHead
        while pNode !=None:
            needdelete = False
            nextNode = pNode.next
            if nextNode != None and nextNode.val == pNode.val:
                needdelete = True
            if needdelete == False:
                preHead= pNode
                pNode = pNode.next

            else:
                nodeval = pNode.val
                pTobeDelete = pNode
                while pTobeDelete !=None and pTobeDelete.val == nodeval:
                    pTobeDelete = pTobeDelete.next
                if preHead == None:
                    pHead=pTobeDelete
                    pNode = pTobeDelete
                    continue
                else:
                    preHead.next = pTobeDelete
                pNode = preHead
        return  pHead



node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(7)
node4 = ListNode(4)
node5 = ListNode(3)
node6 = ListNode(4)
node7 = ListNode(5)
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = node6
node6.next = node7

s = Solution()
print(s.deleteDuplication(node1).next.next.val)
print(s.deleteDuplication2(node1).next.next.val)




