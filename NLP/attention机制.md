### Part1.0 attention的由来

Attention机制最早的应用是在machine translation中，通过seq2seq这种encoder和decoder的模型结构来完成源语言到目标语言的翻译工作。其中encoder和decoder使用的模型主要是RNN/LSTM/Transformer。在早期的seq2seq模型中基本上是使用RNN来进行源语言的encoder工作。但是由于rnn存在梯度消失的问题导致在输入文本过长时模型无法捕获到文本之间的长期依赖关系，导致源语言通过rnn进行编码后会丢失掉很大一部分信息。同时在decoder解码的时候，按照人类的思维在解码当前词时我们应该将注意力关注在源语言相对应的单词的上下文并结合之前已经翻译过的部分。如下图所示

![img](https://pic1.zhimg.com/80/v2-ef2e241114ab58a033e31f76b598a898_1440w.jpg)

当我们翻译“knowledge”时，只需将注意力放在源句中“知识”的部分，当翻译“power”时，只需将注意力集中在"力量“。这样，当我们decoder预测目标翻译的时候就可以看到encoder的所有信息，而不仅局限于原来模型中定长的隐藏向量，并且不会丧失长程的信息。

### part2.0 attention的定义

参考[Attention is all your need](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1706.03762.pdf)中关于attention的定义。假设在当前时刻$T$有一个$query$向量,这个query向量可以看成是一个包含了比较多的信息的一个vector，同时在$T$时刻还有一段key向量，我们使用query向量和这些key向量计算一个similarity得到了query向量和key向量之间的一个相似度。然后我们得到的相似度进行一个归一化操作得到了一组权重序列，然后我们对key向量对应的value向量使用之前得到的权重序列进行加权求和得到了当前时刻$T$的一个新的表示向量。具体的操作可以抽象成如下的形式：
$$
\\ s(q_{t},k_{t}) = f(q_{t},k_{t})
\\a(q_t,k_t) =\frac{exp(s(q_{t},k_{t})}{\sum_{i=1}^{T}{s(q_{t},k_{i})}}
\\Attention(q_t,k,v) =\sum_{i=1}^{T}{a_{i}(q_t,k_i)\cdot{v_{i}}} 
$$
对于同一段key，不同的query会得到不同的输出向量。对应在具体的任务中，比如在machine translation中，query就是decoder中t时刻的hidden state，key就是encoder中每个时刻的hidden state。value等同于encoder中每个时刻的hidden state。

### part3.0 attention类型

attention有很多不同的形式，不同attention的主要区别可以分为如下几个方面：1.query向量和key向量计算similarity的函数形式不同；2.query向量和那些key向量进行similarity计算；

**1. 计算区域**

根据Attention的计算区域，可以分成以下几种：

1）**Soft** Attention，这是比较常见的Attention方式，对所有key求权重概率，每个key都有一个对应的权重，是一种全局的计算方式（也可以叫Global Attention）。这种方式比较理性，参考了所有key的内容，再进行加权。但是计算量可能会比较大一些。

2）**Hard** Attention，这种方式是直接精准定位到某个key，其余key就都不管了，相当于这个key的概率是1，其余key的概率全部是0。因此这种对齐方式要求很高，要求一步到位，如果没有正确对齐，会带来很大的影响。另一方面，因为不可导，一般需要用强化学习的方法进行训练。（或者使用gumbel softmax之类的）

3）**Local** Attention，这种方式其实是以上两种方式的一个折中，对一个窗口区域进行计算。先用Hard方式定位到某个地方，以这个点为中心可以得到一个窗口区域，在这个小区域内用Soft方式来算Attention。



**2. 所用信息**

假设我们要对一段原文计算Attention，这里原文指的是我们要做attention的文本，那么所用信息包括内部信息和外部信息，内部信息指的是原文本身的信息，而外部信息指的是除原文以外的额外信息。

1）**General** Attention，这种方式利用到了外部信息，常用于需要构建两段文本关系的任务，query一般包含了额外信息，根据外部query对原文进行对齐。

比如在阅读理解任务中，需要构建问题和文章的关联，假设现在baseline是，对问题计算出一个问题向量q，把这个q和所有的文章词向量拼接起来，输入到LSTM中进行建模。那么在这个模型中，文章所有词向量共享同一个问题向量，现在我们想让文章每一步的词向量都有一个不同的问题向量，也就是，在每一步使用文章在该步下的词向量对问题来算attention，这里问题属于原文，文章词向量就属于外部信息。

2）**Local** Attention，这种方式只使用内部信息，key和value以及query只和输入原文有关，在self attention中，key=value=query。既然没有外部信息，那么在原文中的每个词可以跟该句子中的所有词进行Attention计算，相当于寻找原文内部的关系。

还是举阅读理解任务的例子，上面的baseline中提到，对问题计算出一个向量q，那么这里也可以用上attention，只用问题自身的信息去做attention，而不引入文章信息。



**3. 结构层次**

结构方面根据是否划分层次关系，分为单层attention，多层attention和多头attention：

1）单层Attention，这是比较普遍的做法，用一个query对一段原文进行一次attention。

2）多层Attention，一般用于文本具有层次关系的模型，假设我们把一个document划分成多个句子，在第一层，我们分别对每个句子使用attention计算出一个句向量（也就是单层attention）；在第二层，我们对所有句向量再做attention计算出一个文档向量（也是一个单层attention），最后再用这个文档向量去做任务。

3）多头Attention，这是Attention is All You Need中提到的multi-head attention，用到了多个query对一段原文进行了多次attention，每个query都关注到原文的不同部分，相当于重复做多次单层attention：

![[公式]](https://www.zhihu.com/equation?tex=head_i+%3D+Attention%28q_i%2C+K%2C+V%29)

最后再把这些结果拼接起来：

![[公式]](https://www.zhihu.com/equation?tex=MultiHead%28Q%EF%BC%8C+K%EF%BC%8C+V%29+%3D+Concat%28head_1%2C+...%2C+head_h%29W%5E%7BO%7D)



**4. 模型方面**

从模型上看，Attention一般用在CNN和LSTM上，也可以直接进行纯Attention计算。

**1）CNN+Attention**

CNN的卷积操作可以提取重要特征，我觉得这也算是Attention的思想，但是CNN的卷积感受视野是局部的，需要通过叠加多层卷积区去扩大视野。另外，Max Pooling直接提取数值最大的特征，也像是hard attention的思想，直接选中某个特征。

CNN上加Attention可以加在这几方面：

a. 在卷积操作前做attention，比如Attention-Based BCNN-1，这个任务是文本蕴含任务需要处理两段文本，同时对两段输入的序列向量进行attention，计算出特征向量，再拼接到原始向量中，作为卷积层的输入。

b. 在卷积操作后做attention，比如Attention-Based BCNN-2，对两段文本的卷积层的输出做attention，作为pooling层的输入。

c. 在pooling层做attention，代替max pooling。比如Attention pooling，首先我们用LSTM学到一个比较好的句向量，作为query，然后用CNN先学习到一个特征矩阵作为key，再用query对key产生权重，进行attention，得到最后的句向量。



**2）LSTM+Attention**

LSTM内部有Gate机制，其中input gate选择哪些当前信息进行输入，forget gate选择遗忘哪些过去信息，我觉得这算是一定程度的Attention了，而且号称可以解决长期依赖问题，实际上LSTM需要一步一步去捕捉序列信息，在长文本上的表现是会随着step增加而慢慢衰减，难以保留全部的有用信息。

LSTM通常需要得到一个向量，再去做任务，常用方式有：

a. 直接使用最后的hidden state（可能会损失一定的前文信息，难以表达全文）

b. 对所有step下的hidden state进行等权平均（对所有step一视同仁）。

c. Attention机制，对所有step的hidden state进行加权，把注意力集中到整段文本中比较重要的hidden state信息。性能比前面两种要好一点，而方便可视化观察哪些step是重要的，但是要小心过拟合，而且也增加了计算量。



**3）纯Attention**

Attention is all you need，没有用到CNN/RNN，乍一听也是一股清流了，但是仔细一看，本质上还是一堆向量去计算attention。



**5. 相似度计算方式**

在做attention的时候，我们需要计算query和某个key的分数（相似度），常用方法有：

1）点乘：最简单的方法， ![[公式]](https://www.zhihu.com/equation?tex=s%28q%2C+k%29+%3D+q%5E%7BT%7Dk)

2）矩阵相乘： ![[公式]](https://www.zhihu.com/equation?tex=s%28q%2C+k%29+%3D+q%5E%7BT%7DWk)

3）cos相似度： ![[公式]](https://www.zhihu.com/equation?tex=s%28q%2C+k%29+%3D+%5Cfrac%7Bq%5E%7BT%7Dk%7D%7B%7C%7Cq%7C%7C%5Ccdot%7C%7Ck%7C%7C%7D)

4）串联方式：把q和k拼接起来， ![[公式]](https://www.zhihu.com/equation?tex=s%28q%2C+k%29+%3D+W%5Bq%3Bk%5D)

5）用多层感知机也可以： ![[公式]](https://www.zhihu.com/equation?tex=s%28q%2C+k%29+%3D+v_%7Ba%7D%5E%7BT%7Dtanh%28Wq+%2B+Uk%29)

------

**Part III：Task分析**

Attention机制只是一种思想，可以用到很多任务上，个人觉得Attention机制比较适合有以下特点的任务：

1）**长文本任务**，document级别，因为长文本本身所携带的信息量比较大，可能会带来信息过载问题，很多任务可能只需要用到其中一些关键信息（比如文本分类），所以Attention机制用在这里正适合capture这些关键信息。

2）涉及到两段的**相关文本**，可能会需要对两段内容进行对齐，找到这两段文本之间的一些相关关系。比如机器翻译，将英文翻译成中文，英文和中文明显是有对齐关系的，Attention机制可以找出，在翻译到某个中文字的时候，需要对齐到哪个英文单词。又比如阅读理解，给出问题和文章，其实问题中也可以对齐到文章相关的描述，比如“什么时候”可以对齐到文章中相关的时间部分。

3）任务很大部分取决于**某些特征**。我举个例子，比如在AI+法律领域，根据初步判决文书来预测所触犯的法律条款，在文书中可能会有一些罪名判定，而这种特征对任务是非常重要的，所以用Attention来capture到这种特征就比较有用。（CNN也可以）



下面介绍我了解到的一些task，其中机器翻译、摘要生成、图文互搜属于seq2seq任务，需要对两段内容进行对齐，文本蕴含用到前提和假设两段文本，阅读理解也用到了文章和问题两段文本，文本分类、序列标注和关系抽取属于单文本Attention的做法。

1）机器翻译：encoder用于对原文建模，decoder用于生成译文，attention用于连接原文和译文，在每一步翻译的时候关注不同的原文信息。

2）摘要生成：encoder用于对原文建模，decoder用于生成新文本，从形式上和机器翻译都是seq2seq任务，但是从任务特点上看，机器翻译可以具体对齐到某几个词，但这里是由长文本生成短文本，decoder可能需要capture到encoder更多的内容，进行总结。

3）图文互搜：encoder对图片建模，decoder生成相关文本，在decoder生成每个词的时候，用attention机制来关注图片的不同部分。



4）文本蕴含：判断前提和假设是否相关，attention机制用来对前提和假设进行对齐。

5）阅读理解：可以对文本进行self attention，也可以对文章和问题进行对齐。



6）文本分类：一般是对一段句子进行attention，得到一个句向量去做分类。

7）序列标注：[Deep Semantic Role Labeling with Self-Attention](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/1712.01586)，这篇论文在softmax前用到了self attention，学习句子结构信息，和利用到标签依赖关系的CRF进行pk。

8）关系抽取：也可以用到self attention







