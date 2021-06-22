



[TOC]



# PART1.0 序列到序列问题

在自然语言处理任务中，存在很多序列到序列的问题，比如机器翻译、词性标注、命名实体识别等。这些问题都是希望输入源序列，然后输出相对应的目标序列。通常将源序列$(x_1,x_2,x_3,x_4,..,x_n)$作为观测序列，将需要输出的目标序列作为隐藏序列$(y_1,y_2,y_3,y_4,..,y_n)$



# PART2.0 HMM简要介绍

HMM模型主要描述的是由一系列不可观察的隐藏状态集合产生可观测的观测集合的过程。模型主要是建模可观测的观察序列$x$和隐藏状态$y$之间的联合概率分布$p(x,y)$

<img src="https://pic4.zhimg.com/80/v2-6c6836a4e9804464d15d2d6db0077967_1440w.jpg" alt="img" style="zoom:50%;" />

那么联合概率分布$p(x,y)$如何表示呢？在HMM模型中有两个重要的假设：

1. 观测独立性假设，也就是t时刻的观察值只和t时刻的隐藏状态相关，和之前的隐藏状态都无关；
2. 齐次马尔科夫假设，当前t时刻的隐藏状态只和上一时刻的隐藏状态有关；

通过以上两个假设，将观察序列$x$和隐藏状态序列$y$的联合概率分布$p(x,y)$表示成下式:

