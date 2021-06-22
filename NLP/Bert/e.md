### Transformer-XL

Transformer-XL通过 segent-level recurrence mechanism 和 releative position-embedding 来解决 *context fragmentation*的问题，在之前Transformer的输入都是固定长度的，对于文本超过fixed-length的文本就需要重新计算新的segment的hidden state，但是这样会造成next segment 与previous segment之间的依赖分裂开了，就会造成了上下文碎片化的问题，Transformer-XL通过引入segent-level recurrence mechanism来解决上下文碎片化的问题使得model可以学的更长的依赖关系。同时对于原Transformer中的position embedding是一种绝对编码，不同segment中的token在固定位置的表示都是一样的，所以这是有问题的，Transformer-XL通过releative position embedding来解决这个问题。



### Model

在 vanilla Transformer中对输入input以大小为4的窗口进行划分segment,然后评估的时候只在窗口的最后一个位置进行评估，同时整个窗口右移一位，目的是为了尽可能利用上下文的信息。处理过程如下所示。

![](https://pic3.zhimg.com/80/v2-086a5ccc7f47316538a4979b0beb3526_hd.jpg)

以上的训练方式有两个很明显的缺陷：

1. 模型所能学习到的上下文的依赖受到segment的长度所限制，最长也就只能学到segment长度的依赖。
2. 将长文本进行截断到fixed length 或者对短文本进行padding会产生上下文碎片化( context fragmentation)的问题。

### Segment-Level Recurrence with State Reuse

![](https://pic2.zhimg.com/80/v2-a2f2843801970c600609488392877f0d_hd.jpg)

为了解决固定长度文本的限制，Transformer-XL通过recurrence mechanism机制，在训练的过程中，通过将之前segment计算出来的hidden state 缓存下来同时用到下一个segment中。从公式上来看第n层中第i+1个segment是如何使用第i个segment的hidden state的。使用$S_{\gamma}=[x_{\gamma,1},...,x_{\gamma,L}]$表示第一个segment，$S_{\gamma+1}=[x_{\gamma+1,1},...,x_{\gamma+1,L}]$表示下一个segment。

第n层的第i+1个segment的隐状态计算公式如下：

![[公式]](https://www.zhihu.com/equation?tex=%5Cwidetilde%7B%5Cmathbf%7Bh%7D%7D_%7B%5Ctau%2B1%7D%5E%7Bn-1%7D%3D%5Cleft%5B%5Cmathrm%7BSG%7D%5Cleft%28%5Cmathbf%7Bh%7D_%7B%5Ctau%7D%5E%7Bn-1%7D%5Cright%29+%5Ccirc+%5Cmathbf%7Bh%7D_%7B%5Ctau%2B1%7D%5E%7Bn-1%7D%5Cright%5D%5C%5C)
![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7Bq%7D_%7B%5Ctau%2B1%7D%5E%7Bn%7D%2C+%5Cmathbf%7Bk%7D_%7B%5Ctau%2B1%7D%5E%7Bn%7D%2C+%5Cmathbf%7Bv%7D_%7B%5Ctau%2B1%7D%5E%7Bn%7D%3D%5Cmathbf%7Bh%7D_%7B%5Ctau%2B1%7D%5E%7Bn-1%7D+%5Cmathbf%7BW%7D_%7Bq%7D%5E%7B%5Ctop%7D%2C+%5Ctilde%7B%5Cmathbf%7Bh%7D%7D_%7B%5Ctau%2B1%7D%5E%7Bn-1%7D+%5Cmathbf%7BW%7D_%7Bk%7D%5E%7B%5Ctop%7D%2C+%5Cwidetilde%7B%5Cmathbf%7Bh%7D%7D_%7B%5Ctau%2B1%7D%5E%7Bn-1%7D+%5Cmathbf%7BW%7D_%7Bv%7D%5E%7B%5Ctop%7D%5C%5C)
![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7Bh%7D_%7B%5Ctau%2B1%7D%5E%7Bn%7D%3D%5Ctext+%7B+Transformer-Layer+%7D%5Cleft%28%5Cmathbf%7Bq%7D_%7B%5Ctau%2B1%7D%5E%7Bn%7D%2C+%5Cmathbf%7Bk%7D_%7B%5Ctau%2B1%7D%5E%7Bn%7D%2C+%5Cmathbf%7Bv%7D_%7B%5Ctau%2B1%7D%5E%7Bn%7D%5Cright%29%5C%5C)

![[公式]](https://www.zhihu.com/equation?tex=SG%28%5Ccdot%29) 函数表示的是梯度截断或者梯度停止(stop-gradient)， ![[公式]](https://www.zhihu.com/equation?tex=%5Cleft%5B%5Cmathbf%7Bh%7D_%7Bu%7D+%5Ccirc+%5Cmathbf%7Bh%7D_%7Bv%7D%5Cright%5D) 表示两者拼接。以上就是Transformer XL的主体结构。在当前步引入上文隐状态，并且复用隐状态，加速训练，并且解决context fragmentation问题。**注意到$q_{\gamma+1}^n$**是没有用到上一个segment的hidden state的。



###  Relative Positional Encodings

我们知道Transformer对时序的信息是不敏感的，但是时序信息却是一个很重要的信息，所以一般都会在word-embedding上加上position-embedding以添加位置信息。但是在Transformer-XL中，不同的segment中相同位置的position-embedding如果使用绝对位置编码的话是无法区分开来的。

引入可以创建一组相对位置编码 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7BR%7D+%5Cin+%5Cmathbb%7BR%7D%5E%7BL_%7B%5Cmax+%7D+%5Ctimes+d%7D) ，其中第i行Ri表示i在两个位置之间的相对距离。绝对位置编码公式为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7BA%7D_%7Bi%2C+j%7D%5E%7B%5Cmathrm%7Babs%7D%7D%3Dq_%7Bi%7D%5E%7B%5Ctop%7D+k_%7Bj%7D%3D%5Cunderbrace%7B%5Cmathbf%7BE%7D_%7Bx_%7Bi%7D%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bq%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bk%7D+%5Cmathbf%7BE%7D_%7Bx_%7Bj%7D%7D%7D_%7B%28a%29%7D%2B%5Cunderbrace%7B%5Cmathbf%7BE%7D_%7Bx_%7Bi%7D%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bq%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bk%7D+%5Cmathbf%7BU%7D_%7Bj%7D%7D_%7B%28b%29%7D%2B%5Cunderbrace%7B%5Cmathbf%7BU%7D_%7Bi%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bq%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bk%7D+%5Cmathbf%7BE%7D_%7Bx_%7Bj%7D%7D%7D_%7B%28c%29%7D%2B%5Cunderbrace%7B%5Cmathbf%7BU%7D_%7Bi%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bq%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bk%7D+%5Cmathbf%7BU%7D_%7Bj%7D%7D_%7B%28d%29%7D%5C%5C)
相对位置编码公式为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7BA%7D_%7Bi%2C+j%7D%5E%7B%5Cmathrm%7Brel%7D%7D%3D%5Cunderbrace%7B%5Cmathbf%7BE%7D_%7Bx_%7Bi%7D%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bq%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bk%2C+E%7D+%5Cmathbf%7BE%7D_%7Bx_%7Bj%7D%7D%7D_%7B%28a%29%7D%2B%5Cunderbrace%7B%5Cmathbf%7BE%7D_%7Bx_%7Bi%7D%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bq%7D%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bk%2C+R%7D+%5Cmathbf%7BR%7D_%7Bi-j%7D%7D_%7B%28b%29%7D%2B%5Cunderbrace%7Bu%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bk%2C+E%7D+%5Cmathbf%7BE%7D_%7Bx_%7Bj%7D%7D%7D_%7B%28c%29%7D%2B%5Cunderbrace%7Bv%5E%7B%5Ctop%7D+%5Cmathbf%7BW%7D_%7Bk%2C+R%7D+%5Cmathbf%7BR%7D_%7Bi-j%7D%7D_%7B%28d%29%7D%5C%5C)

同时，position-embedding的信息也不是和word-embedding相加送到neural network中了，而是在计算attention的时候进行编码位置信息。

