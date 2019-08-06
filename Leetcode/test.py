# -*- coding: utf-8 -*-
# @Time : 2019/1/22 18:47
# @Author : XuYingHao
# @File : test.py


# def GetLeastNumbers_Solution(tinput, k):
#   if not k or not tinput or k > len(tinput):
#       return []
#   # 先维护一个k大小的大根堆
#   sort_list = tinput[:k]
#   length = len(sort_list)
#   # 从最后一个非叶子节点构造大根堆
#   for i in range(length // 2)[::-1]:
#       Headadjust(sort_list, i, length)
#   for j in tinput[k:]:
#       # 如果j小于于大根堆堆顶元素那么交换，更新大根堆
#       if j < sort_list[0]:
#           sort_list[0] = j
#           # 只需要从头部开始调整
#           Headadjust(sort_list, 0, length)
#   return sort_list


# def Headadjust(array, parent, length):
#   # 从最后一个非叶子节点开始构造大根堆
#   tmp = array[parent]
#   child = 2 * parent + 1
#   while child < length:
#       while child < length - 1 and array[child] < array[child + 1]:
#           child += 1
#       if tmp > array[child]:
#           break
#       array[parent] = array[child]
#       parent = child
#       child = 2 * parent + 1
#   array[parent] = tmp
#   return array
def isSum(array, aim):
    if len(array) == 0 or aim is None:
        return False
    # 创建一个二维表
    array_sum = sum(array)
    length = len(array)
    dp = [[False] * array_sum for i in range(length + 1)]
    dp[length][aim] = True
    for i in range(length)[::-1]:
        for j in range(array_sum)[:-1]:
            dp[i][j] = dp[i + 1][j]
            if j + array[i] <= aim:
                dp[i][j] = dp[i + 1][j] | dp[i + 1][j + array[i]]
    return dp[0][0]


if __name__ == "__main__":
    arr = [1, 4, 8]
    aim = 12
    print(isSum(arr, 5))
