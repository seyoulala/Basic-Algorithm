### 封装的参数搜索函数tur


#### 返回得分,参数,更新

```python


def objective(hyperparameters,iteration):
    if 'n_estimators' in hyperparameters.keys():
        del hyperparameters['n_estimators']
    
    cv_result = lgb.cv(hyperparameters,train_data,num_boost_round=10000,nfold=N_FOLDS,early_stopping_rounds=100,metrics='auc',seed=42)
    hyperparameters['n_estimators'] =len(cv_result['auc-mean'])
    model = lgb.LGBMClassifier()
    params = model.get_params()
    params.update(hyperparameters)
    score = cv_result['auc-mean'][-1]
    return [score,params,iteration]
```
####  网格搜索

```python
import itertools

def grid_search(param_grid, out_file):
    """Grid search algorithm (with limit on max evals)
       Writes result of search to csv file every search iteration."""
    
    # Dataframe to store results
    results = pd.DataFrame(columns = ['score', 'params', 'iteration'],
                              index = list(range(MAX_EVALS)))
    
    # https://codereview.stackexchange.com/questions/171173/list-all-possible-permutations-from-a-python-dictionary-of-lists
    keys, values = zip(*param_grid.items())
    
    i = 0
    
    # Iterate through every possible combination of hyperparameters
    for v in itertools.product(*values):
        # Select the hyperparameters
        parameters = dict(zip(keys, v))
        
        # Set the subsample ratio accounting for boosting type
        parameters['subsample'] = 1.0 if parameters['boosting_type'] == 'goss' else parameters['subsample']
        
        # Evalute the hyperparameters
        eval_results = objective(parameters, i)
        
        results.loc[i, :] = eval_results
        
        i += 1
        
        # open connection (append option) and write results
        of_connection = open(out_file, 'a')
        writer = csv.writer(of_connection)
        writer.writerow(eval_results)
        
        # make sure to close connection
        of_connection.close()
        
    # Sort with best score on top
    results.sort_values('score', ascending = False, inplace = True)
    results.reset_index(inplace = True)
    
    return results 

```

#### random search 

```python

def random_search(param_grid, out_file, max_evals = MAX_EVALS):
    """Random search for hyperparameter optimization. 
       Writes result of search to csv file every search iteration."""
    
    
    # Dataframe for results
    results = pd.DataFrame(columns = ['score', 'params', 'iteration'],
                                  index = list(range(MAX_EVALS)))
    for i in range(MAX_EVALS):
        
        # Choose random hyperparameters
        random_params = {k: random.sample(v, 1)[0] for k, v in param_grid.items()}
        random_params['subsample'] = 1.0 if random_params['boosting_type'] == 'goss' else random_params['subsample']

        # Evaluate randomly selected hyperparameters
        eval_results = objective(random_params, i)
        results.loc[i, :] = eval_results

        # open connection (append option) and write results
        of_connection = open(out_file, 'a')
        writer = csv.writer(of_connection)
        writer.writerow(eval_results)
        
        # make sure to close connection
        of_connection.close()
        
    # Sort with best score on top
    results.sort_values('score', ascending = False, inplace = True)
    results.reset_index(inplace = True)

    return results
```

####  使用最佳超参数在test data 测试

```python
def evaluate(results, name):
    """Evaluate model on test data using hyperparameters in results
       Return dataframe of hyperparameters"""
        
    # Sort with best values on top
    results = results.sort_values('score', ascending = False).reset_index(drop = True)
    
    # Print out cross validation high score
    print('The highest cross validation score from {} was {:.5f} found on iteration {}.'.format(name, results.loc[0, 'score'], results.loc[0, 'iteration']))
    
    # Use best hyperparameters to create a model
	hyperparameters = dict(**random_results.loc[0, 'hyperparameters'])
	del hyperparameters['n_estimators']
	

# Cross validation with n_folds and early stopping
	cv_results = lgb.cv(hyperparameters, train_set,
                    num_boost_round = 10000, early_stopping_rounds = 100, 
                    metrics = 'auc', nfold = N_FOLDS)
    
	model = lgb.LGBMClassifier(n_estimators = len(cv_results['auc-mean']), **hyperparameters)
    # Train and make predictions
    model.fit(train_features, train_labels)
    preds = model.predict_proba(test_features)[:, 1]
    
    print('ROC AUC from {} on test data = {:.5f}.'.format(name, roc_auc_score(test_labels, preds)))
    
    # Create dataframe of hyperparameters
    hyp_df = pd.DataFrame(columns = list(results.loc[0, 'hyperparameters'].keys()))

    # Iterate through each set of hyperparameters that were evaluated
    for i, hyp in enumerate(results['hyperparameters']):
        hyp_df = hyp_df.append(pd.DataFrame(hyp, index = [0]), 
                               ignore_index = True)
        
    # Put the iteration and score in the hyperparameter dataframe
    hyp_df['iteration'] = results['iteration']
    hyp_df['score'] = results['score']
    
    return hyp_df
```

## lightgbm 的focal loss

$$
FL = -\alpha(1-p)^{\gamma}ylg(p) -\alpha{p}^{\gamma}(1-y)lg(1-p)
$$

第一个权重不必多说，就是方法一中的根据正负样本量自定义的损失权重，重点看第二个权重。

若是对于某个1样本来说，模型预测其为1样本的概率是0.9，那么第二个权重为：（1-0.9）^ 2 = 0.01,而如果模型预测某个样本为1样本的概率是0.6，那么第二个权重变为：（1-0.6）^2 = 0.16。样本预测越不准确，损失值所占的权重就会更大。

