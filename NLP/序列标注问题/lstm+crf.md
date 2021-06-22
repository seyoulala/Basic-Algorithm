[TOC]



#  PART 1.0  为什么LSTM+CRF框架？

对于为什么要使用LSTM+crf的框架，对于这个问题，我觉得可以从以下几个角度出发：

1. CRF的feature function是如何设计的？
2. LSTM是否能替代CRF中的feature function中的工作？
3. 序列标注本质上是分类任务，为什么不直接使用LSTM+softmax，而是要在LSTM后面加上一层CRF？

## PART1.1  feature function

CRF属于Log Linear model，对于log linear model，对于给定的源序列和目标序列，模型想要建模的是这个条件概率$p(y|x;w)$

其中$y$是一个n维的序列$(y_1,y_2,y_3,....,y_n)$,$x$同样也是一个n维的序列$(x_1,x_2,x_3,....,x_n)$

Log linear model的条件概率可以通过以下形式进行表示：

![[公式]](https://www.zhihu.com/equation?tex=p%28y%7Cx%3Bw%29+%3D+%5Cfrac%7Bexp%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2C+y%29%29%7D%7BZ%28x%2Cw%29%7D+%5C%5C)

其中![[公式]](https://www.zhihu.com/equation?tex=w_j)是整个模型的参数，是需要学习的, ![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2C+y%29)被称为`特征函数`，其描述了观测序列![[公式]](https://www.zhihu.com/equation?tex=x)和隐含状态序列![[公式]](https://www.zhihu.com/equation?tex=y)的某种规则/关系，![[公式]](https://www.zhihu.com/equation?tex=Z%28x%2C+w%29+)是归一化因子，因为我们的输出是条件概率，需要满足取值在![[公式]](https://www.zhihu.com/equation?tex=%5B0%2C+1%5D)之间，所以不能省略了该项，![[公式]](https://www.zhihu.com/equation?tex=Z%28x%2C+w%29)有个专门的名词`partition function`，其形式为：

![[公式]](https://www.zhihu.com/equation?tex=Z%28x%2C+w%29+%3D+%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29+%5C%5C)

注意:

1. $y$是一个n维的序列$(y_1,y_2,y_3,....,y_n)$,$x$同样也是一个n维的序列$(x_1,x_2,x_3,....,x_n)$,同时y序列中的取值状态一般都是有限的，比如词性的个数，实体的类型个数等。x序列理论上取值也是有限的。
2. $f_j(x,y)$表示的feature function，一般是由人手工指定的，该函数的输出值可以是实数值，通常取值为{0,1}。
3. J表示feature function的个数，该个数有特征的大小决定，有几个特征就有多少个feature function。

从Log linear model 的条件概率的表现形式中可以看到，只要清楚了feature function，那么对于给定的观测序列x和隐藏状态序列y就可以计算其条件概率。

将log linear model中的特征函数进行一些限制和修改就能得到CRF模型，CRF模型在特征函数上做了以下的限制：

- ![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2Cy%29) 需要把整个![[公式]](https://www.zhihu.com/equation?tex=x)输入，即考虑全部的输入；
- 新增了一个![[公式]](https://www.zhihu.com/equation?tex=x)序列中的词的位置编码信息![[公式]](https://www.zhihu.com/equation?tex=i)，即需要告诉特征函数当前作用的位置是输入序列![[公式]](https://www.zhihu.com/equation?tex=x)中的第几个输入；
- 当前词/字的对应的标签![[公式]](https://www.zhihu.com/equation?tex=y_i);
- 上一个词/字的标签![[公式]](https://www.zhihu.com/equation?tex=y_%7Bi-1%7D);

因此，CRF模型的特征函数可以表示为：

![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2C+y%29+%3D+%5Csum_%7Bi%3D1%7D%5ET+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+%5C%5C)

其中![[公式]](https://www.zhihu.com/equation?tex=T)表示序列的长度，一般把![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29)叫做`low-level`特征函数，low-level特征函数会扫过整个输入序列，最终求和之后汇聚到![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2Cy%29)上,这样做的好处在于，我们模型中的特征函数![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2Cy%29)的个数可以是固定的，同时我们的训练样本/测试样本的长度是可变的，这样做到一种兼容。

由此，根据Log-Linear模型的形式，可以得到CRF模型的形式为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28y%7Cx%3Bw%29+%26%3D+%5Cfrac%7Bexp%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2C+y%29%29%7D%7BZ%28x%2Cw%29%7D+%5C%5C+++++%26%3D+%5Cfrac%7Bexp%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+%5Csum_%7Bi%3D1%7D%5ET+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+++%29%7D%7BZ%28x%2Cw%29%7D+%5C%5C+++++%26%3D++%5Cfrac%7Bexp%28%5Csum_%7Bj%3D1%7D%5EJ++%5Csum_%7Bi%3D1%7D%5ET+w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+++%29%7D%7BZ%28x%2Cw%29%7D+%5Cend%7Baligned%7D+%5C%5C)

上述公式是CRF的简化形式，很多书籍会从PGM的一些概念开始，如`团与最大团`，`Hammersley-Clifford定理`，`势函数`，最后根据马尔科夫随机场，条件随机场定义等一步步推导到线性链条件CRF的参数化形式，总体上来说理解难度很更大点，这里抛弃了这些概念，发现从Log-Linear更容易接受，下面部分内容可以和李航的统计机器学习的部分内容开始接上了，我们根据上述简化的CRF公式，复杂化一下，将特征函数拆分成两部分(总的个数是一样的)：

- `转移特征函数`：![[公式]](https://www.zhihu.com/equation?tex=t_k%28x%2Cy_%7Bi-1%7D%2Cy_i%2C+i%29), 表示特征函数依赖于当前和上一时刻的标签，有![[公式]](https://www.zhihu.com/equation?tex=K)个；
- `状态特征函数（发射概率）`：![[公式]](https://www.zhihu.com/equation?tex=s_l%28x%2Cy_i%2Ci%29): 表示特征函数只依赖于当前时刻的标签，有![[公式]](https://www.zhihu.com/equation?tex=L)个；

最终，可以把上述公式等价为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28y%7Cx%3Bw%29+%26%3D+%5Cfrac%7Bexp%28%5Csum_%7Bj%3D1%7D%5EJ++%5Csum_%7Bi%3D1%7D%5ET+w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+++%29%7D%7BZ%28x%2Cw%29%7D+%5C%5C+++++%26%3D+%5Cfrac%7B1%7D%7BZ%28x%2Cw%29%7Dexp%5CBig%28+%5Csum_%7Bk%3D1%7D%5EK+%5Csum_%7Bi%3D1%7D%5ET+%5Clambda_k+t_k%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+%2B+%5Csum_%7Bl%3D1%7D%5EL+%5Csum_%7Bi%3D0%7D%5ET+%5Cmu_l+s_l%28x%2C+y_i%2C+i%29+++%5CBig%29+%5Cend%7Baligned%7D+%5C%5C)



最终得到的简化后的crf模型的条件概率公式如上所示，我们发现只要确定了转移特征函数和状态特征函数，我们就能计算出具体的条件概率。通常这两个函数是由手工进行设计的。那么我们可不可以使用一些模型，如LSTM、rnn等来进行特征的提取而避免进行手工设计这两个函数呢？

## PART1.2  LSTM进行特征的提取

通过观察CRF的两个特征函数，首先状态特征函数$s(x,y_i,i)$的输入为整个观测序列x，当前时刻的标签y_i，当前时刻的位置i。因此状态特征函数主要描述的是观测序列和当前隐藏时刻隐藏序列的一种对应关系。转移特征函数主要描述的是隐藏状态标签之间的一种转移关系。

对于多对多的LSTM模型架构，其模型的输入是一个序列，同时每个时间步上都有相应的输出，我们可以认为该输出包含了当前时刻以及之前时刻序列的信息。因此我们可以使用LSTM在每时刻的输出作为状态特征函数每个时刻的输出。但是使用单向的LSTM存在一个问题，就是当前时刻的输入只包含当前时刻以及之前时刻的序列，无法包含当前时刻之后序列中的信息。为了解决这个问题，可以使用双向的LSTM模型，这样当前时刻的输入就包括了整个序列的信息。

<img src="/Users/eason/Library/Application%20Support/typora-user-images/image-20210406101811678.png" alt="image-20210406101811678" style="zoom:50%;" />

## PART1.3  LSTM+CRF

为什么LSTM层之后不直接接上一层softmax分类层还是要接上一层CRF呢？主要原因是LSTM在每一时刻的输出只和当前时刻有关，其并没有考虑到上一时刻的标签输出是什么。**我们在使用LSTM建模的时候只考虑到了输入单词的序列信息，并没有考虑标签输出信息**。比如对于下面这句话“我热爱爬山”，将其分词为"我"，"热爱"，“爬山”。对于"热爱"LSTM可能会将其分类为动词，同样对于“爬山”，LSTM也可能会将其分类为动词，但是根据语法，将“爬山”分类为名词会更加适合。也就是动词+名词这一模式没有被LSTM捕获到。

但是标签之间的转移关系对于词性标注、ner等任务很重要，因此就很有必要引入一个标签状态转移矩阵来捕捉标签之间的转移关系。

<img src="https://pic3.zhimg.com/80/v2-b8e713dbf24afb0431f5670e10c94a86_1440w.jpg" alt="img" style="zoom:50%;" />

如上图所示，通过标签状态转移矩阵我们可以发现：

1. 标签序列的开头应该是以B或者O开头的，而不是以I开头的。
2. 在B-label1,I-label2,I-label3这种模式中，label1，label2，label3可能都是相同的命名实体(B-person->I-person->I-person)

因此在LSTM之后加上一个CRF层的好处是：

1. 能学习到标签之间的转移关系
2. 通过标签转移状态矩阵的限制，可以减少模型输出无效的标签序列



# PART 2.0 三个问题的解决方法

回顾一下，在CRF模型中需要解决以下三个问题：

1. 在给定输入序列x，输出序列y以及CRF模型，如何计算$p(y|x)$？
2. 如何训练模型？
3. 在模型训练好后，如何计算输入序列x对应的最有可能的输出序列y?

同样的，在LSTM+CRF框架中，同样也是需要解决以上三个问题。

## PART 2.1 条件概率计算

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28y%7Cx%3Bw%29+%26%3D+%5Cfrac%7Bexp%28%5Csum_%7Bj%3D1%7D%5EJ++%5Csum_%7Bi%3D1%7D%5ET+w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+++%29%7D%7BZ%28x%2Cw%29%7D+%5C%5C+++++%26%3D+%5Cfrac%7B1%7D%7BZ%28x%2Cw%29%7Dexp%5CBig%28+%5Csum_%7Bk%3D1%7D%5EK+%5Csum_%7Bi%3D1%7D%5ET+%5Clambda_k+t_k%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+%2B+%5Csum_%7Bl%3D1%7D%5EL+%5Csum_%7Bi%3D0%7D%5ET+%5Cmu_l+s_l%28x%2C+y_i%2C+i%29+++%5CBig%29+%5Cend%7Baligned%7D+%5C%5C)

CRF条件概率的简化公式如上图所示，将其近一步简化得到如下公式：
$$
p(y|x;w)=\frac{score_{real}}{score_{path1}+socre_{path2}+score_{path3}+score_{pathn}}
$$
将其取

其中score_real 表示的是真实的路径得分，分母是所有路径的得分和。

在LSTM+CRF框架中，score是有emission score+translation score 得到的。其中emission score表示发射得分,假设每一时刻LSTM都会输出一个K维的向量e，index表示真实的label标签，那么e[index]表示的就是当前时刻输出emission score，用e_i进行表示。定义一个标签转移矩阵T，T[i-1,i]表示的是上一时刻标签为i-1，转移到下一时刻标签为i的转移概率。因此总的得分score=$\sum_{i}^n{e_i}+\sum_{2}^nT[i-1,i]$

<img src="https://pic4.zhimg.com/80/v2-e3255536f84eaf2e5cf295de0ad2c17b_1440w.jpg" alt="img" style="zoom:50%;" />

现在已经计算好分子的score了，那么如何计算分母的得分呢？对于这部分的计算，我们知道，如果通过枚举出所有可能的路径，那么时间复杂度为$m^l$,其中m表示状态的数量(对应标签的数量),l表示序列长度。这是一个指数级别的复杂度，同时由于其可以使用动态规划的算法将复杂度降低到$m^2l$。将分母计算好之后，就能计算条件概率了![[公式]](https://www.zhihu.com/equation?tex=logp%28y%7Cx%29+%3D+score%28y%29-log%28%5Csum_y+e%5E%7Bscore%28y%29%7D%29)



## PART 2.2 模型训练

在LSTM+CRF框架中，模型的条件概率公式如下所示：
$$
p(y|x;w)=\frac{score_{real}}{score_{path1}+socre_{path2}+score_{path3}+score_{pathn}}
$$
我们我们极大似然估计来估计模型的参数，然后使用梯度下降来进行参数的学习。

因此我们的loss function 可以表示为如下所示：
$$
L(\theta) = - log(score_real) + log(score_{path1}+score_{path2}+score_{path3}+..+score_{pathn})
$$

## PART 2.3 解码过程

在训练好模型之后，如果解码出输入序列对应的最有可能的输出序列呢？对于这个问题，可以使用veterbi算法来进行求解

首先，我们要明白我们要寻找的最优路径即为得分最高的路径，下图是一个demo示例，不同颜色的箭头指向不同的节点，任意时刻，带有颜色的箭头表示的路径是指向该节点的得分最高的路径。

<img src="https://pic2.zhimg.com/v2-4782a5ca7340e6fd940e0f11f4e48425_b.jpg" alt="img" style="zoom:50%;" />

在最后一个时刻T=3，我们只需要找出得分最高的路径（某种颜色表示的路径）指向的节点，然后不断回溯即可找到整体的最优路径。

从上面的叙述中，我们可以发现，要想实现这种方法，我们需要保存每个节点对应的得分最高的路径及其分数。

我们扩展到第一个问题定义的情况下，即 ![[公式]](https://www.zhihu.com/equation?tex=x+%3D+%28x_1%2C+x_2%2C+...%2Cx_n%29) ，经过LSTM后得到的发射矩阵为 ![[公式]](https://www.zhihu.com/equation?tex=E+%5Cin+R%5E%7B%28n%2Cm%29%7D) ，标签转移矩阵为 ![[公式]](https://www.zhihu.com/equation?tex=T+%5Cin+R%5E%7B%28m%2Cm%29%7D) 。

首先，t=0时刻，我们获取各个节点对应的最大路径的得分 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_0+%5Cin+R%5E%7Bm%7D) ，即节点的发射得分 ![[公式]](https://www.zhihu.com/equation?tex=E%5B0%2C%3A%5D) 。

然后到t=1时刻我们要求各个节点对应的最大得分路径及其得分。

这时我们对 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_0) 和 ![[公式]](https://www.zhihu.com/equation?tex=T) 使用wise加法，这样，我们就得到一个 ![[公式]](https://www.zhihu.com/equation?tex=R%5E%7B%28m%2Cm%29%7D) 的矩阵 ![[公式]](https://www.zhihu.com/equation?tex=M_1) ， ![[公式]](https://www.zhihu.com/equation?tex=M_1%5Bi%2Cj%5D) 表示t=0的节点 ![[公式]](https://www.zhihu.com/equation?tex=i) 的最大得分路径到t=1时刻的节点 ![[公式]](https://www.zhihu.com/equation?tex=j) 形成的路径得分。如果我们想求得t=1时刻到节点 ![[公式]](https://www.zhihu.com/equation?tex=j+) 的最大得分路径，只需要对 ![[公式]](https://www.zhihu.com/equation?tex=M_1%5B%3A%2Cj%5D) 求最大值。同样的，如果我们想得到t=1时刻的各个节点对应的最大路径得分 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_1) ，我们只需要对 ![[公式]](https://www.zhihu.com/equation?tex=M_1) 的每一列求最大值。求得最大值的同时将最值路径的来源即箭头的尾部节点记下来，便于遍历查找。这样，我们在得到 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_1) 的同时，也得到了t=1时刻各个节点对应的最大路径在t=0时刻对应的节点向量 ![[公式]](https://www.zhihu.com/equation?tex=P_1+%5Cin+R%5Em) 。

然后，不断重复上面的步骤，直到得到t=n-1时刻的 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_%7Bn-1%7D) 和 ![[公式]](https://www.zhihu.com/equation?tex=P_%7Bn-1%7D) 。这时 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_%7Bn-1%7D) 对应的是最后时刻的各个节点对应的最大路径得分。我们求得 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_%7Bn-1%7D) 中最大值对应的索引 ![[公式]](https://www.zhihu.com/equation?tex=I_%7Bn-1%7D) 。

这个索引表示最优路径的最后一个节点。然后我们将 ![[公式]](https://www.zhihu.com/equation?tex=I_%7Bn-1%7D) 带入 ![[公式]](https://www.zhihu.com/equation?tex=P_%7Bn-1%7D) ，得到 ![[公式]](https://www.zhihu.com/equation?tex=I_%7Bn-2%7D+%3D+P_%7Bn-1%7D%5BI_%7Bn-1%7D%5D) ，表示最优路径倒数第二个节点，然后依次类推，知道得到 ![[公式]](https://www.zhihu.com/equation?tex=I_0%3DP_1%5BI_1%5D) ，这时，最优路径为 ![[公式]](https://www.zhihu.com/equation?tex=I+%3D+%5BI_0%2CI_1%2C...%2CI_%7Bn-1%7D%5D)。



# PART 3.0 pytorch 代码

```python
import torch
import torch.nn as nn
import torch.optim as optim

torch.manual_seed(1)

# some helper functions
def argmax(vec):
    # return the argmax as a python int
    # 第1维度上最大值的下标
    # input: tensor([[2,3,4]])
    # output: 2
    _, idx = torch.max(vec, 1)
    return idx.item()


def prepare_sequence(seq, to_ix):
    # 文本序列转化为index的序列形式
    idxs = [to_ix[w] for w in seq]
    return torch.tensor(idxs, dtype=torch.long)


def log_sum_exp(vec):
    # compute log sum exp in a numerically stable way for the forward algorithm
    # 用数值稳定的方法计算正演算法的对数和exp
    # input: tensor([[2,3,4]])
    # max_score_broadcast: tensor([[4,4,4]])
    max_score = vec[0, argmax(vec)]
    max_score_broadcast = max_score.view(1, -1).expand(1, vec.size()[1])

    # 里面先做减法，减去最大值可以避免e的指数次，计算机上溢
    return max_score + torch.log(torch.sum(torch.exp(vec - max_score_broadcast)))


START_TAG = "<s>"
END_TAG = "<e>"

# create model

class BiLSTM_CRF(nn.Module):
    def __init__(self, vocab_size, tag2ix, embedding_dim, hidden_dim):
        super(BiLSTM_CRF, self).__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.tag2ix = tag2ix
        self.tagset_size = len(tag2ix)

        self.word_embeds = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim // 2,
                            num_layers=1, bidirectional=True)

        # maps output of lstm to tog space
        self.hidden2tag = nn.Linear(hidden_dim, self.tagset_size)

        # matrix of transition parameters
        # entry i, j is the score of transitioning to i from j
        # tag间的转移矩阵，是CRF层的参数
        self.transitions = nn.Parameter(
            torch.randn(self.tagset_size, self.tagset_size))

        # these two statements enforce the constraint that we never transfer to the start tag
        # and we never transfer from the stop tag
        self.transitions.data[tag2ix[START_TAG], :] = -10000
        self.transitions.data[:, tag2ix[END_TAG]] = -10000

        self.hidden = self.init_hidden()

    def init_hidden(self):
        return (torch.randn(2, 1, self.hidden_dim // 2),
                torch.randn(2, 1, self.hidden_dim // 2))

    def _forward_alg(self, feats):
        # to compute partition function
        # 求归一化项的值，应用动态归化算法
        # tensor([[-10000.,-10000.,-10000.,-10000.,-10000.]])
        init_alphas = torch.full((1, self.tagset_size), -10000.)
        # START_TAG has all of the score
        # tensor([[-10000.,-10000.,-10000.,0,-10000.]])
        init_alphas[0][self.tag2ix[START_TAG]] = 0

        forward_var = init_alphas  # 初始状态的forward_var，随着step t变化

        for feat in feats:
            # feat指Bi-LSTM模型每一步的输出，大小为tagset_size
            alphas_t = []
            for next_tag in range(self.tagset_size):
                # 取其中的某个tag对应的值进行扩张至（1，tagset_size）大小
                # 如tensor([3]) -> tensor([[3,3,3,3,3]])
                emit_score = feat[next_tag].view(
                    1, -1).expand(1, self.tagset_size)
                # 增维操作
                trans_score = self.transitions[next_tag].view(1, -1)
                # 上一步的路径和+转移分数+发射分数
                next_tag_var = forward_var + trans_score + emit_score
                # log_sum_exp求和
                alphas_t.append(log_sum_exp(next_tag_var).view(1))
            # 增维
            forward_var = torch.cat(alphas_t).view(1, -1)
        terminal_var = forward_var + self.transitions[self.tag2ix[END_TAG]]
        alpha = log_sum_exp(terminal_var)
        # 归一项的值
        return alpha

    def _get_lstm_features(self, sentence):
        self.hidden = self.init_hidden()
        embeds = self.word_embeds(sentence).view(len(sentence), 1, -1)
        lstm_out, self.hidden = self.lstm(embeds, self.hidden)
        lstm_out = lstm_out.view(len(sentence), self.hidden_dim)
        lstm_feats = self.hidden2tag(lstm_out)
        return lstm_feats

    def _score_sentence(self, feats, tags):
        # gives the score of a provides tag sequence
        # 求某一路径的值
        score = torch.zeros(1)
        tags = torch.cat(
            [torch.tensor([self.tag2ix[START_TAG]], dtype=torch.long), tags])
        for i, feat in enumerate(feats):
            score = score + \
                self.transitions[tags[i + 1], tags[i]] + feat[tags[i + 1]]
        score = score + self.transitions[self.tag2ix[END_TAG], tags[-1]]
        return score

    def _viterbi_decode(self, feats):
        # 当参数确定的时候，求解最佳路径
        backpointers = []

        # tensor([[-10000.,-10000.,-10000.,-10000.,-10000.]])
        init_vars = torch.full((1, self.tagset_size), -10000.)
        # tensor([[-10000.,-10000.,-10000.,0,-10000.]]) 初始每个状态的生成概率
        init_vars[0][self.tag2ix[START_TAG]] = 0

        forward_var = init_vars
        for feat in feats:
            bptrs_t = []  # holds the back pointers for this step
            viterbivars_t = []  # holds the viterbi variables for this step

            for next_tag in range(self.tagset_size):
                next_tag_var = forward_var + self.transitions[next_tag]
                best_tag_id = argmax(next_tag_var)
                bptrs_t.append(best_tag_id)
                viterbivars_t.append(next_tag_var[0][best_tag_id].view(1))
            forward_var = (torch.cat(viterbivars_t) + feat).view(1, -1)
            backpointers.append(bptrs_t)

        # Transition to STOP_TAG
        terminal_var = forward_var + self.transitions[self.tag2ix[END_TAG]]
        best_tag_id = argmax(terminal_var)
        path_score = terminal_var[0][best_tag_id]

        # Follow the back pointers to decode the best path.
        best_path = [best_tag_id]
        for bptrs_t in reversed(backpointers):
            best_tag_id = bptrs_t[best_tag_id]
            best_path.append(best_tag_id)
        # Pop off the start tag (we dont want to return that to the caller)
        start = best_path.pop()
        assert start == self.tag2ix[START_TAG]  # Sanity check
        best_path.reverse()
        return path_score, best_path

    def neg_log_likelihood(self, sentence, tags):
        # 由lstm层计算得的每一时刻属于某一tag的值
        feats = self._get_lstm_features(sentence)
        # feats: 11*5 经过了LSTM+Linear矩阵后的输出，之后作为CRF的输入。

        # 归一项的值
        forward_score = self._forward_alg(feats)
        # 正确路径的值
        gold_score = self._score_sentence(feats, tags)
        return forward_score - gold_score  # -(正确路径的分值  -  归一项的值）

    def forward(self, sentence):  # dont confuse this with _forward_alg above.
        # Get the emission scores from the BiLSTM
        lstm_feats = self._get_lstm_features(sentence)

        # Find the best path, given the features.
        score, tag_seq = self._viterbi_decode(lstm_feats)
        return score, tag_seq


if __name__ == "__main__":
    EMBEDDING_DIM = 5
    HIDDEN_DIM = 4

    # Make up some training data
    training_data = [(
        "the wall street journal reported today that apple corporation made money".split(),
        "B I I I O O O B I O O".split()
    ), (
        "georgia tech is a university in georgia".split(),
        "B I O O O O B".split()
    )]

    word2ix = {}
    for sentence, tags in training_data:
        for word in sentence:
            if word not in word2ix:
                word2ix[word] = len(word2ix)

    tag2ix = {"B": 0, "I": 1, "O": 2, START_TAG: 3, END_TAG: 4}

    model = BiLSTM_CRF(len(word2ix), tag2ix, EMBEDDING_DIM, HIDDEN_DIM)
    optimizer = optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)

    # Check predictions before training
    # 输出训练前的预测序列
    with torch.no_grad():
        precheck_sent = prepare_sequence(training_data[0][0], word2ix)
        precheck_tags = torch.tensor(
            [tag2ix[t] for t in training_data[0][1]], dtype=torch.long)
        print(model(precheck_sent))

    # Make sure prepare_sequence from earlier in the LSTM section is loaded
    for epoch in range(300):  # again, normally you would NOT do 300 epochs, it is toy data
        for sentence, tags in training_data:
            # Step 1. Remember that Pytorch accumulates gradients.
            # We need to clear them out before each instance
            model.zero_grad()

            # Step 2. Get our inputs ready for the network, that is,
            # turn them into Tensors of word indices.
            sentence_in = prepare_sequence(sentence, word2ix)
            targets = torch.tensor([tag2ix[t] for t in tags], dtype=torch.long)

            # Step 3. Run our forward pass.
            loss = model.neg_log_likelihood(sentence_in, targets)

            # Step 4. Compute the loss, gradients, and update the parameters by
            # calling optimizer.step()
            loss.backward()
            optimizer.step()

    # Check predictions after training
    with torch.no_grad():
        precheck_sent = prepare_sequence(training_data[0][0], word2ix)
        print(model(precheck_sent))
```











