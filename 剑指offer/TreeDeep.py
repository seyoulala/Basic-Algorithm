#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

class TreeNode:
    def __init__(self,x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def TreeDepth(self, pRoot):
        # write code here
        # 使用层次遍历
        # 当树为空直接返回0
        if pRoot is None:
            return 0
        count = self.orderbylevel(pRoot)
        return count

    def orderbylevel(self, pRoot):
        # 初始化层数
        deep = 0
        if pRoot == None:
            return 0
        # 初始化一个队列
        alist = []
        alist.append(pRoot)

        # width 记录同层节点的数目
        while len(alist) != 0:
            tmp = []  # 记录同层节点的值
            cur = 0
            width = len(alist)  # 宽度
            while cur<width:
                r = alist.pop(0)
                if r.left is not None:
                    alist.append(r.left)
                if r.right is not None:
                    alist.append(r.right)
                tmp.append(r.val)
                cur+=1
            deep +=1
        return deep

    def Is_Balance(self, pRoot):
        self.flag = True
        if pRoot == None:
            return True
        left = self.TreeDepth(pRoot.left)
        right = self.TreeDepth(pRoot.right)
        if abs(right - left) >1:
            self.flag = False
        return  self.flag



if __name__ =="__main__":
    pNode1 = TreeNode(1)
    pNode2 = TreeNode(2)
    pNode3 = TreeNode(3)
    pNode4 = TreeNode(4)
    pNode5 = TreeNode(5)
    pNode6 = TreeNode(6)
    pNode7 = TreeNode(7)
    pNode8 = TreeNode(8)

    pNode1.left = pNode2
    pNode1.right = pNode3
    pNode2.left = pNode4
    pNode2.right = pNode5
    pNode3.right = pNode6
    pNode5.left = pNode7
    pNode7.left = pNode8

    s =Solution()
    print(s.TreeDepth(pNode1))
    print(s.Is_Balance(pNode1))