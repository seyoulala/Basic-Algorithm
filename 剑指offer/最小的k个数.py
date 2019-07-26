class Solution:
    def GetLeastNumbers_Solution(self, tinput, k):
        # write code here
        if not k or not tinput or len(tinput)<k:
            return []
        left = 0
        right = len(tinput)-1
        index = self.partition(tinput,left,right)
        while index != k-1:
            #如果第k个数在前半区
            if k-1 <index:
                index = self.partition(tinput,left,index-1)
            else:
                index = self.partition(tinput,index+1,right)
        output = sorted(tinput[:index+1])
        return output

    def partition(self,array,left,right):
        if left>right:
            return
        base = array[left]
        while left<right:
            while left<right and array[right]>=base:
                right-=1
            array[left] = array[right]
            while left < right and array[left]<=base:
                left+=1
            array[right]=array[left]
        array[left] = base
        return left




#利用大根堆，适合海量数据
def GetLeastNumbers_Solution(tinput, k):
	if not k or not tinput or k > len(tinput):
		return []
	# 先维护一个k大小的大根堆
	sort_list = tinput[:k]
	length = len(sort_list)
	# 从最后一个非叶子节点构造大根堆
	for i in range(length // 2)[::-1]:
		Headadjust(sort_list, i, length)
	for j in tinput[k:]:
		# 如果j小于于大根堆堆顶元素那么交换，更新大根堆
		if j < sort_list[0]:
			sort_list[0] = j
			# 只需要从头部开始调整
			Headadjust(sort_list, 0, length)
	return sort_list


def Headadjust(array, parent, length):
	# 从最后一个非叶子节点开始构造大根堆
	tmp = array[parent]
	child = 2 * parent + 1
	while child < length:
		while child < length - 1 and array[child] < array[child + 1]:
			child += 1
		if tmp > array[child]:
			break
		array[parent] = array[child]
		parent = child
		child = 2 * parent + 1
	array[parent] = tmp
	return array
