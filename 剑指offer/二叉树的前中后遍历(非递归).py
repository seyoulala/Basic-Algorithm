#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

"""
前序遍历：根节点-->左节点-->右节点

中序遍历：左节点-->根节点-->右节点

后序遍历：左节点-->右节点-->根节点

非递归思路：
利用栈的先进后出，需要打印的节点后进。
"""


class TreeNode:

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    # 前序遍历

    def preOrder(self, root):
        if root is None:
            return None
        if not root.left and not root.right:
            return root.val
        stack = [root]
        result = []
        while len(stack) > 0:
            current = stack.pop()
            result.append(current.val)

            # 右节点先进栈
            if current.right:
                stack.append(current.right)

            # 左孩子进栈
            if current.left:
                stack.append(current.left)
        return result

    # 中序遍历
    def MinOrder(self, root):
        if root is None:
            return None
        if not root.left and not root.right:
            return root.val
        # 左节点不断入栈，直到没有左节点,然后指针指向右指针
        stack = []
        result = []
        while stack or root:
            # 左节点不断入栈，直到没有左节点
            if root:
                stack.append(root)
                root = root.left
            # pop出栈定元素，指针指向右指针
            else:
                current = stack.pop()
                result.append(current.val)
                root = current.right
        return result

    # 后序遍历
    """
    
    """
    def posorder(head):
        if head is None:
            return
        helper1 = []
        helper2 = []
        result = []
        helper1.append(head)
        while len(helper1) != 0:
            cur = helper1.pop()
            helper2.append(cur.val)
            if cur.left != None:
                helper1.append(cur.left)
            if cur.right != None:
                helper1.append(cur.right)
        while len(helper2) != 0:
            value = helper2.pop()
            result.append(value)
        return result


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


if __name__ == '__main__':
    s = Solution()
    print("----前序遍历-------")
    print(s.preOrder(pNode1))
    print("----中序遍历-------")
    print(s.MinOrder(pNode1))
    print("----后序遍历-------")
    print(s.postOrder(pNode1))
