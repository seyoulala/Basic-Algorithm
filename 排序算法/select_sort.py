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
    if array is None or len(array) < 2:
        return
    length = len(array)
    for i in range(length - 1):
        min_index = i
        for j in range(i + 1, length):
            if array[j] < array[min_index]:
                min_index = j
        # 将当前位置的数和最小的数字交换
        array[i], array[min_index] = array[min_index], array[i]
    return array

if __name__ == '__main__':
	input_list = list(np.random.randint(0,100,size=100))
	print('排序前',input_list)
	sort = select_sort(input_list)
	print('排序后',sort)