![[公式]](https://www.zhihu.com/equation?tex=p%28x%2Cy%29+%3D+p%28y_1%29p%28x_1%7Cy_1%29%5Cprod_%7Bt%3D2%7D%5ET+p%28y_t%7Cy_%7Bt-1%7D%29+p%28x_t%7C+y_t%29+%5C%5C)

其中$p(y_t|y_t-1)$表示的状态转移概率A，$p(x_t|y_t)$表示的是发射概率B，$p(y_1)$表示初始概率π。

- 状态转移概率A是一个m*m的概率转移矩阵，m表示的隐藏状态的数量。其中`A[i][j]`表示的是状态i转移到状态j的转移概率
- 发射概率B是一个m*n的概率发射矩阵，m表示隐藏状态的数量，n表示生成状态的数量。其中`B[i][j]`表示的是状态i生成观测j的发射概率
- π是一个1*m的初始概率，表示的是每种隐藏状态出现在序列开始位置的概率。

在HMM中，主要有三种问题：

1. 概率估计问题；在给定模型参数$(A,B,π)$，估计p(x)出现的概率，也就是$p(x_1,x_2,x_3,x_4,...x_n)$出现的概率
2. inference问题；在给定模型参数$(A,B,π)$，以及观测序列$(x_1,x_2,x_3,x_4,...,x_n)$,估计生成该观测序列最有可能的隐藏状态序列的概率$p(y_1,y_2,y_3,..,y_n)$的概率
3. 概率学习问题；概率学习分两种情况，一种是complete case,也就是观测序列x和隐藏状态序列y都已知的情况下通过极大似然估计去学习模型参数$(A,B,π)$。第二种情况就是只知道观测序列x但是不知道隐藏状态序列y的情况下去估计模型参数$(A,B,π)$，这时候需要使用EM算法来进行参数的估计。



# PART3.0 inference问题

在给定模型参数$(A,B,π)$,以及观测序列$(x_1,x_2,x_3,x_4,...,x_n)$，估计生成该观测序列最有可能的隐藏状态序列的概率$p(y_1,y_2,y_3,..,y_n)$的概率。

## PART3.1 navie 方法

在长度为L的序列中，序列中的每个位置都有可能m种隐藏状态，我们可以枚举出所有可能的状态组合，那么枚举出所有可能的情况的排列组合情况有$m^l$,然后取概率最大的那一条序列作为估计的状态序列。但是这种指数级的复杂度在l比较长的情况下是无法接受的。

## PART3.1 viterbi 算法

基于hmm的条件独立性假设，当前时刻的隐藏状态之和前一个时刻的隐藏状态有关，可以使用动态规划的算法来降低时间复杂度。

![img](https://pic2.zhimg.com/80/v2-36377092a9c15bae6676352002801bd1_1440w.jpg)
$$
p(x,y) = p(y|x)p(x)\\
p(y|x) = \frac{p(x,y)}{p(x)} \\
$$
由贝叶斯公式可得，p(y|x)的条件概率可通过上述式子进行表示，结合p(x,y)的联合概率的表示形式，

$logp(y|x) = log(p(y_1))+log(p(y_1|x_1))+...+log(p(y_n|x_n))+log(p(y_n|y_{n-1})) $

因此，构建一个m*L的矩阵，第j行，k+1列的值由以下公式得到

<img src="/Users/eason/Library/Application%20Support/typora-user-images/image-20210401094903484.png" alt="image-20210401094903484" style="zoom:50%;" />

其中$p(z_k|z_{k-1})$由状态转移矩阵A得到，$p(x_k|z_k)$由发射矩阵B得到。

在填充好该矩阵的每一个位置时，我们记录每一列最大的值所对应的行数，最后得到一个长为L的最大概率的隐藏序列。通过veterbi算法，可以将时间复杂度从$m^l$降到$m^2l$。

```python
def viterbi(x, pi, A, B):
    """
    x: user input string/sentence: x: "I like playing soccer"
    pi: initial probability of tags
    A: 给定tag, 每个单词出现的概率
    B: tag之间的转移概率
    """
    x = [word2id[word] for word in x.split(" ")]  # x: [4521, 412, 542 ..]
    T = len(x)
    
    dp = np.zeros((T,N))  # dp[i][j]: w1...wi, 假设wi的tag是第j个tag
    ptr = np.array([[0 for x in range(N)] for y in range(T)] ) # T*N
    # TODO: ptr = np.zeros((T,N), dtype=int)
    
    for j in range(N): # basecase for DP算法
        dp[0][j] = log(pi[j]) + log(A[j][x[0]])
    
    for i in range(1,T): # 每个单词
        for j in range(N):  # 每个词性
            # TODO: 以下几行代码可以写成一行（vectorize的操作， 会使得效率变高）
            dp[i][j] = -9999999
            for k in range(N): # 从每一个k可以到达j
                score = dp[i-1][k] + log(B[k][j]) + log(A[j][x[i]])
                if score > dp[i][j]:
                    dp[i][j] = score
                    ptr[i][j] = k
    
    # decoding: 把最好的tag sequence 打印出来
    best_seq = [0]*T  # best_seq = [1,5,2,23,4,...]  
    # step1: 找出对应于最后一个单词的词性
    best_seq[T-1] = np.argmax(dp[T-1])
    
    # step2: 通过从后到前的循环来依次求出每个单词的词性
    for i in range(T-2, -1, -1): # T-2, T-1,... 1, 0
        best_seq[i] = ptr[i+1][best_seq[i+1]]
        
    # 到目前为止, best_seq存放了对应于x的 词性序列
    for i in range(len(best_seq)):
        print (id2tag[best_seq[i]])
```

# PART4.0 概率估计问题

HMM的概率估计问题是给定模型参数的情况下，估计观测序列出现的概率。对于$p(x_1,x_2,..x_n)$，通过边缘化![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28x%29+%26%3D+p%28x_0%2C+x_1%2C+x_2%2C+%5Cdots+x_T%29+%5C%5C+%26%3D+%5Csum_%7By_0%3D+1%7D%5EK+%5Csum_%7By_1%3D+1%7D%5EK+%5Ccdots+%5Csum_%7By_T%3D+1%7D%5EK+p%28x_0%2C+x_1%2C+x_2%2C+%5Cdots+x_T%2C+y_0%2C+y_1%2C+y_2%2C+%5Cdots+y_T%29+%5Cend%7Baligned%7D+%5C%5C)

可以看到通过枚举出所有可能的隐状态序列下该观测序列出现的概率的时间复杂度为$k^T$,其中k表示隐藏状态的数量，T表示观测序列的长度。

##  PART 4.1native 方法

比如，给定的HMM模型参数已知，求出三天观察是(Dizzy,Cold,Normal)的概率是多少？
相关条件如下图所示：

<img src="https://pic4.zhimg.com/v2-c13d7e306fcc83daceffda6c6d51cd37_b.jpg" alt="img" style="zoom:50%;" />

由上图所示，也就是说，可以写成如下代码：

```text
trainsition_probability = [[0.7,0.3],[0.4,0.6]]     
emission_probability = [[0.5,0.4,0.1],[0.1,0.3,0.6]]    
pi = [0.6,0.4]
```

在第一个问题中，我们需要求解出三天观察是(Dizzy,Cold,Normal)的概率是多少？
这里为了演示简单，我只求解出俩天观察为(Dizzy,Cold)的概率是多少！

这个问题太好求解了，最暴力的方法就是将路径全部遍历一遍。下面尽可能通俗易懂的说明一下：
首先画出时间序列状态图如下：

<img src="https://pic3.zhimg.com/v2-ca2964cea9e5aeb09fc74aef9004ad62_b.jpg" alt="img" style="zoom:50%;" />

下面，我详细走一遍一条路径的暴力算法，这样既可以避开公式的晦涩，也不失正确性。其它路径完全类似
第一天为Healthy的概率为：0.6

在第一天为Healthy的基础上，观察为Dizzy的概率为：P（Dizzy|Healthy）=0.6*P(Healthy->Dizzy)=0.6**0.1=0.06

然后求出在第一天为Healthy的基础上，并且第一天表现为Dizzy的前提下，第二天也为Healthy的概率为：
P(Healthy|Healthy,Dizzy)=0.06*p(Healthy->Healthy)  = P(Dizzy|healthy)*07 = 0.06**0.7*

*上面求完的时候，代表下图中的红线已经转移完了。*

<img src="https://pic2.zhimg.com/v2-08380147d9bb3dccab8b8133de25fcb1_b.jpg" alt="img" style="zoom:67%;" />

**好，那么当在前面基础上，第二天观察为Cold的概率为：**
*P(Cold|(Healthy,Dizzy),(Healthy)) = P(Healthy|Healthy,Dizzy)*0.4 = 0.06*0.7*0.4
现在我们已经完成一条路径的完整结果了。

就是在第一天隐含状态为Healthy和第二天隐含状态为Healthy的基础上，观察序列为Dizzy，Cold的概率为
P（Dizzy,Cold|Healthy,Healthy） = 0.06*0.7*0.4=0.0168

那么同理，我们就可以求出其它三条路径。
（1）在第一天隐含状态为Healthy和第二天隐含状态为Fever的基础上，观察序列为Dizzy，Cold的概率
（2）在第一天隐含状态为Fever和第二天隐含状态为Healthy的基础上，观察序列为Dizzy，Cold的概率
（3）在第一天隐含状态为Fever和第二天隐含状态为Fever的基础上，观察序列为Dizzy，Cold的概率

**将上述四种情况的概率值累加起来就是观察序列[Dizzy,Cold]出现的概率**

##  PART 4.2 forward方法

通过暴力枚举出所有隐藏状态下观察序列出现的概率的时间复杂度太高。那么如何解决呢？可以通过前向算法来解决，该方法也是一个动态规划算法。

前向算法的定义如下:给定观察序列(x1,x2,x3,x4,.....,xn)以及t时刻下的隐藏状态的联合概率$\alpha_{i}(T)=p(x_1,x_2,x_3,..,x_n,y_t=i)$

由于我们的目标是推导出动态规划中的状态转移方程，即找到当前时刻![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_i%28t%29)与![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_j%28t-1%29)的关系，所以我们需要凑出这个两者之间的关系，根据前向算法中定义的联合概率公式：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Calpha_i%28t%29+%26%3D+p%28x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_t%2C+y_t%3Di%29+%5C%5C+++++%26%3D+%5Csum_%7Bj%3D1%7D%5EK+p%28x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2C+x_t%2C+y_%7Bt-1%7D%3Dj%2C+y_t%3Di%29+%5Ccdots+%5Ccdots++1+%5C%5C+++++%26%3D+%5Csum_%7Bj%3D1%7D%5EK+p%28x_t%2C+y_t%3Di+%7C+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29++p%28x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29++%5Ccdots+%5Ccdots++2+%5C%5C+++++%26%3D+%5Csum_%7Bj%3D1%7D%5EK+p%28x_t+%7C+y_t+%3D+i%29+p%28y_t+%3D+i+%7C+y_%7Bt-1%7D%3Dj%29+%5Calpha_j%28t-1%29++%5Ccdots+%5Ccdots++3+%5C%5C+++++%26%3D+B_i%28x_t%29+%5Csum_%7Bj%3D1%7D%5EK+A_%7Bj%2Ci%7D%5Calpha_j%28t-1%29++%5Ccdots+%5Ccdots++4+%5Cend%7Baligned%7D+%5C%5C)

下面针对上述推导公式的每一步进行说明：

- 第一步，是一个边缘概率公式，我们在原始的公式中，新增了一个隐变量![[公式]](https://www.zhihu.com/equation?tex=y_%7Bt-1%7D)，为了与原始概率等价，需要将其积分掉，或者说利用全概率公式，令其取值遍历整个状态的取值![[公式]](https://www.zhihu.com/equation?tex=j%3D1%2C%5Ccdots%2C+K);
- 第二步，贝叶斯公式，但是我们需要注意的是，由于我们的目标是找到![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_i%28t%29)与![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_j%28t-1%29)的关系，因此将贝叶斯公式转换成了如上的形式，根据前向算法的公式定义：![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bt-1%7D%28j%29+%3D+p%28x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29+);
- 第三步， 公式中直接推导出了发射概率和转移概率的形式，下面对其进行推导，又是一通贝叶斯公式：![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28x_t%2C+y_t%3Di+%7C+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29+%26%3D+%5Cfrac%7Bp%28x_t%2C+y_t%3Di%2C+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29%7D%7Bp%28+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29%7D+%5C%5C++++++%26%3D+%5Cfrac%7Bp%28x_t+%7C+y_t%3Di%2C+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29+p%28y_t%3Di%2C+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29%7D%7Bp%28+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29%7D+%5C%5C+++++%26%3D+%5Cfrac%7Bp%28x_t%7C+y_t%3Di%29+p%28y_t%3Di%7C+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29+p%28x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29+%7D%7Bp%28+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29%7D+%5C%5C+++++%26%3D+p%28x_t%7C+y_t%3Di%29+p%28y_t%3Di+%7C+y_%7Bt-1%7D%3Dj%29+%5Cend%7Baligned%7D+%5C%5C) 
- 由于HMM中![[公式]](https://www.zhihu.com/equation?tex=x_t)的输出只与![[公式]](https://www.zhihu.com/equation?tex=y_t)有关,因此，![[公式]](https://www.zhihu.com/equation?tex=p%28x_t%7C+y_t%3Di%29+%3D+p%28x_t+%7C+y_t%3Di%2C+x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_%7Bt-1%7D%2Cy_%7Bt-1%7D%3Dj%29)
- 第四步，由于发射概率![[公式]](https://www.zhihu.com/equation?tex=p%28x_t%7Cy_t%3Di%29)与![[公式]](https://www.zhihu.com/equation?tex=j)无关，所有可以移到外面，最终得到整个状态转移方程

通过图表的形式，可以展示出前向算法的流程如下图所示，在前向算法中运算次数是![[公式]](https://www.zhihu.com/equation?tex=K+%5Ctimes+K)次，因此整个时间复杂度为![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BO%7D%28K%5E2T%29)。 

![img](https://pic1.zhimg.com/v2-516e87c857b982e98050bcef5787f3a0_b.jpg)

最后的观测序列出现的概率计算公式如下所示:

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28x%29+%26%3D+p%28x_0%2C+x_1%2C+x_2%2C+%5Cdots+x_T%29+%5C%5C+++++%26%3D+%5Csum_%7Bi%3D1%7D%5EK+p%28x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_T%2C+y_T%3Di%29+%5C%5C+++++%26%3D+%5Csum_%7Bi%3D1%7D%5EK+%5Calpha_i%28T%29+%5Cend%7Baligned%7D+%5C%5C)

也就是将矩阵的最后一列进行累加得到了最后的结果

```python


def Forward(trainsition_probability,emission_probability,pi,obs_seq):
    """
    :param trainsition_probability:trainsition_probability是状态转移矩阵
    :param emission_probability: emission_probability是发射矩阵
    :param pi: pi是初始状态概率
    :param obs_seq: obs_seq是观察状态序列
    :return: 返回结果
    """
    trainsition_probability = np.array(trainsition_probability)
    emission_probability  = np.array(emission_probability)
    print emission_probability[:,0]
    pi = np.array(pi)
    Row = np.array(trainsition_probability).shape[0]

    F = np.zeros((Row,Col))                      #最后要返回的就是F，就是我们公式中的alpha
    F[:,0] = pi * np.transpose(emission_probability[:,obs_seq[0]])  #这是初始化求第一列,就是初始的概率*各自的发射概率
    print F[:,0]
    for t in range(1,len(obs_seq)):              #这里相当于填矩阵的元素值
        for n in range(Row):                     #n是代表隐藏状态的
            F[n,t] = np.dot(F[:,t-1],trainsition_probability[:,n])*emission_probability[n,obs_seq[t]]   #对应于公式,前面是对应相乘


    return F
```



##  PART 4.3 backword 方法

### **后向算法**

对于后向算法，顾名思义，就是从时间![[公式]](https://www.zhihu.com/equation?tex=T)开始计算，依次计算![[公式]](https://www.zhihu.com/equation?tex=T-1), ![[公式]](https://www.zhihu.com/equation?tex=T-2), ![[公式]](https://www.zhihu.com/equation?tex=%5Ccdots),对于后向算法，也需要根据定义推导出![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_i%28t%29+%3D+p%28x_%7Bt%2B1%7D%2C+x_%7Bt%2B2%7D%2C+%5Ccdots%2Cx_T%7C+y_t%3Di%29)和![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_j%28t%2B1%29+%3D+p%28x_%7Bt%2B2%7D%2C+x_%7Bt%2B3%7D%2C+%5Ccdots%2Cx_T%7C+y_%7Bt%2B1%7D%3Dj%29)的关系,即等式右边要提前算出![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_j%28t%2B1%29),这样计算前一个时刻时![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_i%28t%29)才不会重复计算

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Cbeta_i%28t%29+%26%3D+p%28x_%7Bt%2B1%7D%2C+x_%7Bt%2B2%7D%2C+%5Ccdots%2Cx_T%7C+y_t%3Di%29+%5C%5C++++++%26%3D+%5Csum_%7Bj%3D1%7D%5EK+p%28x_%7Bt%2B1%7D%2C+x_%7Bt%2B2%7D%2C+%5Ccdots%2Cx_T%2Cy_%7Bt%2B1%7D%3Dj%2C%7C+y_t%3Di%29+%5C%5C+++++%26%3D+%5Csum_%7Bj%3D1%7D%5EK+p%28x_%7Bt%2B1%7D%2C+x_%7Bt%2B2%7D%2C+%5Ccdots%2Cx_T%7C+y_%7Bt%2B1%7D%3Dj%2C+y_t%3Di%29+p%28y_%7Bt%2B1%7D%3Dj+%7C+y_t%3Di%29+%5C%5C+++++%26%3D++%5Csum_%7Bj%3D1%7D%5EK+p%28+x_%7Bt%2B2%7D%2C+%5Ccdots%2Cx_T%7C+x_%7Bt%2B1%7D%2C+y_%7Bt%2B1%7D%3Dj%2C+y_t%3Di%29+p%28x_%7Bt%2B1%7D+%7C+y_%7Bt%2B1%7D%3Dj%2C+y_t%3Di%29+p%28y_%7Bt%2B1%7D%3Dj+%7C+y_t%3Di%29+%5C%5C++++++%26%3D+%5Csum_%7Bj%3D1%7D%5EK+p%28+x_%7Bt%2B2%7D%2C+%5Ccdots%2Cx_T%7Cy_%7Bt%2B1%7D%3Dj%29++p%28x_%7Bt%2B1%7D+%7C+y_%7Bt%2B1%7D%3Dj%29+p%28y_%7Bt%2B1%7D%3Dj+%7C+y_t%3Di%29+%5C%5C+++++%26%3D+%5Csum_%7Bj%3D1%7D%5EK++%5Cbeta_j%28t%2B1%29+B_j%28x_%7Bt%2B1%7D%29+A_%7Bi%2C+j%7D+%5Cend%7Baligned%7D+%5C%5C)

通过图表的形式，可以展示出前向算法的流程如下图所示，在前向算法中由于是从右到左依次填充各列的![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_%7Bi%7D%28t%29) 

<img src="https://pic1.zhimg.com/v2-9e3c9cecd902a9569328895037e3c3e8_b.jpg" alt="img" style="zoom: 67%;" />

**根据定义，从T+1到T的部分观测序列其实不存在，所以硬性规定初值$\beta_{j}(t+1)=1$。（这个很重要）**

```python

def Backward(trainsition_probability,emission_probability,pi,obs_seq):
    """
    :param trainsition_probability:trainsition_probability是状态转移矩阵
    :param emission_probability: emission_probability是发射矩阵
    :param pi: pi是初始状态概率
    :param obs_seq: obs_seq是观察状态序列
    :return: 返回结果
    """
    trainsition_probability = np.array(trainsition_probability)
    emission_probability = np.array(emission_probability)
    pi = np.array(pi)                 #要进行矩阵运算，先变为array类型

    Row = trainsition_probability.shape[0]
    Col = len(obs_seq)
    F = np.zeros((Row,Col))
    F[:,(Col-1):] = 1                  #最后的每一个元素赋值为1

    for t in reversed(range(Col-1)):
        for n in range(Row):
            F[n,t] = np.sum(F[:,t+1]*trainsition_probability[n,:]*emission_probability[:,obs_seq[t+1]])


    return F
```



### **前向后向算法**

上述前向算法和后向算法都可以用于计算![[公式]](https://www.zhihu.com/equation?tex=p%28x%29+%3D+p%28x_0%2C+x_1%2C+x_2%2C+%5Cdots+x_T%29)观测序列出现的概率，那么当给定观测序列![[公式]](https://www.zhihu.com/equation?tex=x), 计算在![[公式]](https://www.zhihu.com/equation?tex=t)时刻，![[公式]](https://www.zhihu.com/equation?tex=y_t)的条件概率，即:

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28y_t%3Di%7Cx%29+%26%3D+%5Cfrac%7Bp%28y_t%3Di%2C+x%29+%7D%7Bp%28x%29%7D+%5C%5C+++++%26%5Cpropto+p%28y_t%3Di%2C++x_0%2C+x_1%2C%5Ccdots%2C+x_T%29+%5C%5C+++++%26%3Dp%28y_t%3Di%2C+x_0%2C+x_1%2C+%5Ccdots+x_t%2C+x_%7Bt%2B1%7D%2C+x_%7Bt%2B2%7D%2C+%5Ccdots%2C+x_T%29+%5C%5C+++++%26%3D+p%28x_0%2C+x_1%2C+%5Ccdots+x_t%7C+y_t%3Di%2C+x_%7Bt%2B1%7D%2C+x_%7Bt%2B2%7D%2C+%5Ccdots%2C+x_T%29+p%28x_%7Bt%2B1%7D%2C+x_%7Bt%2B2%7D%2C+%5Ccdots%2C+x_T+%7C+y_t%3Di%29+%5C%5C+++++%26%3D+p%28x_0%2C+x_1%2C+%5Ccdots+x_t%7C+y_t%3Di%29+p%28x_%7Bt%2B1%7D%2C+x_%7Bt%2B2%7D%2C+%5Ccdots%2C+x_T+%7C+y_t%3Di%29+%5C%5C+++++%26%3D+%5Calpha_i%28t%29+%5Cbeta_i%28t%29+%5Cend%7Baligned%7D+%5C%5C)

即通过前向算法和后向算法，可以计算得到在任务时刻隐含状态![[公式]](https://www.zhihu.com/equation?tex=y_t%3Di)的概率(条件概率)



# PART5.0 参数学习

hmm的参数学习问题可以分为两种，一种是当源序列和目标序列都知道的情况下，可以通过极大似然估计来进行估计。极大似然估计的思想总结为"存在即概率最大"。另外一种是当观察序列已知，但隐藏序列不清楚的情况下，通过EM算法来估计

## PART 5.1 complete case

<img src="/Users/eason/Library/Application%20Support/typora-user-images/image-20210331170036486.png" alt="image-20210331170036486" style="zoom:25%;" />

## PART 5.2  Incomplete case







