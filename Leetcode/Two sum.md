# Two SUM

### 思路
**使用变量来跟踪进位，从表头开始模拟逐位相加的过程**

<img src="https://leetcode-cn.com/problems/add-two-numbers/Figures/2/2_add_two_numbers.svg" align="middle" />

伪代码如下:

- 将当前列表初始化为返回列表的哑结点(tricks)
- 将进位标志$carry$初始化为0
- 将$p$和$q$分别初始化为链表$l1$和$l2$的头部
- 遍历链表$l1$和$l2$直到到达尾端
   - 将$x$设为节点$p$的值。如果$p$以及到$l1$的末尾，则将其值设置为0。
   - 将$y$设为节点$q$的值。如果$q$以及到$l2$的末尾，则将其值设置为0。
   - 设定$sum=x+y+carry$
   - 更新进位的值,$carry=sum/10$(carry不是0就是1)
   - 创建一个数值为$(sum%10)$的新节点，并将其设置为当前节点的下一个节点，然后将当前节点前进到下一个节点
   - 将$q$$p$前进到下一个节点
 - 检查carry是否为1，如果成立，想链表追加数字1节点
 - 返回链表的头节点(哑结点的下一个节点，这里哑结点也就是虚拟节点)

```python

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        preHead = ListNode(0)
        pNode = preHead
        carry = 0
        while l1 or l2:
            if l1 is not None:
                x = l1.val
            else:
                x= 0
            if l2 is not None:
                y = l2.val
            else:
                y = 0
            sum = x+y+carry
            carry = sum//10
            pNode.next = ListNode(sum%10)
            pNode = pNode.next
            if l1 is not None:
                l1 = l1.next
            if l2 is not None:
                l2 = l2.next
        if carry>0:
            pNode.next = ListNode(1)
        return  preHead.next
```




