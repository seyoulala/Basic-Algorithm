# -*- coding: utf-8 -*-

def bubbleSorted(input_list):
	"""
	冒泡升序
	:param input_list: 要排序的列表
	:return: sorted_list:升序排序好的列表
	"""
	if len(input_list)==0:
		return []
	sorted_list = input_list
	for i in range(len(sorted_list) - 1):#控制扫描次数
		bchanged = False
		print("第%d次排序" %(i+1))
		for j in range(len(sorted_list) - 1):
			if sorted_list[j+1] < sorted_list[j]:
				sorted_list[j],sorted_list[j+1] = sorted_list[j+1],sorted_list[j]
				bchanged = True
			print("排序中",sorted_list)
		if not bchanged:
			break
	return sorted_list
	
if __name__ =='__main__':
	input_list = [6,4,8,1,2,3,9]
	sorted_list = bubbleSorted(input_list)
	print('排序后',sorted_list)
