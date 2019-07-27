#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-27 17:44:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

'''
输入一个复杂链表（每个节点中有节点值，以及两个指针，
一个指向下一个节点，另一个特殊指针指向任意一个节点），返回结果为复制后复杂链表的head。
思路：
非递归法：（三步法）
1.首先 对原链表进行复制，将复制后的节点链到原节点的后面。
2.链接原节点的random节点
3. 将链表拆分
'''


class RandomListNode:
    def __init__(self, x):
        self.label = x
        self.next = None
        self.random = None


# class Solution:
#     def CloneNode(self, pHead):
#         pnode = pHead
#         pcloneNode = RandomListNode(pHead.label)
#         pcloneNode.next = pnode.next
#         pnode.next = pcloneNode
#         pnode = pcloneNode.next
#     # 链表已经复制好了,只需要判断random指针是否存在
#     # 将复制后的指针的random指针链在原链表random指针后面

#     def connectRandoms(self, pHead):
#         pnode = pHead
#         while pnode:
#             pcloneNode = pnode.next
#             if pnode.random != None:
#                 pcloneNode.random = pnode.random.next
#             pnode = pcloneNode.next
#     # 第三步，拆分指针

#     def ReconnectNodes(self, pHead):
#         pnode = pHead
#         pclonenode = pcloneHead = pnode.next
#         pnode.next = pclonenode.next
#         pnode = pnode.next

#         while pnode:
#             pclonenode.next = pnode.next
#             pclonenode = pclonenode.next
#             pnode.next = pclonenode.next
#             pnode = pnode.next
#         return pcloneHead

#     def Clone(self, pHead):
#         if pHead == None:
#             return None
#         self.CloneNode(pHead)
#         self.connectRandoms(pHead)
#         return self.ReconnectNodes(pHead)

class Solution:
    # 返回 RandomListNode
    def Clone(self, pHead):
        if pHead == None:
            return None
        self.CloneNodes(pHead)
        self.ConnectRandomNodes(pHead)
        return self.ReconnectNodes(pHead)
    # 复制原始链表的每个结点, 将复制的结点链接在其原始结点的后面
    def CloneNodes(self, pHead):
        pNode = pHead
        while pNode:
            pCloned = RandomListNode(0)
            pCloned.label = pNode.label
            pCloned.next = pNode.next
            # pCloned.random = None         #不需要写这句话, 因为创建新的结点的时候,random自动指向None

            pNode.next = pCloned
            pNode = pCloned.next

    # 将复制后的链表中的复制结点的random指针链接到被复制结点random指针的后一个结点
    def ConnectRandomNodes(self, pHead):
        pNode = pHead
        while pNode:
            pCloned = pNode.next
            if pNode.random != None:
                pCloned.random = pNode.random.next
            pNode = pCloned.next

    # 拆分链表, 将原始链表的结点组成新的链表, 复制结点组成复制后的链表
    def ReconnectNodes(self, pHead):
        pNode = pHead
        pClonedHead = pClonedNode = pNode.next
        pNode.next = pClonedHead.next
        pNode = pNode.next

        while pNode:
            pClonedNode.next = pNode.next
            pClonedNode = pClonedNode.next
            pNode.next = pClonedNode.next
            pNode = pNode.next

        return pClonedHead

    ##
    def Clone(self, head):
        nodeList = []  # 存放各个节点
        randomList = []  # 存放各个节点指向的random节点。没有则为None
        labelList = []  # 存放各个节点的值

        while head:
            randomList.append(head.random)
            nodeList.append(head)
            labelList.append(head.label)
            head = head.next
        # random节点的索引，如果没有则为1
        labelIndexList = list(map(lambda c: nodeList.index(c) if c else -1, randomList))

        dummy = RandomListNode(0)
        pre = dummy
        # 节点列表，只要把这些节点的random设置好，顺序串起来就ok了。
        nodeList = list(map(lambda c: RandomListNode(c), labelList))
        # 把每个节点的random绑定好，根据对应的index来绑定
        for i in range(len(nodeList)):
            if labelIndexList[i] != -1:
                nodeList[i].random = nodeList[labelIndexList[i]]
        for i in nodeList:
            pre.next = i
            pre = pre.next
        return dummy.next

node1 = RandomListNode(1)
node2 = RandomListNode(3)
node3 = RandomListNode(5)
node1.next = node2
node2.next = node3
node1.random = node3

S = Solution()
clonedNode = S.Clone(node1)
print(clonedNode.random.label)
