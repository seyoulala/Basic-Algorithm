#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/7/11 下午2:53 
# @Author : Ethan
# @Site :  
# @File : 多分类模型.py 
# @Software: PyCharm


import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from lightgbm.sklearn import LGBMClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, log_loss, accuracy_score

import time
import warnings
import gc
warnings.filterwarnings('ignore')
start_all = time.time()
print("开始读取数据....")

train_df = pd.read_csv('xyh/data/train.csv', parse_dates=['auditing_date', 'due_date', 'repay_date'])
train_df['repay_date'] = train_df[['due_date', 'repay_date']].apply(
    lambda x: x['repay_date'] if x['repay_date'] != '\\N' else x['due_date'], axis=1
)
train_df['repay_amt'] = train_df['repay_amt'].apply(lambda x: x if x != '\\N' else 0).astype('float32')
train_df['label'] = (train_df['due_date'] - train_df['repay_date']).dt.days
train_df.loc[train_df['repay_amt'] == 0, 'label'] = 32

train_df.sort_values(by="user_id", inplace=True)
train_df = train_df.reset_index()
train_df.drop("index", axis=1, inplace=True)



clf_labels = train_df['label'].values
amt_labels = train_df['repay_amt'].values
train_due_amt_df = train_df[['due_amt']]
train_num = train_df.shape[0]

test_df = pd.read_csv('xyh/data/test.csv', parse_dates=['auditing_date', 'due_date'])
test_df.sort_values(by="user_id", inplace=True)
test_df = test_df.reset_index()
test_df.drop("index", axis=1, inplace=True)


sub = test_df[['listing_id', 'due_date', 'due_amt']]

print("train shape", train_df.shape)
print("test shape", test_df.shape)

df = pd.read_csv("xyh/data/all_feats_74.csv")
cate_cols = ['gender', 'cell_province', 'id_province']
del df['user_id'], df['listing_id'], df['taglist']

gc.collect()
df["id_city"] = df.id_city.map(df.id_city.value_counts())
df = pd.get_dummies(df, columns=cate_cols)
# df = sparse.hstack((df.values, tag_cv), format='csr', dtype='float32')
# df = sparse.hstack((df, tag_idf), format='csr', dtype='float32')
train_values, test_values = df[:train_num].values, df[train_num:].values

print(train_values.shape)
print("开始训练数据")
# 五折验证也可以改成一次验证，按时间划分训练集和验证集，以避免由于时序引起的数据穿越问题。
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=2019)
clf = LGBMClassifier(
       learning_rate=0.05,
       n_estimators=10000,
       subsample=0.8,
       subsample_freq=1,
       colsample_bytree=0.8,
       random_state=2019
)
amt_oof = np.zeros(train_num)
prob_oof = np.zeros((train_num, 33))
test_pred_prob = np.zeros((test_values.shape[0], 33))
for i, (trn_idx, val_idx) in enumerate(skf.split(train_values, clf_labels)):
    print(i, 'fold...')
    t = time.time()

    trn_x, trn_y = train_values[trn_idx], clf_labels[trn_idx]
    val_x, val_y = train_values[val_idx], clf_labels[val_idx]
    val_repay_amt = amt_labels[val_idx]
    val_due_amt = train_due_amt_df.iloc[val_idx]

    clf.fit(
          trn_x, trn_y,
          eval_set=[(trn_x, trn_y), (val_x, val_y)],
          early_stopping_rounds=60, verbose=200
    )
   # shepe = (-1, 33)
    val_pred_prob_everyday = clf.predict_proba(val_x, num_iteration=clf.best_iteration_)
    prob_oof[val_idx] = val_pred_prob_everyday
    val_pred_prob_today = [val_pred_prob_everyday[i][val_y[i]] for i in range(val_pred_prob_everyday.shape[0])]
    val_pred_repay_amt = val_due_amt['due_amt'].values * val_pred_prob_today
    print('val rmse:', np.sqrt(mean_squared_error(val_repay_amt, val_pred_repay_amt)))
    print('val mae:', mean_absolute_error(val_repay_amt, val_pred_repay_amt))
    amt_oof[val_idx] = val_pred_repay_amt
    test_pred_prob += clf.predict_proba(test_values, num_iteration=clf.best_iteration_) / skf.n_splits

    print('runtime: {}\n'.format(time.time() - t))
    del trn_x, trn_y, val_x, val_y
    gc.collect()

print('\ncv rmse:', np.sqrt(mean_squared_error(amt_labels, amt_oof)))
print('cv mae:', mean_absolute_error(amt_labels, amt_oof))
print('cv logloss:', log_loss(clf_labels, prob_oof))
print('cv acc:', accuracy_score(clf_labels, np.argmax(prob_oof, axis=1)))

prob_cols = ['prob_{}'.format(i) for i in range(33)]
for i, f in enumerate(prob_cols):
       sub[f] = test_pred_prob[:, i]


sub_example = pd.read_csv('xyh/data/submission.csv', parse_dates=['repay_date'])


sub_example = sub_example.merge(sub, on='listing_id', how='left')
sub_example['days'] = (sub_example['due_date'] - sub_example['repay_date']).dt.days

# shape = (-1, 33)
test_prob = sub_example[prob_cols].values
test_labels = sub_example['days'].values
test_prob = [test_prob[i][test_labels[i]] for i in range(test_prob.shape[0])]

sub_example['repay_amt'] = sub_example['due_amt'] * test_prob
sub_example[['listing_id', 'repay_date', 'repay_amt']].to_csv('sub74.csv', index=False)
print('运行时间: {}hours\n'.format((time.time() - start_all) / 3600))
