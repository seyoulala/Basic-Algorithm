#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

"""
树中两个节点的最低公共祖先

思路:从根节点开始,找到根节点到目标节点的路径.这时候两条路径相当于两条有公共节点的链表.
所以最低公共祖先相当于找到倒立的Y形两条链表的第一个公共节点
"""

class TreeNode:
    def __init__(self,x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    #找到根节点到目标节点的路径
    def storeNodes(self, root, targetNode):
        if root is None or targetNode is None:
            return []
        elif root.val == targetNode.val:
            return [[targetNode]]

        stack = [] # 辅助栈
        if root.left:
            path_left = self.storeNodes(root.left,targetNode)
            for node in path_left:
                node.insert(0,root)
                stack.append(node)
        if root.right:
            path_right = self.storeNodes(root.right,targetNode)
            for node in path_right:
                node.insert(0,root)
                stack.append(node)

        return  stack
    #找到两个链表的第一个公共节点
    def lowestCommonAncestor(self, root, A, B):
        if root is None:
            return  False
        left = self.storeNodes(root,A)[0]
        right = self.storeNodes(root,B)[0]

        return [i for i in left if i in right][-1]




node1 = TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)
node4 = TreeNode(4)
node5 = TreeNode(5)
node6 = TreeNode(6)
node7 = TreeNode(7)
node8 = TreeNode(8)
node9 = TreeNode(9)

node1.left = node2
node1.right = node3
node2.left = node4
node2.right = node5
node3.left = node6
node3.right = node7
node5.right = node8
node7.left = node9

s = Solution()
print(s.lowestCommonAncestor(node1,node4,node5).val
      )
