# -*- coding: utf-8 -*-
import time
import numpy as np


def HeadSort(input_list):
	'''
	函数说明:堆排序（升序）
	Author:
		www.cuijiahua.com
	Parameters:
		input_list - 待排序列表
	Returns:
		sorted_list - 升序排序好的列表
	'''

	def HeadAdjust(input_list, parent, length):
		'''
		函数说明:堆调整，调整为最大堆
		Author:
			www.cuijiahua.com
		Parameters:
			input_list - 待排序列表
			parent - 堆的父结点
			length - 数组长度
		Returns:
			无
		'''
		temp = input_list[parent]
		child = 2 * parent + 1

		while child < length:
			if child + 1 < length and input_list[child] < input_list[child + 1]:
				child += 1
			if temp >= input_list[child]:
				break

			input_list[parent] = input_list[child]

			parent = child
			child = 2 * parent + 1
		input_list[parent] = temp

	if len(input_list) == 0:
		return []
	sorted_list = input_list
	length = len(sorted_list)

	for i in range(0, length // 2 + 1)[::-1]:
		HeadAdjust(sorted_list, i, length)

	for j in range(1, length)[::-1]:
		sorted_list[j],sorted_list[0] = sorted_list[0],sorted_list[j]
		HeadAdjust(sorted_list, 0, j)
		# print('第%d趟排序:' % (length - j), end='')
		# print(sorted_list)
	return sorted_list


if __name__ == "__main__":
	start = time.clock()
	input_list = np.random.randint(low=1,high=1000,size=1000) #选取1000个标准正态分布的值
	# input_list = [1,3,4,5,2,6,9,7,8,0]
	print('排序前:', input_list)
	# print(np.shape(input_list))
	sorted_list = HeadSort(input_list)
	print('排序后:', sorted_list)
	end = time.clock()
	print('Running time %f s'%(end - start))

