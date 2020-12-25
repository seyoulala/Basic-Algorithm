### DeepWalk

#### 想要解决什么问题？

学习到社交网络中节点的一个低维embedding，使得嵌入后的节点embedding在嵌入空间中也能保持在原来图中的相似性。希望学习后得到的embedding能够编码节点之间的相似性和社区成员之间的关系

#### 如何学习节点的embedding？

deepwalk通过将随机游走得到的节点序列作为句子，然后使用Word2vec来学习到每个节点的一个embedding。

首先作者希望学习到的social representations具有以下特征:

- Adaptability:真实的社交网络时不断的进化的，新的社会关系不需要重复的从头开始学习
- Community aware：latent representation之间的距离应该是一种用来评估社区成员相似性的一种度量。
- Low dimensional：当有标签的数据不足的时候，低维的representation使得模型的泛化能力变得更好，同时可以使得模型训练的时候loss能快速的收敛，同时在能加快inference的速度。
- Continuous：连续的latent representation使得分类器的决策边界会变得更加平滑，从而使的分类器的分类能力更加鲁棒。

为了使得算法能够满足以上的特征，作者通过随机游走的方式来生成顶点序列，然后将顶点序列作为一个sequence使用word2vec来进行训练，从而得到每个顶点的representation。

#### 为什么有效？

随机游走在内容推荐和社区发现上已经被当做一种相似度的度量，同时随机游走能够提取local structure的信息。随机游走有两点好处：能够并行，多个线程可以同时进行游走产生不同的random walk。第二点：对于已经学习好的模型，如果原始的图结构发生了微小变化，我们不需要从头开始学习，可以使用从新图中产生的random path来迭代更新模型。

作者发现，如果连通图中节点的度服从power low的distribution，那么一个顶点出现在随机路径中的次数也是服从power low的。同时我们注意到单词在文章中出现的频率也是服从power low的。

<img src="/Users/eason/Library/Application Support/typora-user-images/image-20201113100153166.png" alt="image-20201113100153166" style="zoom:50%;" />

同时，在训练语言模型的时候，使用skipgram来进行模型，这样选择考虑的是，skipgram对建模一句话在词袋空间中的概率放宽了一些限制1）不再用句子中前面的词来预测下一个词，而是用当前词去预测句子中周围的词；2）周围的词包括当前词的左右两侧的词；3）丢掉了词序信息，并且在预测周围词的时候，不考虑与当前词的距离。优化目标是最大化同一个句子中同时出现的词的共现概率

这样不需要考虑单词出现在给定单词的前后之间的位置关系，因此这种顺序的独立性假设更加符合随机游走对于节点间距离相近的定义，

#### 如何减少计算量，避免输出端|V|维的分类？

使用**Hierarchical softmax**

<img src="https://pic4.zhimg.com/80/v2-e9cd8e4e60367c6631bed18e247e62ab_1440w.jpg" alt="img" style="zoom: 25%;" />

构建一颗二叉树，将每一个单词(顶点)分配到树的叶子节点上。在实际做分类的时候，从根节点出发一直走到叶子节点，在每一个中间节点都做一个二分类的任务。假设构建的树是一颗满二叉树，词汇表的大小是V，那么从根节点走到叶节点只需要计算logV次，当V是一个很大的数值是，计算效率远远提高。

那么具体如何计算呢？我们以v1作为输入来预测v5.

