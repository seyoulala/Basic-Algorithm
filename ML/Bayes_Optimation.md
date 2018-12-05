## Bayesian Hyperparameter Optimization


与随机或网格搜索相比，贝叶斯方法跟踪过去的评估结果，用于形成概率模型，将超参数映射到目标函数的得分概率

$$
p(score|hyperparameters)
$$

在文献中，该模型被称为目标函数的“代理”，并表示为p（y | x）。代理比目标函数更容易优化，贝叶斯方法通过选择在代理函数上表现最佳的超参数作为下一个超参数集合来评估实际的目标函数.

换句话说,就是一下步骤:

- 建立一个目标函数的代理概率模型

- 找到在代理概率模型上表现最佳的一组超参

- 用这组超参来评估实际的目标函数

- 更新包含新结果的代理概率模型

- 重复步骤2-4，直到达到最大迭代次数或时间

所以贝叶斯优化的目的是通过不断的更新代理概率模型使得目标函数的score更高

基于贝叶斯的优化的概念是通过仅选择最有希望的超参数集来作用在代理概率模型上来减少目标函数的调用.

代理概率模型有不同形式,包括高斯过程,和随机森林回归已经TPE(基于树模型的概率密度函数估计器),其中hyperopt就是基于TPE形式的.

实际上,在贝叶斯优化中,目标函数是使用了一组超参数的模型的验证集上的错误率,目的是希望找到在验证集上错误率最低且能在测试集上有很好泛化性能的hyperparameters.,在目标函数上进行超参数的评估是十分耗时间的,因为每一组参数都要train一次data.然后在validation data 上进行验证.所以通过贝叶斯优化,我们不仅可以搜索参数空间,同时限制对不好的超参数的评估,也就是对那些对概率模型得分没有提升的超参是不会评估的.贝叶斯通过前几次的评估结果来不断的更新概率模型已找到最佳的超参.


**贝叶斯优化包括以下四个组成**:

- 目标函数:我们需要最小化的东西,一般是使用了一组超参的model在validation data 上的错误率.

- domain space : 参数的搜索域

- Optimization Algorithm :建立代理模型的方式以及如何选取下一组超参进行评估

- Result Histtory: 保存validation error 以及对应的Hyperparameters.


#### 1. objective function

```python
import lightgbm as lgb
from hyperopt import STATUS_OK

N_FOLDS = 10

# Create the dataset
train_set = lgb.Dataset(train_features, train_labels)

import csv
from hyperopt import STATUS_OK
from timeit import default_timer as timer

def objective(params, n_folds = N_FOLDS):
    """Objective function for Gradient Boosting Machine Hyperparameter Optimization"""
    
    # Keep track of evals
    global ITERATION
    
    ITERATION += 1
    
    # Retrieve the subsample if present otherwise set to 1.0
    subsample = params['boosting_type'].get('subsample', 1.0)
    
    # Extract the boosting type
    params['boosting_type'] = params['boosting_type']['boosting_type']
    params['subsample'] = subsample
    
    # Make sure parameters that need to be integers are integers
    for parameter_name in ['num_leaves', 'subsample_for_bin', 'min_child_samples']:
        params[parameter_name] = int(params[parameter_name])
    
    start = timer()
    
    # Perform n_folds cross validation
    cv_results = lgb.cv(params, train_set, num_boost_round = 10000, nfold = n_folds, 
                        early_stopping_rounds = 100, metrics = 'auc', seed = 50)
    
    run_time = timer() - start
    
    # Extract the best score
    best_score = np.max(cv_results['auc-mean'])
    
    # Loss must be minimized
    loss = 1 - best_score
    
    # Boosting rounds that returned the highest cv score
    n_estimators = int(np.argmax(cv_results['auc-mean']) + 1)

    # Write to the csv file ('a' means append)
	out_file ='some_path'
    of_connection = open(out_file, 'a')
    writer = csv.writer(of_connection)
    writer.writerow([loss, params, ITERATION, n_estimators, run_time])
    
    # Dictionary with information for evaluation
    return {'loss': loss, 'params': params, 'iteration': ITERATION,
            'estimators': n_estimators, 
            'train_time': run_time, 'status': STATUS_OK}
```

#### 2. Domain Space

在random search 或者grid search 搜索中,搜索域是一个网格形式,参数是一个个离散的数值,在贝叶斯优化总也是类似,但是每个hyperparameter都是一个概率分布,而不是离散的数值.指定搜索域是一个困难的事情,我们可以放宽搜索域,让贝叶斯去找.

定义搜索域
```python
# Define the search space
space = {
    'class_weight': hp.choice('class_weight', [None, 'balanced']),
    'boosting_type': hp.choice('boosting_type', 
                               [{'boosting_type': 'gbdt', 
                                    'subsample': hp.uniform('gdbt_subsample', 0.5, 1)}, 
                                 {'boosting_type': 'dart', 
                                     'subsample': hp.uniform('dart_subsample', 0.5, 1)},
                                 {'boosting_type': 'goss'}]),
    'num_leaves': hp.quniform('num_leaves', 30, 150, 1),
    'learning_rate': hp.loguniform('learning_rate', np.log(0.01), np.log(0.2)),
    'subsample_for_bin': hp.quniform('subsample_for_bin', 20000, 300000, 20000),
    'min_child_samples': hp.quniform('min_child_samples', 20, 500, 5),
    'reg_alpha': hp.uniform('reg_alpha', 0.0, 1.0),
    'reg_lambda': hp.uniform('reg_lambda', 0.0, 1.0),
    'colsample_bytree': hp.uniform('colsample_by_tree', 0.6, 1.0)
}


```
这里解释一下分布的类型

- `choice`: categorical variables
 
- `quniform`:discrete uniform(整数间隔)

- `uniform`:continues uniform(浮点数间隔)

- `loguniform`:continuous log uniform(在对数刻度上均匀间隔的浮点数,分布在不同的数量级中)

**注意到,space中有条件嵌套的参数,对于这种完全相互独立的参数,使用条件嵌套可以使得我们使用不同的超参数集合,但是GBM无法处理这种嵌套的字典,所以要处理一下**

```python

example= sample(space)
subsample = example['boosting_type'].get('boosting_type',1)

example['boosting_type']=example['boosting_type']['boosting_type']

example['subsample']=subsample

```

#### 3. Optimization Algorithm

```python
from hyperopt import tpe

tpe_algorithm = tpe.suggest

```
####  4. History Result


```python
from hyperopt import Trials
bayes_trials = Trials()
```
#### 5. 有了以上四部分之后就可以开始优化

```python
from hyperopt import fmin

MAX_EVALS = 500

# Optimize
best = fmin(fn = objective, space = space, algo = tpe.suggest, 
            max_evals = MAX_EVALS, trials = bayes_trials)

```
`Trials有个result属性,保存了objective function的所有信息`