原论文中有一张图形象地说明了，横坐标代表预测对的概率，纵坐标代表损失值，中间红色虚线代表预测对的概率是0.5，虚线左半边代表模型预测偏差很大，右半边代表模型预测偏差较小。 ![[公式]](https://www.zhihu.com/equation?tex=%5Cgamma+%3D+0) 时，就是第二个权重项不参与情况下的损失值：

![img](https://pic1.zhimg.com/80/v2-97756ea1b1f9e2a63cb2ce0889a900cc_1440w.jpg)



可以看到，相对于图中蓝色曲线来说，随着gamma增大，在红线的左半边，几条曲线损失值差别不大，但是红线的右半边，损失值迅速趋近于0。

而且更巧妙的是，一般来说，如果0样本远比1样本多的话，模型肯定会倾向于将样本预测为0这一类（即使全部样本都判为0类，模型准确率依旧很高），上边的第二个权重也会促使模型花更多精力去关注数量较少的1样本。

~~~python

import numpy as np
import lightgbm as lgb
import pickle

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from scipy.misc import derivative
from hyperopt import hp, tpe, fmin, Trials

def sigmoid(x): return 1./(1. +  np.exp(-x))

#首先定义lossfucn，该函数要返回一阶梯度和二阶梯度
def focal_loss_lgb(y_pred, dtrain, alpha, gamma):
    """
    Focal Loss for lightgbm

    Parameters:
    -----------
    y_pred: numpy.ndarray
        array with the predictions
    dtrain: lightgbm.Dataset
    alpha, gamma: float
        See original paper https://arxiv.org/pdf/1708.02002.pdf
    """
    a,g = alpha, gamma
    y_true = dtrain.label
    def fl(x,t):
        p = 1/(1+np.exp(-x))
        return -( a*t + (1-a)*(1-t) ) * (( 1 - ( t*p + (1-t)*(1-p)) )**g) * ( t*np.log(p)+(1-t)*np.log(1-p) )
    partial_fl = lambda x: fl(x, y_true)
    grad = derivative(partial_fl, y_pred, n=1, dx=1e-6)
    hess = derivative(partial_fl, y_pred, n=2, dx=1e-6)
    return grad, hess
#自定义lossfunction后需要定义评估函数  
def lgb_focal_f1_score(preds, lgbDataset):
    """
    When using custom losses the row prediction needs to passed through a
    sigmoid to represent a probability

    Parameters:
    -----------
    preds: numpy.ndarray
        array with the predictions
    lgbDataset: lightgbm.Dataset
    """
    preds = sigmoid(preds)
    binary_preds = [int(p>0.5) for p in preds]
    y_true = lgbDataset.get_label()
    return 'f1', f1_score(y_true, binary_preds), True
  
  
def objective(params):
    """
    objective function for lightgbm.
    """
    # hyperopt casts as float
    params['num_boost_round'] = int(params['num_boost_round'])
    params['num_leaves'] = int(params['num_leaves'])

    # need to be passed as parameter
    params['verbose'] = -1
    params['seed'] = 1

    focal_loss = lambda x,y: focal_loss_lgb(x, y,
        params['alpha'], params['gamma'])
    # if you do not want an annoying warning related to the unrecognised param
    # 'alpha', simple pop them out from the dict params here and insert them
    # back before return. For this particular notebook I can live  with it, so
    # I will leave it
    cv_result = lgb.cv(
        params,
        train,
        num_boost_round=params['num_boost_round'],
        fobj = focal_loss,
        feval = lgb_focal_f1_score,
        nfold=3,
        stratified=True,
        early_stopping_rounds=20)
    # I save the length or the results (i.e. the number of estimators) because
    # it might have stopped earlier and is always useful to have that
    # information 
    early_stop_dict[objective.i] = len(cv_result['f1-mean'])
    score = round(cv_result['f1-mean'][-1], 4)
    objective.i+=1
    return -score
#定义参数空间 
space = {
    'learning_rate': hp.uniform('learning_rate', 0.01, 0.2),
    'num_boost_round': hp.quniform('num_boost_round', 50, 500, 20),
    'num_leaves': hp.quniform('num_leaves', 31, 255, 4),
    'min_child_weight': hp.uniform('min_child_weight', 0.1, 10),
    'colsample_bytree': hp.uniform('colsample_bytree', 0.5, 1.),
    'subsample': hp.uniform('subsample', 0.5, 1.),
    'reg_alpha': hp.uniform('reg_alpha', 0.01, 0.1),
    'reg_lambda': hp.uniform('reg_lambda', 0.01, 0.1),
    'alpha': hp.uniform('alpha', 0.1, 0.75),
    'gamma': hp.uniform('gamma', 0.5, 5)
    }
  
 ##训练数据 
 X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.25,
    random_state=1, stratify=y)
  
#构建数据集
train = lgb.Dataset(
    X_tr, y_tr,
    feature_name=colnames,
    categorical_feature = categorical_columns,
    free_raw_data=False)

objective.i=0
trials = Trials()
early_stop_dict = {}
best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=5,
            trials=trials)

best['num_boost_round'] = early_stop_dict[trials.best_trial['tid']]
best['num_leaves'] = int(best['num_leaves'])
best['verbose'] = -1
focal_loss = lambda x,y: focal_loss_lgb(x, y, best['alpha'], best['gamma'])
model = lgb.train(best, train, fobj=focal_loss)
preds = model.predict(X_val)
preds = sigmoid(preds)
preds = (preds > 0.5).astype('int')
~~~



