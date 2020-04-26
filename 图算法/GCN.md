### GCN

### 图卷积

![img](https://pic4.zhimg.com/80/v2-4013be2de0ecd8695e30b02b83a5bda3_hd.jpg)图4 图结构实例

### 图的定义

对于图，我们有以下特征定义：

对于图 ![[公式]](https://www.zhihu.com/equation?tex=G%3D%28V%2CE%29) ， ![[公式]](https://www.zhihu.com/equation?tex=V) 为节点的集合， ![[公式]](https://www.zhihu.com/equation?tex=E) 为边的集合，对于每个节点 ![[公式]](https://www.zhihu.com/equation?tex=i) ， 均有其特征 ![[公式]](https://www.zhihu.com/equation?tex=x_i) ，可以用矩阵 ![[公式]](https://www.zhihu.com/equation?tex=X_%7BN%2AD%7D) 表示。其中 ![[公式]](https://www.zhihu.com/equation?tex=N) 表示节点数， ![[公式]](https://www.zhihu.com/equation?tex=D) 表示每个节点的特征数，也可以说是特征向量的维度。

### 图卷积的形象化理解

在一头扎进图卷积公式之前，我们先从其他的角度理解一下这个操作的物理含义，有一个形象化的理解，我们在试图得到节点表示的时候，容易想到的最方便有效的手段就是利用它周围的节点，也就是它的邻居节点或者邻居的邻居等等，这种思想可以归结为一句话：

**图中的每个结点无时无刻不因为邻居和更远的点的影响而在改变着自己的状态直到最终的平衡，关系越亲近的邻居影响越大。**

实际上从邻居节点获取信息的思想在很多领域都有应用，例如word2vec，例如pagerank。关于这个点展开的内容文章[2]有非常详细的解释。

更加细节的如何从傅立叶变换到拉普拉斯算子到拉普拉斯矩阵的数学推倒可以转向博客[7]，为了避免数学功底没有那么强的初学者（比如我）被绕晕，我们先建立大纲，不要太发散。

### 图相关矩阵的定义

那么有什么东西来度量节点的邻居节点这个关系呢，学过图论的就会自然而然的想到邻接矩阵和拉普拉斯矩阵。举个简单的例子，对于下图中的左图（为了简单起见，举了无向图且边没有权重的例子）而言，它的度矩阵 ![[公式]](https://www.zhihu.com/equation?tex=D) ，邻接矩阵 ![[公式]](https://www.zhihu.com/equation?tex=A) 和拉普拉斯矩阵 ![[公式]](https://www.zhihu.com/equation?tex=L) 分别如下图所示，度矩阵 ![[公式]](https://www.zhihu.com/equation?tex=D) 只有对角线上有值，为对应节点的度，其余为0；邻接矩阵![[公式]](https://www.zhihu.com/equation?tex=A)只有在有边连接的两个节点之间为1，其余地方为0；拉普拉斯矩阵 ![[公式]](https://www.zhihu.com/equation?tex=L) 为 ![[公式]](https://www.zhihu.com/equation?tex=D-A) 。但需要注意的是，这是最简单的一种拉普拉斯矩阵，除了这种定义，还有接下来介绍的几种拉普拉斯矩阵。

![img](https://pic1.zhimg.com/80/v2-bc36fb838241c8f1e34b5d913d9b459c_hd.jpg)

图5 一个图的度矩阵，邻接矩阵和拉普拉斯矩阵

### 图卷积的通式

任何一个图卷积层都可以写成这样一个非线性函数：

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7Bl%2B1%7D+%3D+f%28H%5E%7Bl%7D%2CA%29)

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7B0%7D%3DX) 为第一层的输入， ![[公式]](https://www.zhihu.com/equation?tex=X%5Cin+R%5E%7BN%2AD%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=N) 为图的节点个数， ![[公式]](https://www.zhihu.com/equation?tex=D) 为每个节点特征向量的维度， ![[公式]](https://www.zhihu.com/equation?tex=A) 为邻接矩阵，不同模型的差异点在于函数 ![[公式]](https://www.zhihu.com/equation?tex=f) 的实现不同。

下面介绍几种具体的实现，但是每一种实现的参数大家都统称拉普拉斯矩阵。

### 实现一

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7Bl%2B1%7D+%3D+%5Csigma+%28AH%5E%7Bl%7DW%5E%7Bl%7D%29)

其中 ![[公式]](https://www.zhihu.com/equation?tex=W%5E%7Bl%7D) 为第 ![[公式]](https://www.zhihu.com/equation?tex=l) 层的权重参数矩阵， ![[公式]](https://www.zhihu.com/equation?tex=%5Csigma%28%5Ccdot%29) 为非线性激活函数，例如ReLU。

这种思路是基于节点特征与其所有邻居节点有关的思想。邻接矩阵 ![[公式]](https://www.zhihu.com/equation?tex=A) 与特征 ![[公式]](https://www.zhihu.com/equation?tex=H) 相乘，等价于，某节点的邻居节点的特征相加。这样多层隐含层叠加，能利用多层邻居的信息。

但这样存在两个问题：

- **没有考虑节点自身对自己的影响；**
- **邻接矩阵**![[公式]](https://www.zhihu.com/equation?tex=A)**没有被规范化，这在提取图特征时可能存在问题，比如邻居节点多的节点倾向于有更大的影响力。**

因此实现二和实现三针对这两点进行了优化。

### 实现二

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7Bl%2B1%7D+%3D+%5Csigma+%28LH%5E%7Bl%7DW%5E%7Bl%7D%29)

拉普拉斯矩阵 ![[公式]](https://www.zhihu.com/equation?tex=L%3DD-A) ，学名Combinatorial Laplacian，是针对实现一的问题1的改进：

- 引入了度矩阵，从而解决了没有考虑自身节点信息自传递的问题

### 实现三

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7Bl%2B1%7D+%3D+%5Csigma+%28D%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%5Chat%7BA%7DD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7DH%5E%7Bl%7DW%5E%7Bl%7D%29)

对于这里的拉普拉斯矩阵 ![[公式]](https://www.zhihu.com/equation?tex=L%5E%7Bsym%7D%3DD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%5Chat%7BA%7DD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%3DD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%28D-A%29D%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%3DI_n-D%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7DAD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D) ，学名Symmetric normalized Laplacian，也有论文或者博客写 ![[公式]](https://www.zhihu.com/equation?tex=L%3DI_n%2BD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7DAD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D) ， 就是一个符号的差别，但本质上还是实现一的两个问题进行的改进：

- **引入自身度矩阵，解决自传递问题；**
- **对邻接矩阵的归一化操作，通过对邻接矩阵两边乘以节点的度开方然后取逆得到。**具体到每一个节点对 ![[公式]](https://www.zhihu.com/equation?tex=i%EF%BC%8Cj) ，矩阵中的元素由下面的式子给出（对于无向无权图）：

![[公式]](https://www.zhihu.com/equation?tex=L_%7Bi%2C+j%7D%5E%7B%5Cmathrm%7Bsym%7D%7D%3A%3D%5Cleft%5C%7B%5Cbegin%7Barray%7D%7Bll%7D%7B1%7D+%26+%7B%5Ctext+%7B+if+%7D+i%3Dj+%5Ctext+%7B+and+%7D+%5Coperatorname%7Bdeg%7D%5Cleft%28v_%7Bi%7D%5Cright%29+%5Cneq+0%7D+%5C%5C+%7B-%5Cfrac%7B1%7D%7B%5Csqrt%7B%5Coperatorname%7Bdeg%7D%5Cleft%28v_%7Bi%7D%5Cright%29+%5Coperatorname%7Bdeg%7D%5Cleft%28v_%7Bj%7D%5Cright%29%7D%7D%7D+%26+%7B%5Ctext+%7B+if+%7D+i+%5Cneq+j+%5Ctext+%7B+and+%7D+v_%7Bi%7D+%5Ctext+%7B+is+adjacent+to+%7D+v_%7Bj%7D%7D+%5C%5C+%7B0%7D+%26+%7B%5Ctext+%7B+otherwise.+%7D%7D%5Cend%7Barray%7D%5Cright.)

其中 ![[公式]](https://www.zhihu.com/equation?tex=deg%28v_i%29%2Cdeg%28v_j%29) 分别为节点 ![[公式]](https://www.zhihu.com/equation?tex=i%2Cj) 的度，也就是度矩阵在节点 ![[公式]](https://www.zhihu.com/equation?tex=i%2Cj) 处的值。

**可能有一点比较疑惑的是怎么两边乘以一个矩阵的逆就归一化了？**这里需要复习到矩阵取逆的本质是做什么。

我们回顾下矩阵的逆的定义，对于式子 ![[公式]](https://www.zhihu.com/equation?tex=A%2AX%3DB) ，假如我们希望求矩阵X，那么当然是令等式两边都乘以 ![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B-1%7D) ，然后式子就变成了 ![[公式]](https://www.zhihu.com/equation?tex=X%3DA%5E%7B-1%7D%2AA%2AX%3DA%5E%7B-1%7DB) 。

举个例子对于，单个节点运算来说，做归一化就是除以它节点的度，这样每一条邻接边信息传递的值就被规范化了，不会因为某一个节点有10条边而另一个只有1条边导致前者的影响力比后者大，因为做完归一化后者的权重只有0.1了，从单个节点上升到二维矩阵的运算，就是对矩阵求逆了，乘以矩阵的逆的本质，就是做矩阵除法完成归一化。但左右分别乘以节点i,j度的开方，就是考虑一条边的两边的点的度。

常见的拉普拉斯矩阵除了以上举的两种，还有![[公式]](https://www.zhihu.com/equation?tex=L%5E%7Brw%7D%3DD%5E+%7B-1%7D%5Chat%7BA%7D%3DD%5E+%7B-1%7D%28D-A%29%3DI_n-D%5E%7B-1%7DA) 等等[3][4]，归一化的方式有差别，根据论文[5]的实验，这些卷积核的形式并没有一种能够在任何场景下比其他的形式效果好，因此在具体使用的时候可以进行多种尝试，但主流的还是实现三，也就是大多数博客提到的。

### 另一种表述

上面是以矩阵的形式计算，可能会看起来非常让人疑惑，下面从单个节点的角度来重新看下这些个公式（本质是一样的，上文解释过，对于单个节点就是除法，对于矩阵就是乘以度矩阵的逆），对于第 ![[公式]](https://www.zhihu.com/equation?tex=l%2B1) 层的节点的特征 ![[公式]](https://www.zhihu.com/equation?tex=h%5E%7Bl%2B1%7D_i) ，对于它的邻接节点 ![[公式]](https://www.zhihu.com/equation?tex=j%5Cin%7BN%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=N) 是节点 ![[公式]](https://www.zhihu.com/equation?tex=i) 的所有邻居节点的集合，可以通过以下公式计算得到：

![[公式]](https://www.zhihu.com/equation?tex=h%5E%7Bl%2B1%7D_%7Bv_i%7D%3D%5Csigma%28%5Csum_j%7B%5Cfrac%7B1%7D%7Bc_%7Bij%7D%7Dh%5El_%7Bv_j%7DW%5E%7Bl%7D%7D%29)

其中， ![[公式]](https://www.zhihu.com/equation?tex=c_%7Bi%2Cj%7D%3D%5Csqrt%7Bd_id_j%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=j%5Cin+N%7Bi%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=N%7Bi%7D) 为 ![[公式]](https://www.zhihu.com/equation?tex=i) 的邻居节点， ![[公式]](https://www.zhihu.com/equation?tex=d_i%2Cd_j) 为 ![[公式]](https://www.zhihu.com/equation?tex=i%2Cj) 的度，这跟上面的公式其实是等价的，所以有些地方的公式是这个，有些的上面那个。