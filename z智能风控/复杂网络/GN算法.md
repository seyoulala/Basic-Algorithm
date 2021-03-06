### Grivan-Newman

GN算法是社区发现算法中最经典的一种算法。属于分裂的自上而下的层次聚类算法。

其主要思想就是，如果除去社区之间连接的边，留下的就是社群。该算法认为，两个社区之间的点的最短路径总是需要通过社区间的连接边。因此中心度越大的边，越可能是不同社区之间的连接边，所以只需要不断的将中心度大的边去掉，就可以得到独立的社区。

算法步骤如下：

1. 计算所有边的边中心度
2. 将边中心度最高的边去掉
3. 重新计算被去掉的边影响的边的边中心度
4. 重复2，3两个步骤直到不连通的社区个数达到预设值。



![img](https://pic2.zhimg.com/80/v2-482a06f68104d321b03d690b90df5da1_1440w.jpg)

如上图所示：方块团体和圆形团体中的点的最短路径总是要经过AB这条边的，因此AB这条边的边中心度会很高，将这条边去掉之后就能将这整个社区分成1#和2#两个团体。



#### 算法优缺点

**优点**

准确度很高

**缺点**

计算复杂度很高，需要制定划分的社区的个数K

