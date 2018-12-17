# -*- coding: utf-8 -*-
# author='xuyinghao'

'''
输入一个字符串,按字典序打印出该字符串中字符的所有排列。
例如输入字符串abc,则打印出由字符a,b,c所能排列出来的所有字符串abc,acb,bac,bca,cab和cba。
结果请按字母顺序输出。
输入描述:
输入一个字符串,长度不超过9(可能有字符重复),字符只包括大小写字母。
'''

"""
思路：字符串的全排列：
参考网址（https://blog.csdn.net/wzy_1988/article/details/8939140）

"""
class Solution:
	def Permutation(self, ss):
		# 递归出口
		if len(ss)==0:
			return  None
		if len(ss) == 1:
			return ss

		strList = list(ss)
		strList.sort()
		#用一个列表存放结果
		result =[]
		for i in range(len(strList)):
			if i >0 and strList[i] == strList[i-1]:
				continue
			tmp = self.Permutation(''.join(strList[:i]+strList[i+1:]))
			for j in tmp:
				result.append(strList[i]+j)
		return result

s = Solution()
print(s.Permutation('abb'))