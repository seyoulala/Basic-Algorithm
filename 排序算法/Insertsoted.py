# -*- coding: utf-8 -*-
##直接插入排序,每次将一个数据直接插入到一个排好序数组的合适位置.
#当序列接近正序的时候排序最好,0(n),当序列接近反序的时候,时间复杂度为O(n**2)
#在交换的时候需要0(1)一个空间来保存,对于相等的数字不会交换,因此是稳定的排序
def insertSoted(input_list):
	if len(input_list) == 0:
		return []
	sorted_list = input_list
	for i in range(1,len(input_list)):
		tempt = sorted_list[i]
		j = i-1
		while j >= 0 and tempt <sorted_list[j]:
			sorted_list[j + 1] = sorted_list[j]
			j -=1
			sorted_list[j+1] = tempt
		print(sorted_list)
	return sorted_list
if __name__ =='__main__':
	input_list = [6,4,8,9,2,3,1]
	print('排序前',input_list)
	sorted_list = insertSoted(input_list)
	print('排序后',sorted_list)



