# -*- coding: utf-8 -*-
# @Time : 2019/1/23 20:23 
# @Author : XuYingHao
# @File : longest-common-prefix.py

class Solution:
	def longestCommonPrefix(self, strs):
		"""
	    :type strs: List[str]
	    :rtype: str
	    """
		if len(strs) == 0:
			return ""
		if len(strs) == 1:
			return strs[0]
		min_str = sorted(strs, key=len)[0]

		length = len(min_str)
		left = 0
		right = length - 1

		while left <= right:
			middle = (left + right) // 2
			prefix = min_str[:middle + 1]
			if self.is_str(strs, prefix):
				left = middle + 1
			else:
				right = middle - 1

		return min_str[:(left + right) // 2 + 1]

	def is_str(self, strs, prefix):
		for i in strs:
			if not i.startswith(prefix):
				return False
		return True

	def function(self,strs):
		"""
		:type strs: List[str]
		:rtype: str
		"""
		if len(strs)==0:
			return ""
		res=""
		for i in zip(*strs):
			if len(set(i))==1:
				res+=i[0]
			else:
				return res
		return res
