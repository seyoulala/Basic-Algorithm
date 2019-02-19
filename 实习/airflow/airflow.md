## Airflow 简介

###  Airfolw是什么

Airflow 是 Airbnb 开发的用于工作流管理的开源项目，自带 web UI 和调度。现在 Apache 下做孵化，地址是[链接地址](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fapache%2Fincubator-airflow)

![](https://user-gold-cdn.xitu.io/2017/11/15/15fc00779e69d0fc?imageslim)

### Airfolw解决什么问题

简单的来说就是管理和调度各种离线定时 Job ，解决任务之间复杂的依赖关系.代替crontab.

当 cron job 规模达到数百上千时，其对人的要求将会非常高的，如果你的团队经历过这样的事情，应该能体会其中痛苦，所以使用类似 airflow 这样的工具代替 cron 来做定时任务将会极大提高工作效率。

### 使用之前的准备

Airflow 在 pip 上已经更名为 `apache-airflow`，下载最新版请使用后者 `pip install apache-airflow`。
Airflow 1.8 版本依赖的是 MySQL 5.6 以上，5.7 以下报 `1071, u'Specified key was too long; max key length is 767 bytes`，如果你使用 MySQL 作为你的 airflow backend 请升级你的 MySQL 到最新版。

MySQL 5.6 升级到 5.7 在使用 airflow 时会报 1146, `u"Table 'performance_schema.session_variables' doesn't exist"`，执行 `mysql_upgrade -u root -p --force` 解决。

Airflow 的 mysql driver 使用的是 `mysqlclient mysql://root:@127.0.0.1/sqlalchemy_lab?charset=utf8`，如果使用其他 driver 将报 `syntax error`。

### 基础概念

Airflow 中最基本的两个概念是：DAG 和 task。DAG 的全称是 Directed Acyclic Graph 是所有你想执行的任务的集合，在这个集合中你定义了他们的依赖关系，一个 DAG 是指一个 DAG object，一个 DAG object 可以在 Python 脚本中配置完成。
比如一个简单的的 DAG 包含三个 task：A、B、C，A 执行成功之后 B 才能执行，C 不依赖 A 和 B 即可执行。在这个简单的 DAG 中 A B C 可以是任何你想要执行的任务。
DAG 的定义使用 Python 完成的，其实就是一个 Python 文件，存放在 DAG 目录，Airflow 会动态的从这个目录构建 DAG object，每个 DAG object 代表了一个 workflow，每个 workflow 都可以包含任意个 task

###  安装教程

链接如下 [安装教程](http://gitlab.51xf.cn/data/data-team-doc/tree/master/airflow)

###  第一个DAG

DAG的配置使用Python

```python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('tutorial', default_args=default_args, schedule_interval=timedelta(1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag)

t2.set_upstream(t1) # t2 依赖 t1
t3.set_upstream(t1

```
**DAG 脚本的目的只是定义 DAG 的配置，并不包含任何的数据处理，在这里 operator 就是 task**

###DAG的实例化

一个 DAG 脚本是由 DAG object 的实例化和对应的 operator 组成的，除此之外我们还可以定义默认的参数提供给每个任务。

DAG 对象实例化可以根据我们的需要提供对应的初始化参数，实例化 DAG 对象需要提供唯一的 dag_id：

```python
dag = DAG(
    'tutorial', default_args=default_args, schedule_interval=timedelta(1))

```

### Task 的实例化

```python
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

```

**task 对象的定义的就是 operator 的实例化，operator 有 task_id，用来区分任务，可以按照需要定制 bash_command，也可以传递参数等。**

### Task 的依赖

Task 之间是能相互建立依赖的，形如：

```python
t2.set_upstream(t1)

# This means that t2 will depend on t1
# running successfully to run
# It is equivalent to
# t1.set_downstream(t2)

t3.set_upstream(t1)

# all of this is equivalent to
# dag.set_dependency('print_date', 'sleep')
# dag.set_dependency('print_date', 'templated')

```
### 执行和测试

和 airflow.cfg 同级目录下建立 dag 目录，用来存放第一个 DAG 脚本，然后执行 `python tutorial.py` ，如果没有报错说明 tutorial 建立成功了。


### 执行任务和并记录状态

执行任务在 Airflow 中称之为 backfill，以 backfill 执行会真正开始追踪任务的执行状态和依赖，并且会记录日志

```bash
# optional, start a web server in debug mode in the background
# airflow webserver --debug &

# start your backfill on a date range
airflow backfill tutorial -s 2015-06-01 -e 2015-06-0

```

[测试demo](https://github.com/zhyq0826/airflow-tutorial)
