# Airflow 插件安装

Airflow 虽然具有强大的功能，但是配置 DAG 并不是简单的工作，也有一些较为繁琐的概念，对于业务人员来说可能略显复杂,因此,Airflow DAG Creation Manager Plugin提供一个 Web界面来让业务人员可视化的编写及管理 DAG.

![](https://github.com/lattebank/airflow-dag-creation-manager-plugin/raw/master/images/dag_config.png)

##  System Requirements
- Airflow VerSions
 - 1.X

## Deployment Instructions

1. 在airflow目录下新建一个`plugins`目录

```bash
(vpy2) [airflow@cdhagent2 airflow]$ ll
总用量 600
-rw-rw-r--. 1 airflow airflow  21565 11月 13 09:40 airflow.cfg
-rw-rw-r--. 1 airflow airflow 405926 11月 12 09:10 airflow-dag-creation-manager-plugin-master.zip
-rw-r--r--. 1 airflow airflow 171008 11月 13 08:53 airflow.db
-rw-r--r--. 1 airflow airflow      4 11月 13 09:41 airflow-webserver.pid
drwxrwxr-x. 2 airflow airflow     51 11月  9 16:54 dags
drwxrwxr-x. 5 airflow airflow     69 11月  9 16:06 logs
drwxrwxr-x. 3 airflow airflow     18 11月 12 09:16 plugins
-rw-rw-r--. 1 airflow airflow   2329 11月  8 14:30 unittests.cfg

```
在`airflow.cfg`配置文件中设置路径

```bash
# Where your Airflow plugins are stored
plugins_folder = /home/airflow/airflow/plugins
```

2.下载插件 
[https://github.com/lattebank/airflow-dag-creation-manager-plugin/archive/master.zip](https://github.com/lattebank/airflow-dag-creation-manager-plugin/archive/master.zip)

将文件解压
```bash
 unzip airflow-dag-creation-manager-plugin-{RELEASE_VERSION_OR_BRANCH_NAME}.zip

 cp -r airflow-dag-creation-manager-plugin-{RELEASE_VERSION_OR_BRANCH_NAME}/plugins/* {AIRFLOW_PLUGINS_FOLDER} 
```
3 .将以下配置加入`airflow.cfg`文件
```bash
[dag_creation_manager]

 # see https://github.com/d3/d3-3.x-api-reference/blob/master/SVG-Shapes.md#line_interpolate
 # DEFAULT: basis
 dag_creation_manager_line_interpolate = basis
 
 # Choices for queue and pool
 dag_creation_manager_queue_pool = your_queue_pool_name1:your_queue1|your_pool1,your_queue_pool_name2:your_queue2|your_pool2
 
 # MR queue for queue pool
 dag_creation_manager_queue_pool_mr_queue = your_queue_pool_name1:your_mr_queue1,your_queue_pool_name2:your_mr_queue2
 
 # Category for display
 dag_creation_manager_category = custom
 
 # Task category for display
 dag_creation_manager_task_category = custom_task:#ffba40
 
 # Your email address to receive email
 # DEFAULT: 
 #dag_creation_manager_default_email = your_email_address
 
 #dag_creation_manager_need_approver = False
 
 #dag_creation_manager_can_approve_self = True

```
5 更新数据库信息

```bash
python {AIRFLOW_PLUGINS_FOLDER}/dcmp/tools/upgradedb.py
```

# 记录遇到的bug

Airflow DAG Creation Manager Plugin 依赖mysql作为数据库.因此需要修改配置文件.

```bash
# The executor class that airflow should use. Choices include
# SequentialExecutor, LocalExecutor, CeleryExecutor, DaskExecutor
executor = LocalExecutor

# The SqlAlchemy connection string to the metadata database.
# SqlAlchemy supports many different database engine, more information
# their website
sql_alchemy_conn = mysql://root:PASSWORD!@192.192.0.25:3306/airflow
#sql_alchemy_conn = sqlite:////home/airflow/airflow/airflow.db
# If SqlAlchemy should pool database connections.
sql_alchemy_pool_enabled = True

```

在25机器mysql中新建一个airflow数据库,设置权限

```bash
mysql> ues airflow;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'ues airflow' at line 1
mysql> use airflow;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show grants for root@localhost;
+----------------------------------------------------------------------------------------------------------------------------------------+
| Grants for root@localhost                                                                                                              |
+----------------------------------------------------------------------------------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY PASSWORD '*E6B64A0B64B3801F9AA102D607AE36CB8FA020CD' WITH GRANT OPTION |
| GRANT ALL PRIVILEGES ON `airflow`.* TO 'root'@'localhost'                                                                              |
| GRANT PROXY ON ''@'' TO 'root'@'localhost' WITH GRANT OPTION                                                                           |
+----------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```
更新数据库时`airflow initdb`报错
```bash
error :'Global variable explicit_defaults_for_timestamp needs to be on (1) for mysql

```
设置mysql配置文件

```bash
[mysqld]
#
explicit_defaults_for_timestamp=1

```
更新`airflow initdb`
```bash
/home/airflow/.pyenv/versions/2.7.10/envs/vpy2/lib/python2.7/site-packages/sqlalchemy/sql/default_comparator.py:161: SAWarning: The IN-predicate on "dcmp_user_profile.user_id" was invoked with an empty sequence. This results in a contradiction, which nonetheless can be expensive to evaluate.  Consider alternative strategies for improved performance.
  'strategies for improved performance.' % expr)
DB: mysql://root:***@192.192.0.25:3306/airflow
[2018-11-13 09:41:01,600] {db.py:338} INFO - Creating tables
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade d2ae31099d61 -> 0e2a74e0fc9f, Add time zone awareness
INFO  [alembic.runtime.migration] Running upgrade d2ae31099d61 -> 33ae817a1ff4, kubernetes_resource_checkpointing
INFO  [alembic.runtime.migration] Running upgrade 33ae817a1ff4 -> 27c6a30d7c24, kubernetes_resource_checkpointing
INFO  [alembic.runtime.migration] Running upgrade 27c6a30d7c24 -> 86770d1215c0, add kubernetes scheduler uniqueness
INFO  [alembic.runtime.migration] Running upgrade 86770d1215c0, 0e2a74e0fc9f -> 05f30312d566, merge heads
INFO  [alembic.runtime.migration] Running upgrade 05f30312d566 -> f23433877c24, fix mysql not null constraint
INFO  [alembic.runtime.migration] Running upgrade f23433877c24 -> 856955da8476, fix sqlite foreign key
INFO  [alembic.runtime.migration] Running upgrade 856955da8476 -> 9635ae0956e7, index-faskfail
/home/airflow/.pyenv/versions/2.7.10/envs/vpy2/lib/python2.7/site-packages/sqlalchemy/engine/default.py:470: Warning: Data truncated for column 'last_scheduler_run' at row 1
  cursor.execute(statement, parameters)
/home/airflow/.pyenv/versions/2.7.10/envs/vpy2/lib/python2.7/site-packages/sqlalchemy/engine/default.py:470: Warning: Data truncated for column 'last_modified' at row 1
  cursor.execute(statement, parameters)
Done.
```
**更新成功**

之后又有一个bug,插件有个python脚本需要将airflow数据库中插入一个表

```python
def run_version_0_0_1():
    run_sql("""
        CREATE TABLE IF NOT EXISTS `dcmp_dag` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `dag_name` varchar(250) NOT NULL,
          `version` int(11) NOT NULL,
          `category` varchar(50) NOT NULL,
          `editing` tinyint(1) NOT NULL,
          `editing_user_id` int(11) DEFAULT NULL,
          `editing_user_name` varchar(250) DEFAULT NULL,
          `last_editor_user_id` int(11) DEFAULT NULL,
          `last_editor_user_name` varchar(250) DEFAULT NULL,
          `updated_at` datetime(6) NOT NULL,
          PRIMARY KEY (`id`),
          UNIQUE KEY `dag_name` (`dag_name`),
          KEY `category` (`category`),
          KEY `editing` (`editing`),
          KEY `updated_at` (`updated_at`)
        ) DEFAULT CHARSET=utf8mb4;
    """)

    run_sql("""
        CREATE TABLE IF NOT EXISTS `dcmp_dag_conf` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `dag_id` int(11) NOT NULL,
          `dag_name` varchar(250) NOT NULL,
          `action` varchar(50) NOT NULL,
          `version` int(11) NOT NULL,
          `conf` text NOT NULL,
          `creator_user_id` int(11) DEFAULT NULL,
          `creator_user_name` varchar(250) DEFAULT NULL,
          `created_at` datetime(6) NOT NULL,
          PRIMARY KEY (`id`),
          KEY `dag_id` (`dag_id`),
          KEY `dag_name` (`dag_name`),
		) DEFAULT CHARSET=utf8mb4;
    """)

```
此时mysql报错`Specified key was too long; max key length is 767 bytes`

数据库表采用utf8编码,其中dag_name进行唯一键索引,mysql默认单个列索引不能超过767.而这个表是用utf8mb4存储,一个字符四个字节.故250*4 超出.
将`utf8mb4`更改为`utf8` 后成功.




