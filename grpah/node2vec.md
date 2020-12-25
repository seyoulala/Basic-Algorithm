###　node2vec

### 想要解决什么问题？

node2vec希望将顶点的特征构造由领域专家基于经验手动提取转到自动的特征表示学习中来，将节点学习到的embedding用于下游的节点分类任务和链接预测任务。

### 如何学习节点的embedding？

node2vec的基本思路和deepwalk一样，也是借鉴了Word2vec中skipgram的基本思路，通过随机游走采样顶点组成顶点序列，然后将顶点序列作为word2vec中的word sequence采用skipgram的方式进行训练。然后得到每个顶点的embedding。

### 和deepwalk有什么区别？

1.deepwalk中在训练node的embedding的时候为了避免使用sotfmax造成的计算量大的问题，采用的优化方式是分层的softmax，同时在构建二叉树的时候考虑到对于出现越频繁的词，它作为其它词的领居的概率也会越大，那么在树中，从顶点出发的center word访问到该出现频繁的词的路径就应该越短，那么在构建树的时候就可以是用哈夫曼树来进行优化。但是在node2vec中，在训练node的embedding的时候采用的是negative Sample来进行优化。这是第一个不同点。

2.顶点采样策略不同。deepwalk中的采样策略是使用完全无偏的随机游走，这样有个问题就是灵活性不足的同时无法捕捉到网络的结构特征，从而造成顶点的embedding表示能力不足。node2vec的作者通过对社交网络的观察，发现网络中有两种结构模式，首先是homophily。在这种模式下，在相同的community中的顶点之间彼此的连接都很紧密，那么这些顶点之后学出来的emb应该是相似的，同时还有一种模式是structural equivalence，这种模式下，两个顶点属于不同的community，但是两个顶点的领居节点的结构都很相似，embedding也应该接近。node2vec通过参数p和q来产生一种有偏的随机游走，使得模型能够捕捉到网络不同的结构，增强学出来的顶点embedding的表达能力

### random walk的优势?

对比与单纯的使用dfs/bfs,随机游走有以下几点好处:

1. 空间复杂度低，计算效率比较高。空间复杂度主要是存储顶点的一度领居为0(E),对于二阶随机游走，空间复杂度近似为0(a^2|V|),其中a为graph中节点度的平均值。
2. 时间复杂度相对低。在采样生成顶点序列的过程中利用图的连通性，可以重利用一个顶点序列中以不同源顶点开头的样本序列。比如一个长度为L的序列，我们可以生成k个L-k个顶点的样本序列。{ u, s 4, s 5, s 6, s 8, s 9} ，以u为源顶点，N(s4,s5,s6),以s4为源顶点,N(s5,s6,s7),以s5为源顶点,N(S6,S8,S9)。因此每次sample的时间复杂度为$O(\frac{l}{k(l-k)})$



### 模型细节

设f(u)为将顶点ｕ映射为embedding向量的映射函数，对于每个顶点ｕ，将Ns(u)定义为通过采样策略Ｓ采样出的顶点ｕ的近邻点集合。

node2vec的优化目标是最大化在给定节点下，其邻居节点出现的概率最大。
$$
max_{f}\sum_{u \in V}{logPr(N_s(u)|f(u))}
$$



为了求解上式优化问题需要两个条件假设

- 条件独立性假设

  在给定源顶点时，其近邻顶点出现的概率与近邻集合中其它顶点无关
  $$
  Ｐr(N_s(u)|f(u)) = \Pi_{n_i \in \N_s(u)}Pr(n_i|f(u))
  $$
  
- 空间对称性假设

  一个顶点作为源顶点和作为目标顶点时共享同一套embedding向量（word2vec中假设）其上式条件概率公式可以表示为以下形式
  $$
  Pr(n_i|f(u)) = \frac{expf(n_i)\cdot(f(u))}{\sum_{v \in V}f(v) \cdot f(u)}
  $$
  

  根据以上两个假设，最终的目标函数的定义为
  $$
  max_{f}{\sum_{u \in V}} \left[ -logZ_u + \sum_{n_i \in N_s(u)}f(n_i)\cdot f(u	) \right]
  $$
  

其中Ｚu是一个归一化公式。读过word2Vec的同学应该知道，计算这个的代价是很高的。需要遍历所有顶点.因此借鉴word2vec来采用负采样进行优化。



<img src="https://pic3.zhimg.com/v2-147bb9aa6cb646c83680e93bcf016c4e_r.jpg" style="zoom: 33%;" />



## 顶点序列采样策略

