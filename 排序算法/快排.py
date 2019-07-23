#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao


"""
"""

def QuickSort(input_list, left, right):
    '''
    函数说明:快速排序（升序）
    Parameters:
        input_list - 待排序列表
    Returns:
        无
    '''
    if left < right:
        split_index = split(input_list,left,right)
        QuickSort(input_list,left,split_index-1)
        QuickSort(input_list,split_index+1,right)


def quick_sort(array):
	if not array:
		return None
	left = 0
	right = len(array)-1
	stack = []
	stack.append(right)
	stack.append(left)
	while stack:
		left = stack.pop()
		right = stack.pop()
		index = split(array,left,right)
		if left<index-1:
			stack.append(index-1)
			stack.append(left)
		if right> index+1:
			stack.append(right)
			stack.append(index+1)



def split(input_list,left,right):
    """

    :param input_list:
    :param left:
    :param right:
    :return: 返回分割点index
    """
    base = input_list[left] #以左边第一个为基准值
    #left指针和right指针重合时，循环结束
    while left < right:
        # 从右向左扫描，找到比base小的数
        while left<right and input_list[right]>=base:
            right -=1
        input_list[left] = input_list[right]
        # 从左边向右边扫描,找到比base大的数
        while left<right and input_list[left]<=base:
            left +=1
        input_list[right] = input_list[left]
    #指针重合，将基准值赋给重合处指针
    input_list[left] = base
    return  left




if __name__ == '__main__':
    input_list = [6, 4, 8, 9, 2, 3, 1]
    print('排序前:', input_list)
    # QuickSort(input_list, 0, len(input_list) - 1)
    # print('排序后:', input_list)
    quick_sort(input_list)
    print("排序后",input_list)