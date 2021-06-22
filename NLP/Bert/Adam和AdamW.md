#### Adam

Adam优化算法可以看成是`动量法`和`Rmsprop`算法的结合。首先来看看`动量法`和`Rmsprop`的提出是为了解决什么问题。

##### 动量法

首先`动量法`是为了解决使用梯度梯度下降法的过程中，多元变量之间梯度大小不一致而导致在使用较大学习率的情况，梯度较大的那一维梯度变化过快，梯度较小的那一维变量变化较慢而导致的目标函数收敛过慢或者无法收敛的问题。

<img src="https://tangshusen.me/Dive-into-DL-PyTorch/img/chapter07/7.4_output1.png" alt="img" style="zoom:50%;" />

如上图所示，目标函数$y=0.1x^2+2x^2$,在x2这一维度上的梯度明显大于x1这一维度的梯度。因此在使用梯度下降法的过程中，当使用相同学习率的情况下x2这个维度的自变量的变化趋势会明显大于x1这个维度。当学习率过大的时候，很有可能因为x2这维度变化过快而导致自变量不收敛的情况，从而在求解最优解的时候越过最优解。如下图所示：

<img src="https://tangshusen.me/Dive-into-DL-PyTorch/img/chapter07/7.4_output2.png" alt="img" style="zoom:50%;" />

当学习率过大的时候，x2这一维度因为梯度较大，自变量变化较快从而使得在在后续的梯度下降过程中越过了最优解的位置(-1,0),同时在x2这维度上自变量在持续震荡。

为了缓解这个问题，可以使用较低的学习率从而降低自变量的变化速度。但是过小的学习率使用梯度较小的那一维度自变量变化过慢又会影响到最后的寻找最优解的结果。**那么有没有什么方法可以在使用较大的学习率(加速收敛)的情况下避免上诉提到的这些问题呢？**

动量法中引入`速度变量`这个状态变量。

定义时刻$t$时，小批量随机梯度为$g_t$,自变量为$x_t$,速度变量为$v_t$，此时自变量的迭代公式如下图所示:
$$
v_t = \gamma\cdot v_{t-1}+n_t\cdot g_t \\
x_t =x_{t-1} - v_t
$$
当自变量使用这个更新方式后

①当使用较小的学习率时，x1维度也能更快的收敛，同时x1侧移动也会更加平滑。

<img src="https://tangshusen.me/Dive-into-DL-PyTorch/img/chapter07/7.4_output3.png" alt="img" style="zoom:50%;" />



②当使用更大的学习率时，x2侧移动的也更加平滑，x2不再发散。

<img src="https://tangshusen.me/Dive-into-DL-PyTorch/img/chapter07/7.4_output4.png" alt="img" style="zoom:50%;" />

##### 指数移动加权平均

给定超参数$0<\gamma<1$，当前时间步$t$的变量$y_t = \gamma \cdot y_{t-1} +(1-\gamma)\cdot x_t$

<img src="/Users/eason/Library/Application%20Support/typora-user-images/image-20210510152450367.png" alt="image-20210510152450367" style="zoom:50%;" />

<img src="/Users/eason/Library/Application%20Support/typora-user-images/image-20210510152622358.png" alt="image-20210510152622358" style="zoom:50%;" />

##### Rmsprop

Rmsprop算法是在AdaGrad的基础上进行改进的，在动量法中，所有自变量都有相同的学习率，但是我们希望的是自变量梯度小的学习率较大，自变量梯度较大的学习率较小。也就是学习率根据自变量的梯度进行动态调整。AdaGrad中关于自变量的迭代公式如下所示:
$$
s_t = s_{t-1} + g_t \odot g_t \\
x_t = x_{t-1} -\frac{\eta}{\sqrt{s_t+\epsilon}}\odot{g_t}
$$
需要强调的是，小批量随机梯度按元素平方的累加变量$s_t$出现在学习率的分母项中。因此，如果目标函数有关自变量中某个元素的偏导数一直都较大，那么该元素的学习率将下降较快；反之，如果目标函数有关自变量中某个元素的偏导数一直都较小，那么该元素的学习率将下降较慢。然而，由于$s_t$一直在累加按元素平方的梯度，自变量中每个元素的学习率在迭代过程中一直在降低（或不变）。所以，**当学习率在迭代早期降得较快且当前解依然不佳时，AdaGrad算法在迭代后期由于学习率过小，可能较难找到一个有用的解**。

<img src="https://tangshusen.me/Dive-into-DL-PyTorch/img/chapter07/7.5_output1.png" alt="img" style="zoom:50%;" />

为了缓解这种影响，Rmsprop对状态变量$s_t$使用了指数加权平均。这样s_t的累加速度就不会过快，从而在自变量的迭代后期学习率也不会变的过小。

迭代公式如下图所示:
$$
s_t = \gamma\cdot{s_{t-1}}+(1-\gamma)g_t\odot{g_t} \\
x_t = x_{t-1} -\frac{\eta}{\sqrt{s_t+\epsilon}}\odot{g_t}
$$
<img src="https://tangshusen.me/Dive-into-DL-PyTorch/img/chapter07/7.6_output1.png" alt="img" style="zoom:50%;" />

对比上面AdamGrad和Rmsprop的自变量迭代图，可以发现使用AdamGrad优化算法后，在迭代后期，因为学习率一直在变小，x1维度自变量的变化已经很缓慢了，而此时x1并没有收敛。但是使用Rmsprop后，自变量收敛速度明显变快。

` 讲完了动量法和Rmsprop之后，开始Adam优化算法讲解。`

