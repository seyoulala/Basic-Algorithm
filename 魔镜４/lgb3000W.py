#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/7/9  
# @Author : Ethan
# @Site :  
# @File : lgb3000W.py 
# @Software: PyCharm

import pandas as pd 
import numpy as np 
import warnings
import os 
import sys
import gc
import time
import datetime
import scipy as sp
import lightgbm as lgb
from dateutil.relativedelta import  relativedelta
from collections import  Counter
from lightgbm import LGBMClassifier
from sklearn.model_selection import KFold, StratifiedKFold
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
NUM_THREADS = 8
DATA_DIRECTORY = "../input/"
SUBMISSION_SUFIX = "_model_７_9_3000W"



# 模型参数以及超参
GENERATE_SUBMISSION_FILES = True
STRATIFIED_KFOLD = True
RANDOM_SEED = 737851
NUM_FOLDS = 5
EARLY_STOPPING = 100

LIGHTGBM_PARAMS = {
    'boosting_type': 'gbdt',
    'n_estimators': 10000,
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

def kfold_lightgbm_sklearn(df, test, categorical_feature=None):
    print("Train shape: {}, test shape: {}".format(df.shape, test.shape))
    del_features = ['label', 'user_id', 'listing_id', 'auditing_date']
    predictors = list(filter(lambda v: v not in del_features, df.columns))

    if not STRATIFIED_KFOLD:
        folds = KFold(n_splits=NUM_FOLDS, shuffle=False,
                      random_state=RANDOM_SEED)
    else:
        folds = StratifiedKFold(
            n_splits=NUM_FOLDS, shuffle=False, random_state=RANDOM_SEED)

    oof_preds = np.zeros(df.shape[0])
    sub_preds = np.zeros(test.shape[0])
    importance_df = pd.DataFrame()

    for n_fold, (train_idx, valid_idx) in enumerate(folds.split(df[predictors], df['label'])):
        train_x, train_y = df[predictors].iloc[
            train_idx], df['label'].iloc[train_idx]
        valid_x, valid_y = df[predictors].iloc[
            valid_idx], df['label'].iloc[valid_idx]

        print("Fold {} begin train".format(n_fold + 1))
        #验证集还款
        val_repay_due_amt = due_and_reapy.iloc[valid_idx]
        
        params = {'random_state': RANDOM_SEED, 'nthread': NUM_THREADS}
        clf = LGBMClassifier(**{**params, **LIGHTGBM_PARAMS})
#         clf = LGBMClassifier(n_estimators=10000)
        if not categorical_feature:
            clf.fit(train_x, train_y, eval_set=[(train_x, train_y), (valid_x, valid_y)],
                    eval_metric='auc', verbose=200, early_stopping_rounds=EARLY_STOPPING)
        else:
            clf.fit(train_x, train_y, eval_set=[(train_x, train_y), (valid_x, valid_y)],
                    eval_metric='auc', verbose=200, early_stopping_rounds=EARLY_STOPPING,
                    feature_name=list(df[predictors].columns), categorical_feature=categorical_feature)

        vaild_pro = clf.predict_proba(
            valid_x, num_iteration=clf.best_iteration_)[:, 1]
        oof_preds[valid_idx] = vaild_pro

        sub_preds += clf.predict_proba(
            test[predictors], num_iteration=clf.best_iteration_)[:, 1] / folds.n_splits

        # 验证集预测还款金额
     
        val_pred_repay_amt = val_repay_due_amt['due_amt'].values * vaild_pro
        
        due_and_reapy.loc[valid_idx,'valid_predict'] = val_pred_repay_amt
        due_and_reapy.loc[valid_idx,'valid_pro'] = vaild_pro
        
        print('Fold %2d Val rmse: %.6f' % (n_fold + 1, np.sqrt(mean_squared_error(
            val_repay_due_amt['repay_amt'].values, val_pred_repay_amt))))
        print('\n')

        importance = clf.booster_.feature_importance()
        fold_importance = pd.DataFrame(
            {'feature': predictors, 'importance': importance})
        importance_df = pd.concat([importance_df, fold_importance], axis=0)

#         print('Fold %2d AUC : %.6f' % (n_fold + 1, roc_auc_score(valid_y, oof_preds[valid_idx])))
        print('Fold %2d AUC : %.6f' %(n_fold + 1, roc_auc_score(valid_y, vaild_pro)))

        del clf, train_x, train_y, valid_x, valid_y,val_repay_due_amt,val_pred_repay_amt
        gc.collect()
        
    due_and_reapy.to_csv('due_and_repay.csv',index=False)
    del due_and_reapy
    gc.collect()
    
    print('Full AUC score %.6f' % roc_auc_score(df['label'], oof_preds))
    print('Full RMSE score %.6f' %(np.sqrt(mean_squared_error(due_and_reapy['repay_amt'],due_and_reapy['valid_predict']))))
    test['prediction'] = sub_preds.copy()
    mean_importance = importance_df.groupby('feature').mean().reset_index()
    mean_importance.sort_values(by='importance', ascending=False, inplace=True)

    if GENERATE_SUBMISSION_FILES:
        
        oof = pd.DataFrame()
        oof['user_id'] = df['user_id'].copy()
        oof['listing_id']=df['listing_id'].copy()
        oof['predictions'] = oof_preds.copy()
        oof['label'] = df['label'].copy()
        oof.to_csv('oof{}.csv'.format(SUBMISSION_SUFIX), index=False)
        test[['user_id','listing_id', 'prediction']].to_csv('submission_3000W_{}'.format(SUBMISSION_SUFIX), index=False)
        mean_importance.to_csv('featureimp.csv',index=False)
    return mean_importance

if __name__ =="__main__":

    data_path ='/opt/notebook_data/1/xyh/data'
        #
    train_date_feature = pd.read_csv(os.path.join(data_path,'train_date_feature.csv'))
    test_date_feature = pd.read_csv(os.path.join(data_path,'test_date_feature.csv'))

    #训练集特征
    train_feature = pd.read_csv(os.path.join(data_path,'train_feature.csv'))

    #测试集特征
    test_feature = pd.read_csv(os.path.join(data_path,'test_feature.csv'))

    #训练集 train 
    train = pd.read_csv(os.path.join(data_path,'train.csv'))
    train_date_feature = reduce_memory(train_date_feature)
    test_date_feature = reduce_memory(test_date_feature)

    train_feature = reduce_memory(train_feature)
    test_feature = reduce_memory(test_feature)
    #
    join_col = list(filter(lambda x: x not in ['rdate','due_date','date','label','minduedate','duedate_diff','loan_balance'],train_date_feature.columns))

    train_set = train_date_feature[join_col].merge(train_feature,on=['user_id','listing_id'],how='left')
    test_set = test_date_feature[join_col].merge(test_feature,on=['user_id','listing_id'],how='left')
    # train_set = reduce_memory(train_set)
    # test_set = reduce_memory(test_set)
    train['repay_amt'] = train['repay_amt'].map(lambda x : 0 if x=='\\N' else x)
    ##label
    train_set['label'] = train_date_feature['label']
    due_and_reapy = train_set[['user_id','listing_id','label']].merge(train[['user_id','listing_id','repay_amt','due_amt']],on=['user_id','listing_id'],how='left')
    due_and_reapy['repay_amt'] =due_and_reapy['label']*due_and_reapy['repay_amt']
    due_and_reapy['repay_amt'] = due_and_reapy['repay_amt'].map(lambda x: 0 if x=='' else x)
    train_set['auditing_date']=pd.to_datetime(train_set['auditing_date'])
    train_set = train_set.fillna(value=0)
    test_set = test_set.fillna(value=0)
    del train_date_feature,train_feature,test_date_feature,test_feature
    gc.collect()

    kfold_lightgbm_sklearn(train_set,test_set) 
