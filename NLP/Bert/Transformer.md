#  Transformer

## introduction

Transformer 用于神经机器翻译,这个架构抛弃了传统的用RNN和CNN来提取特征.因为RNN无法并行,Transformer并行速度也比CNN更快.

Transformer的encoder部分使用6个堆叠的block,每一个block又分为两层,一个self-attention层,还有一个前馈神经网络层.decoder部分也是6个block的结构的stack,每一个block由三个层组成,self-attention层,Encoder-Decoder-Attention层,还有前馈神经网络层.


## 完整的架构

![](https://pic1.zhimg.com/80/v2-9fb280eb2a69baf5ceafcfa3581aa580_hd.jpg)

## 各个层的作用

## encoder层

![](https://pic1.zhimg.com/80/v2-2f06746893477aec8af0c9c3ca1c6c14_hd.jpg)

举个例子:
**The animal didn't cross the street because it was too tired**
其中it指代的是animal还是street呢?对于人来说这很容易理解,但是对于算法就不是那么容易理解了.self-Attention层可以使得**it**指向**animal**.
主要原始是:当self-attention层处理input每个position的word时,self-attention可以查看其它位置单词来帮助encode当前的word.

**那么self-attention内部是如何计算的呢?**

![](http://jalammar.github.io/images/t/transformer_self_attention_vectors.png)


1. 如上文，将输入单词转化成嵌入向量；
2. 根据嵌入向量得到 q ， k ， v 三个向量；
3. 为每个向量计算一个score： $\text{score} = q \cdot k $；
4. 为了梯度的稳定，Transformer使用了score归一化，即除以 $ \sqrt{d_k}$(编码当前位置时,score决定了对input其它位置放置多少注意力);
5. 对score施以softmax激活函数；(这个分数决定了在当前位置时候,各个单词的表达程度)
6. softmax点乘Value值 v ，得到加权的每个输入向量的 v ；
7. 相加之后得到最终的输出结果 z ： z=\sum v 。

上面步骤的可以表示下图的形式。

![](http://jalammar.github.io/images/t/transformer_self_attention_score.png)

注意,在self-attention层中加入了short-cut结构,目的是解决DL中学习的退化问题.还有BN

### multi-headed attention


Multi-Head Attention相当于 h 个不同的self-attention的集成（ensemble），在这里我们以 h=8 举例说明。Multi-Head Attention的输出分成3步：

1. 将数据 X  分别输入到图13所示的8个self-attention中，得到8个加权后的特征矩阵 Z_i, i\in\{1,2,...,8\} 。
2. 将8个 Z_i 按列拼成一个大的特征矩阵；
3. 特征矩阵经过一层全连接后得到输出 Z 。

![](http://jalammar.github.io/images/t/transformer_multi-headed_self-attention-recap.png)

**优势**
1. 扩展了模型对不同位置编码的注意力能力.
2. 给了attention层多个表示的子空间.

### Encoder-Decoder Attention



### 位置编码,残差连接.

![](http://jalammar.github.io/images/t/transformer_positional_encoding_vectors.png)

![](http://jalammar.github.io/images/t/transformer_resideual_layer_norm_2.png)

### Decoder


![](http://jalammar.github.io/images/t/transformer_decoding_1.gif)

重复以上步骤,上一个解码的输出要作为下一步骤解码的输入

![](http://jalammar.github.io/images/t/transformer_decoding_2.gif)

### Decoder层中的 Encoder-Decoder Attention

**我的理解**

1. Self-Attention：当前翻译和已经翻译的前文之间的关系；(类似RNN中的隐藏层状态,表示上下文关系)
2. Encoder-Decnoder Attention：当前翻译和编码的特征向量之间的关系。(类似RNN中的attention,表示翻译这个位置时候注意力应该放在什么地方)

### Linear layer and softmax layer

![](http://jalammar.github.io/images/t/transformer_decoder_output_softmax.png)




