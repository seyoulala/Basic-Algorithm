# Airflow

Airflow 是 Airbnb 开发的用于工作流管理的开源项目，自带 web UI 和调度。现在 Apache 下做孵化。

[官方网址 https://airflow.apache.org/](https://airflow.apache.org)

## 1. Install

```bash
export AIRFLOW_GPL_UNIDECODE=yes
```

```
(vpy2)
# ~ [15:48:17]
➜ pip install apache-airflow[all]
```

pip install apache-airflow[all] 如果有问题，你就装一个 pip install apache-airflow， 去掉all

```bash
# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
export AIRFLOW_HOME=~/airflow
```

##  2. Initiating Airflow Database

Airflow requires a database to be initiated before you can run tasks. 

```
airflow initdb
```

如果出现问题 ： ImportError: No module named 'pysqlite2'

```bash
yum install libsqlite3x.x86_64
yum install libsqlite3x-devel.x86_64
```

```
pip install pysqlite
```

找不到 cryptography.fernet

```bash
yum install python2-cryptography.x86_64
```

```bash
pip install cryptography
```

如果出现问题 ：airflow.exceptions.AirflowException: Could not create Fernet object: Incorrect paddin

```
(vpy2) [airflow@cdhagent2 ~]$ python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
B9iPmaDz074NcLW0NvcR6RXqC4c2Svk7azbjbaHS_6E=
```

修改 airflow/airflow.cfg

```
fernet_key = your_keycode
```

如果不出现问题，则不用配合 fernet_key， 默认就会出现。 apache-airflow 1.10.0 版本

### airflow initdb 操作演示

**airflow initdb** 之后产生 airflow 目录，操作演示如下：

```
(vpy2) [airflow@cdhagent2 ~]$ ll
total 0
(vpy2) [airflow@cdhagent2 ~]$ pip list | grep air
apache-airflow       1.10.0
(vpy2) [airflow@cdhagent2 ~]$ airflow initdb
(vpy2) [airflow@cdhagent2 ~]$ ll
total 0
drwxrwxr-x. 3 airflow airflow 76 Nov  8 14:30 airflow
(vpy2) [airflow@cdhagent2 ~]$ ll airflow/
total 96
-rw-rw-r--. 1 airflow airflow 20610 Nov  8 14:30 airflow.cfg
-rw-r--r--. 1 airflow airflow 68608 Nov  8 14:30 airflow.db
drwxrwxr-x. 3 airflow airflow    23 Nov  8 14:30 logs
-rw-rw-r--. 1 airflow airflow  2329 Nov  8 14:30 unittests.cfg
(vpy2) [airflow@cdhagent2 ~]$
```

## 3. 启动 webserver

airflow webserver -p 8080

```bash
(vpy2) [airflow@cdhagent2 ~]$ airflow webserver -p 8080
[2018-11-08 13:56:02,190] {__init__.py:57} INFO - Using executor SequentialExecutor
  ____________       _____________
 ____    |__( )_________  __/__  /________      __
____  /| |_  /__  ___/_  /_ __  /_  __ \_ | /| / /
___  ___ |  / _  /   _  __/ _  / / /_/ /_ |/ |/ /
 _/_/  |_/_/  /_/    /_/    /_/  \____/____/|__/
```

http://192.192.0.27:8080/admin/


![airflow DAG](https://upload-images.jianshu.io/upload_images/9094111-c4d1bb23df2557e3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

## 其他：使用 Mysql 配置 db (还未完全操作成功)

进入 mysql， 然后创建 database airflow

```
create database airflow;
```

修改 修改 airflow/airflow.cfg

```
sql_alchemy_conn = mysql://root:password@192.192.0.25:3306/airflow
```

安装 python 操作 mysql 的驱动包

```bash
yum install python-devel mysql-devel
yum install MySQL-python
pip install mysql-python 
```

## Reference

- [AirFlow使用指南一 安装与启动][1]
- [工作流管理平台Airflow][2]
- [Airflow学习笔记 --- airflow安装][3]
- [简书 - 浅谈调度工具—Airflow][4]
- [教程也是坑爹啊][5]

[1]: https://blog.csdn.net/Jdk_yxs/article/details/79191944
[2]: https://www.cnblogs.com/Leo_wl/p/6123926.html
[3]: https://blog.csdn.net/u012965373/article/details/70877311
[4]: https://www.jianshu.com/p/e878bbc9ead2
[5]: https://www.jianshu.com/p/5349168dd346





