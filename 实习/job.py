#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

import  pandas as pd
import  os
from  sqlalchemy import create_engine
from datetime import  datetime,timedelta
import time


def start_job(engine,table_name,dag_name):
    now_time = datetime.now().date()
    yesterday = now_time + timedelta(-1)
    while True:
        try:
            target_table = pd.read_sql_table(table_name=table_name, con=engine)
            job_status = target_table.loc[target_table['task_id']=='999999','task_status'].values[0]
            job_date = target_table.loc[target_table['task_id']=='999999','busidate'].values[0]
            job_date = pd.Timestamp(job_date).date()

        except :
            with open('job_failed','w',encoding='utf-8') as f:
                f.write('{0} \n Not found busidate or task_status'.format(now_time))
                f.close()
        else:
            if job_date == now_time and int(job_status) == 0:
                os.system("airflow unpause {0}".format(dag_name))
                os.system(" airflow trigger_dag {0}".format(dag_name))
                with open('success_flag','w',encoding='utf-8') as f:
                    f.write("{0} \n  作业已经开始运行")
                    f.close()
                break
        time.sleep(60)


if __name__ =="__main__":
   engine  = create_engine('mysql+pymysql://xuyinghao:Xuyinghao@2019@58.59.11.86/man')
   table_name = 'task_info'
   dag_name = ''
   start_job(engine,table_name,dag_name)


