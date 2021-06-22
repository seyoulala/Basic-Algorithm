[TOC]

# Part 1.0 Log Linear Model

Log-Linear模型的身影经常出现很早的自然语言模型的语言模型中，用于描述一种条件概率，对于给定输入序列![[公式]](https://www.zhihu.com/equation?tex=x%2C+y),以及模型参数![[公式]](https://www.zhihu.com/equation?tex=w), 模型如下：

![[公式]](https://www.zhihu.com/equation?tex=p%28y%7Cx%3Bw%29+%3D+%5Cfrac%7Bexp%28w+%5Ccdot+F%28x%2C+y%29%29%7D%7B%5Csum_%7By%27%5Cin+%5Cmathcal%7BY%7D%7D+exp%28w+%5Ccdot+F%28x%2C+y%27%29%29%7D++%5C%5C)

或者非矩阵相乘的形式：

![[公式]](https://www.zhihu.com/equation?tex=p%28y%7Cx%3Bw%29+%3D+%5Cfrac%7Bexp%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2C+y%29%29%7D%7BZ%28x%2Cw%29%7D+%5C%5C)

其中![[公式]](https://www.zhihu.com/equation?tex=w_j)是整个模型的参数，是需要学习的, ![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2C+y%29)被称为`特征函数`，其描述了观测序列![[公式]](https://www.zhihu.com/equation?tex=x)和隐含状态序列![[公式]](https://www.zhihu.com/equation?tex=y)的某种规则/关系，后续将会对其做举例说明； ![[公式]](https://www.zhihu.com/equation?tex=Z%28x%2C+w%29+)是归一化因子，因为我们的输出是条件概率，需要满足取值在![[公式]](https://www.zhihu.com/equation?tex=%5B0%2C+1%5D)之间，所以不能省略了该项，![[公式]](https://www.zhihu.com/equation?tex=Z%28x%2C+w%29)有个专门的名词`partition function`，其形式为：

![[公式]](https://www.zhihu.com/equation?tex=Z%28x%2C+w%29+%3D+%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29+%5C%5C)

看完上面的公式，需要注意的几点是：

- ![[公式]](https://www.zhihu.com/equation?tex=x), ![[公式]](https://www.zhihu.com/equation?tex=y)是序列，在训练集中相当于一个个序列对，![[公式]](https://www.zhihu.com/equation?tex=x+%3D+%28x_0%2C+x_1%2C+x_2%2C+%5Cdots+x_T%29),![[公式]](https://www.zhihu.com/equation?tex=y+%3D+%28y_0%2C+y_1%2C+y_2%2C+%5Cdots+y_T%29)，另外整个隐含状态的个数是有限个数的，比如词性的个数，一般是动词，名词，副词等，命名实体中，实体的标签可能为人名，地名，公司名等，而![[公式]](https://www.zhihu.com/equation?tex=x)也可能是从一个有限集合中抽取出来的，比如从3000个汉字中抽取出来的构成观测序列；
- 特征函数![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2C+y%29)的个数![[公式]](https://www.zhihu.com/equation?tex=J)，与定义的匹配模版有关；
- ![[公式]](https://www.zhihu.com/equation?tex=y%27)表示的一个具体的隐含状态序列，用于区别分子中的![[公式]](https://www.zhihu.com/equation?tex=y)，也可以用其他符号来表示;
- 特征函数![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2C+y%29)的取值可以是实数值，一般的取值为![[公式]](https://www.zhihu.com/equation?tex=%5C%7B0%2C+1%5C%7D),即我们常说指示函数,![[公式]](https://www.zhihu.com/equation?tex=x%2C+y)满足某种条件输出为1，否则为0，在后面有例子；
- ![[公式]](https://www.zhihu.com/equation?tex=w)是模型的要学习的参数集合，参数个数跟![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2Cy%29)特征函数的个数有关,这里是![[公式]](https://www.zhihu.com/equation?tex=J)个，需要通过训练数据进行参数的估计；

对公式的右半部分取![[公式]](https://www.zhihu.com/equation?tex=%5Clog)得到如下形式：

![[公式]](https://www.zhihu.com/equation?tex=%5Clog%28p%28y%7Cx%3Bw%29%29+%3D+%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2C+y%29+-+%5Clog%28%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29%29+%5C%5C)

可以发现上述公式，右半部分中的第一项是关于![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2C+y%29)的线性组合(Linear)，第二部分不依赖于标签![[公式]](https://www.zhihu.com/equation?tex=y), 当固定![[公式]](https://www.zhihu.com/equation?tex=x%2C+w)后，就可以说![[公式]](https://www.zhihu.com/equation?tex=%5Clog%28p%28y%7Cx%3Bw%29%29)就是![[公式]](https://www.zhihu.com/equation?tex=%5Clog)后的关于特征函数的线性组合，同时对于上述公式，我们可以得到几个感性结论：

- 由于我们是需要使得似然函数(log似然函数)的取值最大，那么就需要将等式右边的第一部分取值越大越好，第二部分取值越小越好；
- 对于第一部分由于![[公式]](https://www.zhihu.com/equation?tex=x%2Cy)是训练集中的出现的观测序列和隐含标签状态序列对，![[公式]](https://www.zhihu.com/equation?tex=w_j+f_j%28x%2Cy%29)是取值越大比较符合直觉；
- 对于第二部分，![[公式]](https://www.zhihu.com/equation?tex=y%27)不是训练集中的样本![[公式]](https://www.zhihu.com/equation?tex=w_j+f_j%28x%2Cy%29)取值越小符合直觉,由于有exp,所以取值接近于0，比较符合直觉

# part2.0 模型训练

回到我们的目标，或者说具体的任务，比如输入一个句话进行命名实体识别，

![img](https://pic2.zhimg.com/80/v2-456b182c84e1d863b742cbaf92f46c51_1440w.jpg)

![[公式]](https://www.zhihu.com/equation?tex=x)观测序列是文本，状态序列![[公式]](https://www.zhihu.com/equation?tex=y)是定义好的实体类别的集合，而我们更关心的就是给定一个输入![[公式]](https://www.zhihu.com/equation?tex=x)，模型能够给我们一个与真实标签更像的更一致的![[公式]](https://www.zhihu.com/equation?tex=y),即![[公式]](https://www.zhihu.com/equation?tex=p%28y%7Cx%29), 而不是![[公式]](https://www.zhihu.com/equation?tex=p%28x%2C+y%29), 因此，我们的可以利用最大似然估计对Log-Linear模型参数估计。假设训练集中有![[公式]](https://www.zhihu.com/equation?tex=n)个训练样本![[公式]](https://www.zhihu.com/equation?tex=%5C%7B+%28x_i%2C+y_i%29+%5C%7D_%7Bi%3D1%7D%5En), 似然函数(不带正则化的)可以写为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++L%28w%29+%3D+%5Cprod_%7Bi%3D1%7D%5En+p%28y_i%7Cx_i%3Bw%29%5C%5C+++++L%28w%29+%3D+%5Csum_%7Bi%3D1%7D%5En+%5Clog%28p%28y_i%7Cx_i%3Bw%29%29+%5Cend%7Baligned%7D+%5C%5C)

利用最大似然估计出模型的参数![[公式]](https://www.zhihu.com/equation?tex=w%5E%2A):

![[公式]](https://www.zhihu.com/equation?tex=w%5E%2A+%3D+%5Carg+%5Cmax_%7Bw%7D++%5Csum_%7Bi%3D1%7D%5En+%5Clog%28p%28y_i%7Cx_i%3Bw%29+%5C%5C)

显然，我们可以利用梯度上升优化算法来求解参数![[公式]](https://www.zhihu.com/equation?tex=w%5E%2A);结合似然函数和![[公式]](https://www.zhihu.com/equation?tex=%5Clog)后![[公式]](https://www.zhihu.com/equation?tex=p%28y%7Cx%3Bw%29)展开形式，可以得到最终的似然函数为(注: 为了简洁起见，将![[公式]](https://www.zhihu.com/equation?tex=x_i%2Cy_i)的下标![[公式]](https://www.zhihu.com/equation?tex=i)去除了)：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++L%28w%29+%26%3D+%5Csum_%7Bi%3D1%7D%5En+%5CBig%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2C+y%29+-+%5Clog%28%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29%29%5CBig%29+%5C%5C+++++%26%3D+%5Csum_%7Bi%3D1%7D%5En%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2C+y%29+-+%5Csum_%7Bi%3D1%7D%5En+%5CBig%28%5Clog%28%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29%29%5CBig%29+%5Cend%7Baligned%7D+%5C%5C)

先对等式右边的第一部分求导：

![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac%7Bd%7D%7Bdw_j%7D%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2C+y%29%29+%3D+f_j%28x%2C+y%29+%5C%5C)

对第二部分进行求导：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Cfrac%7Bd%7D%7Bdw_j%7D%28%5Clog%28%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29%29%29+%26%3D+%5Cfrac%7B+%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+f_j%28x%2Cy%27%29+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29++%7D%7B%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29%29%7D+%5C%5C+++++%26%3D+%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+%5CBig%28+f_j%28x%2C+y%27%29+%5Ccdot+%5Cfrac%7Bexp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29%7D%7B%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_jf_j%28x%2C+y%27%29%29%29%7D+++%5CBig%29+%5C%5C+++++%26%3D++%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+f_j%28x%2C+y%27%29+p%28y%27%7Cx%3Bw%29+%5Cend%7Baligned%7D+%5C%5C)

对于上式的第一步到第二步，如果有点绕的话，可以想象如下的一个等式：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Cfrac%7B%5Csum_%7Bi%3D1%7D%5E3++a_i+%5Ccdot+b_i%7D%7BD%7D+%26%3D+%5Cfrac%7Ba_1b_1+%2B+a_2b_2+%2B+a_3b_3%7D%7BD%7D+%5C%5C+++++%26%3D+a_1+%5Cfrac%7Bb_1%7D%7BD%7D++%2B+a_2+%5Cfrac%7Bb_2%7D%7BD%7D+%2B+a_3+%5Cfrac%7Bb_3%7D%7BD%7D%5C%5C+++++%26%3D+%5Csum_%7Bi%3D1%7D%5E3+%28a_i+%5Ccdot+%5Cfrac%7Bb_i%7D%7BD%7D%29+%5Cend%7Baligned%7D+%5C%5C)

同时，我们还发现，根据Log-Linear模型的定义，得到了![[公式]](https://www.zhihu.com/equation?tex=p%28y%27%7Cx%3Bw%29); 综上，最终对于![[公式]](https://www.zhihu.com/equation?tex=w_j)求导之后的公式为(注：加上了样本编码的下标![[公式]](https://www.zhihu.com/equation?tex=i))：

![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac%7BdL%28w%29%7D%7Bd+w_j%7D+%3D+%5Csum_%7Bi%3D1%7D%5En+f_j%28x_i%2C+y_i%29+-+%5Csum_%7Bi%3D1%7D%5En+%5Csum_%7By%27+%5Cin+%5Cmathcal%7BY%7D%7D+f_j%28x_i%2C+y%27%29+p%28y%27%7Cx_i%3Bw%29+%5C%5C)

有了上述求导公式，可以对模型中的![[公式]](https://www.zhihu.com/equation?tex=J)个参数![[公式]](https://www.zhihu.com/equation?tex=w_j)依次求导，利用梯度上升(**由于我们是需要最大化似然函数**)优化算法，依次迭代模型的参数：

![[公式]](https://www.zhihu.com/equation?tex=w_j+%5Cleftarrow+w_j+%2B+%5Calpha+%5Cfrac%7BdL%28w%29%7D%7Bd+w_j%7D+%5C%5C)

心细的同学应该发现了，我们的公式中出现了一个不太好计算的![[公式]](https://www.zhihu.com/equation?tex=p%28y%27%7Cx%3Bw%29)，会对这项的求解产生疑问，后面会专门对这个做一下解释，现在姑且把这一项认为是已知的，很好求解，对于整个Log-Linear模型的求解形成了完整的认识。在第三篇内容中，我们会专门针对动态规划算法，前向算法和后向算法进行介绍，这样来推导出![[公式]](https://www.zhihu.com/equation?tex=p%28y%27%7Cx%3Bw%29)会更好理解。

# part3.0 特征函数

我们对于模型的特征应该都是很熟悉了，比如年龄，性别都可以是一个特征列，而对于特征函数可能就不那么熟悉了，特征函数![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2Cy%29)的特点为：

- 输出是实数，取值一般为0或者1，在自然语言处理中，经常可以看到类似onehot的编码方式，所以输出为0/1也是挺合情合理的；
- 设计![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2Cy%29)可以是只跟![[公式]](https://www.zhihu.com/equation?tex=x),或者只跟![[公式]](https://www.zhihu.com/equation?tex=y)有关，比如![[公式]](https://www.zhihu.com/equation?tex=f_j%28x+%5C+starts+%5C+A%29+%3D+1),表示对于输入的句子中，只要存在字母A开头的单词就输出1，与其对应的标签y序列无关；
- 由于![[公式]](https://www.zhihu.com/equation?tex=x%2Cy)是序列对，![[公式]](https://www.zhihu.com/equation?tex=f_j%28x%2C+y%29)特征函数理论上有无穷个规则模版的，但是在实际模型中，会做一些简化处理，方便计算，如CRF模型中，只考虑相邻状态标签，以及位置关系

想象一下一个更具体的例子，我们的n-gram语言模型，如2-gram,需要对语料库中相邻的两个字进行切分，如果我们把第一字和第二字的具体取值生成一个特征函数的话，即只要出现了语料库中这样的2-gram的词，就输出1，那么我们就可以得到非常多的特征函数；

# Part4.0 CRF

有了上述Log-Linear模型的铺垫，我们发现只需要对特征函数做一些限制，就可以得到我们要讲的CRF模型(没有特别说明指的是linear-chain CRF)，先看CRF模型在特征函数上做了什么限制：

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

下面直接改编一下统计机器学习上的一个例子来直观地展示一下CRF模型：假定输入观测序列![[公式]](https://www.zhihu.com/equation?tex=x+%3D+%28x_0%2Cx_1%2C+x_2%29), 输出标记(状态序列)![[公式]](https://www.zhihu.com/equation?tex=y%3D%28y_0%2Cy_1%2Cy_2%29),其中状态的取值为![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BY%7D+%3D+%5C%7Bred%2Cblack%5C%7D),即![[公式]](https://www.zhihu.com/equation?tex=y_i)的取值只能是red或者black，同时分别给定了5个转移特征函数![[公式]](https://www.zhihu.com/equation?tex=t_k)和3个状态函数![[公式]](https://www.zhihu.com/equation?tex=s_l):

转移特征函数为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++t_1+%26%3D+t_1%28x%2C+y_%7Bi-1%7D%3Dred%2C+y_i%3Dblack%2C+i%3D%5C+1+or+%5C+2%29%2C%5Clambda_1+%3D+1+%5C%5C+++++t_2+%26%3D+t_2%28x%2C+y_0%3Dred%2C+y_1%3Dred%2C+i%3D1%29%2C+%5Clambda_2+%3D+0.5+%5C%5C+++++t_3+%26%3D+t_2%28x%2C+y_1%3Dblack%2C+y_2%3Dred%2C+i%3D2%29%2C+%5Clambda_3+%3D+1+%5C%5C+++++t_4+%26%3D+t_4%28x%2C+y_0%3Dblack%2C+y_1%3Dred%2C+i%3D1%29%2C+%5Clambda_4+%3D+1+%5C%5C+++++t_5+%26%3D+t_5%28x%2C+y_1%3Dblack%2C+y_2%3Dbalck%2C+i%3D2%29%2C+%5Clambda_5+%3D+0.2+%5C%5C+%5Cend%7Baligned%7D+%5C%5C)

状态特征函数为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++s_1+%26%3D+s_1%28x%2Cy_0%3Dred%2Ci%3D0%29%2C+%5Cmu_1+%3D+1+%5C%5C+++++s_2+%26%3D+s_2%28x%2Cy_i%3Dblack%2Ci%3D0%5C+or+%5C+1%29%2C+%5Cmu_2+%3D+0.5+%5C%5C+++++s_3+%26%3D+s_3%28x%2Cy_i%3Dred%2Ci%3D1%5C+or+%5C+2%29%2C+%5Cmu_3+%3D+0.8+%5C%5C+++++s_4+%26%3D+s_4%28x%2Cy_2%3Dblack%2Ci%3D2%29%2C+%5Cmu_4+%3D+0.5+%5C%5C+%5Cend%7Baligned%7D+%5C%5C)

对于给定的观测序列![[公式]](https://www.zhihu.com/equation?tex=x),求状态序列![[公式]](https://www.zhihu.com/equation?tex=y%3D%28y_0%2Cy_1%2Cy_2%29%3D%28red%2Cblack%2Cblack%29)的非规范化的条件概率。直接根据上述CRF的公式，即可得到：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28y%7Cx%3Bw%29+%26%5Cpropto+exp%5CBig%28+%5Csum_%7Bk%3D1%7D%5EK+%5Csum_%7Bi%3D1%7D%5ET+%5Clambda_k+t_k%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+%2B+%5Csum_%7Bl%3D1%7D%5EL+%5Csum_%7Bi%3D0%7D%5ET+%5Cmu_l+s_l%28x%2C+y_i%2C+i%29+++%5CBig%29+%5C%5C+++++%26%3D+exp%5CBig%28+%5Csum_%7Bk%3D1%7D%5E5+%5Csum_%7Bi%3D1%7D%5E2+%5Clambda_k+t_k%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+%2B+%5Csum_%7Bl%3D1%7D%5E4+%5Csum_%7Bi%3D0%7D%5E2+%5Cmu_l+s_l%28x%2C+y_i%2C+i%29+++%5CBig%29+%5C%5C+%5Cend%7Baligned%7D+%5C%5C)

依次对上述公式进行展开：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Csum_%7Bk%3D1%7D%5E5+%5Csum_%7Bi%3D1%7D%5E2+%5Clambda_k+t_k%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29++%26%3D++++%5Cbegin%7Bmatrix%7D+++%5Clambda_1+%5Ccdot+%5CBig%28t_1%28x%2Cy_0%2C+y_1%2C+1%29+%2B+t_1%28x%2C+y_1%2Cy_2%2C2%29+%5CBig%29++%2B+%5C%5C+++%5Clambda_2+%5Ccdot+%5CBig%28t_2%28x%2Cy_0%2C+y_1%2C+1%29+%2B+t_2%28x%2C+y_1%2Cy_2%2C2%29+%5CBig%29++%2B+%5C%5C+++%5Clambda_3+%5Ccdot+%5CBig%28t_3%28x%2Cy_0%2C+y_1%2C+1%29+%2B+t_3%28x%2C+y_1%2Cy_2%2C2%29+%5CBig%29++%2B+%5C%5C+++%5Clambda_4+%5Ccdot+%5CBig%28t_4%28x%2Cy_0%2C+y_1%2C+1%29+%2B+t_4%28x%2C+y_1%2Cy_2%2C2%29+%5CBig%29++%2B+%5C%5C+++%5Clambda_5+%5Ccdot+%5CBig%28t_5%28x%2Cy_0%2C+y_1%2C+1%29+%2B+t_5%28x%2C+y_1%2Cy_2%2C2%29+%5CBig%29++%5C%5C++++%5Cend%7Bmatrix%7D+%5C%5C+++%26%3D++++%5Cbegin%7Bmatrix%7D+++1+%5Ccdot+%5CBig%28t_1%28x%2Cy_0%3Dred%2C+y_1%3Dblack%2C+1%29+%2B+t_1%28x%2C+y_1%3Dblack%2Cy_2%3Dblack%2C2%29+%5CBig%29++%2B+%5C%5C+++0.5+%5Ccdot+%5CBig%28t_2%28x%2Cy_0%3Dred%2C+y_1%3Dblack%2C+1%29+%2B+t_2%28x%2C+y_1%3Dblack%2Cy_2%3Dblack%2C2%29+%5CBig%29++%2B+%5C%5C+++1+%5Ccdot+%5CBig%28t_3%28x%2Cy_0%3Dred%2C+y_1%3Dblack%2C+1%29+%2B+t_3%28x%2C+y_1%3Dblack%2Cy_2%3Dblack%2C2%29+%5CBig%29++%2B+%5C%5C+++1+%5Ccdot+%5CBig%28t_4%28x%2Cy_0%3Dred%2C+y_1%3Dblack%2C+1%29+%2B+t_4%28x%2C+y_1%3Dblack%2Cy_2%3Dblack%2C2%29+%5CBig%29++%2B+%5C%5C+++0.2+%5Ccdot+%5CBig%28t_5%28x%2Cy_0%3Dred%2C+y_1%3Dblack%2C+1%29+%2B+t_5%28x%2C+y_1%3Dblack%2Cy_2%3Dblack%2C2%29+%5CBig%29++%5C%5C++++%5Cend%7Bmatrix%7D+%5C%5C+++%26%3D++++%5Cbegin%7Bmatrix%7D+++1+%5Ccdot+%281+%2B+0+%29++%2B+%5C%5C+++0.5+%5Ccdot+%280+%2B+0+%29++%2B+%5C%5C+++1+%5Ccdot+%280+%2B+0+%29++%2B+%5C%5C+++1+%5Ccdot+%280+%2B+0+%29++%2B+%5C%5C+++0.2+%5Ccdot+%280%2B+1%29++%5C%5C++++%5Cend%7Bmatrix%7D+%5C%5C+++%26%3D+1.2+%5Cend%7Baligned%7D+%5C%5C)

同理：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Csum_%7Bl%3D1%7D%5E4+%5Csum_%7Bi%3D0%7D%5E2+%5Cmu_l+s_l%28x%2C+y_i%2C+i%29++++%26%3D++++%5Cbegin%7Bmatrix%7D+++1.0+%5Ccdot+%281+%2B+0+%2B+0+%29++%2B+%5C%5C+++0.5+%5Ccdot+%280+%2B+1+%2B+0+%29++%2B+%5C%5C+++0.8+%5Ccdot+%280+%2B+0+%2B+0%29++%2B+%5C%5C+++0.5+%5Ccdot+%280+%2B+0+%2B+1+%29+%5C++%5C%5C+++%5Cend%7Bmatrix%7D+%3D+2+%5Cend%7Baligned%7D+%5C%5C)

最终：![[公式]](https://www.zhihu.com/equation?tex=p%28y_0%3Dred%2C+y_1%3Dblack%2C+y_2%3Dblack%29+%5Cpropto+exp%283.2%29)

## part4.1使用forward/backward加速计算概率



我们从Log-Linear模型的角度，推导出了CRF模型的形式，参数学习方法，CRF模型可以表示为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28y%7Cx%3Bw%29+%26%3D+%5Cfrac%7Bexp%28%5Csum_%7Bj%3D1%7D%5EJ++%5Csum_%7Bi%3D1%7D%5ET+w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29+++%29%7D%7BZ%28x%2Cw%29%7D++%5Cend%7Baligned%7D+%5C%5C)

同时，根据指数函数的运算法则，可以对上述形式做如下变换：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++p%28y%7Cx%3Bw%29+%26%3D+%5Cfrac%7B1%7D%7BZ%28x%2Cw%29%7D+exp%28%5Csum_%7Bj%3D1%7D%5EJ++%5Csum_%7Bi%3D1%7D%5ET+w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29%29+%5C%5C+++++%26%3D+%5Cfrac%7B1%7D%7BZ%28x%2Cw%29%7D+%5Cprod_%7Bj%3D1%7D%5EJ+exp%28%5Csum_%7Bi%3D1%7D%5ET+w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29%29+%5C%5C+++++%26%3D+%5Cfrac%7B1%7D%7BZ%28x%2Cw%29%7D+%5Cprod_%7Bi%3D1%7D%5ET+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29%29+%5C%5C+++++%26%3D+%5Cfrac%7B1%7D%7BZ%28x%2Cw%29%7D+%5Cprod_%7Bi%3D1%7D%5ET+%5Cprod_%7Bj%3D1%7D%5EJ+exp%28w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29%29+%5Cend%7Baligned%7D+%5C%5C)

有了上述形式，定义在序列的第![[公式]](https://www.zhihu.com/equation?tex=i)个位置，由状态![[公式]](https://www.zhihu.com/equation?tex=y_%7Bi-1%7D)转移到![[公式]](https://www.zhihu.com/equation?tex=y_i)的非规范化概率为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++M_i%28y_%7Bi-1%7D%2C+y_i+%7C+x%29+%3D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29%29+%5Cend%7Baligned%7D+%5C%5C)

所以上述等式，可以再次等价为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D++++++p%28y%7Cx%3Bw%29+%26%3D+%5Cfrac%7B1%7D%7BZ%28x%2Cw%29%7D+%5Cprod_%7Bi%3D1%7D%5ET+M_i%28y_%7Bi-1%7D%2C+y_i+%7C+x%29+%5Cend%7Baligned%7D+%5C%5C)



### part4.1.1前向算法

首先，先给出CRF模型中的前向算法中要计算的东西是什么，其定义与HMM是一致的，都是要计算出在时刻![[公式]](https://www.zhihu.com/equation?tex=t)上对应的隐含状态![[公式]](https://www.zhihu.com/equation?tex=y_t)的概率，在CRF中是条件概率，在HMM中是联合概率，对比如下：

- `HMM中前向算法计算的概率为`： ![[公式]](https://www.zhihu.com/equation?tex=+%5Calpha_i%28t%29+%3D+p%28x_0%2C+x_1%2C+x_2%2C+%5Ccdots%2Cx_t%2C+y_t%3Di%29)
- `CRF中前向算法计算的概率为`： ![[公式]](https://www.zhihu.com/equation?tex=+%5Calpha_i%28t%29+%3D+p%28y_0%2C+y_1%2C+%5Ccdots%2C+y_t%3Di%7Cx%29)，根据定义，上一时刻可以表示为： ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bk%7D%28t-1%29+%3D+p%28y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk+%7C+x%29)，![[公式]](https://www.zhihu.com/equation?tex=i)和![[公式]](https://www.zhihu.com/equation?tex=k)都是具体的隐含状态取值，为了区分不同时刻的不同状态，故这样写。

下面对CRF前向算法进行推导，得到![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_i%28t%29) 和 ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bk%7D%28t-1%29)的状态转移方程,假定隐含状态的取值有K个状态，

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Calpha_i%28t%29+%26%3D+p%28y_0%2C+y_1%2C+%5Ccdots%2Cy_t%3Di%7Cx%29+%5C%5C+++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+p%28y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk%2C+y_t%3Di%7Cx%29+%5Ccdots+%5Ccdots+1+%5C%5C+++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+%5Cfrac%7Bp%28y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk%2C+y_t%3Di%2C+x%29%7D%7Bp%28x%29%7D+%5Ccdots+%5Ccdots+2%5C%5C++++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+%5Cfrac%7Bp%28y_t%3Di%7Cy_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk%2C+x%29+p%28y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk%2C+x%29+%7D%7Bp%28x%29%7D+%5Ccdots+%5Ccdots+3%5C%5C++++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+%5Cfrac%7Bp%28y_t%3Di%7Cy_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk%2C+x%29+p%28y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk+%7C+x%29+p%28x%29+%7D%7Bp%28x%29%7D+%5Ccdots+%5Ccdots+4%5C%5C++++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+p%28y_t%3Di%7Cy_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk%2C+x%29+p%28y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk+%7C+x%29+%5Ccdots+%5Ccdots+5%5C%5C++++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+p%28y_t%3Di%7Cy_%7Bt-1%7D%3Dk%2C+x%29+%5Calpha_%7Bk%7D%28t-1%29+%5Ccdots+%5Ccdots+6%5C%5C++++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+M_%7Bt-1%7D%28y_%7Bt-1%7D%3Dk%2C+y_t%3Di+%7C+x%29+%5Calpha_%7Bk%7D%28t-1%29+%5Ccdots+%5Ccdots+7%5C%5C++%5Cend%7Baligned%7D+%5C%5C)

下面针对上述推导公式的每一步进行说明：

第一步：全概率公式，增加了上一个隐含时刻![[公式]](https://www.zhihu.com/equation?tex=y_%7Bk-1%7D)的具体取值；
第二步：贝叶斯公式；
第三步：贝叶斯公式，改变条件概率的形式，主要是需要凑出![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bk%7D%28t-1%29+%3D+p%28y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk+%7C+x%29)和条件转移概率；
第四步：还是贝叶斯公式，主要是对![[公式]](https://www.zhihu.com/equation?tex=p%28y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk%2C+x%29)进行展开；
第五步：消去![[公式]](https://www.zhihu.com/equation?tex=p%28x%29)
第六步：替换![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bk%7D%28t-1%29+%3D+p%28y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-1%7D%3Dk+%7C+x%29)，得到![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_i%28t%29) 和 ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7Bk%7D%28t-1%29)的状态转移方程；同时第6步中根据CRF中概率转移的特点，可以发现![[公式]](https://www.zhihu.com/equation?tex=y_t)与![[公式]](https://www.zhihu.com/equation?tex=y_0%2C+y_1%2C+%5Ccdots%2Cy_%7Bt-2%7D)是独立的，只与![[公式]](https://www.zhihu.com/equation?tex=y_%7Bt-1%7D)有关；
第七步：在上述公式中出现了一个概率转移公式(第6行):![[公式]](https://www.zhihu.com/equation?tex=p%28y_t%3Di%7Cy_%7Bt-1%7D%3Dk%2C+x%29),其表示的意思为，对于隐含状态的第![[公式]](https://www.zhihu.com/equation?tex=t)时刻，在给定观测序列![[公式]](https://www.zhihu.com/equation?tex=x)和上一时刻隐含状态为![[公式]](https://www.zhihu.com/equation?tex=y_%7Bt-1%7D%3Dk)时，转移到![[公式]](https://www.zhihu.com/equation?tex=y_t%3Di)(即从状态![[公式]](https://www.zhihu.com/equation?tex=k)转移到![[公式]](https://www.zhihu.com/equation?tex=i))的概率，根据CRF模型整体的条件概率公式![[公式]](https://www.zhihu.com/equation?tex=p%28y%7Cx%2C+w%29)，见上一小节，公式中的![[公式]](https://www.zhihu.com/equation?tex=exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2Cy_%7Bi-1%7D%2C+y_i%2C+i%29%29),表示的就是在第![[公式]](https://www.zhihu.com/equation?tex=i)个时刻，从![[公式]](https://www.zhihu.com/equation?tex=y_%7Bt-1%7D)转移到![[公式]](https://www.zhihu.com/equation?tex=y_%7Bt%7D)的非规范概率，为了简洁起见，我们利用下面的符号来代替（这里面没有值定状态的具体取值，实际计算时需要指定）：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++M_%7Bt-1%7D%28y_%7Bt-1%7D%2C+y_t+%7C+x%29+%3D+exp%28%5Csum_%7Bj%3D1%7D%5EJ+w_j+f_j%28x%2Cy_%7Bt-1%7D%2C+y_t%2C+t%29%29+%5Cend%7Baligned%7D+%5C%5C)

至此，我们完成了前向算法的推导过程，在有些参考资料中，还会引入`矩阵的形式`，在上式中![[公式]](https://www.zhihu.com/equation?tex=+%5Calpha_i%28t%29)表示的是![[公式]](https://www.zhihu.com/equation?tex=y_t%3Di)的一个状态的概率取值，如果利用![[公式]](https://www.zhihu.com/equation?tex=+%5Calpha%28t%29)表示所有的状态向量(![[公式]](https://www.zhihu.com/equation?tex=K)维列向量)：

![[公式]](https://www.zhihu.com/equation?tex=++%5Calpha%28t%29+%3D++++%5Cbegin%7Bbmatrix%7D+++%5Calpha_1%28t%29++%5C%5C+++%5Calpha_2%28t%29++%5C%5C+++%5Cvdots+%5C%5C+++%5Calpha_K%28t%29++++%5Cend%7Bbmatrix%7D+%5C%5C)

同理：

![[公式]](https://www.zhihu.com/equation?tex=++%5Calpha%28t-1%29+%3D++++%5Cbegin%7Bbmatrix%7D+++%5Calpha_1%28t-1%29++%5C%5C+++%5Calpha_2%28t-1%29++%5C%5C+++%5Cvdots+%5C%5C+++%5Calpha_K%28t-1%29++++%5Cend%7Bbmatrix%7D+%5C%5C)

同时利用![[公式]](https://www.zhihu.com/equation?tex=M_%7Bt-1%7D%28x%29)来表示在时刻![[公式]](https://www.zhihu.com/equation?tex=t)上，从状态![[公式]](https://www.zhihu.com/equation?tex=y_%7Bt-1%7D)转移到![[公式]](https://www.zhihu.com/equation?tex=y_%7Bt%7D)的非规范化概率矩阵，相比于HMM模型，CRF模型在各个位置上（时间点上）都有特定的概率转移矩阵， 即

![[公式]](https://www.zhihu.com/equation?tex=++M_%7Bt-1%7D%28x%29+%3D++++%5Cbegin%7Bbmatrix%7D+++M_%7Bt-+1%7D%28y_%7Bt-+1%7D%3D1%2C+y_%7Bt%7D%3D1+%7C+x%29+%26+M_%7Bt-+1%7D%28y_%7Bt-+1%7D%3D1%2C+y_%7Bt%7D%3D2+%7C+x%29++%26+%5Ccdots+%26+M_%7Bt-+1%7D%28y_%7Bt-+1%7D%3D1%2C+y_%7Bt%7D%3DK+%7C+x%29+%5C%5C+++M_%7Bt-+1%7D%28y_%7Bt-+1%7D%3D2%2C+y_%7Bt%7D%3D1+%7C+x%29+%26+M_%7Bt-+1%7D%28y_%7Bt-+1%7D%3D2%2C+y_%7Bt%7D%3D2+%7C+x%29++%26+%5Ccdots+%26+M_%7Bt-+1%7D%28y_%7Bt-+1%7D%3D2%2C+y_%7Bt%7D%3DK+%7C+x%29+%5C%5C+++%5Cvdots+%26+%5Cvdots+%26+%5Cddots+%26+%5Cvdots+%5C%5C+++M_%7Bt-+1%7D%28y_%7Bt-+1%7D%3DK%2C+y_%7Bt%7D%3D1+%7C+x%29+%26+M_%7Bt-+1%7D%28y_%7Bt-+1%7D%3DK%2C+y_%7Bt%7D%3D2+%7C+x%29++%26+%5Ccdots+%26+M_%7Bt-+1%7D%28y_%7Bt-+1%7D%3DK%2C+y_%7Bt%7D%3DK+%7C+x%29++++%5Cend%7Bbmatrix%7D++%5C%5C)

最终：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Calpha%28t%29%5ET+%26%3D+%5Calpha%28t-1%29%5ET+M_%7Bt-1%7D%28x%29+%5C%5C+++++%5Cbig%5B+%5Calpha_1%28t%29%2C+%5Calpha_2%28t%29+%2C+%5Ccdots%2C+%5Calpha_K%28t%29+%5Cbig%5D+%26%3D+%5Cbig%5B+%5Calpha_1%28t-1%29%2C+%5Calpha_2%28t-1%29+%2C+%5Ccdots%2C+%5Calpha_K%28t-1%29+%5Cbig%5D+M_%7Bt-1%7D%28x%29+%5Cend%7Baligned%7D+%5C%5C)

举例,当![[公式]](https://www.zhihu.com/equation?tex=t)时刻的![[公式]](https://www.zhihu.com/equation?tex=y_%7Bt%7D)的隐含状态为1时概率计算：![[公式]](https://www.zhihu.com/equation?tex=%5Calpha_%7B1%7D%28t%29)

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Calpha_%7B1%7D%28t%29+%26%3D+%5Calpha_1%28t-1%29+M_%7Bt-1%7D%28y_%7Bt-1%7D%3D1%2C+y_%7Bt%7D%3D1+%7C+x%29+%5C%5C++++++%26%2B+%5Calpha_2%28t-1%29+M_%7Bt-1%7D%28y_%7Bt-1%7D%3D2%2C+y_%7Bt%7D%3D1+%7C+x%29+%5C%5C+++++++%26+%2B++%5Ccdots+%5C%5C+++++++%26%2B%5Calpha_K%28t-1%29+M_%7Bt-1%7D%28y_%7Bt-1%7D%3DK%2C+y_%7Bt%7D%3D1+%7C+x%29+%5Cend%7Baligned%7D+%5C%5C)

![img](https://pic3.zhimg.com/v2-59611149b46646ca0ae1a2fcc052e5ce_b.jpg)

###  part4.1.2后向算法

CRF中后向算法的计算的条件概率为：

- `CRF中后向算法计算的概率为`： ![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_i%28t%29+%3D+p%28y_t%3Di%2C+y_%7Bt%2B1%7D%2C+%5Ccdots%2C+y_T%7Cx%29), 因此下一时刻的表达式为，![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_k%28t%2B1%29+%3D+p%28y_%7Bt%2B1%7D%3Dk%2C+y_%7Bt%2B2%7D%2C+%5Ccdots%2C+y_T%7Cx%29)，![[公式]](https://www.zhihu.com/equation?tex=i)和![[公式]](https://www.zhihu.com/equation?tex=k)都是具体的隐含状态取值，为了区分不同时刻的不同状态，故这样写。

与前向算法的推导类似，需要构造出![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_i%28t%29)和![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_k%28t%2B1%29)的关系，下面开始推导，部分内容不进行解释，如果疑问，可以参考前向算法：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++++%5Cbeta_i%28t%29+%26%3D+p%28y_t%3Di%2C+y_%7Bt%2B1%7D%2C+%5Ccdots%2C+y_T%7Cx%29+%5C%5C+++++%26%3D%5Csum_%7Bk%3D1%7D%5EK+p%28y_t%3Di%2C+y_%7Bt%2B1%7D%3Dk%2C+%5Ccdots%2C+y_T%7Cx%29++%5C%5C+++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK++%5Cfrac%7Bp%28y_t%3Di%2C+y_%7Bt%2B1%7D%3Dk%2C+%5Ccdots%2C+y_T%2Cx%29%7D%7Bp%28x%29%7D+%5C%5C+++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+%5Cfrac%7Bp%28y_t%3Di%7Cy_%7Bt%2B1%7D%3Dk%2C+%5Ccdots%2C+y_T%2Cx%29p%28y_%7Bt%2B1%7D%3Dk%2C+%5Ccdots%2C+y_T%7Cx%29p%28x%29%7D%7Bp%28x%29%7D+%5C%5C++++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+p%28y_t%3Di%7Cy_%7Bt%2B1%7D%3Dk%2C+x%29+%5Cbeta_k%28t%2B1%29+%5C%5C+++++%26%3D+%5Csum_%7Bk%3D1%7D%5EK+M_%7Bt%2B1%7D%28y_%7Bt%7D%2C+y_%7Bt%2B1%7D+%7C+x%29+%5Cbeta_k%28t%2B1%29+%5Cend%7Baligned%7D+%5C%5C)

### part4.1.3

## part5.0 inference 