Adam优化算法在Rmsprop的基础上对小批量随机梯度也使用指数移动加权平均。同时为了解决早期迭代指数加权和过小的问题，引入了偏差修正。

<img src="/Users/eason/Library/Application%20Support/typora-user-images/image-20210510161953170.png" alt="image-20210510161953170" style="zoom:50%;" />

#### AdamW

AdamW是对Adam+L2 regularization的一种修正。

Adam自动调整学习率，大幅提高了训练速度，也很少需要调整学习率，但是有相当多的资料报告Adam优化的最终精度略低于SGD。问题出在哪呢，其实Adam本身没有问题，问题在于目前大多数DL框架的L2 regularization实现用的是weight decay的方式，而weight decay在与Adam共同使用的时候有互相耦合。

<img src="https://pic1.zhimg.com/80/v2-9f8efff3ca5c7e76a104c662f1a24070_1440w.jpg" alt="img" style="zoom: 50%;" />adam+L2 regularization(红色); adamw(绿色)

红色是传统的Adam+L2 regularization的方式，梯度 ![[公式]](https://www.zhihu.com/equation?tex=g_t) 的移动平均 ![[公式]](https://www.zhihu.com/equation?tex=m_t) 与梯度平方的移动平均 ![[公式]](https://www.zhihu.com/equation?tex=v_t) 都加入了 ![[公式]](https://www.zhihu.com/equation?tex=%5Clambda+%5Cboldsymbol%7B%5Ctheta_%7Bt-1%7D%7D) 。

> line 9的 ![[公式]](https://www.zhihu.com/equation?tex=%5Chat%7B%5Cboldsymbol%7Bm%7D%7D_%7Bt%7D) 是在对于移动平均的初始时刻做修正，当t足够大时， ![[公式]](https://www.zhihu.com/equation?tex=%5Chat%7B%5Cboldsymbol%7Bm%7D%7D_%7Bt%7D%3D%5Cboldsymbol%7Bm%7D_%7Bt%7D) 。初始时刻 ![[公式]](https://www.zhihu.com/equation?tex=t%3D1) 时，假设 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbeta_1%3D0.9) ,初始化![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol+%7Bm%7D_%7B0%7D%3D0) , ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol+%7Bm%7D_1%3D0.9+%5Ccdot+0+%2B+0.1+%5Ccdot+%5Cboldsymbol+%7Bg_1%7D%3D0.1+%5Cboldsymbol+g_1) ，这显然不合理，但是除以 ![[公式]](https://www.zhihu.com/equation?tex=1-%5Cbeta_1%5Et%3D1-0.9%3D0.1) 后 ![[公式]](https://www.zhihu.com/equation?tex=%5Chat%7B%5Cboldsymbol%7Bm%7D%7D_%7Bt%7D%3D%5Cboldsymbol%7Bg%7D_%7Bt%7D) 。line 10同理，因此后面都假设t足够大，![[公式]](https://www.zhihu.com/equation?tex=%5Chat%7B%5Cboldsymbol%7Bm%7D%7D_%7Bt%7D%3D%5Cboldsymbol%7Bm%7D_%7Bt%7D)

如果把line 6, line 7, line 8都带入line 12，并假设 ![[公式]](https://www.zhihu.com/equation?tex=%5Ceta_t%3D1) ( ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha+) 为学习率):

![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol+%5Ctheta_%7Bt%7D+%5Cleftarrow+%5Cboldsymbol+%5Ctheta_%7Bt-1%7D-%5Calpha+%5Cfrac%7B%5Cbeta_%7B1%7D+%5Cboldsymbol+m_%7Bt-1%7D%2B%5Cleft%281-%5Cbeta_%7B1%7D%5Cright%29%5Cleft%28%5Cnabla+%5Cboldsymbol+f_%7Bt%7D%2B%5Clambda+%5Cboldsymbol+%5Ctheta_%7Bt-1%7D%29%5Cright.%7D%7B%5Csqrt%7B%5Chat%7B%5Cboldsymbol+%7Bv%7D%7D_%7Bt%7D%7D%2B%5Cepsilon%7D%5C%5C)

分子右上角的 ![[公式]](https://www.zhihu.com/equation?tex=%5Clambda+%5Cboldsymbol+%7B%5Ctheta%7D_%7Bt-1%7D) 向量各个元素被分母的 ![[公式]](https://www.zhihu.com/equation?tex=%5Csqrt%7B%5Chat%7B%5Cboldsymbol+%7Bv%7D%7D_%7Bt%7D%7D) 项调整了。梯度快速变化的方向上，![[公式]](https://www.zhihu.com/equation?tex=%5Csqrt%7B%5Chat%7B%5Cboldsymbol+%7Bv%7D%7D_%7Bt%7D%7D)有更大的值，而使得调整后的![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac+%7B%5Clambda+%5Cboldsymbol+%7B%5Ctheta%7D_%7Bt-1%7D%7D%7B%5Csqrt%7B%5Chat%7B%5Cboldsymbol+%7Bv%7D%7D_%7Bt%7D%7D%7D)更小，在这个方向上 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol+%5Ctheta) 被正则化地更少。这显然是不合理的，L2 regularization与weight decay都应该是各向同性的，因此论文作者提出绿色方式来接入weight decay。也即不让![[公式]](https://www.zhihu.com/equation?tex=%5Clambda+%5Cboldsymbol+%7B%5Ctheta%7D_%7Bt-1%7D)项被 ![[公式]](https://www.zhihu.com/equation?tex=%5Csqrt%7B%5Chat%7B%5Cboldsymbol+%7Bv%7D%7D_%7Bt%7D%7D) 调整。完成梯度下降与weight decay的解耦。

