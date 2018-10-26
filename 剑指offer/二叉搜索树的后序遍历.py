#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

"""
二叉搜索树是指一颗空树或者具有一下性质的树：
1.若任意节点的左子树不空，则左子树上所有节点的值均小于它的根节点的值；
2.若任意节点的右子树不空，则右子树上所有节点的值均大于它的根节点的值；
3.任意节点的左、右子树也分别为二叉查找树；
4.没有键值相等的节点。

思路：
二叉搜索树后续遍历的最后输出一定是根节点,根节点的左子树所有节点值都小于跟节点的值，
右子树所有节点的值都大于根节点值。
1. 首先找到sequence[-1] 确定根节点，然后遍历sequence找到第一次大于root值的index
2. 遍历index后sequence的值，看是否都是大于root，否，那么肯定不是后序遍历的结果
3. 通过index将sequence分为左右子树，然后递归。
4. 考虑两种特殊情况
    root前所有元素小于root.val ,那么没有右子树
    root前所有元素大于root.val ,那么没有左子树
    这两种情况都返回True
"""


class Solution:
    def VerifySquenceOfBST(self, sequence):
        if len(sequence) ==0:
            return False
        length=len(sequence)
        root=sequence[length-1]
        # 在二叉搜索 树中 左子树节点小于根节点
        index = 0
        for i in range(length):
            index = i
            if sequence[i]>root:
                break
        # 二叉搜索树中右子树的节点都大于根节点
        for j  in range(index,length):
            if sequence[j]<root:
                return False
        # 判断左子树是否为二叉树
        left=True
        if  index>0:
            left=self.VerifySquenceOfBST(sequence[0:index])
        # 判断 右子树是否为二叉树
        right=True
        if index<length-1:
            right=self.VerifySquenceOfBST(sequence[index:length-1])
        return left and right


array = [5, 7, 6, 9, 11, 10, 8]
array2 = [4, 6, 7, 5]
array3 = [1, 2, 3, 4, 5]
array4 = []
S = Solution()
print(S.VerifySquenceOfBST(array))
print(S.VerifySquenceOfBST(array2))
print(S.VerifySquenceOfBST(array3))
print(S.VerifySquenceOfBST(array4))




