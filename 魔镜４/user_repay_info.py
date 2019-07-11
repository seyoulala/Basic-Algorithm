#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-06-30 10:17:00
# @Author  : xuyinghao (xyh650209@163.com)
# @Version : $Id$

import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import gc
import time
import datetime
import scipy as sp
warnings.filterwarnings('ignore')


data_path = "./data"

train = pd.read_csv(os.path.join(data_path, 'train.csv'))
test = pd.read_csv(os.path.join(data_path, 'test.csv'))
user_repay_logs = pd.read_csv(os.path.join(data_path, 'user_repay_logs.csv'))


def gen_user_repay_feature(train_set, test_set, data):
    """
    还款表特征
    """
    train_set = train_set.replace(to_replace="\\N", value=np.NaN)
    train_set['due_date'] = pd.to_datetime(train_set['due_date'])
    train_set['repay_date'] = pd.to_datetime(train_set['repay_date'])
    train_set['auditing_date'] = pd.to_datetime(train_set['auditing_date'])
    test_set['due_date'] = pd.to_datetime(test_set['due_date'])
    test_set['auditing_date'] = pd.to_datetime(test_set['auditing_date'])

    data['due_date'] = pd.to_datetime(data['due_date'])
    data['repay_date'] = pd.to_datetime(data['repay_date'])

    # 成交日
    start_time = train_set['auditing_date'].min()
    end_time = train_set['auditing_date'].max()
    time_range = pd.date_range(start=start_time, end=end_time)

    # testset
    start_time_test = test_set['auditing_date'].min()
    end_time_test = test_set['auditing_date'].max()
    time_range_test = pd.date_range(start=start_time_test, end=end_time_test)

    # 对于user_repay_logs表
    train_feature_table = pd.DataFrame()
    for time in time_range:
        tmp_train = train_set.loc[train_set['auditing_date'] == time, [
            'user_id']]
        # 历史不逾期表
        not_due_df = user_repay_logs.loc[
            user_repay_logs['repay_date'] < time, :]
        not_due_df['time_diff'] = (
            not_due_df['due_date'] - not_due_df['repay_date']).dt.days
        not_due_df['repay_before'] = not_due_df['time_diff'].map(
            lambda x: 1 if x > 0 else 0)
        tmp_join = tmp_train.merge(not_due_df, on='user_id', how='left')
        feature_table = tmp_join.groupby('user_id').agg({'time_diff': ['min', 'mean', 'max', 'var'],
                                                         'repay_before': ['sum'],
                                                         'listing_id': ['nunique'],
                                                         'order_id': ['mean', 'min', 'max'],
                                                         'repay_amt': ['sum', 'mean']})

        feature_table.columns = pd.Index(
            ["{}_{}".format(e[0], e[1]) for e in feature_table.columns.tolist()])
        feature_table = feature_table.reset_index()
        feature_table = tmp_train[['user_id']].merge(
            feature_table, on='user_id', how='left')
        # 历史逾期特征
        his_due_df = user_repay_logs[(
            user_repay_logs['repay_date'] == '2200-01-01') & (user_repay_logs['due_date'] < time)]
        his_due_df['repay_after'] = 1
        tmp_join = tmp_train.merge(his_due_df, on='user_id', how='left')
        due_feature_table = tmp_join.groupby('user_id').agg({'repay_after': ['sum'],
                                                             'listing_id': ['nunique'],
                                                             'due_amt': ['mean', 'min', 'max']})
        due_feature_table.columns = pd.Index(
            ["{}_{}".format(e[0], e[1]) for e in due_feature_table.columns.tolist()])
        due_feature_table = due_feature_table.reset_index()
        due_feature_table = tmp_train[['user_id']].merge(
            due_feature_table, on='user_id', how='left')
        due_feature_table = due_feature_table.rename(
            columns={'listing_id_nunique': 'listing_id_duecount'})
        feature_table = pd.concat(
            [feature_table, due_feature_table.drop(columns='user_id')], axis=1)

        train_feature_table = pd.concat(
            [train_feature_table, feature_table], axis=0)

    test_feature_table = pd.DataFrame()
    for time in time_range_test:
        tmp_test = test_set.loc[test_set['auditing_date'] == time, ['user_id']]
        # 历史不逾期表
        not_due_df = user_repay_logs.loc[
            user_repay_logs['repay_date'] < time, :]
        not_due_df['time_diff'] = (
            not_due_df['due_date'] - not_due_df['repay_date']).dt.days
        not_due_df['repay_before'] = not_due_df['time_diff'].map(
            lambda x: 1 if x > 0 else 0)
        tmp_join = tmp_test.merge(not_due_df, on='user_id', how='left')
        feature_table = tmp_join.groupby('user_id').agg({'time_diff': ['min', 'mean', 'max', 'var'],
                                                         'repay_before': ['sum'],
                                                         'listing_id': ['nunique'],
                                                         'order_id': ['mean', 'min', 'max'],
                                                         'repay_amt': ['sum', 'mean']})

        feature_table.columns = pd.Index(
            ["{}_{}".format(e[0], e[1]) for e in feature_table.columns.tolist()])
        feature_table = feature_table.reset_index()
        feature_table = tmp_test[['user_id']].merge(
            feature_table, on='user_id', how='left')
        # 历史逾期特征
        his_due_df = user_repay_logs[(
            user_repay_logs['repay_date'] == '2200-01-01') & (user_repay_logs['due_date'] < time)]
        his_due_df['repay_after'] = 1
        tmp_join = tmp_test.merge(his_due_df, on='user_id', how='left')
        due_feature_table = tmp_join.groupby('user_id').agg({'repay_after': ['sum'],
                                                             'listing_id': ['nunique'],
                                                             'due_amt': ['mean', 'min', 'max']})
        due_feature_table.columns = pd.Index(
            ["{}_{}".format(e[0], e[1]) for e in due_feature_table.columns.tolist()])
        due_feature_table = due_feature_table.reset_index()
        due_feature_table = tmp_test[['user_id']].merge(
            due_feature_table, on='user_id', how='left')
        due_feature_table = due_feature_table.rename(
            columns={'listing_id_nunique': 'listing_id_duecount'})
        feature_table = pd.concat(
            [feature_table, due_feature_table.drop(columns='user_id')], axis=1)

        test_feature_table = pd.concat(
            [test_feature_table, feature_table], axis=0)

    return train_feature_table, test_feature_table
