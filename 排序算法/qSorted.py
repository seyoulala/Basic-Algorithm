# -*- coding: utf-8 -*-
import  time
def quick(input_list):
	if len(input_list) <= 1:
		return input_list
	base_num = input_list[0]
	return quick([x for x in input_list[1:] if x <= base_num ]) + [base_num ]+  quick([y for  y in input_list[1:] if y >= base_num])

def quick_sort(input_list,left,right):
	"""
	快速排序
	:param input_list:
	:param left:
	:param right:
	:return:
	"""
	if left < right:
		base_index = division(input_list, left, right)
		quick_sort(input_list, left, base_index - 1)
		quick_sort(input_list, base_index + 1, right)

def division(input_list, left, right):
	"""
	根据left 和right 进行扫描找到base——num
	:param input_list:
	:return: 中间位置索引
	"""
	sort_list = input_list

	base_num = sort_list[left]  # 设置基数
	while left < right:
		while left < right and sort_list[right] >= base_num:
			right -= 1
		sort_list[left] = sort_list[right]  # 将找到的比基数小的数付给left所处位置
		while left < right and sort_list[left] <= base_num:
			left += 1
		sort_list[right] = sort_list[left]
	sort_list[left] = base_num
	return left

if __name__ == '__main__':
	start = time.clock()
	input_list =[2,1,3,3,2,2,9,9,1,7,6,6]
	print('排序前',input_list)
	sort_list= quick(input_list)
	print('排序后',sort_list)
	quick_sort(input_list,0,len(input_list)-1)
	print('排序后',input_list)
	end = time.clock()
	print('Running time:%f s '% ( end - start))