lightgbm

### lightGbm直方图优化

不同于xgboost在寻找分裂点的时候遍历所有样本每个特征的每个取值,ligtm通过将连续特征进行离散化也就是将连续特征分桶，将某个区间的值映射成某个数字.统计每个bin中的一阶导和二阶导。对所有特征构建直方图。然后 遍历所有特征的每个bin，使用和xgboost相同的评分函数来寻找最优的分割点.
同时树的树的生长策略和xgboost的也不同。一般的gbdt树生成策略都是按层生长，就是对同一层的每个叶子节点都进行分裂。但是这种分裂方式，某些节点分裂的信息增益很低，这种一般是没必要分裂的。
ligtm树生成策略是带有深度限制的leave-wise生成。就是对所有的叶子节点，只对分裂后信息增益最大的那个进行分裂。但是这样后造成树的深度过深，容易过拟合，所以可以对树的深度进行限制来减少过拟合.

### lightGBMde的优势

- 速度和内存使用的优化
    * 减少分割增益的计算量(构建直方图)
    * 在分割节点的时候通过直方图做差加速(父节点-左子树)
    * 将连续值替换为离散值，如果#bins较小，可以用较小的数据类型替换
    * 不需要存储pre-sorting特征值存储额外的信息
- 稀疏优化
    * 对于稀疏特征只需要o(2*#non_zero_data)来构建直方图
- 准确率的优化
    * Leaf-wise()的决策树生长策略
    * 类别特征值的最优分割
- 并行学习的优化
    * 特征并行
    * 数据并行
    * 投票并行


### 并行算法适用的场景

|            | data is small |  data is large     |
| ---------- | ---          |  ---  |   
| feature is samll |  特征并行 | 数据并行|
| feature is large       |  特征并行 |投票并行|


### 使用one-hot的弊端

1. 使用one-hot编码后，意味着每一个节点分割的时候只能使用one vs many（例如是不是狗，是不是猫）的切分方式，当类别值很多的时候，每个类别的数据可能会很少，这时候就会产生不平衡的切分
2. 会影响决策树的学习。因为在切分后，是要统计每个叶节点里面的一阶梯度和二阶梯度的，但是切分出来的数据很不平衡，如果叶子节点上的数据量很小，统计信息也会不准确，会影响到树的学习。


![](https://img-blog.csdn.net/20181022170912994?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fuc2h1YWlfYXcx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)


### LightGBM处理类别型特征

分为两种情况：one-hot形式和非one-hot形式，ont-hot是一种一对多，非one-hot的是一种多对多的形式。

![](https://img-blog.csdnimg.cn/20181230194614701.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjAwMTA4OQ==,size_16,color_FFFFFF,t_70)

对于取值类型比较多的特征，如果使用one-hot后学习的树会非常深，树的生成会很不平衡，可能会很深，这样很容易就overfitting了。

**大致流程**

在枚举分割点前，计算每个bin中的一阶梯度和二阶梯度，根据sum(g)/sum(H)的值对bin进行排序，然后在选择最优的分割点。复杂度O(klogk)

A.离散特征建立直方图的过程:

统计该特征下每一种离散值出现的次数，并从高到低排序，过滤掉出现次数较少的特征值。然后为每个取值分配一个bin

B计算分裂阈值

- 如果bin的个数比较小的话，那么直接遍历bin，找到最佳的分裂。
- 如果bin较多的话，先进行过滤，只有bin中样本数量较大的bin参与划分阈值的计算，根据sum(g)/sum(H)的值对bin进行排序，然后从左到右，从右到左进行搜索。根据评分函数选择最优分割点。同时在遍历的时候也不是搜索所有的bin，而是会设置一个最大的max_bin。


```c++
//ont-hot情形 (one vs many),类别取值小于4
if (use_onehot) {
        // 遍历每一个bin
      for (int t = 0; t < used_bin; ++t) {
        // 如果按这个bin分割后，分割后叶子节点样本数太少，或者
        二阶梯度sum太小，那么就跳过这个bin
        if (data_[t].cnt < meta_->config->min_data_in_leaf
            || data_[t].sum_hessians < meta_->config->min_sum_hessian_in_leaf) continue;
        data_size_t other_count = num_data - data_[t].cnt;
        // if data not enough
        if (other_count < meta_->config->min_data_in_leaf) continue;
 
        double sum_other_hessian = sum_hessian - data_[t].sum_hessians - kEpsilon;
        // if sum hessian too small
        if (sum_other_hessian < meta_->config->min_sum_hessian_in_leaf) continue;

```

```c++
非one-hot（many vs many）
//过滤bin，要求bin中有一定的样本数
for (int i = 0; i < used_bin; ++i) {
        if (data_[i].cnt >= meta_->config->cat_smooth) {
          sorted_idx.push_back(i);
        }
      }

//根据sum(g)/sum(h)进行排序.
auto ctr_fun = [this](double sum_grad, double sum_hess) {
        return (sum_grad) / (sum_hess + meta_->config->cat_smooth);
      };

//两层循环，从左到右，从右到左边
for (size_t out_i = 0; out_i < find_direction.size(); ++out_i) {
        auto dir = find_direction[out_i];
        auto start_pos = start_position[out_i];
        data_size_t min_data_per_group = meta_->config->min_data_per_group;
        data_size_t cnt_cur_group = 0;
        double sum_left_gradient = 0.0f;
        double sum_left_hessian = kEpsilon;
        data_size_t left_count = 0;
        for (int i = 0; i < used_bin && i < max_num_cat; ++i) {
          auto t = sorted_idx[start_pos];
          start_pos += dir;
 
          sum_left_gradient += data_[t].sum_gradients;
          sum_left_hessian += data_[t].sum_hessians;
          left_count += data_[t].cnt;
          cnt_cur_group += data_[t].cnt

```

`接下来是两个for循环，外面for循环代表的是方向即从左到右和从右到左两种遍历方式，为了便于理解这里举一个简单的例子，假设当前这一特征有4种类别：A,B,C,D,数学化后为0,1,2,3
那么我们先按照从左到右的顺序遍历，从0开始那么左树类别就是0，右树就是1,2,3,4计算增益比较更新，接着到1，那么左树就是0和1，右树就是2,3,4计算增益比较更新,接着到2，那么左树就是0,1,2右树就是3 `

**左右两遍遍历的意义，为的是处理缺失值，也就是稀疏感知算法。**

当从左到右时，我们记录不论是当前一阶导数和也好二阶导数也罢，都是针对有值的（缺省值就没有一阶导数和二阶导数），那么我们用差加速得到右子树，既然左子树没有包括缺省值，那么总的减去左子树自然就将缺省值归到右子树了，假如没有缺省值，其实这里进行两次方向的遍历并没有什么意义，为什么呢？假如最好的划分是样本1和样本3在一边，样本2和样本4在一边，那么两次方向遍历无非就是对应下图两种情况

![](https://img-blog.csdnimg.cn/20181231192237576.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjAwMTA4OQ==,size_16,color_FFFFFF,t_70)


有区别吗？其实并没有，因为下一次根据Leaf-wise原则无非就是选取左面和右面一个进行下去即可所以说1,3到底在左面还是右面并没有关系，可是当有缺省值时就完全不一样了，比如这里有一个缺省值5.于是上图就变为：

![](https://img-blog.csdnimg.cn/20181231192725533.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjAwMTA4OQ==,size_16,color_FFFFFF,t_70)



### 处理连续值特征(和类别型非one-hot一样)


### LightGBM并行学习

#### 特征并行
- 传统算法

1. 垂直划分数据（不同的机器有不同的特征集）
2. 在本地特征集寻找最佳划分点 {特征, 阈值}
3. 本地进行各个划分的通信整合并得到最佳划分
4. 以最佳划分方法对数据进行划分，并将数据划分结果传递给其他线程
5. 其他线程对接受到的数据进一步划分



**http://lightgbm.apachecn.org/#/docs/4[]()**