具体如何计算？我们以上图中用 ![[公式]](https://www.zhihu.com/equation?tex=v_1) 预测 ![[公式]](https://www.zhihu.com/equation?tex=v_5) 为例进行介绍。树的根部输入的是 ![[公式]](https://www.zhihu.com/equation?tex=v_1) 的向量，用 ![[公式]](https://www.zhihu.com/equation?tex=%5Cphi%28v_1%29) 表示。在二叉树的每一个节点上都存放一个向量，需要通过学习得到，最后的叶子节点上没有向量。显而易见，整棵树共有|V|个向量。规定在第k层的节点做分类时，节点左子树为正类别，节点右子树是负类别，该节点的向量用 ![[公式]](https://www.zhihu.com/equation?tex=v%28k%29) 表示。那么正负类的分数如公式(2)(3)所示。在预测的时候，需要按照蓝色箭头的方向做分类，第0层分类结果是负类，第1层分类结果是正类，第2层分类结果是正类，最后到达叶子节点 ![[公式]](https://www.zhihu.com/equation?tex=v_5) 。最后把所有节点的分类分数累乘起来，作为 ![[公式]](https://www.zhihu.com/equation?tex=v_1) 预测 ![[公式]](https://www.zhihu.com/equation?tex=v_5) 的概率，如公式(4)所示，并通过反向传播进行优化。在计算loss的时候可以通过取log的方法将连乘变为累加。

![[公式]](https://www.zhihu.com/equation?tex=p_k%28left%29+%3D+sigmoid%28%5Cphi%28v_1%29+%5Ccdot+v%28k%29%29%09%09%5Ctag%7B2%7D)

![[公式]](https://www.zhihu.com/equation?tex=p_k%28right%29+%3D1-++sigmoid%28%5Cphi%28v_1%29+%5Ccdot+v%28k%29%29+%3D+sigmoid%28-%5Cphi%28v_1%29+%5Ccdot+v%28k%29%29%09%09%5Ctag%7B3%7D)

![[公式]](https://www.zhihu.com/equation?tex=p%28v_5%7Cv_1%29+%3D+%5Cprod+p_k+%3D+p_0%28right%29+%C2%B7+p_1%28left%29%C2%B7+p_2%28left%29%09%09%5Ctag%7B4%7D+)

Huffman编码是一种熵编码方式，对于出现频率高的符号用较短的编码表示，出现频率较低的符号用较长的编码表示，从而达到编码压缩的目的。Hierarchical Softmax树也可以采用Huffman编码的方式生成，高频词用较短的路径到达，低频词用较长的路径到达，可以进一步降低整个训练过程的计算量。

顺便提一句，如果输出端是对所有词的softmax分类的话，那么在Skip-gram模型中，分别有输入和输出两个矩阵，一般是采用输出矩阵作为表示向量。但是如果采用Hierarchical Softmax分类的话，输出端就不存在输出矩阵了，就只能采用输入矩阵作为表示向量了。

#### 具体算法

<img src="/Users/eason/Library/Application Support/typora-user-images/image-20201120154647637.png" alt="image-20201120154647637" style="zoom:50%;" align='left'/><img src="/Users/eason/Library/Application Support/typora-user-images/image-20201120155029492.png" alt="image-20201120155029492" style="zoom:50%;" >











Deepwalk的思想很简单，就是通过随机游走采样节点产生的顶点序列作为句子序列，然后使用skipgram来进行训练，从而顶点的embedding表示。左边的伪代码中G表示图，w表示skipgram中的窗口大小，d表示嵌入维度，$\gamma$表示随机游走的次数，t表示游走的长度。第一步表示初始化节点的表示向量，第二步根据顶点出现的频率来构建哈夫曼树，第5步表示对每一个节点$v_{i}$开始进行随机游走，将生成的顶点序列使用skipgram进行训练。

前文提到过，Skip-Gram丢掉了句子中的词序信息，以及词与词之间的距离信息，这也适合网络表示学习，丢掉随机游走的顺序信息能够灵活地捕获节点之间的邻近关系。另外，如果两个节点具有相同的邻域，Skip-Gram学习出来的表示向量接近或者相似，有利于在下游任务上取得好的效果。

不管是在NLP中，还是在graph中，学习到的向量只是中间结果，用于作为下游任务的输入。例如在图中对节点做多标签分类任务时，第一步先通过DeepWalk进行无监督训练，得到所有节点的特征向量；第二步，通过一些分类器对节点进行分类。不同于传统的方法，DeepWalk将标签和表示空间分割开来，标签和表示向量相互独立，学习到的特征向量可以应用于各种不同的任务。而且试验证明，特征向量和最简单的分类算法相结合，比如逻辑回归，也能获得好的效果。

算法中有一个参数t，是随机游走的步长，即需要限定随机游走的长度，不要过长，有几个好处，1）可以捕获网络中局部区域的结构信息；2）易于实现并行化，多个线程，进程，甚至服务器，可以同时随机游走网络的不同部分，实现分布式计算，这个后边还会再提一下；3）能够适应网络的变化，网络局部发生变化时，可以只对局部网络进行学习和训练，而不需要对整个网络重新学习。

