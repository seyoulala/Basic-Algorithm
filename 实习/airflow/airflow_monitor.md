## 监控Airflow DAG中任务完成情况

### 1. 背景

罗哥想要知道在跑批开始之后的某个时间点,DAG中任务的完成情况来判断跑批是否延迟.

### 2. 方案

通过观察,DAG一旦触发,airflow数据库中task_instance表会生成DAG中所有的task_instance.通过观察表数据,发现DAG中所有task的execute_time都会同时生成,且时间为任务触发的时间. 如下图所示:

<img src='/home/xyh/Pictures/task_instance.png'>

**同时发现 state列为task_instance此时的状态.(实时更新).DAG刚触发时,优先级高的task的state为running.其它等待的task,state为None.一旦某个task完成了,假如执行成功.state会从running更新为success,未执行的开始执行,state从None更新为running.**

**所以为了监控某个DAG在启动之后的运行情况(在某个时刻DAG中task的完成情况)**可以通过读取task_instance表内容.根据execute_time.来找到某个时刻的DAG.然后统计这个DAG中state列的success的数量(success/total)就可以知道某时刻DAG中task的完成情况.然后通过airflow的emailOperate模块来将DAG中任务完成情况通过邮件方式发送给需要被通知的人.

代码如下:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

import pandas as pd
from datetime import datetime,timedelta
from sqlalchemy import create_engine
from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date':days_ago(1)
}
dag = DAG(
    'SendEmail',
    default_args=default_args,
    description='my DAG',
    schedule_interval='05 07 * * *'
)

engine  = create_engine('mysql+pymysql://etl:1qaz@WSX@192.168.20.249/airflow')

instance_list = pd.read_sql_table(table_name='task_instance',con=engine)

now_time = datetime.now()

yesterday = now_time+ timedelta(days=-1)

execute_date = "{} 02:11:00".format(yesterday.date())

df = instance_list.loc[instance_list['execution_date']==execute_date,:]

success_number = len(df.loc[df['state']=='success','state'])

total_number = df.shape[0]

no_runing = total_number - success_number

success_rate = (success_number/(total_number))*100

dag_id = df['dag_id'].values[0]

content = "现在DAG中有{0}个任务 现在完成了{1}个,未完成{2}个,完成率{3}%".format(total_number,success_number,no_runing,success_rate)

send_to_email = ['xyh650209@163.com']

email_tail= "{} 任务完成情况".format(dag_id)

task = EmailOperator(task_id='job',to=send_to_email,html_content=content,subject=email_tail,dag=dag,mime_charset='utf-8')


```

**因为任务都是每天定时执行,所以也可以将这个监控监本也设置为一个DAG,每天定时执行.就可以起到每天定时监控的效果**,

[Airflow地址](http://192.192.0.27:8080/admin/)