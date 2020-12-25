### Two Sum 问题

```
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那两个整数，并返回他们的数组下标。
你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。
给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]

```

题目中假设了每种输入只会对应一个答案，那么就说明了数组中如果存在这样的两个数，那么答案一定是唯一的。此时我们可以通过

固定住一个数a，然后在数组中找是否存在target-a这个数，如果找到了那么就返回这两个数的下标。这种方法因为要遍历两遍数组因此最坏时间复杂度为n^2。有什么办法可以降低时间复杂度呢？通过我们可以通过空间换时间的方法来降低时间复杂度。比如我们使用hashmap来存储数组中所有的数及其对应的索引，那么在固定住a后，在数组中查找target-a是否存在的时候我们就可以在hashmap中去找，我们知道hashmap中查找一个key是否存在的时间复杂度几乎是O(1)的，所以通过空间换时间，可以将时间复杂度降低到O(n)。代码如下

```python

def twosum(nums,target):
	hepler_map = {}
    #对于有重复的元素，只需要保存该元素最后一次出现的索引
	for index, value in enumerate(nums):
		hepler_map[value] = index
	for index, value in enumerate(nums):
		other_ = target - value
		if other_ in hepler_map.keys() and hepler_map.get(other_) != index:
			other_index = hepler_map.get(other_)
			return [index, other_index]
```



如果题目中没有限制只存在一种答案，但是相同的组合只能出现一次。比如target=9，数组[1,1,2,2,3,3,6,6,7,7],那么此时两个数相加等于9的有[2,7],[3,6]两种情况，同时数组中有重复的数存在，因此如果使用双指针从两头往中间移动的过程中需要跳过重复的数。

```python
    def twoSum1(self, nums: List[int], target: int) -> List[int]:
        nums.sort()
        i=0
        j=len(nums)-1
        res =[]
        while i<j:
            left,right = nums[i],nums[j]
            sum=left+right
            if sum>target:
                #跳过重复的数字
                while i<j and nums[j]==right:
                    j-=1
            elif sum<target:
                while  i<j and nums[i]==left:
                    i+=1
            elif  sum==target:
                res.append([left,right])
                while  i<j and nums[i]==left:
                    i+=1
                while  i<j and nums[j]==right:
                    j-=1
        return res
    
```

### 三数之和

给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。

注意：答案中不可以包含重复的三元组。

``` 
示例：

给定数组 nums = [-1, 0, 1, 2, -1, -4]，

满足要求的三元组集合为：
[
  [-1, 0, 1],
  [-1, -1, 2]
]
```

现在题目要求我们求a+b+c=0,其实就是要我们求a+b=-c,其实也就是a+b=target，这里的target可以是nums中任意一个数组，那么题目就转换成了以nums数组中任意一个数作为target，nums中还有其它两个数加起来等于target么？代码如下:

```python

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        def twoSum1( nums: List[int],strat, target: int) -> List[int]:
            i = strat
            j = len(nums) - 1
            res = []
            while i < j:
                left, right = nums[i], nums[j]
                sum = left + right
                if sum > target:
                    # 跳过重复的数字
                    while i < j and nums[j] == right:
                        j -= 1
                elif sum < target:
                    while i < j and nums[i] == left:
                        i += 1
                elif sum == target:
                    res.append([-target,left, right])
                    while i < j and nums[i] == left:
                        i += 1
                    while i < j and nums[j] == right:
                        j -= 1
            return res
        #bad case 
        if len(nums)<3:
            return []
        min_num = min(nums)
        if min_num>0:
            return []
        result =[]
        nums.sort()
        old = None
        for index,target in enumerate(nums):
            #跳过重复的数
            if target==old:
                continue
            else:
                old = target
            #排序后，从num[index+1:]开始位置找。因为要求不能重复
            tmp = twoSum1(nums,index+1,-target)
            result.extend(tmp)
        return result
```

在for循环中有一个时间复杂度为0(n)的程序，所以最终时间复杂度为0(nlogn+n^2)= 0(n^2).



### 4sum的问题

```
给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在四个元素 a，b，c 和 d ，使得 a + b + c + d 的值与 target 相等？找出所有满足条件且不重复的四元组。

注意：

答案中不可以包含重复的四元组。

示例：

给定数组 nums = [1, 0, -1, 0, -2, 2]，和 target = 0。

满足要求的四元组集合为：
[
  [-1,  0, 0, 1],
  [-2, -1, 1, 2],
  [-2,  0, 0, 2]
]

```

四数问题同样可以转换为3数问题，也就是在数组中找是否存在三个数相加等于target-nums[i]的问题了。修改3数之和的代码。

```python
    def nSum(self,nums,n,start,target):
        # 递归终止条件
        size = len(nums)
        res =[]
        if size<n or n<2:
            return res 
        #如果n=2调用twosum函数
        elif n==2:
            i = start
            j = len(nums) - 1
            while i < j:
                left, right = nums[i], nums[j]
                sum = left + right
                if sum > target:
                    # 跳过重复的数字
                    while i < j and nums[j] == right:
                        j -= 1
                elif sum < target:
                    while i < j and nums[i] == left:
                        i += 1
                elif sum == target:
                    res.append([left, right])
                    while i < j and nums[i] == left:
                        i += 1
                    while i < j and nums[j] == right:
                        j -= 1
        else:
            #n>2 继续求解n-1Sum,同时保存固定住的数字不要重复,下次开始位置从start开始
            old=None
            for index in range(start,size-1):
                if nums[index]==old:
                    continue
                else:
                    old=nums[index]
                sub_problem = self.nSum(nums,n-1,index+1,target-nums[index])
                if sub_problem !=None:
                    for arr in sub_problem:
                        arr.append(nums[index])
                        res.append(arr)

        return  res

    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        n=4
        start=0
        return  self.nSum(nums,n,start,target)
```

