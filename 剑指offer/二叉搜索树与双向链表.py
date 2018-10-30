#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

"""
输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的双向链表。要求不能创建任何新的结点，只能调整树中结点指针的指向。

思路:递归法
二叉搜索树的中序遍历后就是按顺序排序的，然后在访问节点的时候搞成双链表
1.将左子树搞成双链表，返回链表头节点
2.如果左子树存在，那么将root节点加到链表尾部
3.将右子树搞成双链表，返回链表头节点
4.右子树存在，将root加上
"""

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def Convert(self, root):
        #递归出口
        if root == None:
            return  None
        if root.left ==None and root.right==None:
            return root

        #将左子树链成双链表,返回链表头节点
        left = self.Convert(root.left)
        p = left

        #判断左子树是否存在，
        if left:
            while left and p.right:
                p = p.right
            p.right = root
            root.left = p

        right = self.Convert(root.right)
        if right:
            right.left = root
            root.right = right

        return  left if left else  root


pNode1 = TreeNode(8)
pNode2 = TreeNode(6)
pNode3 = TreeNode(10)
pNode4 = TreeNode(5)
pNode5 = TreeNode(7)
pNode6 = TreeNode(9)
pNode7 = TreeNode(11)

pNode1.left = pNode2
pNode1.right = pNode3
pNode2.left = pNode4
pNode2.right = pNode5
pNode3.left = pNode6
pNode3.right = pNode7

S = Solution()
newList = S.Convert(pNode1)
print(newList.val)