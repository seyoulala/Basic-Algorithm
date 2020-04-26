###　node2vec算法原理



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



![](https://pic3.zhimg.com/v2-147bb9aa6cb646c83680e93bcf016c4e_r.jpg)



## 顶点序列采样策略

我们知道Deepwalk是通过无偏的随机游走来采样顶点序列的。但是我们知道，对于顶点附近的邻近顶点，我们希望他们在embedding的空间中距离是比较接近，体现一种同质性。同时对于结构相近的顶点，我们也希望他们在embedding的空间是邻近的，体现一种同构性。node2vec中顶点序列的采样也是通过随机游走进行采样的，只是其游走是一种有偏的游走。通过参数p和参数q来控制。



node2vec依然采用随机游走的方式获取顶点的近邻序列，不同的是node2vec采用的是一种有偏的随机游走。

给定当前顶点 ![v](https://www.zhihu.com/equation?tex=v) ，访问下一个顶点 ![x](https://www.zhihu.com/equation?tex=x) 的概率为

![img](https://pic2.zhimg.com/80/v2-84cc0b66ec34043f82649f0d799997e1_hd.jpg)

![\pi_{vx}](https://www.zhihu.com/equation?tex=%5Cpi_%7Bvx%7D) 是顶点 ![v](https://www.zhihu.com/equation?tex=v) 和顶点 ![x](https://www.zhihu.com/equation?tex=x) 之间的未归一化转移概率， ![Z](https://www.zhihu.com/equation?tex=Z) 是归一化常数。



node2vec引入两个超参数 ![p](https://www.zhihu.com/equation?tex=p) 和 ![q](https://www.zhihu.com/equation?tex=q) 来控制随机游走的策略，假设当前随机游走经过边 ![(t,v)](https://www.zhihu.com/equation?tex=%28t%2Cv%29) 到达顶点 ![v](https://www.zhihu.com/equation?tex=v) 设 ![\pi_{vx}=\alpha_{pq}(t,x)\cdot w_{vx}](https://www.zhihu.com/equation?tex=%5Cpi_%7Bvx%7D%3D%5Calpha_%7Bpq%7D%28t%2Cx%29%5Ccdot+w_%7Bvx%7D) ， ![w_{vx}](https://www.zhihu.com/equation?tex=w_%7Bvx%7D) 是顶点 ![v](https://www.zhihu.com/equation?tex=v) 和 ![x](https://www.zhihu.com/equation?tex=x) 之间的边权，

![img](https://pic3.zhimg.com/80/v2-0d170e5c120681823ed6880411a0478e_hd.jpg)

![d_{tx}](https://www.zhihu.com/equation?tex=d_%7Btx%7D) 为顶点 ![t](https://www.zhihu.com/equation?tex=t) 和顶点 ![x](https://www.zhihu.com/equation?tex=x) 之间的最短路径距离。

下面讨论超参数 ![p](https://www.zhihu.com/equation?tex=p) 和 ![q](https://www.zhihu.com/equation?tex=q) 对游走策略的影响

- Return parameter,p

参数![p](https://www.zhihu.com/equation?tex=p)控制重复访问刚刚访问过的顶点的概率。 注意到![p](https://www.zhihu.com/equation?tex=p)仅作用于 ![d_{tx}=0](https://www.zhihu.com/equation?tex=d_%7Btx%7D%3D0) 的情况，而 ![d_{tx}=0](https://www.zhihu.com/equation?tex=d_%7Btx%7D%3D0) 表示顶点 ![x](https://www.zhihu.com/equation?tex=x) 就是访问当前顶点 ![v](https://www.zhihu.com/equation?tex=v) 之前刚刚访问过的顶点。 那么若 ![p](https://www.zhihu.com/equation?tex=p) 较高，则访问刚刚访问过的顶点的概率会变低，反之变高。

- In-out papameter,q

![q](https://www.zhihu.com/equation?tex=q) 控制着游走是向外还是向内，若 ![q>1](https://www.zhihu.com/equation?tex=q%3E1) ，随机游走倾向于访问和 ![t](https://www.zhihu.com/equation?tex=t) 接近的顶点(偏向BFS)。若 ![q<1](https://www.zhihu.com/equation?tex=q%3C1) ，倾向于访问远离 ![t](https://www.zhihu.com/equation?tex=t) 的顶点(偏向DFS)。

下面的图描述的是当从 ![t](https://www.zhihu.com/equation?tex=t) 访问到 ![v](https://www.zhihu.com/equation?tex=v) 时，决定下一个访问顶点时每个顶点对应的 ![\alpha](https://www.zhihu.com/equation?tex=%5Calpha) 。

![img](https://pic3.zhimg.com/80/v2-a4a45ea71c00a8d725916dcea50f9cea_hd.jpg)

由上图可知，t －> x1的最短路径为１，所以alpha为１．t->x2的最短路径为２，所以alpha为１\q。



### 学习算法

------

采样出顶点序列之后，学习方式和deepwalk就是一致的了。使用word2vec中的跳字模型skipgram模型去学习embedding。

**node2vec核心算法**

![img](https://pic4.zhimg.com/80/v2-dae49695db78fda4ff11284e932a7c43_hd.jpg)

**注意采样顶点序列的时候不再时随机采样邻近顶点，而是按照概率抽取。node2vec使用时间复杂度为O(1)的alias采样法**[Alias采样法](<https://blog.csdn.net/haolexiao/article/details/65157026>)





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