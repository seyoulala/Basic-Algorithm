#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-04 21:43:54
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
链接：https://www.nowcoder.com/questionTerminal/762836f4d43d43ca9deb273b3de8e1f4
来源：牛客网

LL今天心情特别好,因为他去买了一副扑克牌,发现里面居然有2个大王,2个小王(一副牌原本是54张^_^)...
他随机从中抽出了5张牌,想测测自己的手气,看看能不能抽到顺子,如果抽到的话,他决定去买体育彩票,嘿嘿！！
“红心A,黑桃3,小王,大王,方片5”,“Oh My God!”不是顺子.....LL不高兴了,他想了想,决定大\小 王可以看成任何数字,
并且A看作1,J为11,Q为12,K为13。上面的5张牌就可以变成“1,2,3,4,5”(大小王分别看作2和4),“So Lucky!”。LL决定去买体育彩票啦。
 现在,要求你使用这幅牌模拟上面的过程,然后告诉我们LL的运气如何， 如果牌能组成顺子就输出true，否则就输出false。为了方便起见,你可以认为大小王是0。
"""
"""
思路：5张牌中除了王以外如果有重复的数字肯定不是顺子
先统计王的数量，然后把牌排序，如果后面的数字比前面的数字大1以上，那么就必须用1来补，如果王的数量不够补，那么肯定就不能组成顺子
"""


class Solution:
    def IsContinuous(self, number):
        if len(number) < 5:
            return False
        # 统计0的数量
        num_zero = number.count(0)
        number = sorted(number, reverse=False)
        for i in range(len(number) - 1):
            if number[i] != 0:
                if number[i] == number[i + 1]:
                    return False
                diff = number[i + 1] - number[i]
                num_zero = num_zero - diff + 1
                if num_zero < 0:
                    return False
        return True


s = Solution()
print(s.IsContinuous([0, 3, 1, 6, 4]))
