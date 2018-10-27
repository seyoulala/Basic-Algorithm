# -*- coding: utf-8 -*-
import  time
import numpy as np

def shell_sort(input_list):
	length= len(input_list)
	if length <= 1:
		return input_list
	sort_list = input_list
	step = length //2
	while step > 0:
		for i in range(step,length):
			temp = sort_list[i]
			j = i - step
			while j >=0 and temp <sort_list[j]:
				sort_list[j+step] = sort_list[j]
				j -= step
				sort_list[j+step] = temp
		step //=2 #更新步长
	return sort_list



if __name__ == '__main__':
	start =time.clock()
	input_list = list(np.random.random_integers(1,1000,size=1000000))
	print('排序前',input_list)
	sort_list = shell_sort(input_list)
	print('排序后',sort_list)
	end = time.clock()
	print('Running time %f s'%(end - start))