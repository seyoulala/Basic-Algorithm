# -*- coding: utf-8 -*-
# author='xuyinghao'

class TreeNode:

	def __init__(self,x):
		self.val = x
		self.left = None
		self.right = None

class Solution:

	def levelorder(self,pRoot):
		if pRoot == None:
			return []
		nodes,res = [pRoot],[]
		while nodes:
			#curstack保存当层节点的值，nextstack保存下一层节点
			curStack,nextStack = [],[]
			for node in nodes:
				curStack.append(node.val)
				if node.left:
					nextStack.append(node.left)
				if node.right:
					nextStack.append(node.right)
			res.append(curStack)
			nodes = nextStack
		return  res

