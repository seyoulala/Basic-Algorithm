BFS 的核心思想应该不难理解的，就是把一些问题抽象成图，从一个点开始，向四周开始扩散。一般来说，我们写 BFS 算法都是用「队列」这种数据结构，每次将一个节点周围的所有节点加入队列。

BFS 相对 DFS 的最主要的区别是：**BFS 找到的路径一定是最短的，但代价就是空间复杂度比 DFS 大很多**，至于为什么，我们后面介绍了框架就很容易看出来了

# 一、算法框架

要说框架的话，我们先举例一下 BFS 出现的常见场景好吧，**问题的本质就是让你在一幅「图」中找到从起点** **`start`** **到终点** **`target`** **的最近距离，这个例子听起来很枯燥，但是 BFS 算法问题其实都是在干这个事儿**，把枯燥的本质搞清楚了，再去欣赏各种问题的包装才能胸有成竹嘛。

这个广义的描述可以有各种变体，比如走迷宫，有的格子是围墙不能走，从起点到终点的最短距离是多少？如果这个迷宫带「传送门」可以瞬间传送呢？

再比如说两个单词，要求你通过某些替换，把其中一个变成另一个，每次只能替换一个字符，最少要替换几次？

再比如说连连看游戏，两个方块消除的条件不仅仅是图案相同，还得保证两个方块之间的最短连线不能多于两个拐点。你玩连连看，点击两个坐标，游戏是如何判断它俩的最短连线有几个拐点的？

```c
// 计算从起点 start 到终点 target 的最近距离
int BFS(Node start, Node target) {
    Queue<Node> q; // 核心数据结构
    Set<Node> visited; // 避免走回头路


    q.offer(start); // 将起点加入队列
    visited.add(start);
    int step = 0; // 记录扩散的步数


    while (q not empty) {
        int sz = q.size();
        /* 将当前队列中的所有节点向四周扩散 */
        for (int i = 0; i < sz; i++) {
            Node cur = q.poll();
            /* 划重点：这里判断是否到达终点 */
            if (cur is target)
                return step;
            /* 将 cur 的相邻节点加入队列 */
            for (Node x : cur.adj())
                if (x not in visited) {
                    q.offer(x);
                    visited.add(x);
                }
        }
        /* 划重点：更新步数在这里 */
        step++;
    }
}
```

队列 `q` 就不说了，BFS 的核心数据结构；`cur.adj()` 泛指 `cur` 相邻的节点，比如说二维数组中，`cur` 上下左右四面的位置就是相邻节点；`visited` 的主要作用是防止走回头路，大部分时候都是必须的，但是像一般的二叉树结构，没有子节点到父节点的指针，不会走回头路就不需要 `visited`。

## 二叉树的最小高度

先来个简单的问题实践一下 BFS 框架吧，判断一棵二叉树的**最小**高度，这也是 LeetCode 第 111 题，看一下题目：

<img src="/Volumes/disk2/Basic-Algorithm/image/二叉树最小深度.jpg" alt="img" style="zoom:50%;" />

怎么套到 BFS 的框架里呢？首先明确一下起点 `start` 和终点 `target` 是什么，怎么判断到达了终点？

**显然起点就是** **`root`** **根节点，终点就是最靠近根节点的那个「叶子节点」嘛**，叶子节点就是两个子节点都是 `null` 的节点：

通过判断当前节点的左右节点是否为空来判断是否到达终点；

```python
if root.left if None and root.right is None:
  return depth
```

接下来根据上述框架修改除如下代码：

```python
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: TreeNode) -> int:
        from  collections import deque
        q = deque()
        if root is None:
            return 0
        q.appendleft(root)
        depth=1
        while  len(q)!=0:
            size = len(q)
            # 当前队列中所有节点都要往外扩散
            for i in range(size):
                cur = q.pop()
                #判断是否到到达终点
                if cur.left is None and cur.right is None:
                    return depth
                # 因为是二叉树，所以当前节点的领居就只有左右两个子节点
                if cur.left is not None:
                    q.appendleft(cur.left)
                if cur.right is not None:
                    q.appendleft(cur.right)
            depth+=1
        return depth
```

# 三、解开密码锁的最少次数

<img src="/Volumes/disk2/Basic-Algorithm/image/转动密码锁的次数.jpg" alt="img" style="zoom:50%;" />



假如没有`死亡数字`和`target`的限制，我们可以穷举的方法穷举出所有的可能的组合。一共4个位置，每个位置可以往上或者往下进行波

动，那穷举出来就是`1000,9000,0100,0900,0010,0090,0001,0009`,然后以这些数字为基础再次的进行穷举。画出递归树:

<img src="/Users/eason/Library/Application Support/typora-user-images/image-20201102214358871.png" alt="image-20201102214358871" style="zoom:50%;" />

上图省略了`第2个位置和第3个位置的转动情况`，通过上图我们知道，从`起始位置0000`开始我们在`4`个位置，`每个位置有上下两种拨动操作`的情

况下得到了`8`个拨动的结果，然后以这8个结果，我们又可以在4个位置进行上下两种拨动得到8个结果，结合题目要求给出我们从`起点`

`0000`开始到`终点target`最少的拨动次数，我们可以想到使用`bfs`来进行求解。在套用框架时，我们需要注意以下几种情况:

```
1.重复结果出现造成死循环，如初始0000，等一层所有节点都出队列之后，我们再次拿到了0000,这样就造成了死循环。我们可以使用备忘录来解决这个问题，准备一个visited数组，记录已经生成的结果，待下次出现重复出现相同的结果时，我们就跳过这个结果。
2.如果拨动的结果产生了死亡数字，那么锁就被锁定了，无法继续拨动。翻译过来就是如果拨出了死亡数字，那么就无法以当前这个死亡数字为基础再次进行波动了，也就是我们需要跳过这个结果。解决这个问题我们也可以通过备忘录来解决，但拨出了死亡数字后我们就需要跳过结果
```

通过上述分析，然后结合框架我们就可以写出如下的代码:

```python

```



