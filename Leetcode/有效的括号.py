#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/5/22 下午2:24
# @Author : Ethan
# @Site :
# @File : demo1.py
# @Software: PyCharm

"""
有效的括号配对

思路，利用辅助栈来进行配对
"""


def maxlengstring(string):
	if string is None or len(string)==0:
		return 0
	#辅助栈记录值
	help_value =[]
	#辅助栈来记录索引
	help_index= []
	maxlength = 0
	for index,value in enumerate(string):
		if value=='(':
			help_value.append(value)
			help_index.append(index)
		elif value==')' and len(help_value)!=0 :
			help_value.pop()
			left_index = help_index.pop()
			maxlength = index - left_index +1

	return  maxlength

if __name__ =="__main__":
	string ='(((()))))'
	print(maxlengstring(string))