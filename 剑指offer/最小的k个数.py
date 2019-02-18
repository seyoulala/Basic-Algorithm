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