我们知道Deepwalk是通过无偏的随机游走来采样顶点序列的。但是我们知道，对于顶点附近的邻近顶点，我们希望他们在embedding的空间中距离是比较接近，体现一种同质性。同时对于结构相近的顶点，我们也希望他们在embedding的空间是邻近的，体现一种同构性。node2vec中顶点序列的采样也是通过随机游走进行采样的，只是其游走是一种有偏的游走。通过参数p和参数q来控制。



node2vec依然采用随机游走的方式获取顶点的近邻序列，不同的是node2vec采用的是一种有偏的随机游走。

给定当前顶点 ![v](https://www.zhihu.com/equation?tex=v) ，访问下一个顶点 ![x](https://www.zhihu.com/equation?tex=x) 的概率为

<img src="https://pic2.zhimg.com/80/v2-84cc0b66ec34043f82649f0d799997e1_hd.jpg" alt="img" style="zoom:50%;" />

![\pi_{vx}](https://www.zhihu.com/equation?tex=%5Cpi_%7Bvx%7D) 是顶点 ![v](https://www.zhihu.com/equation?tex=v) 和顶点 ![x](https://www.zhihu.com/equation?tex=x) 之间的未归一化转移概率， ![Z](https://www.zhihu.com/equation?tex=Z) 是归一化常数。



node2vec引入两个超参数 ![p](https://www.zhihu.com/equation?tex=p) 和 ![q](https://www.zhihu.com/equation?tex=q) 来控制随机游走的策略，假设当前随机游走经过边 ![(t,v)](https://www.zhihu.com/equation?tex=%28t%2Cv%29) 到达顶点 ![v](https://www.zhihu.com/equation?tex=v) 设 ![\pi_{vx}=\alpha_{pq}(t,x)\cdot w_{vx}](https://www.zhihu.com/equation?tex=%5Cpi_%7Bvx%7D%3D%5Calpha_%7Bpq%7D%28t%2Cx%29%5Ccdot+w_%7Bvx%7D) ， ![w_{vx}](https://www.zhihu.com/equation?tex=w_%7Bvx%7D) 是顶点 ![v](https://www.zhihu.com/equation?tex=v) 和 ![x](https://www.zhihu.com/equation?tex=x) 之间的边权，

<img src="https://pic3.zhimg.com/80/v2-0d170e5c120681823ed6880411a0478e_hd.jpg" alt="img" style="zoom:50%;" />

![d_{tx}](https://www.zhihu.com/equation?tex=d_%7Btx%7D) 为顶点 ![t](https://www.zhihu.com/equation?tex=t) 和顶点 ![x](https://www.zhihu.com/equation?tex=x) 之间的最短路径距离。

下面讨论超参数 ![p](https://www.zhihu.com/equation?tex=p) 和 ![q](https://www.zhihu.com/equation?tex=q) 对游走策略的影响

- Return parameter,p

参数![p](https://www.zhihu.com/equation?tex=p)控制重复访问刚刚访问过的顶点的概率。 注意到![p](https://www.zhihu.com/equation?tex=p)仅作用于 ![d_{tx}=0](https://www.zhihu.com/equation?tex=d_%7Btx%7D%3D0) 的情况，而 ![d_{tx}=0](https://www.zhihu.com/equation?tex=d_%7Btx%7D%3D0) 表示顶点 ![x](https://www.zhihu.com/equation?tex=x) 就是访问当前顶点 ![v](https://www.zhihu.com/equation?tex=v) 之前刚刚访问过的顶点。 那么若 ![p](https://www.zhihu.com/equation?tex=p) 较高，则访问刚刚访问过的顶点的概率会变低，反之变高。

- In-out papameter,q

![q](https://www.zhihu.com/equation?tex=q) 控制着游走是向外还是向内，若 ![q>1](https://www.zhihu.com/equation?tex=q%3E1) ，随机游走倾向于访问和 ![t](https://www.zhihu.com/equation?tex=t) 接近的顶点(偏向BFS)。若 ![q<1](https://www.zhihu.com/equation?tex=q%3C1) ，倾向于访问远离 ![t](https://www.zhihu.com/equation?tex=t) 的顶点(偏向DFS)。

下面的图描述的是当从 ![t](https://www.zhihu.com/equation?tex=t) 访问到 ![v](https://www.zhihu.com/equation?tex=v) 时，决定下一个访问顶点时每个顶点对应的 ![\alpha](https://www.zhihu.com/equation?tex=%5Calpha) 。

<img src="https://pic3.zhimg.com/80/v2-a4a45ea71c00a8d725916dcea50f9cea_hd.jpg" alt="img" style="zoom:50%;" />

由上图可知，t －> x1的最短路径为１，所以alpha为１．t->x2的最短路径为２，所以alpha为１\q。



### 学习算法

------

采样出顶点序列之后，学习方式和deepwalk就是一致的了。使用word2vec中的跳字模型skipgram模型去学习embedding。

**node2vec核心算法**

<img src="https://pic4.zhimg.com/80/v2-dae49695db78fda4ff11284e932a7c43_hd.jpg" alt="img" style="zoom: 67%;" />

**注意采样顶点序列的时候不再时随机采样邻近顶点，而是按照概率抽取。node2vec使用时间复杂度为O(1)的alias采样法**[Alias采样法](<https://blog.csdn.net/haolexiao/article/details/65157026>)

因此node2vec算法可以分为三个阶段:1.计算节点间的概率转移矩阵；2.进行随机游走生成节点序列；3.使用随机梯度下降进行参数学习。在这三个步骤中，每个步骤都可以是并行且异步的运行。

### 边的学习

<img src="/Users/eason/Library/Application Support/typora-user-images/image-20201126144704640.png" alt="image-20201126144704640" style="zoom:50%;" />

同时node2vec在学习到顶点的embedding之后提出了以上几种操作来学习顶点对之间边的表示。

```python
import numpy as np

#创建alias采样表
def create_alias_table(area_ratio):
    """

    :param area_ratio: sum(area_ratio)=1
    :return: accept,alias

    采样时分两步走，第一步随机产生一个１~N之间的整数i决定可能
    采样的列，第二步随机产生一个０~1之间的数b.若accept[i]>b,
    那么采样第ｉ列，否则采样alias[i].
    """
    l = len(area_ratio)
    accept, alias = [0] * l, [0] * l
    #设置两个队列
    small, large = [], []
    #将概率发生拉成１*l
    area_ratio_ = area_ratio * l
    for i, prob in enumerate(area_ratio_):
        if prob < 1.0:
            small.append(i)
        else:
            large.append(i)
	
    """
    面积大于１的进入large队列，面积小于１的进入small队列.维护两个数组accept和alias
    
    """
    while small and large:
        small_idx, large_idx = small.pop(), large.pop()
        accept[small_idx] = area_ratio_[small_idx]
        alias[small_idx] = large_idx
        area_ratio_[large_idx] = area_ratio_[large_idx] - \
            (1 - area_ratio_[small_idx])
        if area_ratio_[large_idx] < 1.0:
            small.append(large_idx)
        else:
            large.append(large_idx)

    while large:
        large_idx = large.pop()
        accept[large_idx] = 1
    while small:
        small_idx = small.pop()
        accept[small_idx] = 1

    return accept, alias


def alias_sample(accept, alias):
    """

    :param accept:
    :param alias:
    :return: sample index
    """
    N = len(accept)
    i = int(np.random.random()*N)
    r = np.random.random()
    if r < accept[i]:
        return i
    else:
        return alias[i]

```



### node2vec中同质性和结构性的理解

首先来个结论

- DFS体现同质性
- BFS体现结构性

结构性关注的特定节点在系统中的相对位置（居于中心还是边缘），而不关心节点本身的特有的属性。类似每个品类的热门商品，热销商品，凑单商品等容易有这样的特点。同质性相反，更多关注内容之间本身的相似性，所以同品类，同店铺，同价格区间等内容更容易表现同质性



### 知乎博主解释

作者：Zhihong Deng
链接：https://zhuanlan.zhihu.com/p/68453999

直觉上，我们认为同质性是指微观上，站在结点上来看，相邻的结点应该比较相似，那么 BFS 这种更强调 1 阶邻居的游走方式应该更能表达同质性（比如上图的结点 u 和相邻的 s1, s2, s3, s4）；结构性是指宏观上，俯视整个网络，有着类似连接方式的结点应该比较相似，那么 DFS 这种能探索得更远得游走方式应该对学习结构性更有帮助（比如上图的结点 u 和结点 s6）。

但事实上，论文中给出的结论却是 **DFS擅长学习网络的同质性，BFS擅长学习网络的结构性**。从论文里的 Figure 3 中我们可以直观地进行观察：

![img](https://pic3.zhimg.com/v2-4fa6e257b730c27300547d1ee2428856_b.jpg)

图的上半部分是倾向于 DFS（p=1，q=0.5）的，可以看到，这种方式得到的 embedding 似乎有很好的聚类性质，注意这里要看结点之间的连接而不是在2D平面上的距离，每个簇的边界结点跟内部的联系要比跟外部的联系更多一些。作者认为这反映了网络的同质性；

图的下半部分是倾向于 BFS（p=1，q=2.0），一个很明显的不同就是，这种方式得到的 embedding 似乎是按功能划分的，处于 graph 边缘的结点（黄色）有类似的 embedding，连接 graph 边缘和中心的结点（蓝色，在上半部分中作为簇边界的结点）有类似的 embedding，这些结点并不都是互相连接的，但是 node2vec 得到的 embedding 仍然能学习出这样的信息。作者认为这反映了网络的结构性。

通过这个图，我们再思考一下同质性和结构性的含义，就会发现和直觉上的含义不同了。同质性并不是一个微观上的性质，作者说的同质性是能模型**能找出每个簇的边界**，使得簇内结点彼此联系的紧密程度要超过跟簇外结点的联系，这就要求模型有更大的感受野，DFS 这种能跳出局部的方式就很适合这个要求。

结构性就比较让人疑惑了，Figure 3 给出的关于结构性的表达似乎和我们直觉上差异不大，有着类似连接方式的结点会更相似。但是，BFS竟然能做到这一点？那些 embedding 相似的结点甚至并不相互连接，BFS为什么能有这种效果呢？

这里先给出后面做完实验后，感觉比较合适的一个解释。作者说的结构性并不是宏观上有相似的连接方式，而是指能够**充分学习微观上的局部结构**。比方说结点处于一个三角形连接的内部（很多论文会称之为motif），BFS 会加强对这个三角形的感知，而 DFS 则容易通过连向外界的边跳出去，所以 BFS 对局部结构得学习会比 DFS 好，这也符合对 Figure 3 的观察。**但是**，这并不能解释 Figure 3 中按功能划分结点这个现象，我的结论是：这种现象只能在合适的数据上，在合适的超参设定下被观察到。

## DFS 是否擅长刻画同质性，BFS 是否擅长刻画结构性？为什么？

前面通过 Figure 3 来重新认识了同质性和结构性。但为什么 DFS 会擅长同质性，BFS 会擅长结构性呢？这就得再回顾一下 Figure 2，了解一下 DFS 和 BFS 到底做了什么：

![img](https://pic4.zhimg.com/v2-1333d51e6d70923d54fd056711abecd7_b.jpg)

图中展示的是一次随机游走的中间过程，当前处于结点 v 上，上一步是从结点 t 到结点 v。

- x1 为结点 v 和结点 t 的共同邻居，设置边 v->x1 的权重为 1； 

- t 为前序结点，设置边 v-> t 的权重为返回参数 p：

- - p > 1 则下一步倾向于访问共同邻居；
  - p < 1 则下一步倾向于回到前序结点。

- x2 和 x3 是结点 v 的其他一阶邻居结点，设置边的权重为进出参数 q：

- - q > 1 则下一步倾向于访问共同邻居；
  - q < 1 则下一步倾向于访问其他一阶邻居结点。

通过 p 和 q 这两个参数就可以调整游走的策略从而实现 DFS 或者 BFS。在 node2vec 中： 

- DFS 是 p=1，q=0.5，

- - 此时： P(访问其他一阶邻居结点) > P(返回前序结点)=P（访问共同邻居）

- BFS 是 p=1，q=2.0，

- - 此时：P(访问其他一阶邻居结点) < P(返回前序结点)=P（访问共同邻居）

不妨在想象中检查一下，如果 P(访问其他一阶邻居结点) > P(返回前序结点)=P（访问共同邻居），那么随机游走就有可能一路推进不同的结点，构成一条重复结点较少的路径，确实符合 DFS 的理念。而如果 P(访问其他一阶邻居结点) < P(返回前序结点)=P（访问共同邻居），那么随机游走就有可能在一个较小的连接密集的局部中来会跳，构成一条重复结点较多的路径，这符合 BFS 的理念。

在得到随机游走的路径后，node2vec 就会把结点看作词，像 word2vec 学习词向量那样学习每个结点的 embedding 了。一般会采用 Skip-Gram 模式，也即使用中心词预测上下文，但无论是用 CBOW 还是 Skip-Gram，本质上都是假设一个词应该跟它所在句子的上下文词关系最密切（最相似），这也是我们**理解 DFS 和 BFS 不同的关键**。

- 如果随机游走侧重于 DFS，那么中心结点的上下文就可能同时包含不同阶的邻居；
- 如果随机游走侧重于 BFS，那么中心结点的上下文就可能只包含有共同邻居的1阶邻居。 

因此，侧重于 DFS 的话，即使两个结点不彼此相连，只要它们有共同的1阶2阶邻居，也会得到相似的上下文，从而学到的 embedding 会比较像。这符合我们前面对同质性的分析，具备这种特质的 DFS 可以更好地找到簇的边界。

而侧重于 BFS 的话，处于同一个密集连接的局部的结点会更加相似，因为它们的上下文会有更多的重叠。这符合我们前面对结构性的分析，具备这种性质的 BFS 可以更好地感知结点所处的局部结构。

接下来，尝试用自己构造的网络来实验，看看结果是否会和上述分析一致。为了能观察到期望的结果，构造的网络必须：

1. 有一定的聚簇现象；
2. 包含密集连接的局部结构。

构造的网络比较小，embed 的维数可以直接设置为2，这样可以直接 plot 在 2D 平面上直观地通过距离来衡量结点之间的相似度。随机游走序列的长度设置为10。

首先，测试一下这个像 bridge 一样的网络：

![img](https://pic2.zhimg.com/v2-51d9623bfeb5654abb51e16bc6345915_b.jpg)

这个网络是对称的，有一个中心点 7，左右各有一个三角形局部结构和四边形的密集连接结构。将 node2vec 学到的结点 embedding 画出来：

![img](https://pic2.zhimg.com/v2-ac4c5d3c70f8788c2122d2302363abd1_b.jpg)

我们首先分析一下局部结构，可以看到 BFS 对局部结构非常敏感，同处一个局部结构内的结点的 embedding 几乎相同（比如结点0和1），这与之前的分析一致。另外，我们也可以观察到，比起 DFS，BFS 得到的 embedding 还有个特点，局部结构内的结点跟以外的结点有着明显的划分，即使是相邻结点也可能得到很不一样的 embedding，比如：结点12 是连接两个局部结构的点，在 DFS 中它与相邻的结点10跟11距离较短，而在 BFS 中则相距较远。这个观察其实在一定程度上体现出了 Figure 3 中对结构性的诠释，但是我们也可以看到，处于对称结构另一侧的结点2和结点12同样相距较远，并没能得到像 Figure 3 那么漂亮的结果。

然后再分析一下聚类效果。可以看到 DFS 得到的 embedding 分布比较均匀，不像 BFS 那样会出现比较大的差距。设定的游走序列长度为10，窗口大小为5，在这个网络中相邻结点有类似的上下文的可能性是比较高的，比方说结点10、11和结点12，它们的上下文会比较像，因此 embedding 的结果也会比较像。在 BFS 中上下文不会那么相似，因此 embedding 结果也就会差距更大一些。聚类的话，其实这个网络聚簇现象并不明显，所以 DFS 的结果没有看出有很明显的聚类边界，更倾向于把整个网络分为一个簇；而 BFS 就很明显地把这个网络分为了5个簇，密集连接的部分分到一个簇中，两边的边缘结点各一个簇，两个作为连接枢纽的结点各一个簇。



再测试一下这个像花一样的网络：

![img](https://pic4.zhimg.com/v2-a1c16cbdfcb8d68b48c79a228250f7ff_b.jpg)

这个网络包含两朵分别以结点 0 和结点 19 为中心的花。将 node2vec 学到的结点 embedding 画出来：

![img](https://pic4.zhimg.com/v2-c62f9ea0b7d04675c979c703c42b32bb_b.jpg)

可以看到 DFS 在这个网络中很好地学习到了两个簇（两朵花）的边界，把同一簇的结点 embedding 推到一起，把不同簇之间的距离尽可能拉开。而 BFS 得到的聚类结果就比较糟糕了，可以看到分属两朵花的结点在 embedding 空间中还是有所区分的，但由于 BFS 对局部结构非常敏感，所以在学习 embedding 的拉扯过程中，两个相邻的中心结点 0 和 19 之间的距离无法被推远，这也使得别的结点的 embedding 学习收到影响，无法像 DFS 中那样分散到两个不同的簇中。但是，我们也可以注意到，这种情况下，一些处于边界区域的结点有可能会聚类到一起，比如结点 2 跟结点 29 之间的距离要小于结点 2 跟结点 0 之间的距离。这也在某种程度上体现出了 Figure 3 中表达的结构性，但无法得到那么完美的图像。

通过在这两个网络上进行实验，基本上验证了前面分析的正确性。虽然实验中没能复现出像论文 Figure 3 那么完美的结果，但这并没有否定 node2vec 的效果。一方面，现实中的网络数据不会像这两个网络这么简单，实现不同的任务，使用不同的数据需要的 p 和 q 也不一样，未必要像上面的设置这么极端。另一方面，实际任务中要求的 embedding 不会只要同质性或者只要结构性，一般都是两者兼备。真实数据一般还会包含结点属性和边的属性，这些属性数据对 embedding 的学习也是至关重要的。