#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/7/11 下午2:54 
# @Author : Ethan
# @Site :  
# @File : 二分类多模型.py 
# @Software: PyCharm
import pandas as pd
import numpy as np
import warnings
import gc
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import  mean_squared_error
warnings.filterwarnings('ignore')
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)


def reduce_memory(df):
    """Reduce memory usage of a dataframe by setting data types. """
    start_mem = df.memory_usage().sum() / 1024 ** 2
    print('Initial df memory usage is {:.2f} MB for {} columns'
          .format(start_mem, len(df.columns)))

    for col in df.columns:
        col_type = df[col].dtypes
        if col_type=='<M8[ns]':
            continue
        if col_type != object:
            cmin = df[col].min()
            cmax = df[col].max()
            if str(col_type)[:3] == 'int':
                # Can use unsigned int here too
                if cmin > np.iinfo(np.int8).min and cmax < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif cmin > np.iinfo(np.int16).min and cmax < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif cmin > np.iinfo(np.int32).min and cmax < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif cmin > np.iinfo(np.int64).min and cmax < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if cmin > np.finfo(np.float16).min and cmax < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif cmin > np.finfo(np.float32).min and cmax < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024 ** 2
    memory_reduction = 100 * (start_mem - end_mem) / start_mem
    print('Final memory usage is: {:.2f} MB - decreased by {:.1f}%'.format(end_mem, memory_reduction))
    return df
#
train_date_feature = pd.read_csv('xyh/data/train_date_feature.csv')
test_date_feature = pd.read_csv('xyh/data/test_date_feature.csv')

#训练集特征
train_feature = pd.read_csv('xyh/data/train_feature.csv')

#测试集特征
test_feature = pd.read_csv('xyh/data/test_feature.csv')

#训练集 train
train = pd.read_csv('xyh/data/train.csv')
train_date_feature = reduce_memory(train_date_feature)
# test_date_feature = reduce_memory(test_date_feature)

train_feature = reduce_memory(train_feature)
# test_feature = reduce_memory(test_feature)
#
join_col = list(filter(lambda x: x not in ['rdate','due_date','date','minduedate','duedate_diff','loan_balance'],train_date_feature.columns))

###
train_date_feature.head()
train_date_feature['auditing_date'] = pd.to_datetime(train_date_feature['auditing_date'])
##将训练集分成４分　三个月为窗口,最后两个月来验证
range_time1=pd.date_range(start='2018-1-1',end='2018-3-31')
train_1 = train_date_feature[train_date_feature['auditing_date'].isin(range_time1)]
train_1 = train_1[join_col].merge(train_feature,on=['user_id','listing_id'],how='left')
train_1 = train_1.fillna(value=0)

range_time2 =pd.date_range(start='2018-4-1',end='2018-6-30')
train_2 = train_date_feature[train_date_feature['auditing_date'].isin(range_time2)]
train_2 = train_2[join_col].merge(train_feature,on=['user_id','listing_id'],how='left')
train_2 = train_2.fillna(value=0)
range_time3 =pd.date_range(start='2018-7-1',end='2018-10-31')
train_3 = train_date_feature[train_date_feature['auditing_date'].isin(range_time3)]
train_3 = train_3[join_col].merge(train_feature,on=['user_id','listing_id'],how='left')
train_3 = train_3.fillna(value=0)


range_time4 = pd.date_range(start='2018-11-1',end='2018-12-31')
valid_set = train_date_feature[train_date_feature['auditing_date'].isin(range_time4)]
valid_set = valid_set[join_col].merge(train_feature,on=['user_id','listing_id'],how='left')
valid_set = valid_set.fillna(value=0)
join_col.remove('label')
test_set = test_date_feature[join_col].merge(test_feature,on=['user_id','listing_id'],how='left')
test_set = test_set.fillna(value=0)


train['repay_amt'] = train['repay_amt'].map(lambda x : 0 if x=='\\N' else x)
due_and_reapy = train_date_feature[['user_id','listing_id','auditing_date','label']].merge(train[['user_id','listing_id','repay_amt','due_amt']],on=['user_id','listing_id'],how='left')
due_and_reapy['repay_amt'] =due_and_reapy['label']*due_and_reapy['repay_amt']
due_and_reapy['repay_amt'] = due_and_reapy['repay_amt'].map(lambda x: 0 if x=='' else x)

