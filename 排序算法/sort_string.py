# -*- coding: utf-8 -*-
class Solution:
    def permutation(self,ss):
        if not len(ss):
            return []
        if len(ss) ==1:
            return list(ss)

        charList = list(ss)
        charList.sort()
        pStr = []
        for i in range(len(charList)):
            pStr.append(charList[i])
            if i>0 and charList[i] == charList[i-1]:
                continue
            temp = self.permutation(''.join(charList[i+1:]))
            for j in temp:
                pStr.append(charList[i] +j)
            pStr = list(set(pStr))
            pStr.sort()
        return pStr


if __name__ =='__main__':
    S = Solution()
    print(S.permutation('abc'))
