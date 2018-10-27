# -*- coding: utf-8 -*-


def BinarySearch(input_list, end, values):
    """
    二分查找
    :param input_list:  待插入的有序数组
    :param end:  数组长度
    :param values: 要插入的值
    :return: 目标要插入的值所在数组的坐下标或右下标

    """
    left = 0
    right = end - 1
    while left <= right:
        middle = left + (right - left) // 2
        if input_list[middle] > values:  # 如果中间元素大于目标值，则目标元素在坐边的分割数组中
            right = middle - 1
        else:
            left = middle + 1

    return left if left < end else -1


def insert_sort(input_list):
    if len(input_list) == 0:
        return []
    sort_list = input_list

    for i in range(1, len(input_list)):
        temp = sort_list[i]
        j = i - 1
        insert_index = BinarySearch(sort_list, i, sort_list[i])
        if insert_index != -1:
            while j >= insert_index:
                sort_list[j + 1] = sort_list[j]
                j -= 1
                sort_list[j + 1] = temp
    return sort_list


if __name__ == '__main__':
    input_list = [1, 5, 6, 7, 8, 9, 3, 2, 4]
    print(u'排序前', input_list)
    sort_list = insert_sort(input_list)
    print(u'排序后', sort_list)