due_and_reapy['auditing_date'] = pd.to_datetime(due_and_reapy['auditing_date'])
del train_date_feature,train_feature,test_date_feature,test_feature
gc.collect()
train_1 = reduce_memory(train_1)
train_2 = reduce_memory(train_2)
train_3 = reduce_memory(train_3)
valid_set = reduce_memory(valid_set)
test_set = reduce_memory(test_set)
"""
## 　第一份训练集
"""
NUM_THREADS = 8
RANDOM_SEED = 737851
LIGHTGBM_PARAMS_1 = {
    'boosting_type': 'gbdt',
    'n_estimators': 3000,
    'learning_rate': 0.05134,
    'num_leaves': 54,
    'max_depth': 10,
    'subsample_for_bin': 240000,
    'reg_alpha': 0.436193,
    'reg_lambda': 0.479169,
    'colsample_bytree': 0.508716,
    'min_split_gain': 0.024766,
    'subsample': 1,
    'is_unbalance': False,
    'silent':-1,
    'verbose':-1
}

"""
## 第二份训练集
"""
LIGHTGBM_PARAMS_2 = {
    'boosting_type': 'gbdt',
    'n_estimators': 2000,
    'learning_rate': 0.07134,
    'num_leaves': 31,
    'max_depth': 5,
    'subsample_for_bin': 240000,
    'reg_alpha': 0.436193,
    'reg_lambda': 0.479169,
    'colsample_bytree': 0.508716,
    'min_split_gain': 0.024766,
    'subsample': 1,
    'is_unbalance': False,
    'silent':-1,
    'verbose':-1
}

"""
## 第三份训练集
"""
# XGBoost_parmas={
#     'learning_rate' =0.0612,
#      'n_estimators'=1000,
#      'max_depth'=3,
#      'min_child_weight'=1,
#     'subsample'=0.8,
#     'colsample_bytree'=0.8,
#    'objective'= 'binary:logistic',
#    'nthread'=8
# }

due_and_reapy.head()
def evaluate_lgb(df,test=None,valid=None,LIGHTGBM_PARAMS=None,flag=None):
    print("Train shape {}/ vaild shape {}".format(df.shape,valid.shape))
    del_features = ['label', 'user_id', 'listing_id', 'auditing_date']
    predictors = list(filter(lambda v: v not in del_features, df.columns))
    params = {'random_state': RANDOM_SEED, 'nthread': NUM_THREADS}
    clf = LGBMClassifier(**{**params, **LIGHTGBM_PARAMS})
    clf.fit(df[predictors],df['label'],eval_metric='auc')
    valid_result = clf.predict_proba(valid[predictors])[:,1]
    #应还款金额
    val_due_and_repay = due_and_reapy[due_and_reapy['auditing_date'].isin(valid['auditing_date'])]
    # 预测金额
    val_predict_amt = val_due_and_repay['due_amt']*valid_result
    print("vaild rmse %.6f" %(np.sqrt(mean_squared_error(val_due_and_repay['repay_amt'].values,val_predict_amt))))
    print('AUC : %.6f' %( roc_auc_score(valid['label'], valid_result)))
    importance = clf.booster_.feature_importance()
    feature_importance = pd.DataFrame({'feature':predictors,'importance':importance})
    valid['prediction'] = valid_result
    valid['predict_amt'] = val_predict_amt
    valid[['user_id','listing_id','label','prediction','predict_amt']].to_csv('xyh/data/valid_{}.csv'.format(flag),index=False)
    del valid['prediction'],valid['predict_amt']
    test_result = clf.predict_proba(test[predictors])[:,1]
    test['prediction']=test_result
    test[['user_id','listing_id','prediction']].to_csv('xyh/data/test_{}.csv'.format(flag),index=False)
    return importance


importance = evaluate_lgb(train_1[:100000],valid=valid_set[:100000],LIGHTGBM_PARAMS=LIGHTGBM_PARAMS_1,flag='2018-1-3')
importance.to_csv('xyh/data/featureimp.csv',index=False)

evaluate_lgb(train_2,test=test_set,valid=valid_set,LIGHTGBM_PARAMS=LIGHTGBM_PARAMS_2,flag='2018-4-6')
due_and_reapy.head()
tmp = due_and_reapy[due_and_reapy['auditing_date'].isin(valid_set['auditing_date'])]
tmp.head(100)
valid_set.head(100)
valid_set.to_csv('xyh/data/valid_set.csv',index=False)
tmp.to_csv('xyh/data/valid_set_due_amt.csv',index=False)