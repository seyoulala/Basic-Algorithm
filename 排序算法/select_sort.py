# -*- coding: utf-8 -*-
import  numpy as np
def select_sort(input_list):
	"""
	函数说明；选择排序是从待排序的序列中选出最小的关键字
	如果最小元素不是待排序的第一位则交换。从余下的N-1个元素中
	依次执行以上步骤
	:param input_list: 待排序序列
	:return:排序后的序列
	"""
	length = len(input_list)
	if length <= 1:
		return input_list
	sort_list = input_list
	for i in range(0,length):
		min_index = i #初始化
		for j in range(i+1,length):
			if sort_list[min_index] > sort_list[j]:
				min_index = j
		temp = sort_list[i]
		sort_list[i] = sort_list[min_index]
		sort_list[min_index] = temp

	return sort_list

if __name__ == '__main__':
	input_list = list(np.random.randint(0,100,size=100))
	print('排序前',input_list)
	sort = select_sort(input_list)
	print('排序后',sort)